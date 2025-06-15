from pathlib import Path
from io import BytesIO

import fitz  # PyMuPDF
from PIL import Image
from loguru import logger
from pylatexenc.latex2text import LatexNodes2Text

try:
    from pix2tex.cli import LatexOCR
except Exception as e:  # ImportError or other
    LatexOCR = None
    _import_error = e
else:
    _import_error = None


def extract_with_latexocr(pdf_path: Path) -> str:
    """Extract text from a PDF using the LaTeX-OCR model."""
    if LatexOCR is None:
        raise ImportError(f"LatexOCR unavailable: {_import_error}")

    ocr_model = LatexOCR()
    converter = LatexNodes2Text()
    text_chunks = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            pix = page.get_pixmap()
            image = Image.open(BytesIO(pix.tobytes("png")))
            try:
                latex = ocr_model(image)
            except Exception as e:
                logger.error(f"LatexOCR failed on page {page.number+1}: {e}")
                latex = ""
            text_chunks.append(converter.latex_to_text(latex))
    return "\n".join(text_chunks)
