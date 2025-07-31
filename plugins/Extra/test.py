from telethon import TelegramClient, events, types
from telethon.tl.types import InputPhoto
from info import API_ID, API_HASH, USER_SESSION
from telethon.sessions import StringSession


client = TelegramClient(StringSession(USER_SESSION), API_ID, API_HASH)

thumb_store = {}

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender = await event.get_sender()
    user_id = sender.id

    if event.photo:
        # Store full photo media for thumbnail
        thumb_store[user_id] = event.photo
        await event.reply("✅ Thumbnail saved! Now send a video.")

    elif event.video:
        if user_id not in thumb_store:
            await event.reply("❌ Please send a thumbnail first.")
            return

        thumb = thumb_store[user_id]
        video = event.video

        # Convert thumb to InputPhoto
        input_photo = InputPhoto(
            id=thumb.id,
            access_hash=thumb.access_hash,
            file_reference=thumb.file_reference
        )

        try:
            await client.send_file(
                event.chat_id,
                file=video,
                thumb=input_photo,
                caption="🎥 Custom thumbnail applied!",
                force_document=False,
                allow_cache=False
            )
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
