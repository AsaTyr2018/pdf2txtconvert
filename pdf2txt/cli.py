from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import click
from loguru import logger
from tqdm import tqdm

from .scanner import scan_pdfs
from .converter import convert_pdf_to_text
from .logger_config import configure


@click.command()
@click.option('--input-folder', required=True, type=click.Path(exists=True, file_okay=False))
@click.option('--output-folder', required=True, type=click.Path(file_okay=False))
@click.option('--overwrite', default='skip', type=click.Choice(['skip', 'yes', 'append']), show_default=True)
@click.option('--use-ocr', is_flag=True, help='Enable OCR fallback for image-based PDFs')
@click.option('--jobs', default=1, show_default=True, type=int, help='Number of parallel workers')
def main(input_folder, output_folder, overwrite, use_ocr, jobs):
    """Bulk convert PDF files to TXT."""
    output = Path(output_folder)
    output.mkdir(parents=True, exist_ok=True)
    log_file = output / 'conversion.log'
    configure(log_file)
    pdfs = scan_pdfs(input_folder)
    if not pdfs:
        logger.warning(f'No PDF files found in {input_folder}')
        return

    def process(pdf_path: Path):
        txt_path = output / f"{pdf_path.stem}.txt"
        return convert_pdf_to_text(pdf_path, txt_path, overwrite=overwrite, use_ocr=use_ocr)

    if jobs > 1:
        with ThreadPoolExecutor(max_workers=jobs) as executor:
            list(tqdm(executor.map(process, pdfs), total=len(pdfs), desc='Converting'))
    else:
        for pdf in tqdm(pdfs, desc='Converting'):
            process(pdf)


if __name__ == '__main__':
    main()
