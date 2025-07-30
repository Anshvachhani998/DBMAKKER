from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import os
import re
from moviepy.editor import VideoFileClip
from random import randint


# Download video file
async def download_file(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None

            # Get filename from headers or fallback
            cd = resp.headers.get("Content-Disposition")
            if cd and "filename=" in cd:
                filename = re.findall('filename="?([^"]+)"?', cd)[0]
            else:
                filename = os.path.basename(url.split("?")[0])

            with open(filename, 'wb') as f:
                while True:
                    chunk = await resp.content.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)

    return filename


# Get duration & random thumbnail
def get_video_metadata(filename: str):
    clip = VideoFileClip(filename)
    duration = int(clip.duration)
    mid = randint(5, max(6, duration - 3)) if duration > 10 else 1
    thumb_path = f"{filename}_thumb.jpg"
    clip.save_frame(thumb_path, t=mid)
    clip.close()
    return duration, thumb_path


# Telegram handler
@Client.on_message(filters.command("dl") & filters.private)
async def vahaflix_direct_download(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("🔗 Send a direct `.mp4` video link.\nUsage: `/dl <link>`", quote=True)

    link = message.command[1]

    if not re.search(r'\.mp4(\?|$)', link):
        return await message.reply("⚠️ Only direct `.mp4` links supported for download.", quote=True)

    msg = await message.reply("⏳ Downloading video...", quote=True)

    try:
        filename = await download_file(link)

        if filename and os.path.exists(filename):
            duration, thumbnail = get_video_metadata(filename)

            await client.send_video(
                chat_id=message.chat.id,
                video=filename,
                caption=f"📥 File: `{filename}`\n⏱ Duration: `{duration // 60}m {duration % 60}s`",
                thumb=thumbnail,
                duration=duration,
                reply_to_message_id=message.id
            )

            os.remove(filename)
            if os.path.exists(thumbnail):
                os.remove(thumbnail)
        else:
            await msg.edit("❌ Failed to download the video.")
    except Exception as e:
        await msg.edit(f"❌ Error: `{str(e)}`")
