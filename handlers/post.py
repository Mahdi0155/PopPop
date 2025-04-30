#===== FILE: handlers/post.py =====
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.default import post_action_keyboard, main_keyboard
from data.config import CHANNEL_USERNAME, CHANNEL_TAG
from utils.db import log_file

router = Router()

class PostStates(StatesGroup):
    waiting_for_media = State()
    waiting_for_caption = State()
    waiting_for_action = State()
    waiting_for_schedule = State()

@router.message(F.text == "پست")
async def post_entry(msg: types.Message, state: FSMContext):
    await msg.answer("لطفاً پست مورد نظر را فوروارد کنید:")
    await state.set_state(PostStates.waiting_for_media)

@router.message(PostStates.waiting_for_media, F.forward_from_chat)
async def receive_media(msg: types.Message, state: FSMContext):
    if msg.photo:
        file_id = msg.photo[-1].file_id
        media_type = "photo"
    elif msg.video:
        file_id = msg.video.file_id
        media_type = "video"
    else:
        await msg.answer("فقط عکس یا ویدیو فوروارد کنید.")
        return

    await state.update_data(file_id=file_id, media_type=media_type)
    await msg.answer("لطفاً کپشن مورد نظر را وارد کنید:")
    await state.set_state(PostStates.waiting_for_caption)

@router.message(PostStates.waiting_for_caption)
async def receive_caption(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()
    final_caption = f"{msg.text}\n\n{CHANNEL_TAG}"
    await state.update_data(caption=final_caption)

    if user_data['media_type'] == "photo":
        await msg.answer_photo(user_data['file_id'], caption=final_caption, reply_markup=post_action_keyboard)
    else:
        await msg.answer_video(user_data['file_id'], caption=final_caption, reply_markup=post_action_keyboard)

    await state.set_state(PostStates.waiting_for_action)

@router.message(PostStates.waiting_for_action)
async def handle_post_action(msg: types.Message, state: FSMContext):
    if msg.text == "ارسال در کانال":
        data = await state.get_data()
        await msg.bot.send_photo(chat_id=CHANNEL_USERNAME, photo=data['file_id'], caption=data['caption']) if data['media_type'] == "photo" else await msg.bot.send_video(chat_id=CHANNEL_USERNAME, video=data['file_id'], caption=data['caption'])
        log_file(data['file_id'], data['media_type'], msg.from_user.id)
        await msg.answer("ارسال شد.", reply_markup=main_keyboard)
        await state.clear()
    elif msg.text == "ارسال در آینده":
        await msg.answer("لطفاً زمان تاخیر (دقیقه) را وارد کنید:")
        await state.set_state(PostStates.waiting_for_schedule)
    elif msg.text == "برگشت به پنل اصلی":
        await msg.answer("بازگشت انجام شد.", reply_markup=main_keyboard)
        await state.clear()
    else:
        await msg.answer("یکی از گزینه‌ها را انتخاب کنید.")

@router.message(PostStates.waiting_for_schedule)
async def handle_scheduled_post(msg: types.Message, state: FSMContext):
    try:
        delay_minutes = int(msg.text)
        data = await state.get_data()
        await msg.answer(f"پست برای {delay_minutes} دقیقه بعد زمان‌بندی شد.", reply_markup=main_keyboard)

        async def delayed_post():
            await msg.bot.send_photo(chat_id=CHANNEL_USERNAME, photo=data['file_id'], caption=data['caption']) if data['media_type'] == "photo" else await msg.bot.send_video(chat_id=CHANNEL_USERNAME, video=data['file_id'], caption=data['caption'])
            log_file(data['file_id'], data['media_type'], msg.from_user.id)

        msg.bot.loop.call_later(delay_minutes * 60, lambda: msg.bot.loop.create_task(delayed_post()))
        await state.clear()
    except:
        await msg.answer("لطفاً عدد معتبر وارد کنید.")
