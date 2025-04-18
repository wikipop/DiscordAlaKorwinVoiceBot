"""
Utilities package for the KorwinAI Discord Bot.

This package contains various utility functions and modules used throughout the application.
"""

from utils.audio import generate_speech_from_text
from utils.logging import setup_logging

__all__ = ["generate_speech_from_text", "setup_logging"]
