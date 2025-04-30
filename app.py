# FILE: app.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import BOT_TOKEN
from handlers.panel import router as panel_router
from handlers.super import router as super_router  # اضافه شده
from handlers.post import router as post_router    # اضافه شده
from utils.db import init_db  # مقداردهی اولیه دیتابیس

# ساخت ربات
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# اضافه کردن هندلرها
dp.include_router(panel_router)
dp.include_router(super_router)  # اضافه شده
dp.include_router(post_router)   # اضافه شده

# تعریف دستورات ربات
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="شروع"),
    ]
    await bot.set_my_commands(commands)

# اجرای اصلی
async def main():
    init_db()  # مقداردهی اولیه دیتابیس
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
