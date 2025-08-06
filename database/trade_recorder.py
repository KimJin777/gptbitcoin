"""
거래 기록 저장 모듈
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
from mysql.connector import Error
import logging
from .connection import get_db_connection
from utils.json_cleaner import clean_json_data

class TradeRecorder:
    """거래 기록 저장 클래스"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def save_trade(self, decision: Dict[str, Any], execution_result: Dict[str, Any], 
                   investment_status: Dict[str, Any], market_data: Dict[str, Any] = None) -> bool:
        """거래 기록을 데이터베이스에 저장"""
        try:
            connection = get_db_connection()
            if not connection:
                self.logger.error("데이터베이스 연결 실패")
                return False
            
            cursor = connection.cursor()
            
            # 거래 정보 추출
            timestamp = datetime.now()
            decision_type = decision.get('decision', 'unknown')
            action = execution_result.get('action', 'none')
            price = execution_result.get('price', 0)
            amount = execution_result.get('amount', 0)
            total_value = execution_result.get('total_value', 0)
            fee = execution_result.get('fee', 0)
            balance_krw = investment_status.get('krw_balance', 0)
            balance_btc = investment_status.get('btc_balance', 0)
            order_id = execution_result.get('order_id', '')
            status = execution_result.get('status', 'executed')
            confidence = decision.get('confidence', 0)
            reasoning = decision.get('reasoning', '')
            
            # 시장 데이터를 JSON으로 변환
            market_data_json = None
            if market_data:
                try:
                    # NaN, Infinity 값 정리 후 JSON 변환
                    cleaned_market_data = clean_json_data(market_data)
                    market_data_json = json.dumps(cleaned_market_data, ensure_ascii=False)
                except Exception as e:
                    self.logger.error(f"시장 데이터 JSON 변환 오류: {e}")
                    market_data_json = None
            
            # 거래 기록 저장
            insert_query = """
            INSERT INTO trades (
                timestamp, decision, action, price, amount, total_value, fee,
                balance_krw, balance_btc, order_id, status, confidence, reasoning, market_data
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                timestamp, decision_type, action, price, amount, total_value, fee,
                balance_krw, balance_btc, order_id, status, confidence, reasoning, market_data_json
            ))
            
            connection.commit()
            cursor.close()
            
            self.logger.info(f"거래 기록 저장 완료: {decision_type} - {action}")
            return True
            
        except Error as e:
            self.logger.error(f"거래 기록 저장 오류: {e}")
            return False
    
    def save_market_data(self, market_data: Dict[str, Any]) -> bool:
        """시장 데이터를 데이터베이스에 저장"""
        try:
            connection = get_db_connection()
            if not connection:
                self.logger.error("데이터베이스 연결 실패")
                return False
            
            cursor = connection.cursor()
            
            timestamp = datetime.now()
            current_price = market_data.get('current_price', 0)
            volume_24h = market_data.get('volume_24h', 0)
            change_24h = market_data.get('change_24h', 0)
            rsi = market_data.get('rsi', 0)
            macd = market_data.get('macd', 0)
            macd_signal = market_data.get('macd_signal', 0)
            bollinger_upper = market_data.get('bollinger_upper', 0)
            bollinger_lower = market_data.get('bollinger_lower', 0)
            fear_greed_index = market_data.get('fear_greed_index', 0)
            fear_greed_value = market_data.get('fear_greed_value', 0)
            news_sentiment = market_data.get('news_sentiment', 0)
            
            insert_query = """
            INSERT INTO market_data (
                timestamp, current_price, volume_24h, change_24h, rsi, macd, macd_signal,
                bollinger_upper, bollinger_lower, fear_greed_index, fear_greed_value, news_sentiment
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                timestamp, current_price, volume_24h, change_24h, rsi, macd, macd_signal,
                bollinger_upper, bollinger_lower, fear_greed_index, fear_greed_value, news_sentiment
            ))
            
            connection.commit()
            cursor.close()
            
            self.logger.info("시장 데이터 저장 완료")
            return True
            
        except Error as e:
            self.logger.error(f"시장 데이터 저장 오류: {e}")
            return False
    
    def save_system_log(self, level: str, message: str, module: str = None) -> bool:
        """시스템 로그를 데이터베이스에 저장"""
        try:
            connection = get_db_connection()
            if not connection:
                self.logger.error("데이터베이스 연결 실패")
                return False
            
            cursor = connection.cursor()
            
            timestamp = datetime.now()
            
            insert_query = """
            INSERT INTO system_logs (timestamp, level, message, module)
            VALUES (%s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (timestamp, level, message, module))
            
            connection.commit()
            cursor.close()
            
            return True
            
        except Error as e:
            self.logger.error(f"시스템 로그 저장 오류: {e}")
            return False
    
    def get_recent_trades(self, limit: int = 10) -> list:
        """최근 거래 기록 조회"""
        try:
            connection = get_db_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            select_query = """
            SELECT * FROM trades 
            ORDER BY timestamp DESC 
            LIMIT %s
            """
            
            cursor.execute(select_query, (limit,))
            trades = cursor.fetchall()
            
            cursor.close()
            return trades
            
        except Error as e:
            self.logger.error(f"거래 기록 조회 오류: {e}")
            return []
    
    def get_trade_statistics(self) -> Dict[str, Any]:
        """거래 통계 조회"""
        try:
            connection = get_db_connection()
            if not connection:
                return {}
            
            cursor = connection.cursor(dictionary=True)
            
            # 전체 거래 수
            cursor.execute("SELECT COUNT(*) as total_trades FROM trades")
            total_trades = cursor.fetchone()['total_trades']
            
            # 매수/매도/보유 거래 수
            cursor.execute("""
                SELECT decision, COUNT(*) as count 
                FROM trades 
                GROUP BY decision
            """)
            decision_counts = {row['decision']: row['count'] for row in cursor.fetchall()}
            
            # 총 거래 금액
            cursor.execute("SELECT SUM(total_value) as total_value FROM trades")
            total_value = cursor.fetchone()['total_value'] or 0
            
            # 총 수수료
            cursor.execute("SELECT SUM(fee) as total_fee FROM trades")
            total_fee = cursor.fetchone()['total_fee'] or 0
            
            cursor.close()
            
            return {
                'total_trades': total_trades,
                'decision_counts': decision_counts,
                'total_value': total_value,
                'total_fee': total_fee
            }
            
        except Error as e:
            self.logger.error(f"거래 통계 조회 오류: {e}")
            return {}

# 전역 거래 기록기 객체
trade_recorder = TradeRecorder()

def save_trade_record(decision: Dict[str, Any], execution_result: Dict[str, Any], 
                     investment_status: Dict[str, Any], market_data: Dict[str, Any] = None) -> bool:
    """거래 기록 저장 (편의 함수)"""
    return trade_recorder.save_trade(decision, execution_result, investment_status, market_data)

def save_market_data_record(market_data: Dict[str, Any]) -> bool:
    """시장 데이터 저장 (편의 함수)"""
    return trade_recorder.save_market_data(market_data)

def save_system_log_record(level: str, message: str, module: str = None) -> bool:
    """시스템 로그 저장 (편의 함수)"""
    return trade_recorder.save_system_log(level, message, module)
