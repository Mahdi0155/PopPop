#===== FILE: keyboards/default.py =====
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="سوپر")],
        [KeyboardButton(text="پست")],
        [KeyboardButton(text="آمار")]
    ],
    resize_keyboard=True
)

post_action_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ارسال در کانال")],
        [KeyboardButton(text="ارسال در آینده")],
        [KeyboardButton(text="برگشت به پنل اصلی")]
    ],
    resize_keyboard=True
)

confirm_join_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="عضو شدم")]
    ],
    resize_keyboard=True
)
