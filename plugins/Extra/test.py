import logging
from telethon import TelegramClient, events, errors
from telethon.sessions import StringSession
from telethon.tl.types import InputPhoto
from io import BytesIO
from info import API_ID, API_HASH, USER_SESSION

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

client = TelegramClient(StringSession(USER_SESSION), API_ID, API_HASH)

thumb_store = {}

@client.on(events.NewMessage(pattern="/set"))
async def set_thumbnail(event):
    if event.is_reply:
        replied = await event.get_reply_message()
        if replied.photo:
            thumb_store[event.sender_id] = replied.photo
            await event.reply("✅ Thumbnail saved successfully!")
            logger.info(f"Thumbnail saved for user {event.sender_id}")
        else:
            await event.reply("❌ Reply to an image to set it as a thumbnail.")
            logger.warning(f"User {event.sender_id} tried to set non-photo as thumbnail.")
    else:
        await event.reply("❌ Use /set in reply to a photo.")
        logger.warning(f"User {event.sender_id} used /set without replying.")

@client.on(events.NewMessage)
async def handle_video(event):
    user_id = event.sender_id

    if event.video:
        if user_id not in thumb_store:
            await event.reply("❌ Please set a thumbnail first using /set.")
            logger.info(f"User {user_id} tried to send video without setting thumbnail.")
            return

        thumb = thumb_store[user_id]
        video_bytes = await client.download_media(event.video, file=BytesIO())
        video_bytes.write(b'\0')  # tweak file to force Telegram update
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
            logger.info(f"Video sent with custom thumbnail for user {user_id}")
        except errors.ChatAdminRequiredError:
            await event.reply("❌ I need admin rights in this chat to send videos with custom thumbnails.")
            logger.error(f"Bot lacks admin rights in chat {event.chat_id}")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
            logger.error(f"Error sending video for user {user_id}: {str(e)}")

async def start_telethon_client():
    await client.start()
    logger.info("🚀 Telethon client started successfully!")
    await client.run_until_disconnected()

