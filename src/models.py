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