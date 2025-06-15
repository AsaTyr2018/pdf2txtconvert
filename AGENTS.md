# Agent Task: Create the Ultimate PDF-to-TXT Converter Tool

## Objective

Build a robust and efficient tool that converts PDF files into plain text (TXT) format in bulk. The tool must be designed for automation and minimal user interaction, suitable for large-scale processing environments.

## Key Features

- **Bulk Processing**: The tool must scan an input directory for all `.pdf` files and convert each to `.txt` format.
- **Structured Output**: All resulting `.txt` files should be saved in a specified output directory, preserving original filenames.
- **Robust Parsing**: The tool must handle a wide variety of PDFs (text-based, scanned, multi-column, etc.).
- **Logging**: Log each processed file, any errors, and conversion time.
- **Overwrite Handling**: Provide an option to skip, overwrite, or append if the `.txt` file already exists.
- **CLI Compatible**: Tool must be executable via CLI with parameters for input/output folders and optional flags.
- **Modular Design**: Code should be modular for easy replacement or enhancement of PDF-parsing engines (e.g., PyMuPDF, pdfminer.six, OCR engines like Tesseract).

## Input

- A folder containing any number of `.pdf` files (e.g., `/input_pdfs/`)
- CLI options:
  - `--input-folder`: Path to folder with PDF files.
  - `--output-folder`: Path to save converted TXT files.
  - `--overwrite [skip|yes|append]`: Behavior when TXT file already exists.
  - `--use-ocr`: (Optional) Enable OCR fallback for image-based PDFs.

## Output

- A folder (e.g., `/output_txts/`) containing one `.txt` file for each input `.pdf`.
- Each output file name must match the input file (e.g., `invoice_001.pdf` → `invoice_001.txt`).
- A `conversion.log` file tracking success/fail status per file.

## Examples

### Example 1 – Basic Usage

```bash
pdf2txt --input-folder ./input_pdfs --output-folder ./output_txts
```

Result:
- All PDFs in `./input_pdfs/` are converted to `.txt` files in `./output_txts/`.

### Example 2 – Overwrite Existing

```bash
pdf2txt --input-folder ./input_pdfs --output-folder ./output_txts --overwrite yes
```

Result:
- If a TXT file already exists in the output folder, it is overwritten.

### Example 3 – Use OCR Fallback

```bash
pdf2txt --input-folder ./input_pdfs --output-folder ./output_txts --use-ocr
```

Result:
- The tool attempts OCR on PDFs that fail standard text extraction.

## Agent Implementation Suggestions

1. Use Python with libraries such as:
   - `PyMuPDF` (fitz) for fast and accurate parsing.
   - `pdfminer.six` as a fallback parser.
   - `pytesseract` for OCR support (if `--use-ocr` flag is enabled).
2. Implement parallel processing using `concurrent.futures` or `asyncio` for faster bulk conversion.
3. Include basic error handling for corrupted or password-protected PDFs.
4. Structure code into clear modules:
   - `scanner.py` → scans input directory
   - `converter.py` → handles parsing & conversion
   - `ocr_fallback.py` → triggers OCR when needed
   - `logger.py` → tracks status and writes logs
5. Ensure clean separation between CLI interface and core logic for easy testing or GUI extension later.

## Final Goal

A dependable command-line tool that can be integrated into larger automation systems, run on servers, or scheduled via cron jobs — ideal for digital archiving, data extraction pipelines, and document processing tasks at scale.

