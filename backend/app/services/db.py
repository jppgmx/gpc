"""
    Módulo do serviço de banco de dados.
"""

from logging import getLogger

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from services.data_store import DataStore
from services.secrets import get_env_variable

LOGGER = getLogger(__name__)

def get_default_url() -> str:
    """
    Retorna a URL padrão do banco de dados.
    """

    datastore = DataStore()
    db_path = datastore.allocate_file("db", "gpc.db").path

    return f"sqlite:///{db_path.as_posix()}"

DATABASE_URL = get_env_variable("DATABASE_URL", get_default_url())
engine = create_engine(DATABASE_URL)

@event.listens_for(engine, "connect")
def enable_wal(dbapi_connection, connection_record):
    if engine.dialect.name == "sqlite":
        LOGGER.debug("Habilitando o modo WAL no SQLite...")
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()

def get_db_session() -> Session:
    """
    Retorna uma sessão do banco de dados.
    """
    return Session(engine)
