from typing import Callable, Union

from models.document import Document, DocumentType
from services.document_provider import Transformer

class HTMLTransformer(Transformer):
    @property
    def supports(self) -> list[DocumentType]:
        return [DocumentType.HTML]

    @property
    def returns(self) -> DocumentType:
        return DocumentType.HTML

ElementSelector = Union[str, Callable[[Document], Document]]
class ContentHTMLTransformer(HTMLTransformer):
    def transform(self, document: Document) -> Document:
        el: ElementSelector = self.transformer_config.get("element", "#pageContent")

        fragment = document.data.select_one(el) if isinstance(el, str) else el(document)
        return Document.from_text(
            document.document_id,
            fragment.prettify() if fragment else "",
            document.document_type
        )
