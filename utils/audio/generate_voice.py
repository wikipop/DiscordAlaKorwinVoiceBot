"""
Voice generation utilities for the KorwinAI Discord Bot.

This module provides functions for generating speech from text using the ElevenLabs API.
"""

import io
import os
from typing import BinaryIO

from elevenlabs import ElevenLabs


def generate_speech_from_text(text: str) -> BinaryIO:
    """
    Generate speech from text using the ElevenLabs API.
    
    Args:
        text (str): The text to convert to speech.
        
    Returns:
        BinaryIO: A binary stream containing the generated MP3 audio.
    """
    client = ElevenLabs(api_key=os.environ["ELEVEN_LABS_API_KEY"])
    return io.BytesIO(b"".join(
        client.text_to_speech.convert(
            text=text,
            voice_id="pqHfZKP75CvOlQylNhV4",
            model_id="eleven_flash_v2_5",
            language_code="pl",
            output_format="mp3_44100_128",
        )))