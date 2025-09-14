from typing import List
import re
from src.config import EXCHANGE_FUTURES_URLS

from bot.utils.time import localize_time

async def time_phrase(user_upcoming_funding_time: int) -> str:
        if user_upcoming_funding_time == 1:
            return "в ближайший 1 час"
        elif 2 <= user_upcoming_funding_time <= 4:
            return f"в ближайшие {user_upcoming_funding_time} часа"
        else:
            return f"в ближайшие {user_upcoming_funding_time} часов"
            
async def handle_upcoming_funding_formating(upcoming_funding: List,user_tz, user_upcoming_funding_time: str) -> str:
    text = f"<b>🕒 Фандинги {await time_phrase(user_upcoming_funding_time)}</b>\n\n"
    for i, (exchange, symbol, upcoming_funding, next_settle) in enumerate(upcoming_funding, 1):
        url = EXCHANGE_FUTURES_URLS[exchange.lower()].format(symbol=symbol)
        clean = re.sub(r'(_USDT|_USDC|USDTM?|USDCM?)', '', symbol)
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else ""
        local = localize_time(next_settle, user_tz)
        text += f"{emoji} <a href='{url}'>{clean}</a> | <b>{upcoming_funding:+.4f}%</b> | {local} | <i>{exchange.upper()}</i>\n"

    return text
