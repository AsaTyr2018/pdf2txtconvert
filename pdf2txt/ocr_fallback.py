from pathlib import Path
from io import BytesIO

from PIL import Image
import pytesseract
import fitz  # PyMuPDF


def ocr_pdf_to_text(pdf_path: Path) -> str:
    """Extract text from PDF using OCR without requiring Poppler."""
    text_chunks = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            pix = page.get_pixmap()
            image = Image.open(BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(image)
            text_chunks.append(text)
    return "\n".join(text_chunks)
