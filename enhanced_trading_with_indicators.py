import os
from dotenv import load_dotenv
load_dotenv()

import pyupbit
import pandas as pd
import json
from datetime import datetime, timedelta
import time
import numpy as np

# TA 라이브러리 import
import ta
from ta.trend import SMAIndicator, EMAIndicator, MACD, ADXIndicator
from ta.momentum import StochasticOscillator, WilliamsRIndicator, RSIIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator

from openai import OpenAI

def calculate_technical_indicators(df):
    """
    기술적 지표 계산 함수
    """
    if df.empty:
        return df
    
    # 기본 OHLCV 컬럼명 확인 및 통일
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    df_columns = [col.lower() for col in df.columns]
    
    # 컬럼명 매핑
    column_mapping = {}
    for req_col in required_columns:
        for df_col in df.columns:
            if req_col in df_col.lower():
                column_mapping[req_col] = df_col
                break
    
    # 필수 컬럼이 없으면 원본 반환
    if len(column_mapping) < 5:
        print("필수 OHLCV 컬럼을 찾을 수 없습니다.")
        return df
    
    # 컬럼명 통일
    df_renamed = df.rename(columns={
        column_mapping['open']: 'Open',
        column_mapping['high']: 'High', 
        column_mapping['low']: 'Low',
        column_mapping['close']: 'Close',
        column_mapping['volume']: 'Volume'
    })
    
    try:
        # 1. 이동평균선 (SMA, EMA)
        df_renamed['SMA_20'] = SMAIndicator(close=df_renamed['Close'], window=20).sma_indicator()
        df_renamed['SMA_50'] = SMAIndicator(close=df_renamed['Close'], window=50).sma_indicator()
        df_renamed['EMA_12'] = EMAIndicator(close=df_renamed['Close'], window=12).ema_indicator()
        df_renamed['EMA_26'] = EMAIndicator(close=df_renamed['Close'], window=26).ema_indicator()
        
        # 2. MACD
        macd = MACD(close=df_renamed['Close'])
        df_renamed['MACD'] = macd.macd()
        df_renamed['MACD_Signal'] = macd.macd_signal()
        df_renamed['MACD_Histogram'] = macd.macd_diff()
        
        # 3. RSI
        df_renamed['RSI'] = RSIIndicator(close=df_renamed['Close']).rsi()
        
        # 4. 볼린저 밴드
        bb = BollingerBands(close=df_renamed['Close'])
        df_renamed['BB_Upper'] = bb.bollinger_hband()
        df_renamed['BB_Middle'] = bb.bollinger_mavg()
        df_renamed['BB_Lower'] = bb.bollinger_lband()
        df_renamed['BB_Width'] = bb.bollinger_wband()
        df_renamed['BB_Position'] = bb.bollinger_pband()
        
        # 5. 스토캐스틱
        stoch = StochasticOscillator(high=df_renamed['High'], low=df_renamed['Low'], close=df_renamed['Close'])
        df_renamed['Stoch_K'] = stoch.stoch()
        df_renamed['Stoch_D'] = stoch.stoch_signal()
        
        # 6. 윌리엄스 %R
        df_renamed['Williams_R'] = WilliamsRIndicator(high=df_renamed['High'], low=df_renamed['Low'], close=df_renamed['Close']).williams_r()
        
        # 7. ATR (Average True Range)
        df_renamed['ATR'] = AverageTrueRange(high=df_renamed['High'], low=df_renamed['Low'], close=df_renamed['Close']).average_true_range()
        
        # 8. ADX (Average Directional Index)
        adx = ADXIndicator(high=df_renamed['High'], low=df_renamed['Low'], close=df_renamed['Close'])
        df_renamed['ADX'] = adx.adx()
        df_renamed['ADX_Pos'] = adx.adx_pos()
        df_renamed['ADX_Neg'] = adx.adx_neg()
        
        # 9. 거래량 지표
        df_renamed['OBV'] = OnBalanceVolumeIndicator(close=df_renamed['Close'], volume=df_renamed['Volume']).on_balance_volume()
        
        # 10. 추가 모멘텀 지표
        # ROC (Rate of Change)
        df_renamed['ROC'] = ta.momentum.ROCIndicator(close=df_renamed['Close']).roc()
        
        # CCI (Commodity Channel Index)
        df_renamed['CCI'] = ta.trend.CCIIndicator(high=df_renamed['High'], low=df_renamed['Low'], close=df_renamed['Close']).cci()
        
        print(f"기술적 지표 계산 완료: {len(df_renamed.columns)}개 컬럼")
        
    except Exception as e:
        print(f"기술적 지표 계산 중 오류 발생: {e}")
        return df
    
    return df_renamed

