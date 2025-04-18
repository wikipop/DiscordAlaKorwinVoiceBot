import hashlib
import logging
import pathlib
from time import sleep

import pandas as pd
from elevenlabs import ElevenLabs

from entities.Cache import Cache
from entities.Category import Category


class KorwinCatalogue:
    def __init__(self, df_link, api_key):
        self._df = pd.read_csv(df_link)
        self.api_key = api_key
        self.cache = Cache("./cache")

    @property
    def df(self):
        return self._df

    def get_random_text_from_category(self, category: Category) -> str:
        return self.df[category.value].dropna().sample(n=1).values[0]

    def generate_random_sentence(self) -> str:
        return " ".join([self.get_random_text_from_category(cat) for cat in Category])

    def check_if_all_is_cached(self):
        for category_name, category in self.get_text_hash_map().items():
            for cache_hash, text in category.items():
                if not pathlib.Path(f"./cache/{category_name}/{cache_hash}.mp3").exists():
                    return False
        return True

    def get_random_mp3_from_category(self, category: Category):
        return self.cache.load_random_mp3_from_category(category)

    def get_random_sentence_mp3(self):
        audio = self.get_random_mp3_from_category(category=Category.INTRO)
        audio.fade_in(400)
        for category in Category:
            if category == Category.INTRO:
                continue
            next_audio = self.get_random_mp3_from_category(category)
            next_audio.fade_in(400).fade_out(400)
            audio += next_audio
        return audio + 6

    def generate_cached_mp3(self):
        client = ElevenLabs(api_key=self.api_key)

        for category_name, category in self.get_text_hash_map().items():
            if not pathlib.Path(f"./cache/{category_name}").exists():
                pathlib.Path(f"./cache/{category_name}").mkdir()

            for cache_hash, text in category.items():
                if pathlib.Path(f"./cache/{category_name}/{cache_hash}.mp3").exists():
                    logging.info(f"Skipping {category_name}/{cache_hash}.mp3 - already exists")
                    continue

                previous_text, _, next_text = self.generate_random_pre_n_next_text_without_category(
                    Category(category_name))

                self.cache.save_mp3(audio=b"".join(
                    client.text_to_speech.convert(text=text,
                                                  voice_id="pqHfZKP75CvOlQylNhV4", model_id="eleven_flash_v2_5",
                                                  language_code="pl", output_format="mp3_44100_128", )),
                    category=Category(category_name), hash=cache_hash)

                logging.info(f"Generated {category_name}/{cache_hash}.mp3")
                sleep(1)

    def generate_random_pre_n_next_text_without_category(self, category: Category) -> (str, str):
        output = ["", "", ""]
        index = 0
        for cat in Category:
            if cat == category:
                index = 2
                output[1] += self.get_random_text_from_category(cat) + " "
                continue
            output[index] += self.get_random_text_from_category(cat) + " "
        return output

    def get_text_hash_map(self) -> dict[str, dict[str, str]]:
        hash_map_list: dict[str, dict[str, str]] = dict()

        for column in self.df.columns:
            hash_map_list[column] = dict()
            for cell in self.df[column]:
                if type(cell) is not str:
                    continue
                hash_map_list[column][hashlib.sha256(cell.encode("utf-8")).hexdigest()] = cell

        return hash_map_list
