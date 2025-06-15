from pathlib import Path
from typing import List


def scan_pdfs(folder: str) -> List[Path]:
    """Return a list of all PDF files under the given folder."""
    path = Path(folder)
    if not path.is_dir():
        raise NotADirectoryError(f"{folder} is not a directory")
    return sorted(path.rglob("*.pdf"))
