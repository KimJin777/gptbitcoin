"""
MySQL 데이터베이스 연결 모듈
"""

import mysql.connector
from mysql.connector import Error
from typing import Optional
import logging

class DatabaseConnection:
    """MySQL 데이터베이스 연결 클래스"""
    
    def __init__(self, host=None, port=None, database=None, user=None, password=None):
        from config.settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
        
        self.host = host or DB_HOST
        self.port = port or DB_PORT
        self.database = database or DB_NAME
        self.user = user or DB_USER
        self.password = password or DB_PASSWORD
        self.connection = None
        self.logger = logging.getLogger(__name__)
    
    def connect(self) -> bool:
        """데이터베이스 연결"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                charset='utf8mb4',
                autocommit=True
            )
            
            if self.connection.is_connected():
                self.logger.info("MySQL 데이터베이스 연결 성공")
                return True
            else:
                self.logger.error("MySQL 데이터베이스 연결 실패")
                return False
                
        except Error as e:
            self.logger.error(f"MySQL 연결 오류: {e}")
            return False
    
    def disconnect(self):
        """데이터베이스 연결 해제"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("MySQL 데이터베이스 연결 해제")
    
    def create_tables(self):
        """거래 기록 테이블 생성"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            
            # 거래 기록 테이블
            create_trades_table = """
            CREATE TABLE IF NOT EXISTS trades (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME NOT NULL,
                decision VARCHAR(10) NOT NULL,
                action VARCHAR(10) NOT NULL,
                price DECIMAL(20, 8) NOT NULL,
                amount DECIMAL(20, 8) NOT NULL,
                total_value DECIMAL(20, 2) NOT NULL,
                fee DECIMAL(20, 2) DEFAULT 0,
                balance_krw DECIMAL(20, 2) NOT NULL,
                balance_btc DECIMAL(20, 8) NOT NULL,
                order_id VARCHAR(100),
                status VARCHAR(20) DEFAULT 'executed',
                confidence DECIMAL(5, 4),
                reasoning TEXT,
                market_data JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            
            # 시장 데이터 테이블
            create_market_data_table = """
            CREATE TABLE IF NOT EXISTS market_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME NOT NULL,
                current_price DECIMAL(20, 2) NOT NULL,
                volume_24h DECIMAL(20, 2),
                change_24h DECIMAL(10, 4),
                rsi DECIMAL(10, 4),
                macd DECIMAL(10, 4),
                macd_signal DECIMAL(10, 4),
                bollinger_upper DECIMAL(20, 2),
                bollinger_lower DECIMAL(20, 2),
                fear_greed_index INT,
                fear_greed_value DECIMAL(10, 4),
                news_sentiment DECIMAL(5, 4),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            
            # 시스템 로그 테이블
            create_system_logs_table = """
            CREATE TABLE IF NOT EXISTS system_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME NOT NULL,
                level VARCHAR(10) NOT NULL,
                message TEXT NOT NULL,
                module VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            
            cursor.execute(create_trades_table)
            cursor.execute(create_market_data_table)
            cursor.execute(create_system_logs_table)
            
            self.connection.commit()
            cursor.close()
            
            self.logger.info("데이터베이스 테이블 생성 완료")
            return True
            
        except Error as e:
            self.logger.error(f"테이블 생성 오류: {e}")
            return False
    
    def get_connection(self):
        """데이터베이스 연결 객체 반환"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection

# 전역 데이터베이스 연결 객체
db_connection = DatabaseConnection()

def get_db_connection():
    """데이터베이스 연결 객체 반환"""
    return db_connection.get_connection()

def init_database():
    """데이터베이스 초기화"""
    return db_connection.create_tables()
