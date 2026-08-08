from models.document import Document, DocumentType
from services.data_store import DataStore, FileDescriptor, TextIO
from services.document_provider import DocumentSource

DEFAULT_CACHE_LIFETIME = 3600  # 1 hora em segundos
class CacheSource(DocumentSource):
    def __init__(self, document_id: str, **kwargs):
        super().__init__(document_id, **kwargs)
        self.cached_file: FileDescriptor | None = kwargs.get("cached_file", None)
        self.cache_lifetime: int | None = kwargs.get("cache_lifetime", DEFAULT_CACHE_LIFETIME)
        self.raises_if_stale: bool = kwargs.get("raises_if_stale", False)
        self.data_store: DataStore | None = kwargs.get("data_store", None)

    def _has_cache(self) -> bool:
        return self.cached_file is not None and self.data_store is not None

    def _is_stale(self) -> bool:
        if not self._has_cache():
            return True
        data_store = self.data_store
        return data_store.is_stale(self.cached_file, self.cache_lifetime)

    def _cache_fetch(self, doctype: DocumentType = DocumentType.TEXT) -> Document:
        if self.cache_lifetime and self._is_stale():
            if self.raises_if_stale:
                raise ValueError(f"Cache para {self.document_id} está ausente ou obsoleto.")
            return None
        data_store = self.data_store
        return Document.from_text(
            self.document_id,
            data_store.read(self.cached_file, io=TextIO()),
            doctype
        )

    def fetch(self):
        return self._cache_fetch()
