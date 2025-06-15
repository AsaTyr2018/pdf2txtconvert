# pdf2txtconvert

`pdf2txt` is a minimal command line tool for turning a folder full of PDFs into plain text files. It preserves file names, writes a `conversion.log` with successes and errors and can optionally use OCR for scanned PDFs.

## Quick start

The easiest way to install is the one-line curl setup which downloads this repository and runs the installer:

```bash
curl -sSL https://raw.githubusercontent.com/youruser/pdf2txtconvert/main/quick_install.sh | bash
```

After installation you will find `pdf2txt` in `/opt/pdf2txtconvert` along with helper scripts. To update or remove it simply rerun the script with `--update` or `--deinstall`.

## Manual installation

Clone the repository and install the Python requirements yourself if you prefer a local checkout:

```bash
git clone https://github.com/youruser/pdf2txtconvert.git
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
- `--jobs N` – number of parallel workers (default `1`)

The log file `conversion.log` is created in the output directory. OCR no longer needs Poppler because pages are rendered with PyMuPDF.

## setup.sh helper

`setup.sh` installs the project to `/opt/pdf2txtconvert` with a virtual environment and fixed input/output folders.

```
./setup.sh --install [--daemon]
./setup.sh --deinstall
./setup.sh --update
```

Passing `--daemon` adds a cron entry to process PDFs every five minutes. Logs are stored alongside the installation.
