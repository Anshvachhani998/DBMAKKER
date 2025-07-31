from telethon import TelegramClient, events, types
from info import API_ID, API_HASH, USER_SESSION

client = TelegramClient("session", API_ID, API_HASH).start(session=USER_SESSION)


thumb_store = {}

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender = await event.get_sender()
    user_id = sender.id

    # Thumbnail Save
    if event.photo:
        thumb_store[user_id] = event.media
        await event.reply("✅ Thumbnail saved! Now send a video.")

    # Video Handling
    elif event.video:
        if user_id not in thumb_store:
            await event.reply("❌ Please send a thumbnail first.")
            return

        thumb = thumb_store[user_id]
        video = event.media

        try:
            await client.send_file(
                event.chat_id,
                file=video,                # No download needed
                thumb=thumb,              # New thumb
                caption="🎥 Custom thumbnail applied!",
                force_document=False,
                allow_cache=False         # <--- This forces Telegram to update thumb
            )
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

