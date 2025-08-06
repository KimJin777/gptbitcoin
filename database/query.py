"""
데이터베이스 조회 모듈
거래 기록 및 통계를 조회하는 기능을 제공합니다.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from mysql.connector import Error
import logging
from .connection import get_db_connection

class TradeQuery:
    """거래 기록 조회 클래스"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_recent_trades(self, limit: int = 10) -> List[Dict[str, Any]]:
        """최근 거래 기록 조회"""
        try:
            connection = get_db_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                id, timestamp, decision, action, price, amount, total_value, fee,
                balance_krw, balance_btc, order_id, status, confidence, reasoning
            FROM trades 
            ORDER BY timestamp DESC 
            LIMIT %s
            """
            
            cursor.execute(query, (limit,))
            trades = cursor.fetchall()
            
            cursor.close()
            return trades
            
        except Error as e:
            self.logger.error(f"거래 기록 조회 오류: {e}")
            return []
    
    def get_trades_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """날짜 범위로 거래 기록 조회"""
        try:
            connection = get_db_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                id, timestamp, decision, action, price, amount, total_value, fee,
                balance_krw, balance_btc, order_id, status, confidence, reasoning
            FROM trades 
            WHERE timestamp BETWEEN %s AND %s
            ORDER BY timestamp DESC
            """
            
            cursor.execute(query, (start_date, end_date))
            trades = cursor.fetchall()
            
            cursor.close()
            return trades
            
        except Error as e:
            self.logger.error(f"날짜 범위 거래 기록 조회 오류: {e}")
            return []
    
    def get_trade_statistics(self, days: int = 30) -> Dict[str, Any]:
        """거래 통계 조회"""
        try:
            connection = get_db_connection()
            if not connection:
                return {}
            
            cursor = connection.cursor(dictionary=True)
            
            # 지정된 기간의 거래만 조회
            start_date = datetime.now() - timedelta(days=days)
            
            # 전체 거래 수
            cursor.execute("""
                SELECT COUNT(*) as total_trades 
                FROM trades 
                WHERE timestamp >= %s
            """, (start_date,))
            total_trades = cursor.fetchone()['total_trades']
            
            # 매수/매도/보유 거래 수
            cursor.execute("""
                SELECT decision, COUNT(*) as count 
                FROM trades 
                WHERE timestamp >= %s
                GROUP BY decision
            """, (start_date,))
            decision_counts = {row['decision']: row['count'] for row in cursor.fetchall()}
            
            # 총 거래 금액
            cursor.execute("""
                SELECT SUM(total_value) as total_value 
                FROM trades 
                WHERE timestamp >= %s AND action IN ('buy', 'sell')
            """, (start_date,))
            total_value = cursor.fetchone()['total_value'] or 0
            
            # 총 수수료
            cursor.execute("""
                SELECT SUM(fee) as total_fee 
                FROM trades 
                WHERE timestamp >= %s
            """, (start_date,))
            total_fee = cursor.fetchone()['total_fee'] or 0
            
            # 수익률 계산 (간단한 계산)
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN action = 'buy' THEN -total_value ELSE 0 END) as buy_total,
                    SUM(CASE WHEN action = 'sell' THEN total_value ELSE 0 END) as sell_total
                FROM trades 
                WHERE timestamp >= %s AND action IN ('buy', 'sell')
            """, (start_date,))
            result = cursor.fetchone()
            buy_total = result['buy_total'] or 0
            sell_total = result['sell_total'] or 0
            
            profit = sell_total - buy_total - total_fee
            profit_rate = (profit / buy_total * 100) if buy_total > 0 else 0
            
            cursor.close()
            
            return {
                'period_days': days,
                'total_trades': total_trades,
                'decision_counts': decision_counts,
                'total_value': total_value,
                'total_fee': total_fee,
                'buy_total': buy_total,
                'sell_total': sell_total,
                'profit': profit,
                'profit_rate': profit_rate
            }
            
        except Error as e:
            self.logger.error(f"거래 통계 조회 오류: {e}")
            return {}
    
    def get_market_data_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """시장 데이터 히스토리 조회"""
        try:
            connection = get_db_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                id, timestamp, current_price, volume_24h, change_24h,
                rsi, macd, macd_signal, bollinger_upper, bollinger_lower,
                fear_greed_index, fear_greed_value, news_sentiment
            FROM market_data 
            ORDER BY timestamp DESC 
            LIMIT %s
            """
            
            cursor.execute(query, (limit,))
            market_data = cursor.fetchall()
            
            cursor.close()
            return market_data
            
        except Error as e:
            self.logger.error(f"시장 데이터 조회 오류: {e}")
            return []
    
    def get_system_logs(self, level: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """시스템 로그 조회"""
        try:
            connection = get_db_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            if level:
                query = """
                SELECT id, timestamp, level, message, module
                FROM system_logs 
                WHERE level = %s
                ORDER BY timestamp DESC 
                LIMIT %s
                """
                cursor.execute(query, (level, limit))
            else:
                query = """
                SELECT id, timestamp, level, message, module
                FROM system_logs 
                ORDER BY timestamp DESC 
                LIMIT %s
                """
                cursor.execute(query, (limit,))
            
            logs = cursor.fetchall()
            cursor.close()
            return logs
            
        except Error as e:
            self.logger.error(f"시스템 로그 조회 오류: {e}")
            return []

# 전역 조회 객체
trade_query = TradeQuery()

def get_recent_trades(limit: int = 10) -> List[Dict[str, Any]]:
    """최근 거래 기록 조회 (편의 함수)"""
    return trade_query.get_recent_trades(limit)

def get_trade_statistics(days: int = 30) -> Dict[str, Any]:
    """거래 통계 조회 (편의 함수)"""
    return trade_query.get_trade_statistics(days)

def get_market_data_history(limit: int = 100) -> List[Dict[str, Any]]:
    """시장 데이터 히스토리 조회 (편의 함수)"""
    return trade_query.get_market_data_history(limit)

def get_system_logs(level: str = None, limit: int = 50) -> List[Dict[str, Any]]:
    """시스템 로그 조회 (편의 함수)"""
    return trade_query.get_system_logs(level, limit)
