import logging
import os
import random
from asyncio import sleep

import discord
from discord import app_commands
from discord.ext import tasks

from bot.commands import VoiceCommands
from entities.catalogue import KorwinCatalogue


class DiscordBot(discord.Client):
    """
    Discord bot client that handles the bot's connection and commands.
    """

    def __init__(self, catalogue: KorwinCatalogue):
        # Set up intents
        intents = discord.Intents.default()
        intents.presences = True
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)

        # Initialize bot components
        self.tree = app_commands.CommandTree(self)
        self.catalogue = catalogue
        self.cache = catalogue.cache
        self.voice_commands = None

    @tasks.loop(minutes=3.5)
    async def korwin_with_interval(self):
        if random.random() > 0.1:
            return

        logging.info("Playing korwin with interval")
        guild_id = int(os.getenv("GUILD_ID"))

        vc = await max(
            self.get_guild(guild_id).voice_channels, key=lambda vc: len(vc.members)
        ).connect()

        vc.play(
            discord.FFmpegPCMAudio(self.catalogue.get_random_sentence_mp3().export(), pipe=True)
        )

        while vc.is_playing():
            await sleep(0.1)

        await vc.disconnect()
        logging.info("Korwin with interval finished")

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
        logging.info(f"Logged in as {self.user} (ID: {self.user.id})")
        await self.korwin_with_interval.start()
        logging.info("Korwin with interval started")
