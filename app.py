# FILE: app.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import BOT_TOKEN
from handlers.panel import router as panel_router

# ساخت ربات
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# اضافه کردن هندلرها
dp.include_router(panel_router)

# تعریف دستورات ربات
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="شروع"),
    ]
    await bot.set_my_commands(commands)

# اجرای اصلی
async def main():
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
