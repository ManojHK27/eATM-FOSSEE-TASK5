"""Central logging configuration."""
import logging
from pathlib import Path

def get_logger(log_file):
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("eATM")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(handler)
    return logger
