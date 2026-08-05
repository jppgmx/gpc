from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Protocol, Any

DATA_DIR = ".data"

class IOHandler(Protocol):
    def read(self, path: Path) -> Any: ...
    def write(self, path: Path, content: Any) -> None: ...

class TextIO:
    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def write(self, path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")

class BytesIO:
    def read(self, path: Path) -> bytes:
        return path.read_bytes()

    def write(self, path: Path, content: bytes) -> None:
        path.write_bytes(content)

class JSONIO:
    def read(self, path: Path) -> Any:
        return json.loads(path.read_text(encoding="utf-8"))

    def write(self, path: Path, content: Any) -> None:
        path.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")

@dataclass
class FileDescriptor:
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
        path = self.root.joinpath(*parts)
        self._ensure_dir_exists(path)
        return path

    def dir_exists(self, *parts: str) -> bool:
        path = self.root.joinpath(*parts)
        return path.exists() and path.is_dir()

    def dir_remove(self, *parts: str) -> None:
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
        path = self.root.joinpath(*parts)
        self._ensure_dir_exists(path, True)
        return FileDescriptor(
            path=path
        )

    def exists(self, descriptor: FileDescriptor) -> bool:
        return descriptor.path.exists() and descriptor.path.is_file()

    def cached_at(self, descriptor: FileDescriptor) -> datetime | None:
        return self._read_cache_meta(descriptor.path)

    def write(self, descriptor: FileDescriptor, content: Any, io: IOHandler | None = None) -> None:
        self._ensure_dir_exists(descriptor.path, True)
        io = io or TextIO()
        io.write(descriptor.path, content)
        self._write_cache_meta(descriptor.path)

    def read(self, descriptor: FileDescriptor, io: IOHandler | None = None) -> Any:
        io = io or TextIO()
        return io.read(descriptor.path)

    def is_stale(self, descriptor: FileDescriptor, max_age_seconds: int) -> bool:
        if not self.exists(descriptor):
            return True

        cached_at = self.cached_at(descriptor)
        if cached_at is None:
            return True
        age = (datetime.now(timezone.utc) - cached_at).total_seconds()
        return age > max_age_seconds

    def _meta_path(self, path: Path) -> Path:
        return path.with_suffix(path.suffix + ".meta.json")

    def _read_cache_meta(self, path: Path) -> datetime | None:
        meta_path = self._meta_path(path)
        if not meta_path.exists():
            return None
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        return datetime.fromisoformat(data["cached_at"])

    def _write_cache_meta(self, path: Path) -> None:
        meta_path = self._meta_path(path)
        meta_path.write_text(
            json.dumps({"cached_at": datetime.now(timezone.utc).isoformat()}),
            encoding="utf-8",
        )

    def _ensure_dir_exists(self, path: Path, isparent: bool = False) -> None:
        if isparent:
            path.parent.mkdir(parents=True, exist_ok=True)
            return

        path.mkdir(parents=True, exist_ok=True)
