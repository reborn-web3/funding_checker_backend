import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.models import FundingSnapshot, FundingItem
from src.db import get_all_funding


async def run_fastapi(
    host: str = "127.0.0.1",
    port: int  = 8000,
    log_level: str = "info"
) -> None:
    """Запустить uvicorn из уже запущенного event-loop."""
    config = uvicorn.Config(
        "src.fastapi:app",
        host=host,
        port=port,
        log_level=log_level,
    )
    server = uvicorn.Server(config)
    await server.serve()

app = FastAPI(title="Funding API")

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1.",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/funding", response_model=FundingSnapshot)
async def get_funding():
    rows = await get_all_funding()          # List[tuple]
    data = [
        FundingItem(
            exchange = row[0],
            symbol = re.sub(r'(_USDT|_USDC|USDTM?|USDCM?)', '', row[1]),
            funding = row[2],
            next_settle_utc = row[3]   # уже datetime или str в ISO
        )
        for row in rows
    ]
    return FundingSnapshot(data=data)