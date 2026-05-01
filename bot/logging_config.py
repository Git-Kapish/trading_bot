"""Logging configuration for trading bot."""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name: str = "trading_bot") -> logging.Logger:
    """
    Set up a logger that writes to both file and console.
    
    Logs are written to logs/trading_bot.log with rotation when file size exceeds 1MB.
    Console output is also enabled for real-time feedback.
    
    Args:
        name: Logger name (default: "trading_bot")
    
    Returns:
        Configured logger instance.
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    log_file = os.path.join(logs_dir, "trading_bot.log")
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Format for log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # File handler with rotation (max 1MB per file, keep 5 backups)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
