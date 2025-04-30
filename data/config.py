#===== FOLDER: data/config.py =====
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = list(map(int, os.getenv("ADMINS").split(',')))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
CHANNEL_TAG = os.getenv("CHANNEL_TAG")
REQUIRED_CHANNELS = os.getenv("REQUIRED_CHANNELS").split(',')
