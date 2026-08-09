"""
    Módulo do serviço de provedor de documentos.
"""

from typing import Protocol, runtime_checkable

from models.document import Document, DocumentType
from services.data_store import DataStore

# pylint: disable=too-few-public-methods
@runtime_checkable
class DocumentSource(Protocol):
    """
        Define um protocolo para fontes de documentos. Cada fonte deve implementar 
        o método fetch() para retornar um documento.
    """

    def __init__(self, document_id: str, **kwargs):
        self.document_id = document_id
        self.transformers: list[Transformer] = kwargs.get("transformers", [])

    # Aplica uma cadeia de transformadores ao documento
    def _apply_transformers(self, document: Document) -> Document:
        self._ensure_transformer_compatibility(document)
        for transformer in self.transformers:
            document = transformer.transform(document)
        return document

    # Verifica a compatibilidade dos transformadores com o tipo de documento
    def _ensure_transformer_compatibility(self, document: Document) -> None:
        docinput = document.document_type
        for transformer in self.transformers:
            if docinput not in transformer.supports:
                raise ValueError(
                    f"Transformer {transformer.__class__.__name__} não suporta "
                    f"documento do tipo {docinput}. Tipos suportados: {transformer.supports}"
                )
            docinput = transformer.returns

    def fetch(self) -> Document:
        """
            Método que deve ser implementado por cada fonte de documento.
            Retorna um objeto Document.
        """
# pylint: enable=too-few-public-methods

class Transformer(Protocol):
    """
        Define um protocolo para transformadores de documentos. 
        Cada transformador deve implementar o método transform() para transformar um documento,
        além de propriedades para indicar os tipos de documentos que suporta e retorna.
    """
    def __init__(self, **kwargs):
        self.transformer_config = kwargs

    @property
    def supports(self) -> list[DocumentType]:
        """ Retorna uma lista de tipos de documentos que o transformador suporta. """

    @property
    def returns(self) -> DocumentType:
        """ Retorna o tipo de documento que o transformador retorna após a transformação. """

    def transform(self, document: Document) -> Document:
        """
            Método que deve ser implementado por cada transformador de documento.
            Recebe um objeto Document e retorna um novo objeto Document transformado.
        """

class DocumentProvider:
    """
        Provedor de documentos que gerencia múltiplas fontes de documentos.
        Permite adicionar, buscar e remover fontes de documentos, bem como buscar documentos
        a partir dessas fontes.
    """

    def __init__(self, data_store: DataStore):
        self.data_store = data_store
        self.sources: dict[str, DocumentSource] = {}

    def __contains__(self, item):
        return item in self.sources

    def __getitem__(self, key):
        return self.sources[key]

    def __setitem__(self, key, value):
        if not isinstance(value, DocumentSource):
            raise TypeError("Valor deve ser do tipo DocumentSource")
        self.sources[key] = value

    def __delitem__(self, key):
        del self.sources[key]

    def add_source(self, source: DocumentSource):
        """ Adiciona uma nova fonte de documento ao provedor. """
        if source.document_id in self:
            raise ValueError(f"Fonte {source.document_id} já existe.")

        self[source.document_id] = source

    def get_source(self, document_id: str) -> DocumentSource:
        """ Retorna a fonte de documento correspondente ao document_id. """

        if document_id not in self:
            raise ValueError(f"Fonte {document_id} não encontrada.")
        return self[document_id]

    def fetch_document(self, document_id: str) -> Document:
        """ Busca e retorna o documento a partir da fonte correspondente ao document_id. """

        return self.get_source(document_id).fetch()

    def remove_source(self, document_id: str):
        """ Remove a fonte de documento correspondente ao document_id. """

        if document_id not in self:
            raise ValueError(f"Fonte {document_id} não encontrada.")
        del self[document_id]
