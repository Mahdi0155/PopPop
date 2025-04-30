from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from data.config import ADMINS
from keyboards.default import main_keyboard
from utils.db import add_user, get_file_by_id

router = Router()

@router.message(CommandStart())
async def start_handler(msg: types.Message):
    user_id = msg.from_user.id
    add_user(user_id)

    args = msg.text.split(maxsplit=1)
    if len(args) > 1 and args[1].startswith("super_"):
        try:
            file_id = int(args[1].split("_")[1])
            file_data = get_file_by_id(file_id)
            if file_data and file_data["type"] == "video":
                await msg.answer_video(file_data["file_id"], caption="درخواست شما آماده شد.")
                return
            else:
                await msg.answer("متأسفیم، فایل مورد نظر یافت نشد یا قابل ارسال نیست.")
                return
        except Exception:
            await msg.answer("در پردازش لینک مشکلی پیش آمد.")
            return

    await msg.answer("سلام! به ربات خوش آمدید. برای استفاده از امکانات، دکمه‌های مربوطه را انتخاب کنید.")

@router.message(Command("panel"))
async def panel_handler(msg: types.Message):
    user_id = msg.from_user.id
    if user_id not in ADMINS:
        await msg.answer("شما دسترسی به پنل مدیریت را ندارید.")
        return
    
    await msg.answer("به پنل مدیریت خوش آمدید. یکی از گزینه‌ها را انتخاب کنید:", reply_markup=main_keyboard)
