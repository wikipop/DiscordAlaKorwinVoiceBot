import pathlib
import random
from typing import Dict

from pydub import AudioSegment

from entities.cache import ICache
from entities.catalogue.category import Category


class LocalCache(ICache):
    def __init__(self, cache_dir):
        super().__init__(pathlib.Path(cache_dir))

    @staticmethod
    def _map_category_to_string(category: Category | str = None):
        match category:
            case category if category is None:
                return "custom"
            case category if isinstance(category, Category):
                return category.value
            case category if isinstance(category, str):
                return category
            case _:
                raise ValueError("category must be a Category or None")

    def is_hashmap_cached(self, hashmap: Dict[str, Dict[str, str]]) -> bool:
        for category_name, category in hashmap.items():
            for cache_hash, text in category.items():
                if not self.is_mp3_cached(category=Category(category_name), hash=cache_hash):
                    return False
        return True

    def generate_category_directory(self, category: Category | str = None) -> None:
        category_dir = self._map_category_to_string(category)

        if not self.cache_dir.joinpath(category_dir).exists():
            self.cache_dir.joinpath(category_dir).mkdir()

    def is_mp3_cached(self, hash: str, category: Category | str = None) -> bool:
        category_dir = self._map_category_to_string(category)

        return self.cache_dir.joinpath(category_dir, f"{hash}.mp3").exists()

    def save_mp3(self, audio: bytes, hash: str, category: Category | str = None) -> None:
        category_dir = self._map_category_to_string(category)

        self.generate_category_directory(category)

        with open(self.cache_dir.joinpath(category_dir, f"{hash}.mp3"), "wb") as f:
            f.write(audio)

    def load_mp3(self, hash: str, category: Category | str = None) -> AudioSegment:
        category_dir = self._map_category_to_string(category)

        return AudioSegment.from_mp3(self.cache_dir.joinpath(category_dir, f"{hash}.mp3"))

    def load_random_mp3(self, category: Category | str = None) -> AudioSegment:
        category_dir = self._map_category_to_string(category)
        list_of_files = list(self.cache_dir.joinpath(category_dir).glob("*.mp3"))

        return AudioSegment.from_mp3(random.choice(list_of_files))
