from pyrogram import Client, filters
from pyrogram.types import Message

app = Client
# Per-user thumbnail store
thumb_store = {}

# Save thumbnail
@app.on_message(filters.photo & filters.private)
async def save_thumb(client, message: Message):
    thumb_store[message.from_user.id] = message.photo.file_id
    await message.reply("✅ Thumbnail saved! Now send your video.")

# Send video with custom thumbnail
@app.on_message(filters.video & filters.private)
async def send_custom_video(client, message: Message):
    uid = message.from_user.id
    thumb_id = thumb_store.get(uid)

    if not thumb_id:
        return await message.reply("❗Please send a thumbnail image first.")

    await client.send_video(
        chat_id=message.chat.id,
        video=message.video.file_id,
        thumb=thumb_id,
        caption="🎥 Here is your video with custom thumbnail!"
    )