def get_market_data_with_indicators():
    """
    기술적 지표가 포함된 시장 데이터 수집 함수
    """
    print("=== 시장 데이터 수집 중 (기술적 지표 포함) ===")
    
    # 30일 일봉 데이터
    daily_df = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=30)
    if daily_df is not None:
        print(f"30일 일봉 데이터 수집 완료: {len(daily_df)}개")
        # 기술적 지표 추가
        daily_df = calculate_technical_indicators(daily_df)
    else:
        print("30일 일봉 데이터 수집 실패")
        daily_df = pd.DataFrame()
    
    # 24시간 분봉 데이터 (1분 단위)
    minute_df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=1440)  # 24시간 = 1440분
    if minute_df is not None:
        print(f"24시간 분봉 데이터 수집 완료: {len(minute_df)}개")
        # 기술적 지표 추가
        minute_df = calculate_technical_indicators(minute_df)
    else:
        print("24시간 분봉 데이터 수집 실패")
        minute_df = pd.DataFrame()
    
    # 현재가
    current_price = pyupbit.get_current_price("KRW-BTC")
    if current_price is not None:
        print(f"현재 비트코인 가격: {current_price:,}원")
    else:
        print("현재 비트코인 가격 조회 실패")
        current_price = 0
    
    # 오더북 정보
    orderbook = pyupbit.get_orderbook("KRW-BTC")
    if orderbook and len(orderbook) > 0 and len(orderbook[0]['orderbook_units']) > 0:
        ask_price = orderbook[0]['orderbook_units'][0]['ask_price']  # 최우선 매도호가
        bid_price = orderbook[0]['orderbook_units'][0]['bid_price']  # 최우선 매수호가
        if ask_price is not None and bid_price is not None:
            spread = ask_price - bid_price
            spread_percent = (spread / ask_price) * 100
            print(f"최우선 매도호가: {ask_price:,}원")
            print(f"최우선 매수호가: {bid_price:,}원")
            print(f"스프레드: {spread:,}원 ({spread_percent:.3f}%)")
        else:
            print("오더북 가격 정보 조회 실패")
    else:
        print("오더북 정보 조회 실패")
    
    return daily_df, minute_df, current_price, orderbook

