from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import os
import re
from moviepy.editor import VideoFileClip
from random import randint


# Download video file with custom filename
async def download_file(url: str, filename: str) -> str:
    if not filename.endswith(".mp4"):
        filename += ".mp4"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None

            with open(filename, 'wb') as f:
                while True:
                    chunk = await resp.content.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)

    return filename


# Extract duration and thumbnail
def get_video_metadata(filename: str):
    clip = VideoFileClip(filename)
    duration = int(clip.duration)
    thumb_time = randint(5, max(6, duration - 3)) if duration > 10 else 1
    thumb_path = f"{filename}_thumb.jpg"
    clip.save_frame(thumb_path, t=thumb_time)
    clip.close()
    return duration, thumb_path


# Telegram command handler
@Client.on_message(filters.command("dl") & filters.private)
async def direct_download_with_name(client: Client, message: Message):
    parts = message.text.split(maxsplit=2)

    if len(parts) < 2:
        return await message.reply("🔗 Send a direct `.mp4` video link.\nUsage: `/dl <link> <optional name>`", quote=True)

    link = parts[1]
    custom_name = parts[2].strip() if len(parts) > 2 else None

    if not re.search(r'\.mp4(\?|$)', link):
        return await message.reply("⚠️ Only direct `.mp4` links supported.", quote=True)

    filename = custom_name if custom_name else os.path.basename(link.split("?")[0])
    filename = filename.strip().replace("/", "_").replace("\\", "_") + ".mp4"

    msg = await message.reply(f"⬇️ Downloading as `{filename}`...", quote=True)

    try:
        filepath = await download_file(link, filename)

        if filepath and os.path.exists(filepath):
            duration, thumbnail = get_video_metadata(filepath)

            await client.send_video(
                chat_id=message.chat.id,
                video=filepath,
                caption=f"📥 File: `{filename}`\n⏱ Duration: `{duration // 60}m {duration % 60}s`",
                thumb=thumbnail,
                duration=duration,
                reply_to_message_id=message.id
            )

            os.remove(filepath)
            if os.path.exists(thumbnail):
                os.remove(thumbnail)
        else:
            await msg.edit("❌ Failed to download the video.")
    except Exception as e:
        await msg.edit(f"❌ Error: `{str(e)}`")
