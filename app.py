# FILE: app.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import BOT_TOKEN
from handlers.panel import router as panel_router
from handlers.super import router as super_router
from handlers.post import router as post_router
from utils.db import init_db

# ساخت ربات
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# اضافه کردن هندلرها
dp.include_router(panel_router)
dp.include_router(super_router)
dp.include_router(post_router)

# تعریف دستورات ربات
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="شروع"),
    ]
    await bot.set_my_commands(commands)

# اجرای اصلی
async def main():
    init_db()
    await set_commands(bot)

    # گرفتن نام کاربری ربات و ذخیره در context
    me = await bot.get_me()
    dp['bot_username'] = me.username

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
