from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from bot.middlewares.middleware import DatabaseMiddleware
from bot.config import BOT_TOKEN
from bot.db.user_db import Database

from bot.handlers import handlers_router


async def run_bot():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML",))
    dp = Dispatcher()
    
    db = Database()
    await db.init_db()

    dp.message.middleware(DatabaseMiddleware(db))
    dp.callback_query.middleware(DatabaseMiddleware(db))
    
    dp.include_router(handlers_router)

    await dp.start_polling(bot)
    