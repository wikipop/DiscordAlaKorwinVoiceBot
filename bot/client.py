import logging

import discord
from discord import app_commands

from entities.catalogue import KorwinCatalogue
from bot.commands import VoiceCommands


class DiscordBot(discord.Client):
    """
    Discord bot client that handles the bot's connection and commands.
    """
    def __init__(self, catalogue: KorwinCatalogue):
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        
        # Initialize bot components
        self.tree = app_commands.CommandTree(self)
        self.catalogue = catalogue
        self.voice_commands = None

    async def setup_hook(self):
        """
        Sets up the bot's commands and syncs the command tree.
        This is called automatically when the bot starts.
        """
        self.voice_commands = VoiceCommands(self)
        await self.tree.sync()
        logging.info("Command tree synced")

    async def on_ready(self):
        """
        Called when the bot is ready and connected to Discord.
        """
        logging.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logging.info('------')