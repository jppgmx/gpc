from markdownify import MarkdownConverter

from models.document import Document, DocumentType
from services.document_provider import Transformer

class HTML2MarkdownTransformer(Transformer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.converter_cls = kwargs.get("converter_cls", MarkdownConverter)
        self.converter_options = kwargs.get("converter_options", {})

        if not issubclass(self.converter_cls, MarkdownConverter):
            raise TypeError("converter_cls deve ser uma subclasse de MarkdownConverter")

    @property
    def supports(self) -> list[DocumentType]:
        return [DocumentType.HTML]

    @property
    def returns(self) -> DocumentType:
        return DocumentType.TEXT

    def transform(self, document: Document) -> Document:
        converter = self.converter_cls(**self.converter_options)
        return Document.from_text(
            document.document_id,
            converter.convert(document.text),
            doctype=self.returns
        )
