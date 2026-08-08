"""
    Módulo para transformar documentos usando funções chamáveis
"""
from typing import Callable

from models.document import Document, DocumentType
from services.document_provider import Transformer

class CallableTransformer(Transformer):
    """
        Transformer para transformar documentos usando funções chamáveis
    """

    def __init__(self, transform_func: Callable[[Document], Document], **kwargs):
        super().__init__(**kwargs)
        self.transform_func = transform_func

    @property
    def supports(self) -> list[DocumentType]:
        return self.transformer_config.get("supports", [])

    @property
    def returns(self) -> DocumentType:
        return self.transformer_config.get("returns", DocumentType.TEXT)

    def transform(self, document: Document) -> Document:
        return self.transform_func(document)