def get_investment_status(upbit):
    """
    현재 투자 상태 조회 함수 - 투자 성과 및 수익률 포함
    """
    print("=== 투자 상태 조회 중 ===")
    
    # 전체 잔고 조회
    try:
        balances = upbit.get_balances()
        if balances is None:
            balances = []
    except Exception as e:
        print(f"전체 잔고 조회 실패: {e}")
        balances = []
    
    # KRW 잔고
    try:
        krw_balance = upbit.get_balance("KRW")
        if krw_balance is not None and krw_balance > 0:
            print(f"보유 현금: {krw_balance:,.2f}원")
        else:
            print("보유 현금: 0원")
            krw_balance = 0
    except Exception as e:
        print(f"보유 현금 조회 실패: {e}")
        krw_balance = 0
    
    # BTC 잔고
    try:
        btc_balance = upbit.get_balance("KRW-BTC")
        if btc_balance is not None and btc_balance > 0:
            print(f"보유 비트코인: {btc_balance:.8f} BTC")
        else:
            print("보유 비트코인: 0 BTC")
            btc_balance = 0
    except Exception as e:
        print(f"보유 비트코인 조회 실패: {e}")
        btc_balance = 0
    
    # 현재 비트코인 가격
    current_price = pyupbit.get_current_price("KRW-BTC")
    if current_price is None:
        print("현재 비트코인 가격 조회 실패")
        current_price = 0
    
    # 비트코인 평가금액 및 투자 성과 분석
    if btc_balance > 0:
        btc_value = btc_balance * current_price
        print(f"비트코인 평가금액: {btc_value:,.2f}원")
        
        # 총 자산
        total_assets = krw_balance + btc_value
        print(f"총 자산: {total_assets:,.2f}원")
        
        # 비트코인 비중
        btc_ratio = (btc_value / total_assets) * 100
        print(f"비트코인 비중: {btc_ratio:.2f}%")
        
        # 평균 매수가 계산 (업비트 API에서 제공하는 정보 활용)
        try:
            # 전체 잔고 정보에서 BTC 평균 매수가 조회
            for balance in balances:
                if balance['currency'] == 'BTC':
                    avg_buy_price = float(balance['avg_buy_price'])
                    if avg_buy_price > 0:
                        print(f"평균 매수가: {avg_buy_price:,.0f}원")
                        
                        # 수익률 계산
                        profit_loss = current_price - avg_buy_price
                        profit_loss_percent = (profit_loss / avg_buy_price) * 100
                        
                        print(f"현재 수익/손실: {profit_loss:,.0f}원 ({profit_loss_percent:+.2f}%)")
                        
                        # 총 투자금액 (평균 매수가 * 보유 수량)
                        total_investment = avg_buy_price * btc_balance
                        print(f"총 투자금액: {total_investment:,.0f}원")
                        
                        # 총 수익/손실
                        total_profit_loss = btc_value - total_investment
                        total_profit_loss_percent = (total_profit_loss / total_investment) * 100
                        print(f"총 수익/손실: {total_profit_loss:,.0f}원 ({total_profit_loss_percent:+.2f}%)")
                        
                        # 투자 성과 등급
                        if total_profit_loss_percent >= 20:
                            performance_grade = "A+ (우수)"
                        elif total_profit_loss_percent >= 10:
                            performance_grade = "A (양호)"
                        elif total_profit_loss_percent >= 0:
                            performance_grade = "B (보통)"
                        elif total_profit_loss_percent >= -10:
                            performance_grade = "C (주의)"
                        else:
                            performance_grade = "D (위험)"
                        
                        print(f"투자 성과 등급: {performance_grade}")
                        break
        except Exception as e:
            print(f"평균 매수가 조회 실패: {e}")
    else:
        print("보유 비트코인이 없습니다.")
    
    # 미체결 주문 조회
    try:
        pending_orders = upbit.get_order("KRW-BTC")
        if pending_orders is None:
            pending_orders = []
    except Exception as e:
        print(f"미체결 주문 조회 실패: {e}")
        pending_orders = []
    
    if pending_orders:
        print(f"\n미체결 주문: {len(pending_orders)}개")
        total_pending_value = 0
        for order in pending_orders:
            try:
                # 주문 데이터 구조 확인 및 안전한 접근
                if isinstance(order, dict):
                    order_type = "매수" if order.get('side') == 'bid' else "매도"
                    price = order.get('price')
                    volume = order.get('volume', 0)
                    
                    if price is not None and price != "시장가":
                        try:
                            order_value = float(price) * float(volume)
                            total_pending_value += order_value
                            print(f"  - {order_type}: {price:,.0f}원, {volume:.8f} BTC (가치: {order_value:,.0f}원)")
                        except (ValueError, TypeError):
                            print(f"  - {order_type}: {price}원, {volume} BTC (가치 계산 실패)")
                    else:
                        print(f"  - {order_type}: 시장가, {volume:.8f} BTC")
                else:
                    print(f"  - 주문 데이터 형식 오류: {order}")
            except Exception as e:
                print(f"  - 주문 데이터 처리 실패: {e}")
        
        if total_pending_value > 0:
            print(f"총 미체결 주문 가치: {total_pending_value:,.0f}원")
    else:
        print("미체결 주문 없음")
    
    # 최근 거래 내역 조회 (최근 10개)
    try:
        print("\n=== 최근 거래 내역 ===")
        recent_orders = upbit.get_order("KRW-BTC", state="done", limit=10)
        if recent_orders is None:
            recent_orders = []
        
        if recent_orders:
            for order in recent_orders:
                try:
                    # 주문 데이터 구조 확인 및 안전한 접근
                    if isinstance(order, dict):
                        order_type = "매수" if order.get('side') == 'bid' else "매도"
                        order_time = order.get('created_at', '')[:19] if order.get('created_at') else '시간 없음'
                        volume = order.get('volume', 0)
                        price = order.get('price')
                        fee = order.get('paid_fee', 0)
                        
                        if price is not None and price != "시장가":
                            try:
                                order_value = float(price) * float(volume)
                                print(f"  - {order_time}: {order_type} {volume:.8f} BTC @ {price:,.0f}원 (수수료: {fee:.2f}원)")
                            except (ValueError, TypeError):
                                print(f"  - {order_time}: {order_type} {volume:.8f} BTC @ {price}원 (수수료: {fee:.2f}원)")
                        else:
                            print(f"  - {order_time}: {order_type} {volume:.8f} BTC @ 시장가 (수수료: {fee:.2f}원)")
                    else:
                        print(f"  - 주문 데이터 형식 오류: {order}")
                except Exception as e:
                    print(f"  - 주문 데이터 처리 실패: {e}")
        else:
            print("최근 거래 내역 없음")
    except Exception as e:
        print(f"거래 내역 조회 실패: {e}")
    
    # 시장 상황 요약
    print("\n=== 시장 상황 요약 ===")
    if current_price > 0:
        print(f"현재 비트코인 가격: {current_price:,}원")
    else:
        print("현재 비트코인 가격: 조회 실패")
    
    # 24시간 가격 변화율 계산
    try:
        if current_price > 0:
            daily_data = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=2)
            if daily_data is not None and len(daily_data) >= 2:
                yesterday_close = daily_data.iloc[-2]['close']
                if yesterday_close is not None and yesterday_close > 0:
                    price_change = current_price - yesterday_close
                    price_change_percent = (price_change / yesterday_close) * 100
                    print(f"24시간 변화: {price_change:+,.0f}원 ({price_change_percent:+.2f}%)")
                else:
                    print("24시간 변화: 계산 불가 (전일 종가 조회 실패)")
            else:
                print("24시간 변화: 계산 불가 (일봉 데이터 조회 실패)")
        else:
            print("24시간 변화: 계산 불가 (현재가 조회 실패)")
    except Exception as e:
        print(f"24시간 변화율 계산 실패: {e}")
    
    return {
        'krw_balance': krw_balance,
        'btc_balance': btc_balance,
        'current_price': current_price,
        'pending_orders': pending_orders,
        'total_assets': total_assets if btc_balance > 0 else krw_balance,
        'btc_ratio': btc_ratio if btc_balance > 0 else 0
    }

