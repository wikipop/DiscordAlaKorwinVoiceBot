"""
Cache module for the KorwinAI Discord Bot.

This module provides caching functionality for audio files generated from text segments.
"""

import logging
import pathlib
from abc import ABC
from typing import Union, Dict
from pydub import AudioSegment

from entities.catalogue.category import Category


class ICache(ABC):
    """
    Handles caching of audio files for the Korwin catalogue.

    This class provides methods to save and load MP3 files from a cache,
    organized by category.
    """
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        if not pathlib.Path(f"./{cache_dir}").exists():
            logging.info(f"Creating cache directory: {cache_dir}")
            pathlib.Path(f"./{cache_dir}").mkdir()
        logging.info(f"Cache directory: {cache_dir}")

    @staticmethod
    def _map_category_to_string(category: Category | str = None) -> str:
        raise NotImplemented

    def is_all_cached(self) -> bool:
        raise NotImplemented

    def is_hashmap_cached(self, hashmap: Dict[str, Dict[str, str]]) -> bool:
        raise NotImplemented

    def generate_category_directory(self, category: Category | str = None) -> None:
        raise NotImplemented

    def is_mp3_cached(self, hash: str, category: Category | str = None) -> bool:
        raise NotImplemented

    def save_mp3(self, audio: bytes, hash: str, category: Category | str = None) -> None:
        raise NotImplemented

    def load_mp3(self, hash: str, category: Category | str = None) -> AudioSegment:
        raise NotImplemented

    def load_random_mp3(self, category: Category | str = None) -> AudioSegment:
        raise NotImplemented
