import os
from dotenv import load_dotenv
load_dotenv()

import pyupbit
import pandas as pd

access = os.getenv("UPBIT_ACCESS_KEY")
secret = os.getenv("UPBIT_SECRET_KEY")
upbit = pyupbit.Upbit(access, secret)

my_krw = upbit.get_balance("KRW")
print(f"Current KRW balance: {my_krw}")

my_btc = upbit.get_balance("KRW-BTC")
print(f"Current BTC balance: {my_btc}")

current_price = upbit.get_current_price("KRW-BTC")['orderbook_units'][0]['ask_price']
print(f"Current BTC price: {current_price}")