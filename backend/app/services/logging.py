"""
    Módulo do serviço de logging.
"""

from datetime import timedelta
import logging
from logging.handlers import RotatingFileHandler
from time import perf_counter
from typing import Callable

# O projeto usa uvicorn, pegamos o formatador dele
from uvicorn.logging import DefaultFormatter

from services.data_store import DataStore
from services.secrets import get_env_variable

# Controle de configuração do logging
_configured = False
DEFAULT_LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
DEFAULT_LOG_BACKUP_COUNT = 5  # Número de arquivos de log antigos a serem mantidos

_raw_log_level = get_env_variable("LOG_LEVEL", "INFO").strip().upper()
LOG_LEVEL = getattr(logging, _raw_log_level, logging.INFO)

def setup_logging(store: DataStore, log_file: str = "gpc.log",
                  level: int = LOG_LEVEL, **kwargs) -> None:
    """ Configura o logging para a aplicação backend. """

    global _configured
    if _configured:
        return

    # Arquivo rotacionado para logs
    log_path = store.allocate_file("logs", log_file).path
    rotating_handler = RotatingFileHandler(
        str(log_path),
        maxBytes=kwargs.get("max_bytes", DEFAULT_LOG_MAX_BYTES),
        backupCount=kwargs.get("backup_count", DEFAULT_LOG_BACKUP_COUNT),
        encoding="utf-8"
    )
    rotating_handler.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s"))

    # O console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(DefaultFormatter("%(levelprefix)s %(name)s | %(message)s"))

    # Obtém logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(rotating_handler)
    root_logger.addHandler(console_handler)

    # O uvicorn tem seus próprios handlers, então limpamos os handlers de seus loggers para evitar duplicação de logs
    for uvicorn_logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(uvicorn_logger_name).handlers.clear()
        logging.getLogger(uvicorn_logger_name).propagate = True

    logging.info(f"Logging configurado. Logs serão gravados em: {log_path}")
    _configured = True

def start_chronometer() -> Callable[[], timedelta]:
    """ Inicia um cronômetro e retorna o tempo inicial. """

    start_time = perf_counter()

    def elapsed_time() -> timedelta:
        """ Retorna o tempo decorrido desde o início do cronômetro. """
        return timedelta(seconds=perf_counter() - start_time)

    return elapsed_time
