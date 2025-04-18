import logging
import os

import discord
from anyio import sleep
from discord import app_commands
from entities.KorwinCatalogue import KorwinCatalogue
from utils.generate_voice_on_go import generate_speech_from_text


class HelloCommand:
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self._setup_commands()

    def _setup_commands(self):
        @self.bot.tree.command(name="dziegiel", description="dziegiel")
        async def hello(interaction: discord.Interaction):
            vc = await interaction.user.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(self.bot.catalogue.get_random_sentence_mp3().export(), pipe=True))
            while vc.is_playing():
                await sleep(0.1)
            await vc.disconnect()

        @self.bot.tree.command(name="wykurz", description="wykurz")
        async def wykurz(interaction: discord.Interaction, dziegiel: str):
            if str(interaction.user.id) != str(os.getenv("AUTHOR_ID")):
                logging.warning(f"User {interaction.user.id} tried to use command wykurz")
                logging.warning(f"Only author - {os.getenv("AUTHOR_ID")} can use this command")
                return

            vc = await interaction.user.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(generate_speech_from_text(dziegiel), pipe=True))
            while vc.is_playing():
                await sleep(0.1)
            await vc.disconnect()

class DiscordBot(discord.Client):
    def __init__(self, catalogue: KorwinCatalogue):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.catalogue = catalogue
        self.hello_command = None

    async def setup_hook(self):
        self.hello_command = HelloCommand(self)
        await self.tree.sync()

    async def on_ready(self):
        logging.info(f'Logged in as {self.user} (ID: {self.user.id})')

def run_discord_bot(catalogue: KorwinCatalogue):
    bot = DiscordBot(catalogue)
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
