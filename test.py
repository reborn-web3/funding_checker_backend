import ccxt
import time
import numpy as np
from typing import Dict, List, Tuple

class FundingArbitrage:
    def __init__(self):
        self.exchanges = {
            'bybit': ccxt.bybit({'enableRateLimit': True}),
            'gate': ccxt.gateio({'enableRateLimit': True}),

        }
        
    def get_weighted_orderbook(self, symbol: str, depth: int = 10) -> Dict:
        """Получает взвешенный стакан с нескольких бирж"""
        orderbooks = {}
        
        for name, exchange in self.exchanges.items():
            try:
                orderbook = exchange.fetch_order_book(symbol, depth * 2)
                orderbooks[name] = orderbook
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                print(f"Ошибка получения данных с {name}: {e}")
        
        return orderbooks
    
    def calculate_optimal_prices(self, orderbooks: Dict, amount: float) -> Tuple[float, float, str, str]:
        """Вычисляет оптимальные цены для хеджирования"""
        best_buy = {'price': 0, 'exchange': '', 'available': 0}
        best_sell = {'price': float('inf'), 'exchange': '', 'available': 0}
        
        # Анализируем цены покупки
        for exchange, ob in orderbooks.items():
            if 'bids' in ob and ob['bids']:
                cumulative_amount = 0
                for price, qty in ob['bids']:
                    cumulative_amount += qty
                    if cumulative_amount >= amount:
                        if price > best_buy['price']:
                            best_buy = {'price': price, 'exchange': exchange, 'available': cumulative_amount}
                        break
        
        # Анализируем цены продажи
        for exchange, ob in orderbooks.items():
            if 'asks' in ob and ob['asks']:
                cumulative_amount = 0
                for price, qty in ob['asks']:
                    cumulative_amount += qty
                    if cumulative_amount >= amount:
                        if price < best_sell['price']:
                            best_sell = {'price': price, 'exchange': exchange, 'available': cumulative_amount}
                        break
        
        return best_buy['price'], best_sell['price'], best_buy['exchange'], best_sell['exchange']
    
    def find_best_arbitrage_pair(self, amount: float = 0.1) -> Dict:
        """Находит лучшую пару для арбитража"""
        symbol = 'ZKC/USDT'
        
        print("🔍 Анализируем стаканы на нескольких биржах...")
        orderbooks = self.get_weighted_orderbook(symbol)
        
        buy_price, sell_price, buy_exchange, sell_exchange = self.calculate_optimal_prices(orderbooks, amount)
        
        if buy_exchange and sell_exchange:
            spread = sell_price - buy_price
            spread_percent = (spread / buy_price) * 100
            
            return {
                'buy_exchange': buy_exchange,
                'sell_exchange': sell_exchange,
                'buy_price': buy_price,
                'sell_price': sell_price,
                'spread': spread,
                'spread_percent': spread_percent,
                'amount': amount,
                'potential_pnl': spread * amount if spread > 0 else 0
            }
        
        return None

    def monitor_spreads(self, monitoring_time: int = 300):
        """Мониторинг спредов в реальном времени"""
        print(f"📊 Мониторинг спредов в течение {monitoring_time} секунд...")
        print("Время | Buy Exch | Sell Exch | Спред | Спред % | PNL")
        print("-" * 60)
        
        start_time = time.time()
        best_spread = float('inf')
        best_opportunity = None
        
        while time.time() - start_time < monitoring_time:
            try:
                opportunity = self.find_best_arbitrage_pair(0.1)
                
                if opportunity and opportunity['spread'] > 0:
                    current_time = time.strftime("%H:%M:%S")
                    print(f"{current_time} | {opportunity['buy_exchange']:8} | {opportunity['sell_exchange']:8} | "
                          f"{opportunity['spread']:6.2f} | {opportunity['spread_percent']:6.4f}% | "
                          f"{opportunity['potential_pnl']:6.4f}")
                    
                    if opportunity['spread'] < best_spread:
                        best_spread = opportunity['spread']
                        best_opportunity = opportunity
                
                time.sleep(2)  # Проверяем каждые 2 секунды
                
            except Exception as e:
                print(f"Ошибка мониторинга: {e}")
                time.sleep(5)
        
        print("\n🎯 Лучшая возможность за период:")
        if best_opportunity:
            self.print_opportunity(best_opportunity)
        else:
            print("Не найдено подходящих возможностей")

    def print_opportunity(self, opportunity: Dict):
        """Выводит информацию об арбитражной возможности"""
        print("=" * 60)
        print("🎯 ОПТИМАЛЬНАЯ АРБИТРАЖНАЯ СТРАТЕГИЯ")
        print("=" * 60)
        print(f"Купить на: {opportunity['buy_exchange'].upper()}")
        print(f"Цена покупки: ${opportunity['buy_price']:.2f}")
        print(f"Продать на: {opportunity['sell_exchange'].upper()}")
        print(f"Цена продажи: ${opportunity['sell_price']:.2f}")
        print(f"Спред: ${opportunity['spread']:.4f} ({opportunity['spread_percent']:.6f}%)")
        print(f"Количество: {opportunity['amount']} ZKC")
        print(f"Потенциальный PNL: ${opportunity['potential_pnl']:.4f}")
        print("=" * 60)

# Запуск мониторинга
if __name__ == "__main__":
    arb = FundingArbitrage()
    arb.monitor_spreads(60)  # Мониторинг 60 секунд