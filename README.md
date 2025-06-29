# pdf2txtconvert

`pdf2txt` is a minimal command line tool for turning a folder full of PDFs into plain text files. It preserves file names, writes a `conversion.log` with successes and errors and can optionally use OCR for scanned PDFs.

## Quick start

The easiest way to install is the one-line curl setup which downloads this repository and runs the installer:

```bash
curl -sSL https://raw.githubusercontent.com/AsaTyr2018/pdf2txtconvert/main/quick_install.sh | bash
```

After installation you will find `pdf2txt` in `/opt/pdf2txtconvert` along with helper scripts. To update or remove it simply rerun the script with `--update` or `--deinstall`.

## Manual installation

Clone the repository and install the Python requirements yourself if you prefer a local checkout:

```bash
git clone https://github.com/AsaTyr2018/pdf2txtconvert.git
cd pdf2txtconvert
pip install -r requirements.txt
```

## Usage

Run the converter by pointing it at an input directory with PDFs and an output directory for the text files:

```bash
python -m pdf2txt --input-folder ./input_pdfs --output-folder ./output_txts
```

### Useful options

- `--overwrite [skip|yes|append]` – what to do if the TXT already exists (default `skip`)
- `--use-ocr` – enable OCR fallback for scanned PDFs
- `--via-latex` – force LaTeX-OCR on all pages for better formula handling. Without this flag the first pages are scanned for formulas and automatically reprocessed when needed.
- `--jobs N` – number of parallel workers (default `1`)

The log file `conversion.log` is created in the output directory. OCR no longer needs Poppler because pages are rendered with PyMuPDF.

### Handling mathematical formulas

Extraction now preserves whitespace and ligatures so multi-line mathematical formulas and special characters survive conversion. The PyMuPDF extraction flags were adjusted to keep spaces even when PDFs lack explicit space characters.
When the optional `--via-latex` flag is used, pages are processed with [LaTeX-OCR](https://github.com/lukas-blecher/LaTeX-OCR) to generate LaTeX code first and then converted to plain text for improved table and formula handling.
Without the flag the first pages are scanned automatically and rerun through LaTeX-OCR whenever formulas are detected.

## setup.sh helper

`setup.sh` installs the project to `/opt/pdf2txtconvert` with a virtual environment and fixed input/output folders.

```
./setup.sh --install [--daemon] [--gpu]
./setup.sh --deinstall
./setup.sh --update [--gpu]
```

Use `--gpu` during install or update to set up PyTorch with CUDA support. Passing `--daemon` adds a cron entry to process PDFs every five minutes. Logs are stored alongside the installation.