def create_market_analysis_data_with_indicators(daily_df, minute_df, current_price, orderbook):
    """
    기술적 지표가 포함된 AI 분석용 시장 데이터 생성
    """
    # 최근 기술적 지표 요약
    technical_summary = {}
    
    if not daily_df.empty:
        # 일봉 데이터의 최근 기술적 지표
        latest_daily = daily_df.iloc[-1] if len(daily_df) > 0 else None
        if latest_daily is not None:
            technical_summary['daily_indicators'] = {
                'sma_20': float(latest_daily.get('SMA_20', 0)),
                'sma_50': float(latest_daily.get('SMA_50', 0)),
                'ema_12': float(latest_daily.get('EMA_12', 0)),
                'ema_26': float(latest_daily.get('EMA_26', 0)),
                'rsi': float(latest_daily.get('RSI', 50)),
                'macd': float(latest_daily.get('MACD', 0)),
                'macd_signal': float(latest_daily.get('MACD_Signal', 0)),
                'bb_upper': float(latest_daily.get('BB_Upper', 0)),
                'bb_lower': float(latest_daily.get('BB_Lower', 0)),
                'bb_position': float(latest_daily.get('BB_Position', 0.5)),
                'stoch_k': float(latest_daily.get('Stoch_K', 50)),
                'stoch_d': float(latest_daily.get('Stoch_D', 50)),
                'williams_r': float(latest_daily.get('Williams_R', -50)),
                'atr': float(latest_daily.get('ATR', 0)),
                'adx': float(latest_daily.get('ADX', 25)),
                'cci': float(latest_daily.get('CCI', 0)),
                'roc': float(latest_daily.get('ROC', 0))
            }
    
    if not minute_df.empty:
        # 분봉 데이터의 최근 기술적 지표
        latest_minute = minute_df.iloc[-1] if len(minute_df) > 0 else None
        if latest_minute is not None:
            technical_summary['minute_indicators'] = {
                'sma_20': float(latest_minute.get('SMA_20', 0)),
                'rsi': float(latest_minute.get('RSI', 50)),
                'macd': float(latest_minute.get('MACD', 0)),
                'bb_position': float(latest_minute.get('BB_Position', 0.5)),
                'stoch_k': float(latest_minute.get('Stoch_K', 50)),
                'williams_r': float(latest_minute.get('Williams_R', -50))
            }
    
    analysis_data = {
        "current_price": current_price,
        "daily_data": daily_df.to_dict('records') if not daily_df.empty else [],
        "minute_data": minute_df.tail(100).to_dict('records') if not minute_df.empty else [],
        "technical_indicators": technical_summary,
        "orderbook": orderbook[0] if orderbook else None,
        "analysis_time": datetime.now().isoformat()
    }
    
    return analysis_data

