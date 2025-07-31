FROM python:3.10-slim

WORKDIR /app

# Install only required system dependencies (without Playwright stuff)
RUN apt update && apt install -y \
    ffmpeg aria2 git curl wget gnupg ca-certificates \
    fonts-liberation libasound2 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy your code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install spotipy yt-dlp spotdl telethon
RUN pip install git+https://github.com/AliAkhtari78/SpotifyScraper.git

# Note: Removed Playwright install commands here

CMD ["python", "bot.py"]
