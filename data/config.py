import os
from dotenv import load_dotenv

# بارگذاری از ریشه پروژه
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = list(map(int, os.getenv("ADMINS", "").split(',')))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
CHANNEL_TAG = os.getenv("CHANNEL_TAG")
REQUIRED_CHANNELS = os.getenv("REQUIRED_CHANNELS", "").split(',')

# تنظیمات Webhook
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "https://your-app-name.onrender.com")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
