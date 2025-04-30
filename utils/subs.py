#===== FILE: utils/subs.py =====
from aiogram import Bot
from data.config import REQUIRED_CHANNELS

async def check_subscriptions(user_id: int) -> tuple[bool, list]:
    not_joined = []
    for channel in REQUIRED_CHANNELS:
        try:
            member = await Bot.get_current().get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ("left", "kicked"):
                not_joined.append(channel)
        except Exception:
            not_joined.append(channel)
    return (len(not_joined) == 0, not_joined)
