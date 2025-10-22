import asyncio

# from src.fastapi import run_fastapi
from bot.run import run_bot
from src.scheduler import run_scheduler


async def main():
    
    await asyncio.gather(
        run_scheduler(),
        # run_fastapi(),
        run_bot()
    )
    

if __name__ == "__main__":
    asyncio.run(main())