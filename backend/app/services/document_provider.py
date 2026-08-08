from typing import Protocol, runtime_checkable

from models.document import Document, DocumentType
from services.data_store import DataStore

@runtime_checkable
class DocumentSource(Protocol):
    def __init__(self, document_id: str, **kwargs):
        self.document_id = document_id
        self.transformers: list[Transformer] = kwargs.get("transformers", [])

    def _apply_transformers(self, document: Document) -> Document:
        self._ensure_transformer_compatibility(document)
        for transformer in self.transformers:
            document = transformer.transform(document)
        return document

    def _ensure_transformer_compatibility(self, document: Document) -> None:
        docinput = document.document_type
        for transformer in self.transformers:
            if docinput not in transformer.supports:
                raise ValueError(
                    f"Transformer {transformer.__class__.__name__} não suporta "
                    f"documento do tipo {docinput}. Tipos suportados: {transformer.supports}"
                )
            docinput = transformer.returns

    def fetch(self) -> Document: ...

class Transformer(Protocol):
    def __init__(self, **kwargs): 
        self.transformer_config = kwargs

    @property
    def supports(self) -> list[DocumentType]: ...

    @property
    def returns(self) -> DocumentType: ...

    def transform(self, document: Document) -> Document: ...

class DocumentProvider:
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
        if source.document_id in self:
            raise ValueError(f"Fonte {source.document_id} já existe.")

        self[source.document_id] = source

    def get_source(self, document_id: str) -> DocumentSource:
        if document_id not in self:
            raise ValueError(f"Fonte {document_id} não encontrada.")
        return self[document_id]

    def fetch_document(self, document_id: str) -> Document:
        return self.get_source(document_id).fetch()

    def remove_source(self, document_id: str):
        if document_id not in self:
            raise ValueError(f"Fonte {document_id} não encontrada.")
        del self[document_id]
