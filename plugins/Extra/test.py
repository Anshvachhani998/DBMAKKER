from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import os
import re

async def download_file(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None

            # Try to get actual filename from headers
            cd = resp.headers.get("Content-Disposition")
            if cd and "filename=" in cd:
                filename = re.findall('filename="?([^"]+)"?', cd)[0]
            else:
                # fallback if header not found
                filename = os.path.basename(url.split("?")[0])

            with open(filename, 'wb') as f:
                while True:
                    chunk = await resp.content.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
    return filename


@Client.on_message(filters.command("dl") & filters.private)
async def vahaflix_direct_download(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("🔗 Please send a direct video link.\nUsage: `/dl <.mp4 link>`", quote=True)

    link = message.command[1]

    if not re.search(r'\.(mp4|m3u8)(\?|$)', link):
        return await message.reply("⚠️ Only direct `.mp4` or `.m3u8` links are supported.", quote=True)

    msg = await message.reply("⬇️ Downloading video...", quote=True)

    try:
        filename = await download_file(link)
        if filename and os.path.exists(filename):
            await client.send_video(
                chat_id=message.chat.id,
                video=filename,
                caption=f"📥 Downloaded: `{filename}`",
                reply_to_message_id=message.id
            )
            os.remove(filename)
        else:
            await msg.edit("❌ Failed to download the video.")
    except Exception as e:
        await msg.edit(f"❌ Error occurred:\n`{e}`")
