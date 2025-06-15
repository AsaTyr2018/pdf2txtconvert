from pathlib import Path
from loguru import logger
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text as pdfminer_extract

from .ocr_fallback import ocr_pdf_to_text


def extract_with_pymupdf(pdf_path: Path) -> str:
    text = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text)


def extract_with_pdfminer(pdf_path: Path) -> str:
    return pdfminer_extract(str(pdf_path))


def convert_pdf_to_text(pdf_path: Path, txt_path: Path, *, overwrite: str = "skip", use_ocr: bool = False) -> str:
    """Convert a PDF to text file. Returns status string."""
    mode = "w"
    if txt_path.exists():
        if overwrite == "skip":
            logger.info(f"Skipping {pdf_path.name} (exists)")
            return "skipped"
        elif overwrite == "append":
            mode = "a"
        else:
            mode = "w"
    try:
        text = extract_with_pymupdf(pdf_path)
        if not text.strip():
            text = extract_with_pdfminer(pdf_path)
        if not text.strip() and use_ocr:
            text = ocr_pdf_to_text(pdf_path)
        if not text:
            raise ValueError("No text extracted")
        with open(txt_path, mode, encoding="utf-8") as f:
            f.write(text)
        logger.success(f"Converted {pdf_path.name}")
        return "success"
    except Exception as e:
        logger.error(f"Failed {pdf_path.name}: {e}")
        return "error"
