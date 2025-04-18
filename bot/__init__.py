import os
import logging

from entities.catalogue import KorwinCatalogue
from bot.client import DiscordBot


def run_discord_bot(catalogue: KorwinCatalogue):
    """
    Initializes and runs the Discord bot with the provided catalogue.
    
    Args:
        catalogue: The KorwinCatalogue instance to use for the bot.
    """
    logging.info("Initializing Discord bot...")
    bot = DiscordBot(catalogue)
    
    # Get the Discord bot token from environment variables
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logging.error("DISCORD_BOT_TOKEN environment variable not set!")
        raise ValueError("DISCORD_BOT_TOKEN environment variable not set!")
    
    logging.info("Starting Discord bot...")
    bot.run(token)