"""
    Módulo de model para documentos
"""

from dataclasses import dataclass
from enum import Enum

from bs4 import BeautifulSoup, Tag

DocumentData = str | Tag
class DocumentType(Enum):
    """Enumeração para tipos de documentos"""

    HTML = "html"
    TEXT = "text"

    @property
    def python_type(self):
        """Retorna o tipo Python correspondente ao tipo de documento"""

        return {
            DocumentType.HTML: Tag,
            DocumentType.TEXT: str
        } [self]

@dataclass(frozen=True)
class Document:
    """Classe para representar um documento"""
    document_id: str
    document_type: DocumentType
    data: DocumentData

    @classmethod
    def from_text(cls, docid: str, text: str,
                  doctype: DocumentType = DocumentType.TEXT) -> "Document":
        """
            Cria um documento a partir de texto
        """

        if doctype == DocumentType.HTML:
            data = BeautifulSoup(text, "html.parser")
        else:
            data = text
        return cls(docid, doctype, data)

    @classmethod
    def from_file(cls, docid: str, file_path: str,
                  doctype: DocumentType = DocumentType.TEXT) -> "Document":
        """
            Cria um documento a partir de um arquivo
        """

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return cls.from_text(docid, text, doctype)

    @property
    def text(self) -> str:
        """Retorna o conteúdo do documento como texto"""

        if self.document_type == DocumentType.HTML:
            return str(self.data)
        return self.data

    def convert(self, doctype: DocumentType) -> "Document":
        """
            Converte o documento para outro tipo de documento
        """

        if self.document_type == doctype:
            return self

        if doctype == DocumentType.HTML:
            data = BeautifulSoup(self.text, "html.parser")
        else:
            data = self.text
        return Document(self.document_id, doctype, data)
