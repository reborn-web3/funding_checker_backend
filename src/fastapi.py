from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models import FundingSnapshot, FundingItem
from src.db.database import db, get_all_funding, get_top_spread  # глобальный объект Database

app = FastAPI(title="Funding API")

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
