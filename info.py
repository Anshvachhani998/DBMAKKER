import os

SESSION = "spotifydl"
API_ID = int(os.getenv("API_ID", "8012239"))
API_HASH = os.getenv("API_HASH", "171e6f1bf66ed8dcc5140fbe827b6b08")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8047216869:AAGAVxhA8POdmZW7xjr1PQCVmKjz0pbISIg")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002884716564"))
DUMP_CHANNEL_ID = int(os.getenv("DUMP_CHANNEL_ID", "-1002884716564"))
PORT = int(os.getenv("PORT", "8080"))
FORCE_CHANNEL = int(os.getenv("FORCE_CHANNEL", "-1002884716564"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Ansh089:Ansh089@cluster0.y8tpouc.mongodb.net/?retryWrites=true&w=majority")
MONGO_NAME = os.getenv("MONGO_NAME", "SpotifyDsL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "medias")
ADMINS = [5660839376, 6167872503, 5961011848, 6538627123]
DAILY_LIMITS = 20
MAINTENANCE_MODE = False
USER_SESSION = "BQFk8gAANfr9yto-xlnMgjRjNnbuBE36n_AmmzEB47aKeWyhes2Jw7F8PbJ8gZppISDtDPwNC3O7K03seYVfs47T4As758jp24XzpshFqCPs44UfT_aWdUxhRDK7cbK3rIfIlZplGzu79pXzt0BlKb0cKfmNsxp78HlNdJLF_Ko_j-1sFFQPCqOnWrBkJCIhLx5qZabC6ITbhu7qXoyzqeACqe21UDImLPMpLRDB3_8HM3lkYmeXnu01c-O7mE44HDAi6NUgYuNKDruXTxkFIqK07rVeuEt2vcCzQUyZKcQm54_vZYT_Uj8f5xx1PGmZ-3IfRMH-5UUwIf6kCiNW1SMGaeRkZgAAAAHjFRcWAA"
USERBOT_CHAT_ID = 5785483456

MAINTENANCE_MESSAGE = (
    "⚠️ **Maintenance Mode Activated** ⚙️\n\n"
    "Our bot is currently undergoing scheduled maintenance to improve performance and add new features.\n\n"
    "Please check back in a while. We’ll be back soon, better than ever!\n\n"
    "💬 **Support Group:** [SUPPORT](https://t.me/AnSBotsSupports)\n\n"
    "**– Team Support**"
)
