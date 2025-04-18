"""
Main entry point for the KorwinAI Discord Bot.

This module initializes the application, sets up logging, loads the catalogue,
and starts the Discord bot.
"""

import os
import logging
from dotenv import load_dotenv

from entities import KorwinCatalogue
from utils import setup_logging
from bot import run_discord_bot


def main():
    """
    Main function that initializes and runs the application.
    """
    # Load environment variables
    load_dotenv()

    # Set up logging
    setup_logging()

    # Get configuration from environment variables
    google_sheets_link = os.getenv("GOOGLE_SHEETS_LINK")
    eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")

    if not google_sheets_link or not eleven_labs_api_key:
        logging.error("Missing required environment variables: GOOGLE_SHEETS_LINK and/or ELEVEN_LABS_API_KEY")
        return

    # Initialize the catalogue
    logging.info("Initializing Korwin catalogue...")
    catalogue = KorwinCatalogue(google_sheets_link, eleven_labs_api_key)

    # Check if all texts are cached
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
            return

        logging.info("All texts are cached! Have fun :3")

    # Run the Discord bot
    logging.info("Starting Discord bot...")
    run_discord_bot(catalogue)


if __name__ == '__main__':
    main()
