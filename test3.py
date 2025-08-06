import pyupbit

# 단일 종목 조회
current_price = pyupbit.get_current_price("KRW-BTC")
print(current_price)

# 여러 종목 조회
tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP"]
current_prices = pyupbit.get_current_price(tickers)
print(current_prices)