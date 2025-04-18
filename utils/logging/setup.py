"""
Logging setup utilities for the KorwinAI Discord Bot.

This module provides functions for setting up and configuring logging.
"""

import logging
from typing import Optional


def setup_logging(log_file: str = "voice_generator.log", level: int = logging.INFO) -> None:
    """
    Set up logging configuration for the application.
    
    This function configures both file and console logging.
    
    Args:
        log_file (str, optional): Path to the log file. Defaults to "voice_generator.log".
        level (int, optional): Logging level. Defaults to logging.INFO.
    """
    logging.basicConfig(
        level=level,
        filename=log_file,
        filemode="w",
        format="[%(asctime)s] %(message)s"
    )
    
    # Add console logging
    logging.getLogger().addHandler(logging.StreamHandler())