"""
    API de tags
"""

from logging import getLogger

from fastapi import APIRouter

from services.data_store import DataStore, JSONIO
from services.db import get_db_session
from models.problemset import Tag

LOGGER = getLogger(__name__)

router = APIRouter(prefix="/problemset")
data_store = DataStore()

@router.get("/tags")
def get_tags():
    """
        Retorna todas as tags disponíveis.
    """

    LOGGER.debug("Recebida requisição em /problemset/tags")

    with get_db_session() as session:
        tags = session.query(Tag).all()

    descs = load_tags_descriptions()
    return {
        "count": len(tags),
        "tags": [
            {
                "name": tag.name,
                "description": descs.get(tag.name, "Descrição não disponível.")
            }
            for tag in tags
        ]
    }

def load_tags_descriptions():
    """
        Carrega as descrições das tags a partir do arquivo JSON.
    """

    LOGGER.debug("Carregando descrições das tags a partir do arquivo JSON")

    desc_path = data_store.allocate_file(".assets", "docs", "tags.json")

    return data_store.read(desc_path, JSONIO())
