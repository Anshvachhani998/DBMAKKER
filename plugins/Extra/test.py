from telethon import TelegramClient, events
from telethon.sessions import StringSession
from info import API_ID, API_HASH, USER_SESSION

client = TelegramClient(StringSession(USER_SESSION), API_ID, API_HASH)

thumb_store = {}

@client.on(events.NewMessage(pattern='/set'))
async def set_thumbnail(event):
    # Check if this message is a reply
    if not event.is_reply:
        await event.reply("❌ Please reply to a video to set its thumbnail.")
        return

    replied = await event.get_reply_message()

    if not replied.video:
        await event.reply("❌ Please reply to a **video** message.")
        return

    user_id = event.sender_id
    thumb_store[user_id] = replied.video
    await event.reply("✅ Thumbnail saved successfully!")

@client.on(events.NewMessage)
async def handle_video(event):
    user_id = event.sender_id

    if event.video:
        if user_id not in thumb_store:
            await event.reply("❌ No thumbnail found. Reply to a video with /set to save it.")
            return

        try:
            await client.send_file(
                event.chat_id,
                file=await client.download_media(event.video),
                thumb=thumb_store[user_id],
                caption="🎥 Custom thumbnail applied!",
                force_document=False,
                allow_cache=False
            )
        except Exception as e:
            await event.reply(f"❌ Error sending file: {str(e)}")

async def start_telethon_client():
    await client.start()
    print("✅ Telethon client started")
    await client.run_until_disconnected()
