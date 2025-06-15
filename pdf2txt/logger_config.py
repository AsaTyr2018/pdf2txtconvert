from pathlib import Path
from loguru import logger
import sys


def configure(log_file: Path):
    """Configure loguru logger to log to stderr and a file."""
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger.add(log_file, level="INFO", rotation="5 MB")
    return logger
