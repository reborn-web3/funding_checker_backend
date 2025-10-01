import asyncio
from src.get_funding import FundingChecker
from src.config import EXCHANGES
from src.db.database import db  # глобальный объект Database

async def run_scheduler():
    # Подключаемся к БД
    await db.connect()
    columns = await db.describe_table("funding")
    for name, dtype in columns:
        print(f"{name}: {dtype}")


    checkers = [FundingChecker(config) for config in EXCHANGES.values()]

    while True:
        tasks = [checker.fetch_and_save() for checker in checkers]
        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(180)  # раз в 3 минуты

if __name__ == "__main__":
    asyncio.run(run_scheduler())
