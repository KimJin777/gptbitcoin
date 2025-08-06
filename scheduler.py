"""
자동 반성 및 회고 스케줄러
"""

import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging

from analysis.reflection_system import (
    create_periodic_reflection, 
    analyze_learning_patterns, 
    generate_strategy_improvements
)
from database.connection import init_database
from utils.logger import get_logger

class ReflectionScheduler:
    """반성 및 회고 스케줄러"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.setup_scheduler()
    
    def setup_scheduler(self):
        """스케줄러 설정"""
        try:
            # 일일 회고 (매일 자정)
            schedule.every().day.at("00:00").do(self.daily_reflection)
            
            # 주간 회고 (매주 일요일 자정)
            schedule.every().sunday.at("00:00").do(self.weekly_reflection)
            
            # 월간 회고 (매월 1일 자정)
            schedule.every().month.at("00:00").do(self.monthly_reflection)
            
            # 학습 패턴 분석 (매일 오전 6시)
            schedule.every().day.at("06:00").do(self.learning_pattern_analysis)
            
            # 전략 개선 제안 (매주 토요일 오전 9시)
            schedule.every().saturday.at("09:00").do(self.strategy_improvement_analysis)
            
            self.logger.info("반성 스케줄러 설정 완료")
            
        except Exception as e:
            self.logger.error(f"스케줄러 설정 오류: {e}")
    
    def daily_reflection(self):
        """일일 회고 실행"""
        try:
            self.logger.info("일일 회고 시작")
            
            # 어제 날짜 계산
            yesterday = datetime.now() - timedelta(days=1)
            start_date = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            # 일일 회고 생성
            success = create_periodic_reflection('daily', start_date, end_date)
            
            if success:
                self.logger.info("일일 회고 완료")
            else:
                self.logger.warning("일일 회고 실패")
                
        except Exception as e:
            self.logger.error(f"일일 회고 오류: {e}")
    
    def weekly_reflection(self):
        """주간 회고 실행"""
        try:
            self.logger.info("주간 회고 시작")
            
            # 지난주 날짜 계산
            today = datetime.now()
            days_since_monday = today.weekday()
            last_monday = today - timedelta(days=days_since_monday + 7)
            last_sunday = last_monday + timedelta(days=6)
            
            start_date = last_monday.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = last_sunday.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            # 주간 회고 생성
            success = create_periodic_reflection('weekly', start_date, end_date)
            
            if success:
                self.logger.info("주간 회고 완료")
            else:
                self.logger.warning("주간 회고 실패")
                
        except Exception as e:
            self.logger.error(f"주간 회고 오류: {e}")
    
    def monthly_reflection(self):
        """월간 회고 실행"""
        try:
            self.logger.info("월간 회고 시작")
            
            # 지난달 날짜 계산
            today = datetime.now()
            if today.month == 1:
                last_month = today.replace(year=today.year-1, month=12)
            else:
                last_month = today.replace(month=today.month-1)
            
            start_date = last_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # 지난달 마지막 날 계산
            if today.month == 1:
                end_date = today.replace(day=1) - timedelta(days=1)
            else:
                end_date = today.replace(day=1) - timedelta(days=1)
            
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            # 월간 회고 생성
            success = create_periodic_reflection('monthly', start_date, end_date)
            
            if success:
                self.logger.info("월간 회고 완료")
            else:
                self.logger.warning("월간 회고 실패")
                
        except Exception as e:
            self.logger.error(f"월간 회고 오류: {e}")
    
    def learning_pattern_analysis(self):
        """학습 패턴 분석 실행"""
        try:
            self.logger.info("학습 패턴 분석 시작")
            
            # 학습 패턴 분석
            insights = analyze_learning_patterns()
            
            if insights:
                self.logger.info(f"학습 패턴 분석 완료: {len(insights)}개 인사이트 발견")
                for insight in insights:
                    self.logger.info(f"- {insight.get('insight_title', 'Unknown')}")
            else:
                self.logger.info("학습 패턴 분석 완료: 새로운 인사이트 없음")
                
        except Exception as e:
            self.logger.error(f"학습 패턴 분석 오류: {e}")
    
    def strategy_improvement_analysis(self):
        """전략 개선 제안 분석 실행"""
        try:
            self.logger.info("전략 개선 제안 분석 시작")
            
            # 전략 개선 제안 생성
            improvements = generate_strategy_improvements()
            
            if improvements:
                self.logger.info(f"전략 개선 제안 완료: {len(improvements)}개 개선안 생성")
                for improvement in improvements:
                    self.logger.info(f"- {improvement.get('improvement_type', 'Unknown')}: {improvement.get('reason', 'No reason')}")
            else:
                self.logger.info("전략 개선 제안 완료: 새로운 개선안 없음")
                
        except Exception as e:
            self.logger.error(f"전략 개선 제안 분석 오류: {e}")
    
    def run(self):
        """스케줄러 실행"""
        self.logger.info("반성 스케줄러 시작")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 1분마다 체크
                
        except KeyboardInterrupt:
            self.logger.info("반성 스케줄러 종료")
        except Exception as e:
            self.logger.error(f"스케줄러 실행 오류: {e}")

def run_reflection_scheduler():
    """반성 스케줄러 실행 (편의 함수)"""
    # 데이터베이스 초기화
    init_database()
    
    # 스케줄러 생성 및 실행
    scheduler = ReflectionScheduler()
    scheduler.run()

if __name__ == "__main__":
    run_reflection_scheduler()
