#===== FILE: app.py =====
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from data.config import BOT_TOKEN
from utils.db import init_db
from handlers import panel

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    init_db()

    dp.include_routers(
        start.router,
        post.router,
        super.router,
        stats.router,
    )

    print("ربات با موفقیت راه‌اندازی شد.")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("ربات خاموش شد.")
