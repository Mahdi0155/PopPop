from aiogram import Router, types, F
from aiogram.filters import CommandStart
from data.config import ADMINS
from keyboards.default import main_keyboard
from utils.db import add_user, get_file_by_id
from utils.subs import check_subscriptions, generate_force_sub_keyboard
import asyncio

router = Router()

@router.message(CommandStart(deep_link=True))
async def start_handler(msg: types.Message, state):
    user_id = msg.from_user.id
    add_user(user_id)

    args = msg.text.split(maxsplit=1)
    if len(args) == 2 and args[1].startswith("super_"):
        file_id = args[1].replace("super_", "")

        result, not_joined = await check_subscriptions(user_id)
        if not result:
            text = "برای دریافت فایل، ابتدا در کانال‌های زیر عضو شوید:"
            reply_markup = generate_force_sub_keyboard(not_joined)
            sent = await msg.answer(text, reply_markup=reply_markup)
            # ذخیره برای پاک کردن در بررسی مجدد
            await state.update_data(join_msg_id=sent.message_id, file_id=file_id)
            return

        file = get_file_by_id(file_id)
        if file:
            sent_msg = await msg.answer_video(file['file_id'], caption="درخواست شما آماده شد.")
            await asyncio.sleep(30)
            await sent_msg.delete()
        else:
            await msg.answer("فایل مورد نظر پیدا نشد.")
        return

    await msg.answer("سلام! به ربات خوش آمدید. از دکمه‌های زیر استفاده کنید.", reply_markup=main_keyboard)

@router.callback_query(F.data == "check_again")
async def check_again_callback(callback: types.CallbackQuery, state):
    user_id = callback.from_user.id
    result, not_joined = await check_subscriptions(user_id)

    if result:
        data = await state.get_data()
        file = get_file_by_id(data.get("file_id"))
        if file:
            sent_msg = await callback.message.answer_video(file['file_id'], caption="درخواست شما آماده شد.")
            await callback.message.delete()
            await asyncio.sleep(30)
            await sent_msg.delete()
        else:
            await callback.message.edit_text("فایل مورد نظر پیدا نشد.")
        await state.clear()
    else:
        await callback.message.delete()
        text = "هنوز عضو نشده‌اید. لطفاً در کانال‌های زیر عضو شوید:"
        reply_markup = generate_force_sub_keyboard(not_joined)
        new_msg = await callback.message.answer(text, reply_markup=reply_markup)
        await state.update_data(join_msg_id=new_msg.message_id)
