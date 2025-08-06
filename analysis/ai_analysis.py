"""
AI 분석 모듈
OpenAI API를 사용하여 매매 결정을 수행합니다.
"""

import json
from datetime import datetime
from typing import Optional, Dict, Any
from openai import OpenAI
from .models import TradingDecision
from config.settings import OPENAI_API_KEY

def create_market_analysis_data(daily_df, minute_df, current_price, orderbook, fear_greed_data, analyzed_news):
    """AI 분석용 시장 데이터 생성"""
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
    
    # 뉴스 감정 분석 요약
    news_summary = None
    if analyzed_news:
        sentiment_scores = [news['sentiment_score'] for news in analyzed_news]
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        positive_news = [news for news in analyzed_news if news['sentiment'] == '긍정']
        negative_news = [news for news in analyzed_news if news['sentiment'] == '부정']
        
        news_summary = {
            'total_news': len(analyzed_news),
            'average_sentiment': avg_sentiment,
            'positive_count': len(positive_news),
            'negative_count': len(negative_news),
            'neutral_count': len(analyzed_news) - len(positive_news) - len(negative_news),
            'recent_news': analyzed_news[:5]  # 최근 5개 뉴스만
        }
    
    analysis_data = {
        "current_price": current_price,
        "daily_data": daily_df.to_dict('records') if not daily_df.empty else [],
        "minute_data": minute_df.tail(100).to_dict('records') if not minute_df.empty else [],
        "technical_indicators": technical_summary,
        "fear_greed_index": fear_greed_data,
        "news_analysis": news_summary,
        "orderbook": orderbook if orderbook and isinstance(orderbook, dict) else None,
        "analysis_time": datetime.now().isoformat()
    }
    
    return analysis_data

def ai_trading_decision_with_indicators(market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """기술적 지표를 포함한 AI 매매 결정 함수"""
    print("=== AI 매매 결정 분석 중 (기술적 지표 포함) ===")
    
    client = OpenAI()
    
    # 기술적 지표, 공포탐욕지수, 뉴스를 포함한 개선된 시스템 메시지
    system_message = """
    You are a Bitcoin investment expert with deep knowledge of technical analysis, market psychology, and news sentiment analysis.
    
    Analyze the provided market data including:
    1. 30-day daily OHLCV data with technical indicators
    2. Recent 100-minute OHLCV data with technical indicators
    3. Current price and orderbook information
    4. Technical indicators summary (RSI, MACD, Bollinger Bands, etc.)
    5. Fear and Greed Index data (market sentiment indicator)
    6. Recent news sentiment analysis (positive/negative/neutral news distribution)
    
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
    
    Fear and Greed Index Analysis:
    - Extreme Fear (0-25): Often indicates oversold conditions, potential buying opportunities
    - Fear (26-45): Market uncertainty, cautious approach recommended
    - Neutral (46-55): Balanced market sentiment
    - Greed (56-75): Market optimism, watch for overbought conditions
    - Extreme Greed (76-100): Often indicates overbought conditions, potential selling opportunities
    
    News Sentiment Analysis:
    - Positive news sentiment: May indicate bullish momentum or positive market sentiment
    - Negative news sentiment: May indicate bearish pressure or negative market sentiment
    - Neutral news sentiment: Balanced market sentiment
    - Consider news sentiment in combination with technical indicators for confirmation
    
    Price trends and momentum patterns
    Volume patterns and OBV trends
    Support/resistance levels from Bollinger Bands
    Market volatility from ATR
    Orderbook depth and spread
    Market sentiment from Fear and Greed Index
    News sentiment impact on market psychology
    
    Be conservative and consider risk management in your recommendations.
    Use technical indicators to confirm signals rather than relying on single indicators.
    Consider market sentiment from Fear and Greed Index for contrarian opportunities.
    Consider news sentiment for additional market psychology insights.
    
    Provide your analysis in JSON format using the structured output function.
    """
    
    try:
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
            temperature=0.3,  # 더 보수적인 결정을 위해 낮은 temperature 사용
            tools=[{
                "type": "function",
                "function": {
                    "name": "get_trading_decision",
                    "description": "비트코인 매매 결정을 위한 구조화된 출력",
                    "parameters": TradingDecision.model_json_schema()
                }
            }],
            tool_choice={"type": "function", "function": {"name": "get_trading_decision"}}
        )
        
        # Structured output 파싱
        tool_calls = response.choices[0].message.tool_calls
        if tool_calls and len(tool_calls) > 0:
            arguments = json.loads(tool_calls[0].function.arguments)
            decision = TradingDecision(**arguments)
            
            # 결과 출력
            print(f"📈 AI 결정: {decision.decision}")
            print(f"🎯 신뢰도: {decision.confidence}")
            print(f"⚠️ 위험도: {decision.risk_level}")
            print(f"💰 예상 가격 범위: {decision.expected_price_range.min:,.0f}원 ~ {decision.expected_price_range.max:,.0f}원")
            print(f"📊 주요 지표:")
            print(f"   - RSI 신호: {decision.key_indicators.rsi_signal}")
            print(f"   - MACD 신호: {decision.key_indicators.macd_signal}")
            print(f"   - 볼린저밴드 신호: {decision.key_indicators.bb_signal}")
            print(f"   - 트렌드 강도: {decision.key_indicators.trend_strength}")
            print(f"   - 시장 심리: {decision.key_indicators.market_sentiment}")
            print(f"   - 뉴스 감정: {decision.key_indicators.news_sentiment}")
            print(f"📝 분석 이유: {decision.reason}")
            
            return decision.model_dump()
        else:
            print("❌ Structured output 파싱 실패")
            return None
            
    except Exception as e:
        print(f"❌ AI 분석 중 오류 발생: {e}")
        return None

