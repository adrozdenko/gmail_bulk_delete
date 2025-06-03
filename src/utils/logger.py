"""Logging utilities following Emex standards."""

import logging
import sys
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Get configured logger instance.

    Args:
        name: Logger name (usually __name__)
        level: Logging level

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, level.upper()))

    # Rich handler for beautiful console output
    console = Console(stderr=True)
    handler = RichHandler(
        console=console,
        show_time=True,
        show_path=False,
        markup=True
    )

    formatter = logging.Formatter(
        fmt="%(message)s",
        datefmt="[%X]"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger


def setup_file_logging(
    logger: logging.Logger,
    filename: str,
    level: str = "DEBUG"
) -> None:
    """Add file logging to existing logger.

    Args:
        logger: Logger instance to configure
        filename: Log file path
        level: File logging level
    """
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(getattr(logging, level.upper()))

    file_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)