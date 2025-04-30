# FILE: handlers/panel.py
from aiogram import Router, types
from aiogram.filters import CommandStart
from data.config import ADMINS
from keyboards.default import main_keyboard
from utils.db import add_user
from utils.subs import check_subscriptions
import asyncio

router = Router()

@router.message(CommandStart(deep_link=True))
async def start_handler(msg: types.Message):
    user_id = msg.from_user.id
    add_user(user_id)

    args = msg.text.split(maxsplit=1)
    if len(args) == 2 and args[1].startswith("super_"):
        file_id = args[1].replace("super_", "")

        # چک عضویت
        result, not_joined = await check_subscriptions(user_id)
        if not result:
            text = "برای دریافت فایل، ابتدا در کانال‌های زیر عضو شوید:\n\n"
            for ch in not_joined:
                text += f"@{ch}\n"
            await msg.answer(text)
            return

        # ارسال فایل
        from utils.db import get_file_by_id
        file = get_file_by_id(file_id)
        if file:
            await msg.answer_video(file['file_id'], caption="درخواست شما آماده شد.")
            await asyncio.sleep(30)
            await msg.delete()
        else:
            await msg.answer("فایل مورد نظر پیدا نشد.")
        return

    # حالت عادی بدون startdata
    await msg.answer("سلام! به ربات خوش آمدید. از دکمه‌های زیر استفاده کنید.", reply_markup=main_keyboard)
