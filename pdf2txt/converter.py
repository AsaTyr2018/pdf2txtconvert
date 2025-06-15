from pathlib import Path
from loguru import logger
import fitz  # PyMuPDF

# Flags to preserve layout and special characters
MUPDF_FLAGS = (
    fitz.TEXT_PRESERVE_WHITESPACE
    | fitz.TEXT_PRESERVE_LIGATURES
    | fitz.TEXT_INHIBIT_SPACES
)
from pdfminer.high_level import extract_text as pdfminer_extract

from .ocr_fallback import ocr_pdf_to_text
from .latex_converter import detect_formulas, extract_with_latexocr


def extract_with_pymupdf(pdf_path: Path) -> str:
    """Extract text from a PDF using PyMuPDF with layout preservation."""
    text = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text.append(page.get_text("text", flags=MUPDF_FLAGS))
    return "\n".join(text)


def extract_with_pdfminer(pdf_path: Path) -> str:
    return pdfminer_extract(str(pdf_path))


def convert_pdf_to_text(
    pdf_path: Path,
    txt_path: Path,
    *,
    overwrite: str = "skip",
    use_ocr: bool = False,
    via_latex: bool = False,
) -> str:
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
        if via_latex:
            text = extract_with_latexocr(pdf_path)
        else:
            page_texts = []
            first_pages = []
            with fitz.open(pdf_path) as doc:
                for i, page in enumerate(doc):
                    ptext = page.get_text("text", flags=MUPDF_FLAGS)
                    page_texts.append(ptext)
                    if i < 2:
                        first_pages.append(ptext)
            text = "\n".join(page_texts)

            if not text.strip():
                text = extract_with_pdfminer(pdf_path)
                page_texts = [text]
            if not text.strip() and use_ocr:
                text = ocr_pdf_to_text(pdf_path)
                page_texts = [text]

            if first_pages and detect_formulas("\n".join(first_pages)):
                try:
                    latex_pages = extract_with_latexocr(pdf_path, pages=range(min(2, len(page_texts))))
                    for idx, ltxt in enumerate(latex_pages):
                        if idx < len(page_texts):
                            page_texts[idx] = ltxt
                    text = "\n".join(page_texts)
                except Exception as e:
                    logger.error(f"LaTeX-OCR auto retry failed for {pdf_path.name}: {e}")
        if not text:
            raise ValueError("No text extracted")
        with open(txt_path, mode, encoding="utf-8") as f:
            f.write(text)
        logger.success(f"Converted {pdf_path.name}")
        return "success"
    except Exception as e:
        logger.error(f"Failed {pdf_path.name}: {e}")
        return "error"
