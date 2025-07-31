import asyncio
from pyrogram import Client as PyroClient
from telethon import TelegramClient as TeleClient, events
from telethon.sessions import StringSession
from telethon.tl.types import InputPhoto
from io import BytesIO
from info import API_ID, API_HASH, USER_SESSION, PYRO_API_ID, PYRO_API_HASH, PYRO_BOT_TOKEN

# Pyrogram client
pyro = PyroClient("pyro_bot", api_id=PYRO_API_ID, api_hash=PYRO_API_HASH, bot_token=PYRO_BOT_TOKEN)

# Telethon client
tele = TeleClient(StringSession(USER_SESSION), API_ID, API_HASH)

thumb_store = {}

# Telethon event handler
@tele.on(events.NewMessage(incoming=True))
async def tele_handler(event):
    user_id = event.sender_id

    if event.photo:
        thumb_store[user_id] = event.photo
        await event.reply("✅ Thumbnail saved! Now send a video.")

    elif event.video:
        if user_id not in thumb_store:
            await event.reply("❌ Please send a thumbnail first.")
            return

        thumb = thumb_store[user_id]

        video_bytes = await tele.download_media(event.video, file=BytesIO())
        video_bytes.write(b'\0')
        video_bytes.seek(0)

        input_photo = InputPhoto(
            id=thumb.id,
            access_hash=thumb.access_hash,
            file_reference=thumb.file_reference
        )

        try:
            await tele.send_file(
                event.chat_id,
                file=video_bytes,
                thumb=input_photo,
                caption="🎥 Custom thumbnail applied!",
                force_document=False,
                allow_cache=False
            )
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

async def main():
    # Start both clients
    await pyro.start()
    await tele.start()

    print("Both Pyrogram and Telethon clients started")

    # Run both clients concurrently
    await asyncio.gather(
        pyro_idle(),
        tele.run_until_disconnected()
    )

async def pyro_idle():
    await pyro.idle()

if __name__ == "__main__":
    asyncio.run(main())
