#===== FILE: handlers/stats.py =====
from aiogram import Router, types
from datetime import datetime
from utils.db import get_stats

router = Router()

@router.message(lambda msg: msg.text == "آمار")
async def stats_handler(msg: types.Message):
    stats = get_stats()
    now = datetime.now().strftime("%H:%M:%S - %Y/%m/%d")

    text = (
        f"🤖 آمار شما در ساعت {now} به این صورت می‌باشد:\n\n"
        f"👥 تعداد اعضا : {stats['total_users']:,}\n"
        f"🕒 تعداد کاربران ساعت گذشته : {stats['hour_users']:,}\n"
        f"☪️ تعداد کاربران 24 ساعت گذشته : {stats['day_users']:,}\n"
        f"7️⃣ تعداد کاربران هفته گذشته : {stats['week_users']:,}\n"
        f"🌛 تعداد کاربران ماه گذشته : {stats['month_users']:,}\n"
        f"🗂 تعداد فایل ها : {stats['total_files']:,}"
    )

    await msg.answer(text)
