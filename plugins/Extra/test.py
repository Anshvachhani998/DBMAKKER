from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import os
import re
from urllib.parse import urlparse, unquote


# Download function with dynamic filename
async def download_file(url: str, filename: str) -> str:
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


# Extract filename from URL
def extract_filename_from_url(url: str) -> str:
    path = urlparse(url).path
    filename = os.path.basename(path)
    return unquote(filename)


# Pyrogram command handler
@Client.on_message(filters.command("dl") & filters.private)
async def vahaflix_direct_download(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("🔗 Please send a direct video link.\nUsage: `/dl <direct .mp4/.m3u8 link>`", quote=True)

    link = message.command[1]

    # Validate CDN video link
    if not re.search(r'\.(mp4|m3u8)(\?|$)', link):
        return await message.reply("⚠️ Only direct `.mp4` or `.m3u8` links are allowed.", quote=True)

    filename = extract_filename_from_url(link)
    msg = await message.reply(f"⬇️ Downloading `{filename}`...", quote=True)

    try:
        filepath = await download_file(link, filename)
        if filepath and os.path.exists(filepath):
            await client.send_video(
                chat_id=message.chat.id,
                video=filepath,
                caption=f"📥 Downloaded: `{filename}`",
                reply_to_message_id=message.id
            )
            os.remove(filepath)
        else:
            await msg.edit("❌ Download failed.")
    except Exception as e:
        await msg.edit(f"❌ Error: `{str(e)}`")
