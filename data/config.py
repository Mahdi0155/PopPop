#===== FILE: data/config.py =====
from aiogram.types import ChatPermissions

BOT_TOKEN = 'YOUR_BOT_TOKEN'
ADMINS = [123456789, 987654321]
CHANNEL_TAG = '@hottof | تُفِ داغ'
CHANNEL_USERNAME = '@hottof'

FORCE_SUB_CHANNELS = [
    "@channel1",
    "@channel2"
]

PERMISSIONS_RESTRICTED = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
)

PERMISSIONS_FULL = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
)
