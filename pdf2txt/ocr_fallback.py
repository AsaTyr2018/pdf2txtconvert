from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import pytesseract


def ocr_pdf_to_text(pdf_path: Path) -> str:
    """Extract text from PDF using OCR."""
    text_chunks = []
    images = convert_from_path(str(pdf_path))
    for img in images:
        text = pytesseract.image_to_string(img)
        text_chunks.append(text)
    return "\n".join(text_chunks)
