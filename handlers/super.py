from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.default import main_keyboard, confirm_join_keyboard
from data.config import CHANNEL_USERNAME, CHANNEL_TAG
from utils.db import log_file
from utils.subs import check_subscriptions
import asyncio

router = Router()

class SuperStates(StatesGroup):
    waiting_for_video = State()
    waiting_for_cover = State()
    waiting_for_caption = State()
    waiting_for_confirmation = State()
    waiting_for_schedule_time = State()

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
    video_id = data['video_id']
    user_id = msg.from_user.id

    # ثبت فایل و گرفتن شناسه دیتابیس
    file_db_id = log_file(video_id, 'video', user_id)

    # ساخت لینک با شناسه دیتابیس
    bot_username = (await msg.bot.get_me()).username
    caption_text = msg.text
    full_caption = f"{caption_text}\n\nمشاهده: [دریافت فایل](https://t.me/{bot_username}?start=super_{file_db_id})\n\n{CHANNEL_TAG}"

    await state.update_data(full_caption=full_caption)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ارسال در کانال", callback_data="send_now")],
        [InlineKeyboardButton(text="ارسال در آینده", callback_data="schedule_later")],
        [InlineKeyboardButton(text="لغو", callback_data="cancel")]
    ])

    await msg.answer_photo(data['cover_id'], caption=full_caption, parse_mode='Markdown', reply_markup=keyboard)
    await state.set_state(SuperStates.waiting_for_confirmation)

@router.callback_query(F.data == "send_now")
async def send_now_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.bot.send_video(chat_id=CHANNEL_USERNAME, video=data['video_id'], caption=data['full_caption'], parse_mode='Markdown')
    await callback.message.edit_caption(caption="✅ ویدیو با موفقیت در کانال ارسال شد.", parse_mode='Markdown')
    await state.clear()

@router.callback_query(F.data == "schedule_later")
async def schedule_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption("⏰ لطفاً زمان ارسال را به دقیقه وارد کنید (مثلاً 10 برای ۱۰ دقیقه بعد):", parse_mode='Markdown')
    await state.set_state(SuperStates.waiting_for_schedule_time)

@router.message(SuperStates.waiting_for_schedule_time, F.text.regexp(r"^\d+$"))
async def schedule_time_handler(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    minutes = int(msg.text)

    await msg.answer(f"✅ ویدیو در {minutes} دقیقه دیگر ارسال خواهد شد.")

    async def delayed_send():
        await asyncio.sleep(minutes * 60)
        await msg.bot.send_video(chat_id=CHANNEL_USERNAME, video=data['video_id'], caption=data['full_caption'], parse_mode='Markdown')

    asyncio.create_task(delayed_send())
    await state.clear()

@router.message(SuperStates.waiting_for_schedule_time)
async def invalid_schedule_input(msg: types.Message):
    await msg.answer("لطفاً فقط عدد وارد کنید (مثلاً 5 برای ۵ دقیقه بعد).")

@router.callback_query(F.data == "cancel")
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption("❌ عملیات ارسال لغو شد.", parse_mode='Markdown')
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
