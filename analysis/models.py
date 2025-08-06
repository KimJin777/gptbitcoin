"""
분석 모델 정의
AI 분석 결과를 위한 데이터 모델들을 정의합니다.
"""

from pydantic import BaseModel, Field
from typing import Optional

class KeyIndicators(BaseModel):
    rsi_signal: str = Field(description="RSI 신호: overbought, oversold, neutral")
    macd_signal: str = Field(description="MACD 신호: bullish, bearish, neutral")
    bb_signal: str = Field(description="볼린저 밴드 신호: upper_band, lower_band, middle")
    trend_strength: str = Field(description="트렌드 강도: strong, weak, neutral")
    market_sentiment: str = Field(description="시장 심리: extreme_fear, fear, neutral, greed, extreme_greed")
    news_sentiment: str = Field(description="뉴스 감정: positive, negative, neutral")

class ChartAnalysis(BaseModel):
    price_action: str = Field(description="가격 액션: bullish, bearish, neutral")
    support_level: Optional[str] = Field(description="지지선 가격 레벨")
    resistance_level: Optional[str] = Field(description="저항선 가격 레벨")
    chart_pattern: Optional[str] = Field(description="차트 패턴 이름")
    volume_analysis: str = Field(description="거래량 분석: high, low, normal")

class ExpectedPriceRange(BaseModel):
    min: float = Field(description="예상 최저 가격")
    max: float = Field(description="예상 최고 가격")

class TradingDecision(BaseModel):
    decision: str = Field(description="매매 결정: buy, sell, hold")
    reason: str = Field(description="상세한 기술적 분석 설명 (차트 분석, 지표 신호, 시장 심리, 뉴스 감정 포함)")
    confidence: float = Field(description="신뢰도 (0.0-1.0)", ge=0.0, le=1.0)
    risk_level: str = Field(description="위험도: low, medium, high")
    expected_price_range: ExpectedPriceRange = Field(description="예상 가격 범위")
    key_indicators: KeyIndicators = Field(description="주요 지표 신호")
    chart_analysis: Optional[ChartAnalysis] = Field(description="차트 분석 (Vision API 사용시)")
