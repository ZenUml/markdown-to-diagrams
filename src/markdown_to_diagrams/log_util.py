"""Module for handling logging operations"""

import logging
import os
from datetime import datetime
from typing import Optional, Union
from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme

# Environment variable name for log level
LOG_LEVEL_ENV = "DEEP_RESEARCH_LOG_LEVEL"

class LogUtil:
    """Class for managing logging operations"""

    _instance = None
    _initialized = False
    _console = None

    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super(LogUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize logging configuration"""
        if not LogUtil._initialized:
            # Initialize Rich console with custom theme
            self._console = Console(theme=Theme({
                "info": "cyan",
                "warning": "yellow",
                "error": "red",
                "critical": "red bold",
                "debug": "dim cyan"
            }))
            
            # Get log level from environment variable or default to INFO
            log_level_str = os.getenv(LOG_LEVEL_ENV, 'INFO').upper()
            try:
                log_level = getattr(logging, log_level_str)
            except AttributeError:
                log_level = logging.INFO
                print(f"Invalid log level {log_level_str}, defaulting to INFO")
            
            self.logger = logging.getLogger('deep_research')
            self.logger.setLevel(log_level)
            LogUtil._initialized = True
            self._setup_logging()

    def _setup_logging(self):
        """Setup logging configuration with Rich handler"""
        # Create Rich handler with custom format
        rich_handler = RichHandler(
            console=self._console,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            show_time=True,
            show_path=True,
            enable_link_path=True
        )
        rich_handler.setLevel(logging.DEBUG)
        
        # Set format to include minimal timestamp since Rich handler adds its own
        rich_handler.setFormatter(logging.Formatter('%(message)s', datefmt='[%X]'))
        
        # Remove any existing handlers and add Rich handler
        self.logger.handlers = []
        self.logger.addHandler(rich_handler)

    def debug(self, message: str, *args, **kwargs):
        """Log debug message with Rich formatting

        Args:
            message: The message to log
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log info message with Rich formatting

        Args:
            message: The message to log
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log warning message with Rich formatting

        Args:
            message: The message to log
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log error message with Rich formatting

        Args:
            message: The message to log
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log critical message with Rich formatting

        Args:
            message: The message to log
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.logger.critical(message, *args, **kwargs)

    @staticmethod
    def get_logger() -> 'LogUtil':
        """Get singleton instance of LogUtil

        Returns:
            LogUtil instance
        """
        return LogUtil()

if __name__ == "__main__":
    # Create logger instance
    logger = LogUtil.get_logger()

    # Example usage of different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")