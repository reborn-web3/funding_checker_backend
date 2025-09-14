import ccxt
import time

# --- Настройки ---
symbol = 'PLAY_USDT'   # монета
exchange_gate = ccxt.gate()
exchange_mexc = ccxt.mexc()

my_order = 34000.0

def get_orderbook(my_order, exchange, symbol):
    try:
        orderbook = exchange.fetch_order_book(symbol)
        if orderbook['bids']:   
            best_bid_price = orderbook['bids'][0][0]
            best_bid_amount = orderbook['bids'][0][1]
            while best_bid_amount < my_order:
                pass


        if orderbook['asks']:
            best_ask_price = orderbook['asks'][0][0]
            best_ask_amount = orderbook['asks'][0][1]


        return best_bid_price, best_bid_amount, best_ask_price, best_ask_amount
    except Exception as e:
        print(f"Ошибка {exchange.id}: {e}")
        return None, None

# bid_a, ask_a = get_orderbook(exchange_a, symbol)
best_bid_price_mexc, best_bid_amount_mexc, best_ask_price_mexc, best_ask_amount_mexc = get_orderbook(my_order, exchange_mexc, symbol)

print(f"MEXC  -> best bid price: {best_bid_price_mexc}, best bid amount {best_bid_amount_mexc*10}K,  best ask price: {best_ask_price_mexc}, bes ask amount: {best_ask_amount_mexc*10}")
print(f"USDT price  -> bid price: {best_bid_price_mexc*best_bid_amount_mexc*10},  ask price: {best_ask_price_mexc*best_ask_amount_mexc*10}")


# while True:
#     bid_a, ask_a = get_orderbook(exchange_a, symbol)
#     bid_b, ask_b = get_orderbook(exchange_b, symbol)

#     if bid_a and bid_b:
#         print(f"\n=== {symbol} ===")
#         print(f"Gate  -> bid: {bid_a:.6f}, ask: {ask_a:.6f}")
#         print(f"MEXC  -> bid: {bid_b:.6f}, ask: {ask_b:.6f}")

#         # считаем возможный арбитраж
#         diff_long_gate = (bid_a - ask_b) / ask_b * 100  # купить на MEXC (ask_b), продать на Gate (bid_a)
#         diff_long_mexc = (bid_b - ask_a) / ask_a * 100  # купить на Gate (ask_a), продать на MEXC (bid_b)

#         print(f"Потенциал (MEXC->Gate): {diff_long_gate:.2f}%")
#         print(f"Потенциал (Gate->MEXC): {diff_long_mexc:.2f}%")

#     time.sleep(3)  # обновление каждые 3 секунды
