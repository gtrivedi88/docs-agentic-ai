"""
Structured logging configuration for Lyra.
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from rich.logging import RichHandler
from src.config.settings import settings


def setup_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    Setup structured logger with console and file handlers.
    
    Args:
        name: Logger name (usually __name__)
        log_file: Optional log file path
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with Rich formatting
    console_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=True,
        show_path=True
    )
    console_handler.setLevel(settings.log_level)
    console_format = logging.Formatter(
        "%(message)s",
        datefmt="[%X]"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler
    file_path = log_file or settings.log_file
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.DEBUG)  # Always log everything to file
    file_format = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    return logger


# Global logger
logger = setup_logger("lyra")

