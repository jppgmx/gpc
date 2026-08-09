"""
    Módulo para buscar documentos a partir de URLs
"""

import requests as req

from bs4 import BeautifulSoup

from models.document import Document, DocumentType
from models.sources.cache import CacheSource
from services.data_store import TextIO

DOCUMENT_LIFETIME = 3600  # 1 hora em segundos
DEFAULT_TIMEOUT = 10  # 10 segundos

class URLSource(CacheSource):
    """
        Fonte de documentos a partir de URLs
    """
    def __init__(self, document_id: str, url: str, **kwargs):
        super().__init__(document_id, **kwargs)
        self.url = url
        self.timeout = kwargs.get("timeout", DEFAULT_TIMEOUT)
        self.request_options = kwargs.get("request_options", {})

    def fetch(self):
        # Tenta buscar do cache
        document = self._cache_fetch()
        if document is not None:
            return document

        reqopts = {
            **self.request_options,
            "timeout": self.timeout
        }
        # Se não tiver no cache, busca da URL
        response = req.get(self.url, **reqopts)
        response.raise_for_status()

        # Converte o conteúdo para BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Cria o documento
        document = Document(
            document_id=self.document_id,
            document_type=DocumentType.HTML,
            data=soup
        )

        # Aplica os transformadores
        document = self._apply_transformers(document)

        # Salva no cache
        if self._has_cache():
            self.data_store.write(
                descriptor=self.cached_file,
                content=document.text,
                io=TextIO()
            )

        return document
