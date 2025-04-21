import logging
import os
from typing import TYPE_CHECKING

import discord
from anyio import sleep

from utils.audio import generate_speech_from_text

if TYPE_CHECKING:
    from bot.client import DiscordBot


class VoiceCommands:
    """
    Handles voice-related commands for the Discord bot.
    """

    def __init__(self, bot: "DiscordBot"):
        self.bot = bot
        self._setup_commands()

    def _setup_commands(self):
        @self.bot.tree.command(
            name="korwin", description="Plays a random sentence from the catalogue"
        )
        async def play_message_from_catalogue(interaction: discord.Interaction):
            """
            Command that plays a random sentence from the catalogue in the voice channel.
            """
            # Check if the user is in a voice channel
            if not interaction.user.voice:
                await interaction.response.send_message(
                    "You need to be in a voice channel to use this command!", ephemeral=True
                )
                return

            await interaction.response.send_message("Playing a random sentence...", ephemeral=True)

            vc = await interaction.user.voice.channel.connect()
            vc.play(
                discord.FFmpegPCMAudio(
                    self.bot.catalogue.get_random_sentence_mp3().export(), pipe=True
                )
            )

            # Wait until the audio finishes playing
            while vc.is_playing():
                await sleep(0.1)

            await vc.disconnect()

        @self.bot.tree.command(name="bóg", description="Plays a custom text-to-speech message")
        async def play_custom_message(interaction: discord.Interaction, dziegiel: str):
            """
            Command that plays a custom text-to-speech message in the voice channel.
            Only the author can use this command.
            """
            # Check if the user is authorized
            if str(interaction.user.id) != str(os.getenv("AUTHOR_ID")):
                logging.warning(f"User {interaction.user.id} tried to use command wykurz")
                logging.warning(f"Only author - {os.getenv('AUTHOR_ID')} can use this command")
                await interaction.response.send_message(
                    "You are not authorized to use this command!", ephemeral=True
                )
                return

            # Check if the user is in a voice channel
            if not interaction.user.voice:
                await interaction.response.send_message(
                    "You need to be in a voice channel to use this command!", ephemeral=True
                )
                return

            await interaction.response.send_message(f"Playing: {dziegiel}", ephemeral=True)

            vc = await interaction.user.voice.channel.connect()
            vc.play(
                discord.FFmpegPCMAudio(
                    generate_speech_from_text(dziegiel, cache=self.bot.cache).export(), pipe=True
                )
            )

            # Wait until the audio finishes playing
            while vc.is_playing():
                await sleep(0.1)

            await vc.disconnect()
