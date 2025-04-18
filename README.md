# KorwinAI Discord Bot

A Discord bot that generates and plays Korwin-style sentences, combining random text segments into humorous audio clips.

## Features

- Generate random sentences by combining text segments from different categories
- Play generated sentences in Discord voice channels
- Text-to-speech functionality using ElevenLabs API
- Caching of generated audio for better performance

## Setup

1. Clone the repository
2. Install dependencies:

   Using pip:
   ```
   pip install -e .
   ```

   Alternatively, using uv (faster alternative to pip):
   ```
   uv sync
   ```
3. Create a `.env` file with the following variables:
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token
   GOOGLE_SHEETS_LINK=your_google_sheets_link (or you can use mine https://docs.google.com/spreadsheets/d/1w9nfZaAWvT_jBd0zKkj2zD2cV4k0bYS5FMD-UAa76ng/export?gid=0&format=csv)
   ELEVEN_LABS_API_KEY=your_elevenlabs_api_key
   AUTHOR_ID=your_discord_user_id
   ```
4. Run the bot:
   ```
   python main.py
   uv run main.py
   ```

## Docker

You can run the bot using Docker:

1. Build the Docker image:
   ```
   docker build -t korwinai-discord-bot .
   ```

2. Run the Docker container with your environment variables:
   ```
   docker run -d \
     -e DISCORD_BOT_TOKEN=your_discord_bot_token \
     -e GOOGLE_SHEETS_LINK=your_google_sheets_link \
     -e ELEVEN_LABS_API_KEY=your_elevenlabs_api_key \
     -e AUTHOR_ID=your_discord_user_id \
     -e GUILD_ID=your_guild_id \
     --name korwinai-bot \
     korwinai-discord-bot
   ```

3. View logs:
   ```
   docker logs -f korwinai-bot
   ```

4. Stop the bot:
   ```
   docker stop korwinai-bot
   ```

5. Remove the container:
   ```
   docker rm korwinai-bot
   ```

## Commands

- `/korwin`: Plays a random sentence from the catalogue in the voice channel
- `/bóg`: Plays a custom text-to-speech message (only available to the bot owner)

## Development

For development, install the optional development dependencies:

Using pip:
```
pip install -e ".[dev]"
```

Alternatively, using uv:
```
uv sync --all-extras
```

This will install:
- black for code formatting
- isort for import sorting

## License

This project is licensed under the MIT License.
