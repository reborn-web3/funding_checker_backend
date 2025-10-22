from aiogram import Router, F
from aiogram.types import Message

from bot.utils.time import localize_time
from bot.db.user_db import Database
from bot.text.ticker_info_format import handle_ticker_info_formating

from src.db.database import get_funding_for_symbol


ticker_information = Router()

@ticker_information.message(F.text)
async def any_ticker(message: Message, db: Database):
    ticker = message.text.strip().upper()
    rows = await get_funding_for_symbol(ticker)
    if not rows:
        await message.answer(f"Для {ticker} нет данных. Введите правильный тикер")
        return
    
    rows = sorted(rows, key=lambda r: abs(r[2]), reverse=True)
    user_tz = await db.get_user_timezone(message.from_user.id)  # если нужен TZ
    await message.answer(text=await handle_ticker_info_formating(rows, ticker, user_tz), parse_mode="HTML", disable_web_page_preview=True,)