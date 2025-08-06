import os
from dotenv import load_dotenv
load_dotenv()

import pyupbit
import pandas as pd
import json
# df = pyupbit.get_ohlcv("KRW-BTC")
# print(df.tail())
df = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=30)
# print(df.to_json())

from openai import OpenAI
import pandas as pd  # Assuming df is a pandas DataFrame

def ai_trading_decision():
    """
    인공지능 활용 비트코인 매매 결정 함수
    이 함수는 OpenAI API를 사용하여 비트코인 매매 결정을 내립니다.
    매매 결정을 내리기 위해 최근 30일간의 비트코인 가격 데이터를 사용합니다.
    """
    client = OpenAI()

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "You are a Bitcoin investment expert. Based on the chart data provided, tell me what to do now: buy, sell, or hold. Response in JSON format.\n\nResponse Example:\n{'decision': 'buy', 'reason': 'some technical reason'}\n{'decision': 'sell', 'reason': 'some technical reason'}\n{'decision': 'hold', 'reason': 'some technical reason'}"
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": df.to_json()
            }
        ]
        }
        # {
        # "role": "assistant",
        # "content": [
        #     {
        #     "type": "text",
        #     "text": "{\n  \"decision\": \"hold\",\n  \"reason\": \"Upon further analysis, the price has been fluctuating with signs of potential stabilization, as evidenced by the recent few sessions hovering around the 145,000 level without severe drops in price. The trading volume has decreased, indicating reduced selling pressure. The current market sentiment does not strongly indicate either a bullish or bearish trend, suggesting that holding is prudent until a clear trend emerges.\"\n}"
        #     }
        # ]
        # }
    ],
    response_format={
        "type": "text",
        "type": "json_object"
    },
    #   temperature=1,
    #   max_completion_tokens=2048,
    #   top_p=1,
    #   frequency_penalty=0,
    #   presence_penalty=0
    )

    # print(response)
    result = response.choices[0].message.content
    # print(result)
    # print(type(result))
    
    result_json = json.loads(result)
    # print(result_json)
    # print(type(result_json))

    access = os.getenv("UPBIT_ACCESS_KEY")
    secret = os.getenv("UPBIT_SECRET_KEY")
    upbit = pyupbit.Upbit(access, secret)
    
    print("### AI Decision Result ###", result_json['decision'], "###")
    print("### AI Decision Reason ###", result_json['reason'])

    
    if result_json['decision'] == 'buy':
        # 현금보유 조회
        my_krw = upbit.get_balance("KRW")
        print(f"Current KRW balance: {my_krw}")
        print("Buying Bitcoin") 
        if my_krw*0.9995 > 5000:
            # 5000원 이상일 때만 매수
            print("Executing buy order")
            print(upbit.buy_market_order("KRW-BTC", my_krw*0.9995))  # Example: Buy Bitcoin with 10,000 KRW
        else:
            print("5000원 미만, Not enough KRW to buy Bitcoin, skipping buy order")

    elif result_json['decision'] == 'sell':
        my_btc = upbit.get_balance("KRW-BTC")
        print(f"Current BTC balance: {my_btc}")
        # current_price = upbit.get_current_price("KRW-BTC")['orderbook_units'][0]['ask_price']
        # print(f"Current BTC price: {current_price}")
        
        current_price = pyupbit.get_current_price("KRW-BTC")
        print(f"Current BTC price: {current_price}")

        if my_btc*0.9995 > 5000:
            # 5000원 이상일 때만 매도
            print("Executing sell order")
            print("Selling Bitcoin")        
            print(upbit.sell_market_order("KRW-BTC", my_btc*0.9995))
        else:
            print("5000원 미만, Not enough BTC to sell, skipping sell order")
        
    elif result_json['decision'] == 'hold':
        pass
    
    
if __name__ == "__main__":
    import time
    while True:
        print("#"*60)
        print("### AI Trading Decision Start ###")
        ai_trading_decision()
        print("### AI Trading Decision End ###")
        print("#"*60)
        time.sleep(60*5)  # 5분 마다 실행
        
        # ai_trading_decision()
    # df = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=30)
    # print(df.to_json())