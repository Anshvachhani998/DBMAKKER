import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import os
import asyncio
import time  # For timestamp

# ----------------- Logging Setup -----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# ----------------- Spotify Auth -----------------
SPOTIFY_CLIENT_ID = "c6e8b0da7751415e848a97f309bc057d"
SPOTIFY_CLIENT_SECRET = "97d40c2c7b7948589df58d838b8e9e68"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# ----------------- Regex -----------------
SPOTIFY_PLAYLIST_REGEX = r"https://open\.spotify\.com/playlist/([a-zA-Z0-9]+)"

# ----------------- Extractor -----------------
async def extract_track_ids_spotify(playlist_id):
    try:
        results = sp.playlist_tracks(playlist_id)
        tracks = results["items"]

        # Handle pagination (if >100 songs)
        while results["next"]:
            results = sp.next(results)
            tracks.extend(results["items"])

        track_ids = []
        for item in tracks:
            track = item["track"]
            if track:
                track_ids.append(track["id"])

        logger.info(f"✅ Extracted {len(track_ids)} tracks from playlist {playlist_id}")
        return track_ids
    except Exception as e:
        logger.error(f"❌ Error scraping playlist {playlist_id}: {e}")
        return []

# ----------------- Command Handler -----------------
@Client.on_message(filters.command("extracttracks") & filters.reply)
async def extract_from_txt(client, message: Message):
    if not message.reply_to_message.document:
        return await message.reply("⚠️ Reply to a `.txt` file containing Spotify playlist links.")

    file_path = await message.reply_to_message.download()
    final_track_ids = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        playlist_ids = re.findall(SPOTIFY_PLAYLIST_REGEX, content)
        total = len(playlist_ids)
        logger.info(f"📂 Found {total} playlist links to extract.")
        status = await message.reply(f"🌀 Found {total} playlists. Extracting...")

        for idx, pid in enumerate(playlist_ids, start=1):
            ids = await extract_track_ids_spotify(pid)
            final_track_ids.extend(ids)

            if idx % 5 == 0 or idx == total:
                await status.edit(f"🔍 Extracted {idx}/{total} playlists.")
                logger.info(f"⏳ Progress: {idx}/{total}")

            await asyncio.sleep(0.5)

        unique_ids = list(set(final_track_ids))

        # Unique filename with timestamp
        timestamp = int(time.time())
        result_file = f"all_tracks_{timestamp}.txt"

        with open(result_file, "w") as f:
            f.write("\n".join(unique_ids))

        logger.info(f"✅ Total Unique Tracks Extracted: {len(unique_ids)}")
        await message.reply_document(result_file, caption=f"✅ Extracted {len(unique_ids)} unique track IDs.")
        
        # Remove the result file after sending
        os.remove(result_file)

    except Exception as e:
        logger.exception("An error occurred during processing.")
        await message.reply(f"❌ Error: {e}")
    finally:
        # Remove the downloaded playlist file safely
        if os.path.exists(file_path):
            os.remove(file_path)
