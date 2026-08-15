"""
    Módulo do serviço de banco de dados.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from services.data_store import DataStore
from services.secrets import get_env_variable

def get_default_url() -> str:
    """
    Retorna a URL padrão do banco de dados.
    """

    datastore = DataStore()
    db_path = datastore.allocate_file("db", "gpc.db").path

    return f"sqlite:///{db_path.as_posix()}"

DATABASE_URL = get_env_variable("DATABASE_URL", get_default_url())
engine = create_engine(DATABASE_URL)

def get_db_session() -> Session:
    """
    Retorna uma sessão do banco de dados.
    """
    return Session(engine)
