import asyncio
import re
import traceback

from datetime import datetime, timezone  
import aiohttp
import ccxt.async_support as ccxt

from src.db import replace_funding_atomically
from src.config import *
from src.log_config import configure_logging

logger = configure_logging()

class FundingChecker:
    '''Прямой запрос для бирж, которые предоставляют данные в одном эндпоинте (тикер, фандинг, время начисления)'''
    def __init__(self, 
                 config: ExchangeConfig,
                 api_key: str = '', 
                 secret: str = ''
                 ):
        
        self.url = config.url
        self.funding_title = config.funding_title
        self.time_title = config.time_title
        self.time_format = config.time_format
        self.exchange_name = config.name
        self.tickers_number = config.tickers_number
        
        cls = getattr(ccxt, self.exchange_name)

        self.ccxt_exchange: ccxt.Exchange = cls({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'swap',  # только фьючерсы USDT-марджин
            },
            'timeout': 25000,  # увеличить до 25 секунд
        })

    def format_time(self, ts: int) -> datetime:
        """Возвращает объект datetime UTC+0"""
        ts = float(ts)
        if self.time_format == 'milliseconds':
            dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
        else:
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt


    async def fetch_via_http(self):
        """Получение данных через HTTP API"""
        
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(self.url) as response:
                
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                
                resp = await response.json()
                if isinstance(resp, dict) and "data" in resp:
                    return resp["data"]
                elif isinstance(resp, list):
                    return resp
                else:
                    raise Exception(f"Unexpected response format: {resp}")

    async def fetch_via_ccxt(self):
        """Получение данных через CCXT с автоматическим закрытием"""
        try:
            resp = await self.ccxt_exchange.fetch_funding_rates()
            data = []
            for symbol, rate_data in resp.items():
                if rate_data.get(self.funding_title) is not None:         
                    item = {
                        'symbol': symbol.split('/')[0],
                        'fundingRate': rate_data.get('info', {}).get(self.funding_title), 
                        'nextFundingTime': rate_data.get('info', {}).get(self.time_title)
                    }
                    data.append(item)
            return data
        except ccxt.RequestTimeout:
            logger.error("Bybit API timeout")
        finally:
            await self.ccxt_exchange.close()

    async def fetch_and_save(self):
        """Универсальный метод"""
        try:
            if self.url:
                # в fetch_and_save
                try:
                    data = await self.fetch_via_http()
                except (aiohttp.ClientError, asyncio.TimeoutError, OSError) as e:
                    logger.error(f"{self.exchange_name} network error: {e}")
                    return  # пропускаем биржу, но не крашим бота
            else:
                data = await self.fetch_via_ccxt() 
            
            if data:           
                valid_data = [item for item in data if item.get(self.funding_title) is not None]
                sorted_data = sorted(valid_data, key=lambda x: abs(float(x[self.funding_title])), reverse=True)[:self.tickers_number]
                
                new_funding_data = []
                for item in sorted_data:
                    symbol = item.get("symbol") or item.get("contract") or item.get("name")
                    clean_symbol = re.sub(r'(_USDT|_USDC|USDTM?|USDCM?)', '', symbol)           
                    funding_pct = float(item[self.funding_title]) * 100
                    next_settle = self.format_time(item.get(self.time_title))
                    
                    new_funding_data.append((
                        self.exchange_name, 
                        clean_symbol, 
                        round(funding_pct, 4), 
                        next_settle.isoformat(),
                        datetime.utcnow()
                    ))

                if new_funding_data:
                    try:
                        await replace_funding_atomically(self.exchange_name, new_funding_data)
                        logger.info(f"Data updated for {self.exchange_name}")
                    except Exception as e:
                        logger.error(f"DB error for {self.exchange_name}: {e}")

        except Exception as e:
            traceback.print_exc()


