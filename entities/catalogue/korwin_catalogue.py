"""
KorwinCatalogue module for the KorwinAI Discord Bot.

This module provides the main catalogue functionality for generating and managing
text and audio segments.
"""

import hashlib
import logging
import pathlib
from time import sleep
from typing import Dict, List, Optional, Tuple

import pandas as pd
from elevenlabs import ElevenLabs
from pydub import AudioSegment

from entities.catalogue.cache import Cache
from entities.catalogue.category import Category


class KorwinCatalogue:
    """
    Main catalogue class for managing text segments and their audio representations.

    This class handles loading text from a CSV file, generating random sentences,
    converting text to speech, and caching the results.
    """

    def __init__(self, df_link: str, api_key: str):
        """
        Initialize the KorwinCatalogue with a data source and API key.

        Args:
            df_link (str): Link to the CSV file containing text segments.
            api_key (str): ElevenLabs API key for text-to-speech conversion.
        """
        self._df = pd.read_csv(df_link)
        self.api_key = api_key
        self.cache = Cache("./cache")

    @property
    def df(self) -> pd.DataFrame:
        """
        Get the DataFrame containing text segments.

        Returns:
            pd.DataFrame: The DataFrame with text segments.
        """
        return self._df

    def get_random_text_from_category(self, category: Category) -> str:
        """
        Get a random text segment from the specified category.

        Args:
            category (Category): The category to get text from.

        Returns:
            str: A random text segment from the category.
        """
        return self.df[category.value].dropna().sample(n=1).values[0]

    def generate_random_sentence(self) -> str:
        """
        Generate a random sentence by combining text from all categories.

        Returns:
            str: The generated sentence.
        """
        return " ".join([self.get_random_text_from_category(cat) for cat in Category])

    def check_if_all_is_cached(self) -> bool:
        """
        Check if all text segments have corresponding cached audio files.

        Returns:
            bool: True if all segments are cached, False otherwise.
        """
        for category_name, category in self.get_text_hash_map().items():
            for cache_hash, text in category.items():
                if not pathlib.Path(f"./cache/{category_name}/{cache_hash}.mp3").exists():
                    return False
        return True

    def get_random_mp3_from_category(self, category: Category) -> AudioSegment:
        """
        Get a random MP3 file from the specified category.

        Args:
            category (Category): The category to get audio from.

        Returns:
            AudioSegment: The audio segment.
        """
        return self.cache.load_random_mp3_from_category(category)

    def get_random_sentence_mp3(self) -> AudioSegment:
        """
        Generate a random sentence as an audio segment by combining audio from all categories.

        Returns:
            AudioSegment: The combined audio segment.
        """
        audio = self.get_random_mp3_from_category(category=Category.INTRO)
        audio.fade_in(400)
        for category in Category:
            if category == Category.INTRO:
                continue
            next_audio = self.get_random_mp3_from_category(category)
            next_audio.fade_in(400).fade_out(400)
            audio += next_audio
        return audio + 6

    def generate_cached_mp3(self) -> None:
        """
        Generate and cache MP3 files for all text segments.

        This method uses the ElevenLabs API to convert text to speech and
        caches the results for future use.
        """
        client = ElevenLabs(api_key=self.api_key)

        for category_name, category in self.get_text_hash_map().items():
            if not pathlib.Path(f"./cache/{category_name}").exists():
                pathlib.Path(f"./cache/{category_name}").mkdir()

            for cache_hash, text in category.items():
                if pathlib.Path(f"./cache/{category_name}/{cache_hash}.mp3").exists():
                    logging.info(f"Skipping {category_name}/{cache_hash}.mp3 - already exists")
                    continue

                previous_text, _, next_text = self.generate_random_pre_n_next_text_without_category(
                    Category(category_name)
                )

                self.cache.save_mp3(
                    audio=b"".join(
                        client.text_to_speech.convert(
                            text=text,
                            voice_id="pqHfZKP75CvOlQylNhV4",
                            model_id="eleven_flash_v2_5",
                            language_code="pl",
                            output_format="mp3_44100_128",
                        )
                    ),
                    category=Category(category_name),
                    hash=cache_hash,
                )

                logging.info(f"Generated {category_name}/{cache_hash}.mp3")
                sleep(1)

    def generate_random_pre_n_next_text_without_category(
        self, category: Category
    ) -> Tuple[str, str, str]:
        """
        Generate random text before and after the specified category.

        Args:
            category (Category): The category to exclude.

        Returns:
            Tuple[str, str, str]: A tuple containing (previous_text, current_text, next_text).
        """
        output = ["", "", ""]
        index = 0
        for cat in Category:
            if cat == category:
                index = 2
                output[1] += self.get_random_text_from_category(cat) + " "
                continue
            output[index] += self.get_random_text_from_category(cat) + " "
        return output

    def get_text_hash_map(self) -> Dict[str, Dict[str, str]]:
        """
        Get a mapping of text segments to their hash values, organized by category.

        Returns:
            Dict[str, Dict[str, str]]: A dictionary mapping category names to dictionaries
                mapping hash values to text segments.
        """
        hash_map_list: Dict[str, Dict[str, str]] = dict()

        for column in self.df.columns:
            hash_map_list[column] = dict()
            for cell in self.df[column]:
                if type(cell) is not str:
                    continue
                hash_map_list[column][hashlib.sha256(cell.encode("utf-8")).hexdigest()] = cell

        return hash_map_list
