from aiogram import Router, F
from aiogram.types import Message

from src.db.database import get_top_spread, get_funding_for_symbol

from bot.handlers.arbi.funding_spread import build_funding_spread
from bot.utils.time import localize_time
from bot.db.user_db import Database

arbi_router = Router()

@arbi_router.message(F.text.startswith("/arbi"))
async def cmd_arbi(message: Message, db: Database):
    raw = message.text.strip().split(maxsplit=1)

    # 1) просто /arbi  → топ-5 спредов
    if len(raw) == 1:
        rows = await get_top_spread(limit=5)
        if not rows:
            await message.answer("Нет данных для показа спредов.")
            return

        user_tz = await db.get_user_timezone(message.from_user.id) or "UTC+0"
        text = "<b>🔥 Топ-5 спредов фандинга</b>\n\n"
        # bot/handlers/arbi/arbi.py

        for sym, exchange1, exchange2, funding1, funding2, spread in rows:
            funding1, funding2 = float(funding1), float(funding2)
            text += f"{sym} | {exchange1} {funding1:+.4f}% ↔ {exchange2} {funding2:+.4f}%\n|  Δ = {spread:+.4f}%\n"
        await message.answer(text, parse_mode="HTML")

    # 2) /arbi <ticker>
    else:
        symbol = raw[1].upper()
        rows = await build_funding_spread(symbol)
        
        if not rows:
            await message.answer(f"Для {symbol} нет данных.")
            return

        user_tz = await db.get_user_timezone(message.from_user.id) or "UTC+0"
        text = f"<b>Фандинг-спреды {symbol}</b>\n\n"
        for e1, e2, f1, f2 in rows:
            text += f"{e1} {f1:+.4f}% ↔ {e2} {f2:+.4f}%  |  Δ = {(f1-f2):+.4f}%\n"

        await message.answer(text, parse_mode="HTML")

