import asyncio
from src.get_funding import FundingChecker
from src.config import EXCHANGES
from src.db import init_db


async def run_scheduler():
    await init_db()
    checkers = []
    
    for exchange_name, config in EXCHANGES.items():
        checker = FundingChecker(config)
        checkers.append(checker)

    while True:
        tasks = [checker.fetch_and_save() for checker in checkers]
        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(180)