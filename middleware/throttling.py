#===== FILE: middleware/throttling.py =====
import asyncio
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit=1.0):
        super().__init__()
        self.rate_limit = rate_limit
        self.last_call = {}

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        now = asyncio.get_event_loop().time()
        last_time = self.last_call.get(user_id)

        if last_time:
            elapsed = now - last_time
            if elapsed < self.rate_limit:
                await message.answer("لطفاً کمی صبر کن...")
                raise Exception("Throttled")
        
        self.last_call[user_id] = now
