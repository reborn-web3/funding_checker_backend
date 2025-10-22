from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models import FundingSnapshot, FundingItem
from src.db.database import db, get_all_funding, get_funding_for_symbol, get_latest_funding, get_top_funding_across_exchanges, get_top_spread, get_upcoming_funding  # глобальный объект Database

app = FastAPI(title="Funding API")

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1",
    "http://localhost:8080",
    "http://192.168.0.106:5173",
    "http://192.168.0.106:5174",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем БД при старте сервера
@app.on_event("startup")
async def startup_event():
    await db.connect()

@app.get("/funding", response_model=FundingSnapshot)
async def get_funding():
    rows = await get_all_funding()
    data = [
        FundingItem(
            exchange=row[0],
            symbol=row[1],
            funding=row[2],
            next_settle_utc=row[3]
        )
        for row in rows
    ]
    return FundingSnapshot(data=data)

@app.get("/arbitrage")
async def get_arbitrage():
    return await get_top_spread()

@app.get("/arbitrage")
async def get_upcoming_funding_route(hours):
    return await get_upcoming_funding(hours)

@app.get("/arbitrage")
async def get_arbitrage():
    return await get_latest_funding()

@app.get("/arbitrage")
async def get_arbitrage():
    return await get_top_funding_across_exchanges()

@app.get("/arbitrage")
async def get_arbitrage():
    return await get_funding_for_symbol()


