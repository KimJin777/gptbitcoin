"""
로깅 유틸리티 모듈
로그 기록 및 출력을 관리합니다.
"""

import logging
from datetime import datetime
import os

def setup_logger(name: str = "gptbitcoin", level: int = logging.INFO) -> logging.Logger:
    """로거 설정"""
    # 로그 디렉토리 생성
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 이미 핸들러가 설정되어 있으면 추가하지 않음
    if logger.handlers:
        return logger
    
    # 파일 핸들러 설정
    timestamp = datetime.now().strftime("%Y%m%d")
    file_handler = logging.FileHandler(f"logs/{name}_{timestamp}.log", encoding='utf-8')
    file_handler.setLevel(level)
    
    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # 포맷터 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 핸들러 추가
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_trading_decision(logger: logging.Logger, decision: dict, market_data: dict):
    """매매 결정 로깅"""
    logger.info("=" * 60)
    logger.info("AI 매매 결정 결과")
    logger.info("=" * 60)
    logger.info(f"결정: {decision.get('decision', 'unknown')}")
    logger.info(f"신뢰도: {decision.get('confidence', 0)}")
    logger.info(f"위험도: {decision.get('risk_level', 'unknown')}")
    logger.info(f"이유: {decision.get('reason', 'No reason provided')}")
    
    # 예상 가격 범위
    if 'expected_price_range' in decision:
        price_range = decision['expected_price_range']
        logger.info(f"예상 가격 범위: {price_range.get('min', 0):,.0f}원 ~ {price_range.get('max', 0):,.0f}원")
    
    # 주요 지표
    if 'key_indicators' in decision:
        indicators = decision['key_indicators']
        logger.info("주요 지표:")
        logger.info(f"  - RSI: {indicators.get('rsi_signal', 'unknown')}")
        logger.info(f"  - MACD: {indicators.get('macd_signal', 'unknown')}")
        logger.info(f"  - 볼린저밴드: {indicators.get('bb_signal', 'unknown')}")
        logger.info(f"  - 트렌드 강도: {indicators.get('trend_strength', 'unknown')}")
        logger.info(f"  - 시장 심리: {indicators.get('market_sentiment', 'unknown')}")
        logger.info(f"  - 뉴스 감정: {indicators.get('news_sentiment', 'unknown')}")
    
    # 시장 데이터 요약
    current_price = market_data.get('current_price', 0)
    logger.info(f"현재 가격: {current_price:,.0f}원")
    
    # 공포탐욕지수
    if 'fear_greed_index' in market_data and market_data['fear_greed_index']:
        fgi = market_data['fear_greed_index']
        logger.info(f"공포탐욕지수: {fgi.get('current_value', 0)} ({fgi.get('current_classification', 'unknown')})")
    
    # 뉴스 분석
    if 'news_analysis' in market_data and market_data['news_analysis']:
        news = market_data['news_analysis']
        logger.info(f"뉴스 분석: 긍정 {news.get('positive_count', 0)}개, 부정 {news.get('negative_count', 0)}개, 중립 {news.get('neutral_count', 0)}개")
    
    logger.info("=" * 60)

def log_execution_result(logger: logging.Logger, decision: dict, success: bool, error: str = None):
    """매매 실행 결과 로깅"""
    logger.info("=" * 40)
    logger.info("매매 실행 결과")
    logger.info("=" * 40)
    logger.info(f"결정: {decision.get('decision', 'unknown')}")
    logger.info(f"성공 여부: {'성공' if success else '실패'}")
    
    if error:
        logger.error(f"오류: {error}")
    
    logger.info("=" * 40)
