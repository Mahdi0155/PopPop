import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from data.config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_URL
from handlers.panel import router as panel_router
from handlers.super import router as super_router
from handlers.post import router as post_router
from utils.db import init_db

# ایجاد نمونه‌ها
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(panel_router)
dp.include_router(super_router)
dp.include_router(post_router)

async def on_startup():
    init_db()
    await bot.set_webhook(WEBHOOK_URL)
    await bot.set_my_commands([BotCommand(command="start", description="شروع")])
    me = await bot.get_me()
    dp['bot_username'] = me.username

async def on_shutdown():
    await bot.delete_webhook()

# ساخت اپ FastAPI
app = FastAPI(on_startup=[on_startup], on_shutdown=[on_shutdown])

# ثبت هندلر وبهوک
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)
