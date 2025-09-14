import re
from src.config import EXCHANGE_FUTURES_URLS
from bot.utils.time import localize_time

async def format_funding(latest_funding, exchange: str, user_tz) -> str:
    text = f"<b>ТОП-10 по фандингу ({exchange.upper()})</b>\n\n"
    for symbol, funding, next_settle in latest_funding:
        url = EXCHANGE_FUTURES_URLS[exchange.lower()].format(symbol=symbol)
        clean = re.sub(r'(_USDT|_USDC|USDTM?|USDCM?)', '', symbol)
        local = localize_time(next_settle, user_tz)
        text += f"<a href='{url}'>{clean}</a> | {funding:+.4f}% | {local}\n"
    return text