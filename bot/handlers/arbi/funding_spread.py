from typing import List, Tuple
from src.db.database import get_funding_for_symbol

async def build_funding_spread(ticker: str) -> List[Tuple[str, str, float, float]]:
    rows = await get_funding_for_symbol(ticker)  # [(exchange, symbol, funding, next_settle), ...]

    if len(rows) < 2:
        return []  # нет пары

    # извлекаем (exchange, funding)
    pairs = [(ex, fund) for ex, _sym, fund, _time in rows]

    spreads = []
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            e1, f1 = pairs[i]
            e2, f2 = pairs[j]
            spreads.append((e1, e2, f1, f2, abs(f1 - f2)))

    # сортировка по модулю спреда
    spreads.sort(key=lambda x: x[4], reverse=True)
    return [(e1, e2, f1, f2) for e1, e2, f1, f2, _ in spreads]