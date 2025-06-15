# pdf2txtconvert

`pdf2txt` is a command-line tool for bulk converting PDF files to plain text. It
scans an input directory for PDFs and saves the results to an output directory
with the same base filenames. A log file is created to record successes and
failures.

## Installation

Install dependencies with pip:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m pdf2txt --input-folder ./input_pdfs --output-folder ./output_txts
```

Options:

- `--overwrite [skip|yes|append]` – control existing TXT files (default `skip`).
- `--use-ocr` – enable OCR fallback for scanned PDFs (requires Tesseract).
- `--jobs N` – number of parallel workers (default `1`).

The log file `conversion.log` is written inside the output folder.

Note: OCR processing now renders pages with PyMuPDF, so Poppler is **not**
required for image-based PDFs.
