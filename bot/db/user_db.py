import logging
import aiosqlite
from typing import Optional, Dict, Any
from typing import Tuple
from bot.models.user import User   # теперь импортируем модель

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "bot/db/users.db"):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id            INTEGER PRIMARY KEY,
                    username      TEXT,
                    first_name    TEXT,
                    last_name     TEXT,
                    timezone      TEXT,
                    upcoming_funding_time INTEGER,
                    language_code TEXT,
                    is_bot        BOOLEAN,
                    UTC0_created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UTC0_updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()
            logger.info("User database initialized")

    async def ensure_user(self, user: User) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR IGNORE INTO users
                (id, username, first_name, last_name, timezone, language_code, is_bot)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user.id,
                user.username,
                user.first_name,
                user.last_name,
                user.timezone,
                user.language_code,
                user.is_bot,
            ))
            await db.commit()

    async def user_exists(self, user_id: int) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT 1 FROM users WHERE id = ?", (user_id,)
            ) as cursor:
                if await cursor.fetchone() is not None:
                    return True
                else:
                    return False
    
    
    async def is_user_upcoming_funding_time_exist(self, user_id: int) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT upcoming_funding_time FROM users WHERE id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row and row[0]:
                    return True
                else:
                    return False
   
    async def set_user_timezone(self, user_id: int, tz: str) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET timezone = ? WHERE id = ?", (tz, user_id)
            )
            await db.commit()
    
    async def set_user_upcoming_funding_time(self, user_id: int, hours: int) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET upcoming_funding_time = ? WHERE id = ?",
                (hours, user_id)
            )
            await db.commit()
    
    async def get_user_timezone(self, user_id: int) -> str:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT timezone FROM users WHERE id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row and row[0] else "UTC+0"
    
    async def get_user_upcoming_funding_time(self, user_id: int) -> Tuple:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT upcoming_funding_time FROM users WHERE id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return row
  
    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                """SELECT id, username, first_name, last_name,
                          timezone, upcoming_funding_time, language_code, is_bot, UTC0_created_at, UTC0_updated_at
                   FROM users WHERE id = ?""",
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'username': row[1],
                        'first_name': row[2],
                        'last_name': row[3],
                        'timezone': row[4],
                        'upcoming_funding_time': row[5],
                        'language_code': row[6],
                        'is_bot': bool(row[7]),
                        'UTC0_created_at': row[8],
                        'UTC0_updated_at': row[9],
                    }
                return None
            