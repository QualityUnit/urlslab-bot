from .base import BinaryContentReader
from .pdf_document_reader import PDFContentReader
from .docx_document_reader import DOCXContentReader


# Factory method to create the appropriate content reader
def get_content_reader(file_content: bytes, content_type: str) -> BinaryContentReader:
    if content_type == "application/pdf":
        return PDFContentReader(file_content)
    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return DOCXContentReader(file_content)
    else:
        raise ValueError("Unsupported file type")


__all__ = [
    "get_content_reader",
    "PDFContentReader",
    "DOCXContentReader",
]
