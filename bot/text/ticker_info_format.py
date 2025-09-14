from typing import List
import re
from src.config import EXCHANGE_FUTURES_URLS
from bot.utils.time import localize_time

async def handle_ticker_info_formating(rows, ticker: str, user_tz: str) -> str:
    text = f"<b>{ticker} — фандинг на всех биржах</b>\n\n"

    for exchange, symbol, funding, next_settle in rows:
            url = EXCHANGE_FUTURES_URLS[exchange.lower()].format(symbol=symbol)
            local = localize_time(next_settle, user_tz)
            text += f" <a href='{url}'>{exchange.upper()}</a> | <b>{funding:+.4f}%</b> | {local}\n"

    return text