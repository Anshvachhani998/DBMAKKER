from telethon import TelegramClient, events
from telethon.tl.types import InputPhoto
from io import BytesIO

from info import API_ID, API_HASH, USER_SESSION
from telethon.sessions import StringSession

client = TelegramClient(StringSession(USER_SESSION), API_ID, API_HASH)

thumb_store = {}

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    user_id = event.sender_id

    if event.photo:
        thumb_store[user_id] = event.photo
        await event.reply("✅ Thumbnail saved! Now send a video.")

    elif event.video:
        if user_id not in thumb_store:
            await event.reply("❌ Please send a thumbnail first.")
            return

        thumb = thumb_store[user_id]

        # Download video into memory
        video_bytes = await client.download_media(event.video, file=BytesIO())

        # Append zero byte to tweak file (modify file so Telegram treats as new)
        video_bytes.write(b'\0')

        # Seek to start for upload
        video_bytes.seek(0)

        input_photo = InputPhoto(
            id=thumb.id,
            access_hash=thumb.access_hash,
            file_reference=thumb.file_reference
        )

        try:
            await client.send_file(
                event.chat_id,
                file=video_bytes,
                thumb=input_photo,
                caption="🎥 Custom thumbnail applied!",
                force_document=False,
                allow_cache=False
            )
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

client.start()
client.run_until_disconnected()
