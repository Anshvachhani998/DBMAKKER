
from os import getenv

class Config(object):
      API_HASH = getenv("API_HASH", "a1a06a18eb9153e9dbd447cfd5da2457")
      API_ID = int(getenv("API_ID", "20389440"))
      AS_COPY = True
      BOT_TOKEN = getenv("BOT_TOKEN", "8047216869:AAGAVxhA8POdmZW7xjr1PQCVmKjz0pbISIg")
      CHANNEL = list(x for x in getenv("CHANNEL_ID", "-1001698167203:-1002884716564").replace("\n", " ").split(' '))