def ai_trading_decision_with_vision(market_data: Dict[str, Any], chart_image_base64: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Vision API를 사용한 AI 매매 결정 함수"""
    print("=== AI 매매 결정 분석 중 (Vision API 포함) ===")
    
    client = OpenAI()
    
    # Vision API를 위한 시스템 메시지
    system_message = """
    You are a Bitcoin investment expert with deep knowledge of technical analysis, market psychology, and news sentiment analysis.
    
    You will analyze:
    1. Market data including technical indicators, Fear and Greed Index, and news sentiment
    2. A chart screenshot showing the current Bitcoin price chart with technical indicators (1-hour timeframe with Bollinger Bands)
    
    When analyzing the chart image, focus on:
    - Price action patterns and trends
    - Technical indicator positions (Bollinger Bands, moving averages, etc.)
    - Support and resistance levels
    - Volume patterns
    - Chart patterns (head and shoulders, triangles, etc.)
    - Candlestick patterns
    - Overall market structure and momentum
    
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
    
    Fear and Greed Index Analysis:
    - Extreme Fear (0-25): Often indicates oversold conditions, potential buying opportunities
    - Fear (26-45): Market uncertainty, cautious approach recommended
    - Neutral (46-55): Balanced market sentiment
    - Greed (56-75): Market optimism, watch for overbought conditions
    - Extreme Greed (76-100): Often indicates overbought conditions, potential selling opportunities
    
    News Sentiment Analysis:
    - Positive news sentiment: May indicate bullish momentum or positive market sentiment
    - Negative news sentiment: May indicate bearish pressure or negative market sentiment
    - Neutral news sentiment: Balanced market sentiment
    - Consider news sentiment in combination with technical indicators for confirmation
    
    Be conservative and consider risk management in your recommendations.
    Use technical indicators to confirm signals rather than relying on single indicators.
    Consider market sentiment from Fear and Greed Index for contrarian opportunities.
    Consider news sentiment for additional market psychology insights.
    
    Provide your analysis in JSON format using the structured output function.
    """
    
    try:
        # 메시지 구성
        messages = [
            {
                "role": "system",
                "content": system_message
            }
        ]
        
        # 차트 이미지가 있는 경우 Vision API 사용
        if chart_image_base64:
            user_content = [
                {
                    "type": "text",
                    "text": f"Please analyze this Bitcoin market data with technical indicators and the provided chart image to provide trading decision: {json.dumps(market_data, default=str)}"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{chart_image_base64}"
                    }
                }
            ]
        else:
            # 이미지가 없는 경우 기존 방식 사용
            user_content = f"Please analyze this Bitcoin market data with technical indicators and provide trading decision: {json.dumps(market_data, default=str)}"
        
        messages.append({"role": "user", "content": user_content})
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.3,
            tools=[{
                "type": "function",
                "function": {
                    "name": "get_trading_decision_with_vision",
                    "description": "비트코인 매매 결정을 위한 구조화된 출력 (Vision API 포함)",
                    "parameters": TradingDecision.model_json_schema()
                }
            }],
            tool_choice={"type": "function", "function": {"name": "get_trading_decision_with_vision"}}
        )
        
        # Structured output 파싱
        tool_calls = response.choices[0].message.tool_calls
        if tool_calls and len(tool_calls) > 0:
            arguments = json.loads(tool_calls[0].function.arguments)
            decision = TradingDecision(**arguments)
            
            # 결과 출력
            print(f"📈 AI 결정: {decision.decision}")
            print(f"🎯 신뢰도: {decision.confidence}")
            print(f"⚠️ 위험도: {decision.risk_level}")
            print(f"💰 예상 가격 범위: {decision.expected_price_range.min:,.0f}원 ~ {decision.expected_price_range.max:,.0f}원")
            print(f"📊 주요 지표:")
            print(f"   - RSI 신호: {decision.key_indicators.rsi_signal}")
            print(f"   - MACD 신호: {decision.key_indicators.macd_signal}")
            print(f"   - 볼린저밴드 신호: {decision.key_indicators.bb_signal}")
            print(f"   - 트렌드 강도: {decision.key_indicators.trend_strength}")
            print(f"   - 시장 심리: {decision.key_indicators.market_sentiment}")
            print(f"   - 뉴스 감정: {decision.key_indicators.news_sentiment}")
            
            if decision.chart_analysis:
                print(f"📊 차트 분석:")
                print(f"   - 가격 액션: {decision.chart_analysis.price_action}")
                print(f"   - 지지선: {decision.chart_analysis.support_level}")
                print(f"   - 저항선: {decision.chart_analysis.resistance_level}")
                print(f"   - 차트 패턴: {decision.chart_analysis.chart_pattern}")
                print(f"   - 거래량 분석: {decision.chart_analysis.volume_analysis}")
            
            print(f"📝 분석 이유: {decision.reason}")
            
            return decision.model_dump()
        else:
            print("❌ Structured output 파싱 실패")
            return None
            
    except Exception as e:
        print(f"❌ AI 분석 중 오류 발생: {e}")
        return None
