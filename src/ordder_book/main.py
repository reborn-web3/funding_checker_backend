import asyncio
import ccxt.pro as ccxtpro

class AsyncWebsocket:
    def __init__(self):
        self.exchanges = [ccxtpro.mexc(), ccxtpro.gateio()]
    
    async def watch_order_book(self, symbol):
        while True:
            try:
                for exchange in self.exchanges:
                    orderbook = await exchange.watch_order_book(symbol, limit=5)
                
                
                best_bid_price = orderbook['bids'][0][0] if orderbook['bids'] else 'N/A'
                best_ask_price = orderbook['asks'][0][0] if orderbook['asks'] else 'N/A'

                best_bid_size = (orderbook['bids'][0][1] if orderbook['bids'] else 'N/A') * 10
                best_ask_size = (orderbook['asks'][0][1] if orderbook['asks'] else 'N/A') * 10


                print(f"Symbol: {symbol} | Best Bid price: {best_bid_price} Best Bid size: {best_bid_size}| Best Ask price: {best_ask_price} Best Ask size: {best_ask_size}")
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(5)  # wait before retrying
    async def run(self, symbols: list):
        tasks = [self.watch_order_book(symbol) for symbol in symbols]
        await asyncio.gather(*tasks)
    
    async def close(self):
        await self.exchange.close()

async def main():
    bot = AsyncWebsocket()
    try:
        symbols = ['GATA_USDT']
        await bot.run(symbols)
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())