import aiosqlite
from typing import List, Tuple
from datetime import datetime, timedelta




FUNDING_DB_PATH = 'src/funding.db'

async def init_db():
    async with aiosqlite.connect(FUNDING_DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS funding (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exchange TEXT,
                symbol TEXT,
                funding REAL,
                next_settle TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def replace_funding_atomically(exchange: str, funding_data: List[tuple]):
    """Атомарная замена данных по бирже"""
    async with aiosqlite.connect(FUNDING_DB_PATH) as db:
        await db.execute("BEGIN TRANSACTION")
        try:
            # Удаляем старые данные
            await db.execute("DELETE FROM funding WHERE exchange = ?", (exchange,))
            
            # Вставляем новые данные одним запросом
            await db.executemany("""
                INSERT INTO funding (exchange, symbol, funding, next_settle, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, funding_data)
            
            await db.execute("COMMIT")
        except Exception as e:
            await db.execute("ROLLBACK")
            raise e

async def get_all_funding() -> List[Tuple[str, str, float, str]]:
    async with aiosqlite.connect(FUNDING_DB_PATH) as db:
        cursor = await db.execute("""
            SELECT exchange, symbol, funding, next_settle
            FROM funding
            ORDER BY ABS(funding) DESC
        """)
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def get_latest_funding(exchange, limit=10):
    async with aiosqlite.connect(FUNDING_DB_PATH) as db:
        cursor = await db.execute("""
            SELECT symbol, funding, next_settle
            FROM funding
            WHERE exchange=?
            ORDER BY ABS(funding) DESC
            LIMIT ?
        """, (exchange, limit))
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def get_upcoming_funding(hours: int) -> List[Tuple[str, str, float, str]]:
    """
    Возвращает UTC-строки next_settle.
    hours — целое количество часов вперёд.
    """
    now_utc   = datetime.utcnow()
    future_utc = now_utc + timedelta(hours=hours)

    async with aiosqlite.connect(FUNDING_DB_PATH) as db:
        cur = await db.execute(
            """
            SELECT exchange, symbol, funding, next_settle
            FROM funding
            WHERE next_settle BETWEEN ? AND ?
            ORDER BY next_settle ASC,
                     ABS(funding) DESC
            LIMIT 5
            """,
            (now_utc.isoformat(), future_utc.isoformat())
        )
        rows = await cur.fetchall()
        return rows

    
    
async def get_top_funding_across_exchanges(limit=5) -> List[Tuple[str, str, float, str]]:
    """
    Получает топ самых больших фандингов среди всех бирж
    Возвращает: List[(exchange, symbol, funding, next_settle)]
    """
    async with aiosqlite.connect(FUNDING_DB_PATH) as db:
        cursor = await db.execute("""
            SELECT exchange, symbol, funding, next_settle
            FROM funding
            ORDER BY ABS(funding) DESC
            LIMIT ?
        """, (limit,))
        rows = await cursor.fetchall()
        return rows
    
async def get_funding_for_symbol(symbol: str) -> List[Tuple[str, str, float, str]]:
    """
    Найдёт записи, где symbol содержит ticker (без учёта регистра).
    Пример: ticker='CTSI' найдёт CTSIUSDTM, CTSI_USDT и т.д.
    """
    pattern = f"%{symbol}%"
    async with aiosqlite.connect(FUNDING_DB_PATH) as db:
        cur = await db.execute(
            """
            SELECT exchange, symbol, funding, next_settle
            FROM funding
            WHERE symbol LIKE ? COLLATE NOCASE
            """,
            (pattern,)
        )
        return await cur.fetchall()
    
async def get_top_spread(limit: int = 5) -> List[Tuple[str, str, str, float, float, float]]:
    """
    Возвращает топ-монет по модулю спреда:
    (symbol, exchange1, exchange2, f1, f2, |f1-f2|)
    """
    async with aiosqlite.connect(FUNDING_DB_PATH) as db:
        cur = await db.execute(
            """
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
            LIMIT ?
            """,
            (limit,)
        )
        return await cur.fetchall()