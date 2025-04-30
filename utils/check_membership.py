#===== FILE: utils/check_membership.py =====
from aiogram import Bot
from data.config import FORCE_SUB_CHANNELS

async def check_user_membership(bot: Bot, user_id: int):
    not_joined = []
    for channel in FORCE_SUB_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["left", "kicked"]:
                not_joined.append(channel)
        except:
            not_joined.append(channel)
    return not_joined
