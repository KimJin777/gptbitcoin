"""
시장 데이터 수집 모듈
업비트 API를 통해 비트코인 시장 데이터를 수집합니다.
"""

import pyupbit
import pandas as pd
import requests
from typing import Optional, Dict, Any, Tuple
from config.settings import TRADING_SYMBOL, DAILY_DATA_COUNT, MINUTE_DATA_COUNT

def get_current_price(symbol: str = TRADING_SYMBOL) -> Optional[float]:
    """현재 가격 조회"""
    try:
        price = pyupbit.get_current_price(symbol)
        if price:
            print(f"📊 현재 {symbol} 가격: {price:,}원")
        return price
    except Exception as e:
        print(f"❌ 현재 가격 조회 실패: {e}")
        return None

def get_ohlcv_data(symbol: str = TRADING_SYMBOL, interval: str = "day", count: int = 30) -> Optional[pd.DataFrame]:
    """OHLCV 데이터 조회"""
    try:
        df = pyupbit.get_ohlcv(symbol, interval=interval, count=count)
        if df is not None and not df.empty:
            print(f"✅ {interval} 데이터 수집 완료: {len(df)}개")
            return df
        else:
            print(f"❌ {interval} 데이터 수집 실패")
            return None
    except Exception as e:
        print(f"❌ {interval} 데이터 조회 중 오류: {e}")
        return None

def get_orderbook(symbol: str = TRADING_SYMBOL) -> Optional[Dict[str, Any]]:
    """오더북 정보 조회"""
    try:
        orderbook = pyupbit.get_orderbook(symbol)
        if orderbook and isinstance(orderbook, dict):
            if 'orderbook_units' in orderbook and len(orderbook['orderbook_units']) > 0:
                ask_price = orderbook['orderbook_units'][0]['ask_price']
                bid_price = orderbook['orderbook_units'][0]['bid_price']
                if ask_price and bid_price:
                    spread = ask_price - bid_price
                    spread_percent = (spread / ask_price) * 100
                    print(f"📈 최우선 매도호가: {ask_price:,}원")
                    print(f"📉 최우선 매수호가: {bid_price:,}원")
                    print(f"📊 스프레드: {spread:,}원 ({spread_percent:.3f}%)")
            return orderbook
        else:
            print("❌ 오더북 정보 조회 실패")
            return None
    except Exception as e:
        print(f"❌ 오더북 조회 중 오류: {e}")
        return None

def get_fear_greed_index() -> Optional[Dict[str, Any]]:
    """공포탐욕지수 데이터 수집"""
    try:
        url = "https://api.alternative.me/fng/?limit=2"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['metadata']['error'] is None and len(data['data']) > 0:
            latest = data['data'][0]
            previous = data['data'][1] if len(data['data']) > 1 else None
            
            fear_greed_data = {
                'current_value': int(latest['value']),
                'current_classification': latest['value_classification'],
                'current_timestamp': latest['timestamp'],
                'time_until_update': latest.get('time_until_update', 0),
                'previous_value': int(previous['value']) if previous else None,
                'previous_classification': previous['value_classification'] if previous else None,
                'value_change': int(latest['value']) - int(previous['value']) if previous else 0
            }
            
            print(f"😨 공포탐욕지수: {fear_greed_data['current_value']} ({fear_greed_data['current_classification']})")
            if previous:
                print(f"📊 이전 지수: {fear_greed_data['previous_value']} ({fear_greed_data['previous_classification']})")
                print(f"📈 변화: {fear_greed_data['value_change']:+d}")
            
            return fear_greed_data
        else:
            print("❌ 공포탐욕지수 데이터 조회 실패")
            return None
            
    except Exception as e:
        print(f"❌ 공포탐욕지수 조회 중 오류: {e}")
        return None

def get_market_data() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[float], Optional[Dict], Optional[Dict]]:
    """전체 시장 데이터 수집"""
    print("=== 시장 데이터 수집 중 ===")
    
    # 일봉 데이터
    daily_df = get_ohlcv_data(TRADING_SYMBOL, "day", DAILY_DATA_COUNT)
    
    # 분봉 데이터
    minute_df = get_ohlcv_data(TRADING_SYMBOL, "minute1", MINUTE_DATA_COUNT)
    
    # 현재가
    current_price = get_current_price(TRADING_SYMBOL)
    
    # 오더북
    orderbook = get_orderbook(TRADING_SYMBOL)
    
    # 공포탐욕지수
    fear_greed_data = get_fear_greed_index()
    
    return daily_df, minute_df, current_price, orderbook, fear_greed_data
