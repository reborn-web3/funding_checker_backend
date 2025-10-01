import asyncio
import asyncpg
from typing import List, Tuple
from datetime import datetime
from src.config import DATABASE_DSN
from src.log_config import configure_logging

logger = configure_logging()

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: asyncpg.pool.Pool | None = None

    async def connect(self, retries=10, delay=2):
        """Подключение с retry на случай, если БД ещё стартует"""
        for i in range(retries):
            try:
                self.pool = await asyncpg.create_pool(dsn=self.dsn)
                logger.info("Database pool created✅")
                await self.init_db()
                return
            except (asyncpg.CannotConnectNowError, ConnectionError) as e:
                logger.warning(f"DB not ready, retry {i+1}/{retries}: {e}")
                await asyncio.sleep(delay)
        raise Exception("Cannot connect to Postgres after several retries")

    async def init_db(self):
        """Создание таблицы funding, если нет"""
        async with self.pool.acquire() as conn:
            await conn.execute("DROP TABLE IF EXISTS funding;")
            logger.info("Database droped❌")
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS funding (
                    id SERIAL PRIMARY KEY,
                    exchange TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    funding REAL NOT NULL,
                    next_settle TEXT NOT NULL,
                    updated_at TEXT NOT NULL

                )
            """)
        logger.info("Database initialized✅")
    
    async def describe_table(self, table_name: str = "funding"):
        """Получить список колонок и их типы"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = $1
                ORDER BY ordinal_position;
            """, table_name)
            return [(r["column_name"], r["data_type"]) for r in rows]


    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def executemany(self, query: str, args_list: list[tuple]):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.executemany(query, args_list)

    async def fetch(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

# глобальный объект для использования в fastapi / scheduler
db = Database(DATABASE_DSN)

# вспомогательные функции для работы с funding
async def replace_funding_atomically(exchange: str, funding_data: List[tuple]):
    """Атомарная замена данных по бирже"""
    query_delete = "DELETE FROM funding WHERE exchange=$1"
    query_insert = """
        INSERT INTO funding (exchange, symbol, funding, next_settle, updated_at)
        VALUES ($1, $2, $3, $4, $5)
    """
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(query_delete, exchange)
            await conn.executemany(query_insert, funding_data)

async def get_all_funding() -> List[Tuple[str, str, float, datetime]]:
    rows = await db.fetch("""
        SELECT exchange, symbol, funding, next_settle
        FROM funding
        ORDER BY ABS(funding) DESC
    """)
    return [(r['exchange'], r['symbol'], r['funding'], r['next_settle']) for r in rows]

async def get_top_spread(limit: int = 5):
    rows = await db.fetch("""
        WITH ranked AS (
            SELECT
                symbol,
                exchange,
                funding,
                ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY ABS(funding) DESC) AS rn
            FROM funding
        ),
        pairs AS (
            SELECT
                r1.symbol,
                r1.exchange AS e1,
                r2.exchange AS e2,
                r1.funding  AS f1,
                r2.funding  AS f2,
                ABS(r1.funding - r2.funding) AS spread
            FROM ranked r1
            JOIN ranked r2
              ON r1.symbol = r2.symbol
             AND r1.rn = 1
             AND r2.rn = 2
        )
        SELECT symbol, e1, e2, f1, f2, spread
        FROM pairs
        ORDER BY spread DESC
        LIMIT $1
    """, limit)
    return [(r['symbol'], r['e1'], r['e2'], r['f1'], r['f2'], r['spread']) for r in rows]
