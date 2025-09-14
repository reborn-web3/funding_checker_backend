from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.db.user_db import Database


class DatabaseMiddleware(BaseMiddleware):
    """Middleware для передачи экземпляра базы данных в хендлеры"""
    
    def __init__(self, db: Database):
        self.db = db
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Добавляем БД в данные для хендлера
        data["db"] = self.db
        return await handler(event, data)