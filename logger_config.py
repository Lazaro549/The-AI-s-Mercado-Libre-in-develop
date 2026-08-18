"""Logging configuration for the AI Mercado Libre Optimizer.

This module sets up logging for the entire application.
"""

import logging
import logging.handlers
from pathlib import Path
from config_loader import get_config


def setup_logging():
    """Configure logging for the application.
    
    Sets up both console and file handlers based on config.yaml settings.
    """
    config = get_config()
    log_config = config.get("logging", {})
    
    # Create logs directory if it doesn't exist
    log_dir = Path(log_config.get("file", "logs/app.log")).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Set root logger level
    log_level = getattr(logging, log_config.get("level", "INFO"))
    logging.basicConfig(level=log_level)
    
    # Create formatter
    formatter = logging.Formatter(log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # File handler with rotation
    log_file = log_config.get("file", "logs/app.log")
    max_bytes = log_config.get("max_file_size", 10485760)  # 10MB
    backup_count = log_config.get("backup_count", 5)
    
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setFormatter(formatter)
    
    # Add handlers to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.
    
    Args:
        name (str): The name of the logger (usually __name__).
        
    Returns:
        logging.Logger: Logger instance.
    """
    return logging.getLogger(name)
