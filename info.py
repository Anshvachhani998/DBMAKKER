import os

SESSION = "spotifydl"
API_ID = int(os.getenv("API_ID", "8012239"))
API_HASH = os.getenv("API_HASH", "171e6f1bf66ed8dcc5140fbe827b6b08")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7277194738:AAH6bnCSQ_VI_4CuhzZO13p1vUjNeWIeono")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002884716564"))
DUMP_CHANNEL_ID = int(os.getenv("DUMP_CHANNEL_ID", "-1002884716564"))
PORT = int(os.getenv("PORT", "8080"))
FORCE_CHANNEL = int(os.getenv("FORCE_CHANNEL", "-1002884716564"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Ansh089:Ansh089@cluster0.y8tpouc.mongodb.net/?retryWrites=true&w=majority")
MONGO_NAME = os.getenv("MONGO_NAME", "SpotifyDL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "media")
ADMINS = [5660839376, 6167872503, 5961011848, 6538627123]
DAILY_LIMITS = 20
MAINTENANCE_MODE = False
USER_SESSION = "1BVtsOKEBu8JF3u8uHGlWehCqHHv7n9XE1Y9C-nEtKP2iiJld-sc-voBSWo4InolTDFOUL4eHhCWs1D1t-KJKbMYOiT2ZdLOpz0rhnymMKRLZhx6u2EMXI3_TGuz9SxeXwrt7MrMYeoDGNKmKoBqjtQNGhbjn6hQ4mFF2GckhcInX9wbwlKMv4kaBdDkrGOcLAopXEs_Q3QJoCObWEH7XqQlrOyZOtlt-5YbckkKRzeWmL_itUXUD2TeJK7KqL9JHPXVCI_YlHpmR4Jqq2PXACWiHLvLyQIXYI2WaWQAjhLMfdVCwQcpf3L70="
USERBOT_CHAT_ID = 5785483456

MAINTENANCE_MESSAGE = (
    "⚠️ **Maintenance Mode Activated** ⚙️\n\n"
    "Our bot is currently undergoing scheduled maintenance to improve performance and add new features.\n\n"
    "Please check back in a while. We’ll be back soon, better than ever!\n\n"
    "💬 **Support Group:** [SUPPORT](https://t.me/AnSBotsSupports)\n\n"
    "**– Team Support**"
)
