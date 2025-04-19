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

from entities import Cache


def generate_speech_from_text(text: str) -> AudioSegment:
    """
    Generate speech from text using the ElevenLabs API.

    Args:
        text (str): The text to convert to speech.

    Returns:
        BinaryIO: A binary stream containing the generated MP3 audio.
    """
    cache = Cache(cache_dir="cache")

    if cached_mp3 := cache.is_custom_mp3_cached(text):
        logging.info(f"Using cached MP3 for {text} - by hash")
        return cached_mp3 + 6

    text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if cached_mp3 := cache.is_custom_mp3_cached(text_hash):
        logging.info(f"Using cached MP3 for {text_hash}")
        return cached_mp3 + 6

    logging.info(f"Generating MP3 for {text_hash}")
    client = ElevenLabs(api_key=os.environ["ELEVEN_LABS_API_KEY"])
    audio = b"".join(client.text_to_speech.convert(
        text=text, voice_id="pqHfZKP75CvOlQylNhV4", model_id="eleven_flash_v2_5",
        language_code="pl", output_format="mp3_44100_128", ))

    logging.info(f"Saving MP3 for {text_hash}")
    cache.save_custom_mp3(audio, text_hash)

    return cache.load_custom_mp3(text_hash) + 6
