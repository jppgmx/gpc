"""
    Módulo do serviço de banco de dados.
"""

from logging import getLogger
from typing import Any, TypeVar

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase

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
def enable_wal(dbapi_connection, _):
    """ 
        Habilita WAL (Write-Ahead Logging) caso o banco de dados seja SQLite.
    """

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

Model = TypeVar('Model', bound=DeclarativeBase)
Rows = list[dict[str, Any]]
def insert_update(session: Session, model: Model, rows: Rows, index_elements: list[str]):
    """
    Insere ou atualiza em lote, deixando o banco resolver os conflitos.
    `index_elements` é ignorado no MySQL (ele detecta via chave única/primária sozinho),
    mas continua obrigatório na assinatura para manter a chamada consistente entre dialetos.
    """

    # Determinamos que tipo de banco estamos usando
    dialect = session.get_bind().dialect.name
    columns_to_update = [
        col.name for col in model.__table__.columns
        if col.name not in index_elements
    ]

    # Aplicamos a inserção/atualização com base nos dialetos

    if dialect == "sqlite":
        # pylint disable=import-outside-toplevel
        from sqlalchemy.dialects.sqlite import insert
        stmt = insert(model).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=index_elements,
            set_={col: getattr(stmt.excluded, col) for col in columns_to_update},
        )
    elif dialect == "postgresql":
        # pylint disable=import-outside-toplevel
        from sqlalchemy.dialects.postgresql import insert
        stmt = insert(model).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=index_elements,
            set_={col: getattr(stmt.excluded, col) for col in columns_to_update},
        )
    elif dialect == "mysql":
        # pylint disable=import-outside-toplevel
        from sqlalchemy.dialects.mysql import insert
        stmt = insert(model).values(rows)
        stmt = stmt.on_duplicate_key_update(
            **{col: getattr(stmt.inserted, col) for col in columns_to_update}
        )
    else:
        raise NotImplementedError(f"insert_update não implementado para o dialeto '{dialect}'")

    session.execute(stmt)

def get_max_batch_size(session: Session, model: Model, margin: float = 0.9) -> int:
    """
    Retorna o tamanho máximo de lote para inserção/atualização em massa.
    """

    db_limit = 1000  # Limite padrão para a maioria dos bancos de dados
    dialect = session.get_bind().dialect.name
    if dialect == "sqlite":
        # pylint disable=import-outside-toplevel
        from sqlite3 import Connection, SQLITE_LIMIT_VARIABLE_NUMBER
        conn: Connection = session.connection().connection
        db_limit = conn.getlimit(SQLITE_LIMIT_VARIABLE_NUMBER)
    elif dialect in ["postgresql", "mysql"]:
        db_limit = 65535  # Limite teórico para PostgreSQL e MySQL
    else:
        raise NotImplementedError(f"get_max_batch_size não implementado para o dialeto '{dialect}'")

    column_count = len(model.__table__.columns)

    return int((db_limit * margin) // column_count)
