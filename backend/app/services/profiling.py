"""
    Serviço de profiling para medir consumo de recursos.
"""

from __future__ import annotations

import csv
from abc import ABC, abstractmethod
from asyncio import sleep
from datetime import UTC, datetime
from gzip import GzipFile
from importlib.resources import path
from logging import getLogger
from pathlib import Path
from typing import Any, TextIO

import psutil

from services.data_store import DataStore

PROFILING_INTERVAL = 500 # 500 milissegundos
METRIC_MAX_SIZE = 50 * 1024 * 1024 # * 1024 # 50 MB
METRIC_MAX_FILES = 5 # Máximo de arquivos de métricas a manter
LOGGER = getLogger(__name__)

class MetricWriterBase(ABC):
    """
    Base para escritores de métricas em CSV.

    A classe é responsável pela persistência das amostras.
    As subclasses são responsáveis pela coleta das métricas.
    """

    BASE_FIELDS = ("timestamp",)

    def __init__(self, path: Path, max_size: int = METRIC_MAX_SIZE, max_files: int = METRIC_MAX_FILES) -> None:
        self._file = path.open(
            mode="a",
            newline="",
            encoding="utf-8",
        )
        self._max_size = max_size
        self._max_files = max_files

    @property
    @abstractmethod
    def fields(self) -> tuple[str, ...]:
        """
        Retorna os campos específicos da implementação.
        """

    @abstractmethod
    def collect(self) -> dict[str, Any]:
        """
        Coleta uma amostra das métricas.
        """

    def write(self) -> None:
        """
        Coleta e persiste uma amostra.
        """
        row = {
            "timestamp": datetime.now(UTC).isoformat(),
            **self.collect(),
        }

        self._writer.writerow(row)
        self._file.flush()

    def close(self) -> None:
        """
        Fecha o arquivo de métricas.
        """
        self._file.close()

    @property
    def _writer(self) -> csv.DictWriter:
        """
            Retorna o escritor CSV, com rotação de arquivo se necessário.
        """
        self._file = rotate_file(self._file, self._max_size, self._max_files)
        writer = csv.DictWriter(
            self._file,
            fieldnames=(*self.BASE_FIELDS, *self.fields),
        )

        if self._file.tell() == 0:
            writer.writeheader()

        return writer

    def __enter__(self) -> MetricWriterBase:
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        self.close()

class ProcessMetricWriter(MetricWriterBase):
    """
    Coleta métricas do processo atual.
    """

    def __init__(self, path: Path) -> None:
        self._process = psutil.Process()

        # Inicializa a medição de CPU.
        self._process.cpu_percent(None)

        super().__init__(path)

    @property
    def fields(self) -> tuple[str, ...]:
        return (
            "cpu_percent",
            "rss_bytes",
            "vms_bytes",
            "num_threads",
            "num_fds",
        )

    def collect(self) -> dict[str, Any]:
        from platform import system
        memory = self._process.memory_info()
        if system() == "Windows" and not hasattr(self._process, "num_fds"):
            LOGGER.warning("Não há num_fds no Windows, injetando função dummy.")
            setattr(self._process, "num_fds", lambda: None)  # type: ignore

        return {
            "cpu_percent": self._process.cpu_percent(None),
            "rss_bytes": memory.rss,
            "vms_bytes": memory.vms,
            "num_threads": self._process.num_threads(),
            "num_fds": self._process.num_fds(),
        }

class SystemMetricWriter(MetricWriterBase):
    """
    Coleta métricas do sistema operacional.
    """

    def __init__(self, path: Path) -> None:
        # Inicializa a medição de CPU.
        psutil.cpu_percent(None)

        super().__init__(path)

    @property
    def fields(self) -> tuple[str, ...]:
        return (
            "cpu_percent",
            "memory_percent",
            "swap_percent",
            "load_1m",
        )

    def collect(self) -> dict[str, Any]:
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            "cpu_percent": psutil.cpu_percent(None),
            "memory_percent": memory.percent,
            "swap_percent": swap.percent,
            "load_1m": psutil.getloadavg()[0],
        }

def rotate_file(f: TextIO, max_size: int = METRIC_MAX_SIZE, 
                max_rotations: int = METRIC_MAX_FILES) -> TextIO:
    """
        Rotaciona o arquivo de métricas se ele ultrapassar o tamanho máximo, comprimindo-o
        os arquivos antigos em .1.csv.gz, .2.csv.gz, etc. 
        Mantém no máximo `max_rotations` arquivos antigos.
    """

    f.flush()
    if f.tell() < max_size:
        return f

    path = Path(f.name)
    f.close()

    for i in range(1, max_rotations + 1):
        old_path = path.with_suffix(f".{i}.csv.gz")
        if old_path.exists():
            if i == max_rotations:
                old_path.unlink()
            else:
                new_path = path.with_suffix(f".{i + 1}.csv.gz")
                old_path.rename(new_path)

    with open(path, "rb") as f_in:
        with GzipFile(path.with_suffix(".1.csv.gz"), "wb") as f_out:
            f_out.writelines(f_in)

    return open(path, "w", encoding="utf-8", newline="")

async def start_profiling(data_store: DataStore):
    """
    Inicia o profiling do sistema e do processo atual.
    """

    LOGGER.info("Iniciando profiling do sistema e do processo atual...")

    process_writer = ProcessMetricWriter(
        data_store.allocate_file("logs", "profiling_process.csv").path
    )
    system_writer = SystemMetricWriter(
        data_store.allocate_file("logs", "profiling_system.csv").path
    )

    try:
        while True:
            try:
                process_writer.write()
                system_writer.write()
            except:
                LOGGER.exception("Erro durante a coleta de métricas.")
            await sleep(PROFILING_INTERVAL / 1000)
    finally:
        process_writer.close()
        system_writer.close()
        LOGGER.info("Profiling finalizado.")
