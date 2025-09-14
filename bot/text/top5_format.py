from typing import List
import re
from src.config import EXCHANGE_FUTURES_URLS
from bot.utils.time import localize_time

async def handle_top5_formating(top_funding: List, user_tz: str) -> str:
    text = "<b>🔥 ТОП-5 самых больших фандингов</b>\n\n"
    for i, (exchange, symbol, funding, next_settle) in enumerate(top_funding, 1):
        url = EXCHANGE_FUTURES_URLS[exchange.lower()].format(symbol=symbol)
        clean = re.sub(r'(_USDT|_USDC|USDTM?|USDCM?)', '', symbol)
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else ""        
        local = localize_time(next_settle, user_tz)
        text += f"{emoji} <a href='{url}'>{clean}</a> | <b>{funding:+.4f}%</b> | {local} | <i>{exchange.upper()}</i>\n"
    return text