"""
    Módulo do serviço de gerenciamento de arquivos em .data
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Protocol, Any

# Diretório padrão
DATA_DIR = ".data"

class IOHandler(Protocol):
    """
        Define um protocolo básico para leitura e escrita de arquivos, 
        permitindo a implementação de diferentes estratégias de I/O.
    """

    def read(self, path: Path) -> Any:
        """
            Lê o conteúdo de um arquivo especificado pelo caminho fornecido.
        """
    def write(self, path: Path, content: Any) -> None:
        """
            Escreve o conteúdo fornecido em um arquivo especificado pelo caminho.
        """

# read e write já foram documentados, desativando o aviso de métodos não documentados
# pylint: disable=missing-function-docstring
class TextIO:
    """ Implementação de IOHandler para leitura e escrita de arquivos de texto """
    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def write(self, path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")

class BytesIO:
    """ Implementação de IOHandler para leitura e escrita de arquivos binários """
    def read(self, path: Path) -> bytes:
        return path.read_bytes()

    def write(self, path: Path, content: bytes) -> None:
        path.write_bytes(content)

class JSONIO:
    """ Implementação de IOHandler para leitura e escrita de arquivos JSON """
    def read(self, path: Path) -> Any:
        return json.loads(path.read_text(encoding="utf-8"))

    def write(self, path: Path, content: Any) -> None:
        path.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")

# pylint: enable=missing-function-docstring

@dataclass
class FileDescriptor:
    """
        Descreve um arquivo dentro do DataStore, encapsulando seu caminho.
    """
    path: Path

class DataStore:
    """
    Gerencia arquivos dentro de .data — evita os.path.exists/os.path.join
    espalhado pelos serviços. Cada serviço só pede um descritor e escreve/lê.

    TODO (ideia futura, não bloqueante):
    manifest por pasta (_manifest.json) + scan() pra detectar arquivos
    órfãos/modificados por fora do DataStore, caso isso vire um problema real.
    """

    def __init__(self, root: str = DATA_DIR):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def allocate_dir(self, *parts: str) -> Path:
        """
            Aloca (cria) um diretório dentro do DataStore, garantindo que ele exista.
        """
        path = self.root.joinpath(*parts)
        self._ensure_dir_exists(path)
        return path

    def dir_exists(self, *parts: str) -> bool:
        """
            Verifica se um diretório existe dentro do DataStore.
        """

        path = self.root.joinpath(*parts)
        return path.exists() and path.is_dir()

    def dir_remove(self, *parts: str) -> None:
        """
            Remove um diretório e todo o seu conteúdo dentro do DataStore.
            Não é permitido remover o diretório raiz do DataStore.
        """

        path = self.root.joinpath(*parts)
        if path.absolute() == self.root.absolute():
            raise ValueError("Não é permitido remover o diretório raiz do DataStore.")

        if path.exists() and path.is_dir():
            for child in path.iterdir():
                if child.is_file():
                    child.unlink()
                elif child.is_dir():
                    self.dir_remove(*child.relative_to(self.root).parts)
            path.rmdir()

    def allocate_file(self, *parts: str) -> FileDescriptor:
        """
            Aloca um arquivo dentro do DataStore, garantindo que o diretório pai exista.
            Não é garantido que o arquivo em si exista; apenas o diretório pai será criado 
            se necessário.
        """

        path = self.root.joinpath(*parts)
        self._ensure_dir_exists(path, True)
        return FileDescriptor(
            path=path
        )

    def exists(self, descriptor: FileDescriptor) -> bool:
        """
            Verifica se o arquivo descrito pelo FileDescriptor existe dentro do DataStore.
        """
        return descriptor.path.exists() and descriptor.path.is_file()

    def cached_at(self, descriptor: FileDescriptor) -> datetime | None:
        """
            Retorna a data e hora em que o arquivo foi armazenado no cache,
            ou None se o arquivo não existir ou não tiver metadados de cache.
        """
        return self._read_cache_meta(descriptor.path)

    def write(self, descriptor: FileDescriptor, content: Any, io: IOHandler | None = None) -> None:
        """
            Escreve o conteúdo fornecido no arquivo descrito pelo FileDescriptor,
            utilizando o IOHandler especificado (ou TextIO por padrão).
            Garante que o diretório pai do arquivo exista antes de escrever.
        """

        self._ensure_dir_exists(descriptor.path, True)
        io = io or TextIO()
        io.write(descriptor.path, content)
        self._write_cache_meta(descriptor.path)

    def read(self, descriptor: FileDescriptor, io: IOHandler | None = None) -> Any:
        """
            Lê o conteúdo do arquivo descrito pelo FileDescriptor,
            utilizando o IOHandler especificado (ou TextIO por padrão).
            Lança FileNotFoundError se o arquivo não existir.
        """

        if not self.exists(descriptor):
            relpath = self._relative_to_root(descriptor.path)
            raise FileNotFoundError(f"Arquivo {relpath} não encontrado.")
        io = io or TextIO()
        return io.read(descriptor.path)

    def remove(self, descriptor: FileDescriptor) -> None:
        """
            Remove o arquivo descrito pelo FileDescriptor do DataStore,
            juntamente com seus metadados de cache, se existirem.
        """

        if self.exists(descriptor):
            descriptor.path.unlink()
        meta_path = self._meta_path(descriptor.path)
        if meta_path.exists():
            meta_path.unlink()

    def is_stale(self, descriptor: FileDescriptor, max_age_seconds: int) -> bool:
        """
            Verifica se o arquivo descrito pelo FileDescriptor está obsoleto
            com base no tempo máximo de vida fornecido (em segundos).
        """

        if not self.exists(descriptor):
            return True

        cached_at = self.cached_at(descriptor)
        if cached_at is None:
            return True
        age = (datetime.now(timezone.utc) - cached_at).total_seconds()
        return age > max_age_seconds

    # Obtém caminho do arquivo de metadados associado ao arquivo principal
    def _meta_path(self, path: Path) -> Path:
        return path.with_suffix(path.suffix + ".meta.json")

    # Lê os metadados de cache do arquivo, retornando a data de cache ou None se não existir
    def _read_cache_meta(self, path: Path) -> datetime | None:
        meta_path = self._meta_path(path)
        if not meta_path.exists():
            return None
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        return datetime.fromisoformat(data["cached_at"])

    # Escreve os metadados de cache para o arquivo, registrando a data e hora atual
    def _write_cache_meta(self, path: Path) -> None:
        meta_path = self._meta_path(path)
        meta_path.write_text(
            json.dumps({"cached_at": datetime.now(timezone.utc).isoformat()}),
            encoding="utf-8",
        )

    # Obtém o caminho relativo do arquivo em relação ao diretório raiz do DataStore
    def _relative_to_root(self, path: Path) -> Path:
        return path.relative_to(self.root)

    # Garante que o diretório especificado exista; se isparent for True, cria o diretório pai
    def _ensure_dir_exists(self, path: Path, isparent: bool = False) -> None:
        if isparent:
            path.parent.mkdir(parents=True, exist_ok=True)
            return

        path.mkdir(parents=True, exist_ok=True)
