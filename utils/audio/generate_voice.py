"""
Voice generation utilities for the KorwinAI Discord Bot.

This module provides functions for generating speech from text using the ElevenLabs API.
"""
import hashlib
import io
import logging
import os
from typing import BinaryIO

from elevenlabs import ElevenLabs
from pydub import AudioSegment

from entities import LocalCache
from entities.cache import ICache


def generate_speech_from_text(text: str, cache: ICache) -> AudioSegment:
    """
    Generate speech from text using the ElevenLabs API.

    Args:
        text (str): The text to convert to speech.
        cache (ICache): The cache instance to use for caching.

    Returns:
        BinaryIO: A binary stream containing the generated MP3 audio.
    """

    if cache.is_mp3_cached(text):
        logging.info(f"Using cached MP3 for {text} - by hash")
        return cache.load_mp3(text) + 6

    text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if cache.is_mp3_cached(text_hash):
        logging.info(f"Using cached MP3 for {text_hash}")
        return cache.load_mp3(text_hash) + 6

    logging.info(f"Generating MP3 for {text_hash}")
    client = ElevenLabs(api_key=os.environ["ELEVEN_LABS_API_KEY"])
    audio = b"".join(client.text_to_speech.convert(
        text=text, voice_id="pqHfZKP75CvOlQylNhV4", model_id="eleven_flash_v2_5",
        language_code="pl", output_format="mp3_44100_128", ))

    logging.info(f"Saving MP3 for {text_hash}")
    cache.save_mp3(audio, text_hash)

    return cache.load_mp3(text_hash) + 6
