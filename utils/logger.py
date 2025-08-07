"""
로깅 유틸리티
"""

import logging
from datetime import datetime
from typing import Optional

def get_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    로거 인스턴스를 반환합니다.
    
    Args:
        name: 로거 이름
        level: 로그 레벨
        
    Returns:
        로거 인스턴스
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(level)
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # 포맷터
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger

def log_trade_execution(logger: logging.Logger, decision: dict, execution_result: dict) -> None:
    """
    거래 실행 로그를 기록합니다.
    
    Args:
        logger: 로거 인스턴스
        decision: 매매 결정
        execution_result: 실행 결과
    """
    logger.info(f"거래 실행: {decision.get('decision', 'unknown')} - {execution_result.get('action', 'none')}")

def log_reflection_creation(logger: logging.Logger, reflection_type: str, trade_id: int) -> None:
    """
    반성 생성 로그를 기록합니다.
    
    Args:
        logger: 로거 인스턴스
        reflection_type: 반성 타입
        trade_id: 거래 ID
    """
    logger.info(f"반성 생성: {reflection_type} - 거래 ID: {trade_id}")

def log_performance_analysis(logger: logging.Logger, period_type: str, metrics: dict) -> None:
    """
    성과 분석 로그를 기록합니다.
    
    Args:
        logger: 로거 인스턴스
        period_type: 기간 타입
        metrics: 성과 지표
    """
    logger.info(f"성과 분석: {period_type} - 승률: {metrics.get('win_rate', 0):.2%}")

def setup_logger(name: str = "gptbitcoin") -> logging.Logger:
    """
    로거를 설정하고 반환합니다.
    
    Args:
        name: 로거 이름
        
    Returns:
        로거 인스턴스
    """
    return get_logger(name)

def log_trading_decision(logger: logging.Logger, decision: dict, market_data: dict) -> None:
    """
    매매 결정 로그를 기록합니다.
    
    Args:
        logger: 로거 인스턴스
        decision: 매매 결정
        market_data: 시장 데이터
    """
    logger.info(f"매매 결정: {decision.get('decision', 'unknown')} - 이유: {decision.get('reasoning', 'none')}")

def log_execution_result(logger: logging.Logger, decision: dict, execution_result: dict) -> None:
    """
    실행 결과 로그를 기록합니다.
    
    Args:
        logger: 로거 인스턴스
        decision: 매매 결정
        execution_result: 실행 결과
    """
    logger.info(f"실행 결과: {execution_result.get('action', 'none')} - 성공: {execution_result.get('success', False)}")
