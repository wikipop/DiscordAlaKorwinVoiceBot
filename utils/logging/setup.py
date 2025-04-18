"""
Logging setup utilities for the KorwinAI Discord Bot.

This module provides functions for setting up and configuring logging.
"""

import logging
from typing import Optional


def setup_logging(log_file: str = "voice_generator.log", level: int = logging.INFO) -> None:
    """
    Set up logging configuration for the application.

    This function configures both file and console logging with consistent formatting.

    Args:
        log_file (str, optional): Path to the log file. Defaults to "voice_generator.log".
        level (int, optional): Logging level. Defaults to logging.INFO.
    """
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Create formatters
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Set up file handler
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)