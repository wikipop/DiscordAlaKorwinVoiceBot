"""
Cache module for the KorwinAI Discord Bot.

This module provides caching functionality for audio files generated from text segments.
"""

import random
import pathlib
from pydub import AudioSegment

from entities.catalogue.category import Category


class Cache:
    """
    Handles caching of audio files for the Korwin catalogue.
    
    This class provides methods to save and load MP3 files from a cache directory,
    organized by category.
    """
    def __init__(self, cache_dir):
        """
        Initialize the Cache with a specified cache directory.
        
        Args:
            cache_dir (str): Path to the directory where cached files are stored.
        """
        self.cache_dir = cache_dir

    def load_random_mp3_from_category(self, category: Category) -> AudioSegment:
        """
        Load a random MP3 file from the specified category.
        
        Args:
            category (Category): The category to load from.
            
        Returns:
            AudioSegment: The loaded audio segment.
        """
        directory = pathlib.Path(f"{self.cache_dir}/{category.value}")
        list_of_files = list(directory.glob("*.mp3"))
        return AudioSegment.from_mp3(random.choice(list_of_files))

    def save_mp3(self, audio: bytes, category: Category, hash: str) -> None:
        """
        Save an MP3 file to the cache.
        
        Args:
            audio (bytes): The audio data to save.
            category (Category): The category to save under.
            hash (str): The hash identifier for the file.
        """
        with open(f"{self.cache_dir}/{category.value}/{hash}.mp3", "wb") as f:
            f.write(audio)