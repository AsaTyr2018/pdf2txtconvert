from pathlib import Path
from io import BytesIO
from typing import Iterable, List, Optional, Union

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


def extract_with_latexocr(
    pdf_path: Path, pages: Optional[Iterable[int]] = None
) -> Union[str, List[str]]:
    """Extract text from a PDF using the LaTeX-OCR model.

    Parameters
    ----------
    pdf_path: Path
        PDF file to process.
    pages: Optional iterable of page numbers (0-indexed)
        If provided, only these pages are processed and a list of strings is
        returned in the same order. Otherwise the entire document is processed
        and a single joined string is returned.
    """

    if LatexOCR is None:
        raise ImportError(f"LatexOCR unavailable: {_import_error}")

    ocr_model = LatexOCR()
    converter = LatexNodes2Text()
    results: List[str] = []
    with fitz.open(pdf_path) as doc:
        if pages is None:
            page_numbers = range(len(doc))
        else:
            page_numbers = pages
        for pno in page_numbers:
            if pno >= len(doc):
                continue
            page = doc[pno]
            pix = page.get_pixmap()
            image = Image.open(BytesIO(pix.tobytes("png")))
            try:
                latex = ocr_model(image)
            except Exception as e:
                logger.error(f"LatexOCR failed on page {pno+1}: {e}")
                latex = ""
            results.append(converter.latex_to_text(latex))

    if pages is None:
        return "\n".join(results)
    return results


def detect_formulas(text: str) -> bool:
    """Heuristically determine if the text contains mathematical formulas."""
    math_keywords = ["\\int", "\\sum", "\\frac", "\\sqrt", "\\begin{equation}"]
    if any(k in text for k in math_keywords):
        return True
    special_chars = "+=-*^_{}[]()<>|\\/"
    special_count = sum(text.count(c) for c in special_chars)
    if len(text) > 0 and special_count / len(text) > 0.05:
        return True
    return False
