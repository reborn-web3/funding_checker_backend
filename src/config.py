from pydantic import BaseModel
from dataclasses import dataclass

DATABASE_DSN = "postgresql://myuser:mypassword@db:5432/funding"

@dataclass
class ExchangeConfig:
    url: str = None
    funding_title: str = None
    time_title: str = None 
    time_format: str = None
    name: str = None
    tickers_number: int = 500

EXCHANGES = {
    "mexc": ExchangeConfig(
        url="https://contract.mexc.com/api/v1/contract/funding_rate",
        funding_title="fundingRate",
        time_title="nextSettleTime",
        time_format = 'milliseconds',
        name="mexc"
    ),
    "kucoin": ExchangeConfig(
        url="https://api-futures.kucoin.com/api/v1/contracts/active",
        funding_title="fundingFeeRate", 
        time_title="nextFundingRateDateTime",
        time_format = 'milliseconds',
        name="kucoin"
    ),
    "gate": ExchangeConfig(
        url="https://api.gateio.ws/api/v4/futures/usdt/contracts",
        funding_title="funding_rate",
        time_title="funding_next_apply", 
        time_format = 'seconds',
        name="gate"
    ),
    
    "bybit": ExchangeConfig(
        funding_title='fundingRate',
        time_title='nextFundingTime',
        time_format = 'milliseconds',
        name="bybit"
    ),
    
#     "bingx": ExchangeConfig(
#         name="bingx"
#     )
}


EXCHANGE_FUTURES_URLS = {
    "mexc": "https://www.mexc.com/futures/{symbol}_USDT",
    "kucoin": "https://www.kucoin.com/trade/futures/{symbol}USDTM",
    "gate": "https://www.gate.com/futures/USDT/{symbol}_USDT",
    "bybit": "https://www.bybit.com/trade/usdt/{symbol}USDT",
    # "bingx": "https://www.bingx.com/en-us/futures/{symbol}",
}
