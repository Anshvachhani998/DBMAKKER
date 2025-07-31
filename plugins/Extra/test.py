from pyrogram import Client, filters
from pyrogram.types import Message
from info import API_ID, API_HASH, USER_SESSION

app = Client(
    session_name=USER_SESSION,
    api_id=API_ID,
    api_hash=API_HASH
)

thumb_store = {}

@app.on_message(filters.photo & filters.private)
async def save_thumb(client, message: Message):
    thumb_store[message.from_user.id] = message.photo.file_id
    await message.reply("✅ Thumbnail saved! Now send a video.")

@app.on_message(filters.video & filters.private)
async def send_video_with_thumb(client, message: Message):
    uid = message.from_user.id
    thumb_id = thumb_store.get(uid)

    if not thumb_id:
        return await message.reply("❗Please send a thumbnail image first.")

    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=message.video.file_id,  # reuse from CDN
            thumb=thumb_id,
            caption="🎯 Your video with custom thumbnail (Pyrogram User Session)",
            force_document=False,
            supports_streaming=True
        )
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

