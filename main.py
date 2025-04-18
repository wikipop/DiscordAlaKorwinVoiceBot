import os

from pydub.playback import play

from bot import run_discord_bot
from entities.Category import Category
from entities.KorwinCatalogue import KorwinCatalogue
from dotenv import load_dotenv
import logging
import discord
from utils.setup_logging import setup_logging

load_dotenv()

GOOGLE_SHEETS_LINK = os.getenv("GOOGLE_SHEETS_LINK")
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

if __name__ == '__main__':
    setup_logging()

    catalogue = KorwinCatalogue(GOOGLE_SHEETS_LINK, ELEVEN_LABS_API_KEY)

    logging.info("Checking if all texts are cached...")
    if catalogue.check_if_all_is_cached():
        logging.info("All texts are cached")
    else:
        logging.warning("Not all texts are cached")
        logging.warning("Would you like to generate them now?")
        if input("(y/N): ") == "y":
            logging.info("Generating all texts...")
            catalogue.generate_cached_mp3()
            logging.info("Generated all texts")
        else:
            logging.error("Cannot continue without cached texts")
            exit(1)

        logging.info("All texts are cached! Have fun :3")

    run_discord_bot(catalogue)