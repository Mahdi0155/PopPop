#===== FILE: handlers/panel.py =====
from aiogram import Router, types
from aiogram.filters import Command
from data.config import ADMINS
from keyboards.default import main_keyboard
from utils.db import add_user

router = Router()

@router.message(Command("start"))
async def start_handler(msg: types.Message):
    user_id = msg.from_user.id
    add_user(user_id)
    
    if user_id not in ADMINS:
        await msg.answer("شما دسترسی به این ربات را ندارید.")
        return
    
    await msg.answer("به پنل مدیریت خوش آمدید. یکی از گزینه‌ها را انتخاب کنید:", reply_markup=main_keyboard)
