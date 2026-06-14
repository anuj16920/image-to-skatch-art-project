"""Professional logging system with multiple handlers."""

from __future__ import annotations
import logging
import sys
from pathlib import Path
from typing import Optional, Callable
from datetime import datetime


class Logger:
    """
    Thread-safe logger with file and console output.
    
    Attributes:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        callback: Optional GUI callback for log messages
    """
    
    def __init__(
        self,
        name: str = "ArtAnimator",
        level: str = "INFO",
        log_file: Optional[Path] = None,
    ):
        self.name = name
        self.callback: Optional[Callable[[str], None]] = None
        
        # Create logger
        self._logger = logging.getLogger(name)
        self._logger.setLevel(getattr(logging, level.upper()))
        self._logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)
        
        # File handler (optional)
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self._logger.addHandler(file_handler)
    
    def log(self, msg: str, level: str = "INFO") -> None:
        """Log a message at the specified level."""
        log_func = getattr(self._logger, level.lower())
        log_func(msg)
        
        if self.callback:
            ts = datetime.now().strftime("%H:%M:%S")
            self.callback(f"[{ts}] {msg}")
    
    def debug(self, msg: str) -> None:
        """Log debug message."""
        self.log(msg, "DEBUG")
    
    def info(self, msg: str) -> None:
        """Log info message."""
        self.log(msg, "INFO")
    
    def warning(self, msg: str) -> None:
        """Log warning message."""
        self.log(msg, "WARNING")
    
    def error(self, msg: str) -> None:
        """Log error message."""
        self.log(msg, "ERROR")
    
    def critical(self, msg: str) -> None:
        """Log critical message."""
        self.log(msg, "CRITICAL")
