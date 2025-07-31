FROM python:3.10-slim

WORKDIR /app

# Install only required system dependencies (without Playwright stuff)
RUN apt update && apt install -y \
    ffmpeg aria2 git curl wget gnupg ca-certificates \
    fonts-liberation libasound2 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*


COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install spotipy  telethon



CMD ["python", "bot.py"]
