from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import REQUIRED_CHANNELS

async def check_subscriptions(user_id: int) -> tuple[bool, list[str]]:
    not_joined = []
    for channel in REQUIRED_CHANNELS:
        try:
            member = await Bot.get_current().get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ("left", "kicked"):
                not_joined.append(channel)
        except Exception:
            not_joined.append(channel)
    return (len(not_joined) == 0, not_joined)

def generate_force_sub_keyboard(channels: list[str]) -> InlineKeyboardMarkup:
    buttons = []
    for ch in channels:
        buttons.append([InlineKeyboardButton(text=f"عضویت در @{ch}", url=f"https://t.me/{ch}")])
    buttons.append([InlineKeyboardButton(text="عضو شدم ✅", callback_data="check_again")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
