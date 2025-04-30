import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, Update

from data.config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_URL
from handlers.panel import router as panel_router
from handlers.super import router as super_router
from handlers.post import router as post_router
from utils.db import init_db

# ایجاد نمونه‌ها
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()

# افزودن روت‌ها
dp.include_router(panel_router)
dp.include_router(super_router)
dp.include_router(post_router)

@app.on_event("startup")
async def on_startup():
    init_db()
    await bot.set_webhook(WEBHOOK_URL)
    await bot.set_my_commands([
        BotCommand(command="start", description="شروع")
    ])
    me = await bot.get_me()
    dp['bot_username'] = me.username

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

@app.post(WEBHOOK_PATH)
async def receive_update(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}
