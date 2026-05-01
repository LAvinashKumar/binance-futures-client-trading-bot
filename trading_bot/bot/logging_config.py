"""
Logging configuration for the Binance trading bot.
Sets up file-based and console logging with separate handlers for
requests, responses, and errors.
"""

import logging
import logging.handlers
import os
from pathlib import Path


LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

REQUEST_LOG = LOG_DIR / "requests.log"
ERROR_LOG = LOG_DIR / "errors.log"
GENERAL_LOG = LOG_DIR / "trading_bot.log"

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger with file and console handlers.

    Args:
        name: Logger name, typically __name__ of the calling module.

    Returns:
        Configured logging.Logger instance.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # General rotating file handler (DEBUG+)
    general_handler = logging.handlers.RotatingFileHandler(
        GENERAL_LOG, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    general_handler.setLevel(logging.DEBUG)
    general_handler.setFormatter(formatter)

    # Request/response file handler (INFO+)
    request_handler = logging.handlers.RotatingFileHandler(
        REQUEST_LOG, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    request_handler.setLevel(logging.INFO)
    request_handler.setFormatter(formatter)

    # Error file handler (ERROR+)
    error_handler = logging.handlers.RotatingFileHandler(
        ERROR_LOG, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Console handler (INFO+)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(general_handler)
    logger.addHandler(request_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    # Prevent messages from bubbling up to the root logger (avoids duplicate output)
    logger.propagate = False

    return logger
