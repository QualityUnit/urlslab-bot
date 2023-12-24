from io import BytesIO

from .base import BinaryContentReader
from docx import Document


class DOCXContentReader(BinaryContentReader):
    """Concrete class for reading DOCX content."""

    def read(self) -> str:
        document = Document(BytesIO(self.binary_content))
        doc_text = '\n'.join(paragraph.text for paragraph in document.paragraphs)
        return doc_text
