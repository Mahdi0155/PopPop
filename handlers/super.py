# FILE: handlers/super.py
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.default import main_keyboard, confirm_join_keyboard
from data.config import CHANNEL_USERNAME, CHANNEL_TAG, REQUIRED_CHANNELS
from utils.db import log_file
from utils.subs import check_subscriptions
import asyncio

router = Router()

class SuperStates(StatesGroup):
    waiting_for_video = State()
    waiting_for_cover = State()
    waiting_for_caption = State()
    waiting_for_check = State()

@router.message(F.text == "سوپر")
async def start_super(msg: types.Message, state: FSMContext):
    await msg.answer("لطفاً ویدیوی مورد نظر را ارسال کنید:")
    await state.set_state(SuperStates.waiting_for_video)

@router.message(SuperStates.waiting_for_video, F.video)
async def get_video(msg: types.Message, state: FSMContext):
    await state.update_data(video_id=msg.video.file_id)
    await msg.answer("اکنون کاور (عکس) را ارسال کنید:")
    await state.set_state(SuperStates.waiting_for_cover)

@router.message(SuperStates.waiting_for_cover, F.photo)
async def get_cover(msg: types.Message, state: FSMContext):
    await state.update_data(cover_id=msg.photo[-1].file_id)
    await msg.answer("لطفاً کپشن خود را وارد کنید:")
    await state.set_state(SuperStates.waiting_for_caption)

@router.message(SuperStates.waiting_for_caption)
async def get_caption(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    me = await msg.bot.get_me()
    bot_username = me.username
    caption = f"{msg.text}\n\nمشاهده: [دریافت فایل](https://t.me/{bot_username}?start=super_{msg.from_user.id})\n\n{CHANNEL_TAG}"

    await state.update_data(caption=caption)

    await msg.answer_photo(data['cover_id'], caption=caption, parse_mode='Markdown', reply_markup=main_keyboard)
    log_file(data['video_id'], 'video', msg.from_user.id)
    await msg.bot.send_video(chat_id=CHANNEL_USERNAME, video=data['video_id'], caption=caption, parse_mode='Markdown')
    await state.clear()

@router.message(F.text.startswith("عضو شدم"))
async def check_joined(msg: types.Message):
    result, not_joined = await check_subscriptions(msg.from_user.id)
    if not result:
        text = "لطفاً در کانال‌های زیر عضو شوید:\n\n"
        for ch in not_joined:
            text += f"@{ch}\n"
        await msg.answer(text, reply_markup=confirm_join_keyboard)
    else:
        await msg.answer("عضویت شما تأیید شد. ارسال فایل آغاز می‌شود...")
        await asyncio.sleep(2)
        await msg.answer_video("USER_RELATED_VIDEO", caption="درخواست شما آماده شد.")
        await asyncio.sleep(30)
        await msg.delete()
