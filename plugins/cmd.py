

import logging
import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import Message

# Logger Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

channelforward = Client

CHANNEL = [
    "-1001698167203:-1002884716564"
]


# /start command handler
@channelforward.on_message(filters.private & filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply_text("👋 Hello! I’m a channel forwarder bot.\nI only forward audio with custom captions.")

# Audio message from channel handler
@channelforward.on_message(filters.channel & filters.audio)
async def forward_audio(client, message: Message):
    try:
        for id in CHANNEL:
            from_channel, to_channel = id.split(":")
            if message.chat.id == int(from_channel):

                audio = message.audio
                title = audio.title or "Unknown Title"
                performer = audio.performer or "Unknown Artist"

                # Track ID extraction from caption
                track_id = "N/A"
                if message.caption:
                    match = re.search(r'track/([A-Za-z0-9]+)', message.caption)
                    if match:
                        track_id = match.group(1)

                # Custom Caption
                caption = f"🎵 {title}\n👤 {performer}\n🆔 {track_id}"

                # Send audio with new caption
                await client.send_audio(
                    chat_id=int(to_channel),
                    audio=audio.file_id,
                    caption=caption,
                    title=title,
                    performer=performer,
                    duration=audio.duration
                )

                logger.info(f"✅ Audio forwarded from {from_channel} to {to_channel}")
                await asyncio.sleep(1)

    except Exception as e:
        logger.exception(e)

