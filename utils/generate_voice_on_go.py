import io
import os

from discord import AudioSource
from elevenlabs import ElevenLabs


def generate_speech_from_text(text):
    client = ElevenLabs(api_key=os.environ["ELEVEN_LABS_API_KEY"])
    return io.BytesIO(
        b"".join(
            client.text_to_speech.convert(
                text=text,
                voice_id="pqHfZKP75CvOlQylNhV4",
                model_id="eleven_flash_v2_5",
                language_code="pl",
                output_format="mp3_44100_128",
            )
        )
    )
