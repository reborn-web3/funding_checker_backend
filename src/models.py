from pydantic import BaseModel
from datetime import datetime
from typing import List

class FundingItem(BaseModel):
    exchange: str
    symbol: str
    funding: float
    next_settle_utc: datetime

class FundingSnapshot(BaseModel):
    data: List[FundingItem]

# class Arbitrage(BaseModel):
#     symbol: str
#     exchange1: str
#     exchange2: str
#     funding_rate1: float
#     funding_rate2: float
#     spread: float

# class ArbitrageResponse(BaseModel):
#     data: List[Arbitrage]