def ai_trading_decision_with_indicators(market_data):
    """
    기술적 지표를 포함한 AI 매매 결정 함수
    """
    print("=== AI 매매 결정 분석 중 (기술적 지표 포함) ===")
    
    client = OpenAI()
    
    # 기술적 지표를 포함한 개선된 시스템 메시지
    system_message = """
    You are a Bitcoin investment expert with deep knowledge of technical analysis and market psychology.
    
    Analyze the provided market data including:
    1. 30-day daily OHLCV data with technical indicators
    2. Recent 100-minute OHLCV data with technical indicators
    3. Current price and orderbook information
    4. Technical indicators summary (RSI, MACD, Bollinger Bands, etc.)
    
    Consider these technical analysis factors:
    - Moving Averages (SMA, EMA) trends and crossovers
    - RSI overbought/oversold conditions (RSI > 70 = overbought, RSI < 30 = oversold)
    - MACD signal line crossovers and histogram patterns
    - Bollinger Bands position and width (BB_Position: 0-1, where 0.5 is middle)
    - Stochastic oscillator signals (K and D lines)
    - Williams %R overbought/oversold levels
    - ATR for volatility assessment
    - ADX for trend strength (ADX > 25 = strong trend)
    - CCI for momentum (CCI > 100 = overbought, CCI < -100 = oversold)
    - ROC for momentum confirmation
    
    Price trends and momentum patterns
    Volume patterns and OBV trends
    Support/resistance levels from Bollinger Bands
    Market volatility from ATR
    Orderbook depth and spread
    
    Provide your decision in JSON format with the following structure:
    {
        "decision": "buy|sell|hold",
        "reason": "detailed technical analysis explanation including indicator signals",
        "confidence": 0.0-1.0,
        "risk_level": "low|medium|high",
        "expected_price_range": {"min": price, "max": price},
        "key_indicators": {
            "rsi_signal": "overbought|oversold|neutral",
            "macd_signal": "bullish|bearish|neutral", 
            "bb_signal": "upper_band|lower_band|middle",
            "trend_strength": "strong|weak|neutral"
        }
    }
    
    Be conservative and consider risk management in your recommendations.
    Use technical indicators to confirm signals rather than relying on single indicators.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": f"Please analyze this Bitcoin market data with technical indicators and provide trading decision: {json.dumps(market_data, default=str)}"
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.3  # 더 보수적인 결정을 위해 낮은 temperature 사용
    )
    
    result = response.choices[0].message.content
    result_json = json.loads(result)
    
    print(f"AI 결정: {result_json['decision']}")
    print(f"신뢰도: {result_json['confidence']:.2f}")
    print(f"위험도: {result_json['risk_level']}")
    print(f"예상 가격 범위: {result_json['expected_price_range']['min']:,}원 ~ {result_json['expected_price_range']['max']:,}원")
    
    # 주요 지표 신호 출력
    if 'key_indicators' in result_json:
        indicators = result_json['key_indicators']
        print(f"RSI 신호: {indicators.get('rsi_signal', 'N/A')}")
        print(f"MACD 신호: {indicators.get('macd_signal', 'N/A')}")
        print(f"볼린저밴드 신호: {indicators.get('bb_signal', 'N/A')}")
        print(f"트렌드 강도: {indicators.get('trend_strength', 'N/A')}")
    
    print(f"분석 근거: {result_json['reason']}")
    
    return result_json

def execute_trading_decision(upbit, decision, investment_status):
    """
    AI 결정에 따른 매매 실행
    """
    print("=== 매매 실행 중 ===")
    
    krw_balance = investment_status['krw_balance']
    btc_balance = investment_status['btc_balance']
    current_price = investment_status['current_price']
    
    if decision['decision'] == 'buy':
        print("매수 신호 감지")
        
        if krw_balance * 0.9995 > 5000:  # 최소 거래금액 확인
            buy_amount = krw_balance * 0.9995  # 수수료 고려
            print(f"매수 실행: {buy_amount:,.2f}원")
            
            try:
                result = upbit.buy_market_order("KRW-BTC", buy_amount)
                print(f"매수 주문 결과: {result}")
                return True
            except Exception as e:
                print(f"매수 주문 실패: {e}")
                return False
        else:
            print("보유 현금이 부족하여 매수 건너뜀")
            return False
            
    elif decision['decision'] == 'sell':
        print("매도 신호 감지")
        
        if btc_balance * 0.9995 > 5000 / current_price:  # 최소 거래금액 확인
            sell_amount = btc_balance * 0.9995  # 수수료 고려
            print(f"매도 실행: {sell_amount:.8f} BTC")
            
            try:
                result = upbit.sell_market_order("KRW-BTC", sell_amount)
                print(f"매도 주문 결과: {result}")
                return True
            except Exception as e:
                print(f"매도 주문 실패: {e}")
                return False
        else:
            print("보유 비트코인이 부족하여 매도 건너뜀")
            return False
            
    elif decision['decision'] == 'hold':
        print("보유 신호 - 현재 포지션 유지")
        return True
    
    return False

def main_trading_cycle_with_indicators(upbit):
    """
    기술적 지표가 포함된 메인 트레이딩 사이클
    """
    print("=" * 60)
    print("비트코인 AI 자동매매 시스템 시작 (기술적 지표 포함)")
    print("=" * 60)
    
    try:
        # 시장 데이터 수집 (기술적 지표 포함)
        daily_df, minute_df, current_price, orderbook = get_market_data_with_indicators()
        
        # 투자 상태 조회
        investment_status = get_investment_status(upbit)
        
        # AI 분석용 데이터 생성 (기술적 지표 포함)
        market_data = create_market_analysis_data_with_indicators(daily_df, minute_df, current_price, orderbook)
        
        # AI 매매 결정 (기술적 지표 포함)
        decision = ai_trading_decision_with_indicators(market_data)
        
        # 매매 실행
        execution_result = execute_trading_decision(upbit, decision, investment_status)
        
        if execution_result:
            print("매매 실행 완료")
        else:
            print("매매 실행 실패 또는 건너뜀")
            
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    import time
    
    # 업비트 연결 (전역 변수로 설정)
    access = os.getenv("UPBIT_ACCESS_KEY")
    secret = os.getenv("UPBIT_SECRET_KEY")
    
    if not access or not secret:
        print("오류: UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY가 설정되지 않았습니다.")
        exit()
    
    upbit = pyupbit.Upbit(access, secret)
    
    while True:
        try:
            # 메인 트레이딩 사이클 실행 (기술적 지표 포함)
            main_trading_cycle_with_indicators(upbit)
            print("\n" + "=" * 60)
            print("5분 후 다음 분석을 시작합니다...")
            print("=" * 60 + "\n")
            time.sleep(60 * 5)  # 5분 대기
            
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"예상치 못한 오류 발생: {e}")
            print("1분 후 재시도합니다...")
            time.sleep(60)
