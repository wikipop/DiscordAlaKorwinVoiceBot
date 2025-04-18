import random

from entities.Category import Category
from pydub import AudioSegment
import pathlib

class Cache:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def load_random_mp3_from_category(self, category: Category):
        directory = pathlib.Path(f"{self.cache_dir}/{category.value}")
        list_of_files = list(directory.glob("*.mp3"))
        return AudioSegment.from_mp3(random.choice(list_of_files))

    def save_mp3(self, audio: bytes, category: Category, hash: str):
        with open(f"{self.cache_dir}/{category.value}/{hash}.mp3", "wb") as f:
            f.write(audio)