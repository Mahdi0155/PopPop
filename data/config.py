import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
REQUIRED_CHANNELS = ["YourChannel1", "YourChannel2"]  # آی‌دی بدون @
FORCE_SUB_CHANNELS = REQUIRED_CHANNELS  # اگر فرق دارن جدا تعریف کن

WEBHOOK_HOST = "https://<your-app-name>.onrender.com"  # آدرس دامنه Render
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
