import logging
import sys
from typing import Optional

from app.core.config import settings


def setup_logging(name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name or __name__)
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logger.level)
        formatter = logging.Formatter(settings.log_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logging("readmission_api")
