# Use Python 3.13 as the base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies including ffmpeg for audio playback
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    portaudio19-dev python3-pyaudio \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install uv
RUN pip install uv

# Install Python dependencies using uv
RUN uv sync

# Create cache directories for audio files
RUN mkdir -p cache/Intro cache/Podmiot cache/Cechy cache/Działanie cache/Uzasadnienie cache/Komentarz cache/custom

# Set environment variables (these will be overridden by docker run -e)
ENV DISCORD_BOT_TOKEN=""
ENV GOOGLE_SHEETS_LINK=""
ENV ELEVEN_LABS_API_KEY=""
ENV AUTHOR_ID=""
ENV GUILD_ID=""

# Modify main.py to handle the interactive prompt automatically
RUN sed -i 's/if input("(y\/N): ") == "y":/if True:/' main.py

# Run the bot using uv
CMD ["uv", "run", "main.py"]
