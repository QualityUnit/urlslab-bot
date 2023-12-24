from io import BytesIO

from PyPDF2 import PdfFileReader
from .base import BinaryContentReader


class PDFContentReader(BinaryContentReader):
    """Concrete class for reading PDF content."""

    def read(self) -> str:
        pdf_content = BytesIO(self.binary_content)
        reader = PdfFileReader(pdf_content)

        text = ""
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()

        return text
