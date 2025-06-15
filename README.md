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

### Setup Script

The repository includes a `setup.sh` script that can install the converter to
`/opt/pdf2txtconvert` with a Python virtual environment and fixed input/output
folders. The script accepts the following commands:

```
./setup.sh --install [--daemon]
./setup.sh --deinstall
./setup.sh --update
```

`--install` copies the project to `/opt/pdf2txtconvert`, installs dependencies
(including Tesseract if available), and creates a `run_converter.sh` helper in
that directory. If `--daemon` is supplied, a cron job is added to run the
converter every five minutes. Use `--deinstall` to remove the installation and
`--update` to pull the latest changes from git.

### Quick Install via Curl

For a one-liner installation that clones the repository and runs the setup
script, use the provided `quick_install.sh` helper. This requires `git` and
`sudo` to be available on the machine.

```bash
curl -sSL https://raw.githubusercontent.com/youruser/pdf2txtconvert/main/quick_install.sh | bash
```

Any arguments after the script URL are passed directly to `setup.sh`. For
example, to install and enable daemon mode:

```bash
curl -sSL https://raw.githubusercontent.com/youruser/pdf2txtconvert/main/quick_install.sh | bash -s -- --daemon
```

