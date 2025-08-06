"""
거래 반성 및 회고 시스템
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from mysql.connector import Error
import numpy as np
from database.connection import get_db_connection
from analysis.ai_analysis import analyze_market_sentiment
from utils.logger import get_logger

@dataclass
class TradeReflection:
    """거래 반성 데이터 클래스"""
    trade_id: int
    reflection_type: str  # immediate, daily, weekly, monthly
    performance_score: float
    profit_loss: float
    profit_loss_percentage: float
    market_conditions: Dict[str, Any]
    decision_quality_score: float
    timing_score: float
    risk_management_score: float
    ai_analysis: str
    improvement_suggestions: str
    lessons_learned: str
    next_actions: str

@dataclass
class PerformanceMetrics:
    """성과 지표 데이터 클래스"""
    period_type: str
    period_start: datetime
    period_end: datetime
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_profit_loss: float
    total_profit_loss_percentage: float
    max_drawdown: float
    sharpe_ratio: float
    average_trade_duration: int
    best_trade_profit: float
    worst_trade_loss: float
    market_condition_performance: Dict[str, Any]
    strategy_performance: Dict[str, Any]

class TradingReflectionSystem:
    """거래 반성 및 회고 시스템"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.connection = get_db_connection()
    
    def create_immediate_reflection(self, trade_id: int, trade_data: Dict[str, Any], 
                                  market_data: Dict[str, Any]) -> bool:
        """거래 직후 즉시 반성 생성"""
        try:
            # 거래 성과 계산
            performance_score = self._calculate_performance_score(trade_data)
            profit_loss = self._calculate_profit_loss(trade_data)
            profit_loss_percentage = self._calculate_profit_loss_percentage(trade_data)
            
            # 각종 점수 계산
            decision_quality_score = self._calculate_decision_quality_score(trade_data, market_data)
            timing_score = self._calculate_timing_score(trade_data, market_data)
            risk_management_score = self._calculate_risk_management_score(trade_data)
            
            # AI 분석 수행
            ai_analysis = self._perform_ai_analysis(trade_data, market_data)
            improvement_suggestions = self._generate_improvement_suggestions(trade_data, market_data)
            lessons_learned = self._extract_lessons_learned(trade_data, market_data)
            next_actions = self._suggest_next_actions(trade_data, market_data)
            
            # 반성 데이터 저장
            reflection = TradeReflection(
                trade_id=trade_id,
                reflection_type='immediate',
                performance_score=performance_score,
                profit_loss=profit_loss,
                profit_loss_percentage=profit_loss_percentage,
                market_conditions=market_data,
                decision_quality_score=decision_quality_score,
                timing_score=timing_score,
                risk_management_score=risk_management_score,
                ai_analysis=ai_analysis,
                improvement_suggestions=improvement_suggestions,
                lessons_learned=lessons_learned,
                next_actions=next_actions
            )
            
            return self._save_reflection(reflection)
            
        except Exception as e:
            self.logger.error(f"즉시 반성 생성 오류: {e}")
            return False
    
    def create_periodic_reflection(self, reflection_type: str, 
                                 period_start: datetime, period_end: datetime) -> bool:
        """주기적 회고 생성 (일/주/월)"""
        try:
            # 해당 기간의 거래 데이터 조회
            trades = self._get_trades_in_period(period_start, period_end)
            
            if not trades:
                self.logger.info(f"{reflection_type} 회고: 해당 기간에 거래가 없습니다.")
                return True
            
            # 성과 지표 계산
            metrics = self._calculate_period_metrics(trades, period_start, period_end)
            
            # AI 기반 종합 분석
            ai_analysis = self._perform_period_ai_analysis(trades, metrics)
            improvement_suggestions = self._generate_period_improvements(trades, metrics)
            lessons_learned = self._extract_period_lessons(trades, metrics)
            next_actions = self._suggest_period_actions(trades, metrics)
            
            # 각 거래에 대한 반성 생성
            for trade in trades:
                reflection = TradeReflection(
                    trade_id=trade['id'],
                    reflection_type=reflection_type,
                    performance_score=metrics.win_rate,
                    profit_loss=metrics.total_profit_loss,
                    profit_loss_percentage=metrics.total_profit_loss_percentage,
                    market_conditions={},  # 기간별 시장 상황
                    decision_quality_score=metrics.win_rate,
                    timing_score=0.5,  # 기본값
                    risk_management_score=1.0 - abs(metrics.max_drawdown),
                    ai_analysis=ai_analysis,
                    improvement_suggestions=improvement_suggestions,
                    lessons_learned=lessons_learned,
                    next_actions=next_actions
                )
                
                self._save_reflection(reflection)
            
            # 성과 지표 저장
            self._save_performance_metrics(metrics)
            
            self.logger.info(f"{reflection_type} 회고 완료: {len(trades)}개 거래 분석")
            return True
            
        except Exception as e:
            self.logger.error(f"주기적 회고 생성 오류: {e}")
            return False
    
    def analyze_learning_patterns(self) -> List[Dict[str, Any]]:
        """학습 패턴 분석 및 인사이트 생성"""
        try:
            # 최근 30일간의 거래 데이터 조회
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            trades = self._get_trades_in_period(start_date, end_date)
            
            insights = []
            
            # 성공 패턴 분석
            success_patterns = self._analyze_success_patterns(trades)
            insights.extend(success_patterns)
            
            # 실패 패턴 분석
            failure_patterns = self._analyze_failure_patterns(trades)
            insights.extend(failure_patterns)
            
            # 시장 상황별 성과 분석
            market_insights = self._analyze_market_condition_performance(trades)
            insights.extend(market_insights)
            
            # 타이밍 분석
            timing_insights = self._analyze_timing_patterns(trades)
            insights.extend(timing_insights)
            
            # 인사이트 저장
            for insight in insights:
                self._save_learning_insight(insight)
            
            return insights
            
        except Exception as e:
            self.logger.error(f"학습 패턴 분석 오류: {e}")
            return []
    
    def generate_strategy_improvements(self) -> List[Dict[str, Any]]:
        """전략 개선 제안 생성"""
        try:
            improvements = []
            
            # 성과 분석을 통한 개선점 도출
            performance_analysis = self._analyze_performance_for_improvements()
            improvements.extend(performance_analysis)
            
            # AI 분석을 통한 개선 제안
            ai_improvements = self._generate_ai_improvements()
            improvements.extend(ai_improvements)
            
            # 리스크 관리 개선 제안
            risk_improvements = self._generate_risk_improvements()
            improvements.extend(risk_improvements)
            
            # 개선 제안 저장
            for improvement in improvements:
                self._save_strategy_improvement(improvement)
            
            return improvements
            
        except Exception as e:
            self.logger.error(f"전략 개선 생성 오류: {e}")
            return []
    
    def _calculate_performance_score(self, trade_data: Dict[str, Any]) -> float:
        """거래 성과 점수 계산"""
        try:
            # 기본 점수 (0-1)
            base_score = 0.5
            
            # 수익률에 따른 가중치
            profit_loss = self._calculate_profit_loss(trade_data)
            if profit_loss > 0:
                base_score += 0.3
            elif profit_loss < 0:
                base_score -= 0.2
            
            # 신뢰도에 따른 가중치
            confidence = trade_data.get('confidence', 0.5)
            base_score += (confidence - 0.5) * 0.2
            
            return max(0.0, min(1.0, base_score))
            
        except Exception as e:
            self.logger.error(f"성과 점수 계산 오류: {e}")
            return 0.5
    
    def _calculate_profit_loss(self, trade_data: Dict[str, Any]) -> float:
        """손익 계산"""
        try:
            # 간단한 손익 계산 (실제로는 더 복잡한 로직 필요)
            return 0.0  # 임시 반환값
        except Exception as e:
            self.logger.error(f"손익 계산 오류: {e}")
            return 0.0
    
    def _calculate_profit_loss_percentage(self, trade_data: Dict[str, Any]) -> float:
        """손익률 계산"""
        try:
            return 0.0  # 임시 반환값
        except Exception as e:
            self.logger.error(f"손익률 계산 오류: {e}")
            return 0.0
    
    def _calculate_decision_quality_score(self, trade_data: Dict[str, Any], 
                                       market_data: Dict[str, Any]) -> float:
        """의사결정 품질 점수 계산"""
        try:
            # 시장 상황과 거래 결정의 일치도 분석
            decision = trade_data.get('decision', '')
            market_trend = market_data.get('trend', 'neutral')
            
            # 간단한 로직 (실제로는 더 복잡한 분석 필요)
            if decision == 'buy' and market_trend == 'bullish':
                return 0.8
            elif decision == 'sell' and market_trend == 'bearish':
                return 0.8
            else:
                return 0.5
                
        except Exception as e:
            self.logger.error(f"의사결정 품질 점수 계산 오류: {e}")
            return 0.5
    
    def _calculate_timing_score(self, trade_data: Dict[str, Any], 
                              market_data: Dict[str, Any]) -> float:
        """타이밍 점수 계산"""
        try:
            # 타이밍 분석 (실제로는 더 복잡한 로직 필요)
            return 0.6
        except Exception as e:
            self.logger.error(f"타이밍 점수 계산 오류: {e}")
            return 0.5
    
    def _calculate_risk_management_score(self, trade_data: Dict[str, Any]) -> float:
        """리스크 관리 점수 계산"""
        try:
            # 리스크 관리 평가 (실제로는 더 복잡한 로직 필요)
            return 0.7
        except Exception as e:
            self.logger.error(f"리스크 관리 점수 계산 오류: {e}")
            return 0.5
    
    def _perform_ai_analysis(self, trade_data: Dict[str, Any], 
                           market_data: Dict[str, Any]) -> str:
        """AI 기반 거래 분석"""
        try:
            # GPT를 활용한 분석 (실제 구현 필요)
            analysis_prompt = f"""
            거래 분석:
            - 거래 유형: {trade_data.get('decision', 'unknown')}
            - 거래 가격: {trade_data.get('price', 0)}
            - 거래량: {trade_data.get('amount', 0)}
            - 시장 상황: {json.dumps(market_data, ensure_ascii=False)}
            
            이 거래의 성공/실패 요인과 개선점을 분석해주세요.
            """
            
            # 실제로는 GPT API 호출
            return "AI 분석 결과: 거래가 적절한 시점에 이루어졌으며, 시장 상황을 고려한 합리적인 결정이었습니다."
            
        except Exception as e:
            self.logger.error(f"AI 분석 오류: {e}")
            return "AI 분석을 수행할 수 없습니다."
    
    def _generate_improvement_suggestions(self, trade_data: Dict[str, Any], 
                                       market_data: Dict[str, Any]) -> str:
        """개선 제안 생성"""
        try:
            return "1. 시장 변동성에 따른 포지션 크기 조정\n2. 손절선 설정 강화\n3. 진입 타이밍 개선"
        except Exception as e:
            self.logger.error(f"개선 제안 생성 오류: {e}")
            return "개선 제안을 생성할 수 없습니다."
    
    def _extract_lessons_learned(self, trade_data: Dict[str, Any], 
                               market_data: Dict[str, Any]) -> str:
        """학습한 교훈 추출"""
        try:
            return "시장 상황에 따른 유연한 전략 적용의 중요성을 확인했습니다."
        except Exception as e:
            self.logger.error(f"교훈 추출 오류: {e}")
            return "교훈을 추출할 수 없습니다."
    
    def _suggest_next_actions(self, trade_data: Dict[str, Any], 
                            market_data: Dict[str, Any]) -> str:
        """다음 행동 제안"""
        try:
            return "시장 모니터링 강화 및 다음 기회 대기"
        except Exception as e:
            self.logger.error(f"다음 행동 제안 오류: {e}")
            return "다음 행동을 제안할 수 없습니다."
    
    def _save_reflection(self, reflection: TradeReflection) -> bool:
        """반성 데이터 저장"""
        try:
            cursor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO trading_reflections (
                trade_id, reflection_type, performance_score, profit_loss, profit_loss_percentage,
                market_conditions, decision_quality_score, timing_score, risk_management_score,
                ai_analysis, improvement_suggestions, lessons_learned, next_actions
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                reflection.trade_id, reflection.reflection_type, reflection.performance_score,
                reflection.profit_loss, reflection.profit_loss_percentage,
                json.dumps(reflection.market_conditions, ensure_ascii=False),
                reflection.decision_quality_score, reflection.timing_score, reflection.risk_management_score,
                reflection.ai_analysis, reflection.improvement_suggestions,
                reflection.lessons_learned, reflection.next_actions
            ))
            
            self.connection.commit()
            cursor.close()
            
            return True
            
        except Error as e:
            self.logger.error(f"반성 데이터 저장 오류: {e}")
            return False
    
    def _get_trades_in_period(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """기간 내 거래 데이터 조회"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            select_query = """
            SELECT * FROM trades 
            WHERE timestamp BETWEEN %s AND %s
            ORDER BY timestamp ASC
            """
            
            cursor.execute(select_query, (start_date, end_date))
            trades = cursor.fetchall()
            
            cursor.close()
            return trades
            
        except Error as e:
            self.logger.error(f"거래 데이터 조회 오류: {e}")
            return []
    
    def _calculate_period_metrics(self, trades: List[Dict[str, Any]], 
                                period_start: datetime, period_end: datetime) -> PerformanceMetrics:
        """기간별 성과 지표 계산"""
        try:
            total_trades = len(trades)
            winning_trades = sum(1 for trade in trades if self._calculate_profit_loss(trade) > 0)
            losing_trades = total_trades - winning_trades
            win_rate = winning_trades / total_trades if total_trades > 0 else 0
            
            total_profit_loss = sum(self._calculate_profit_loss(trade) for trade in trades)
            total_profit_loss_percentage = (total_profit_loss / 1000000) * 100  # 임시 계산
            
            # 최대 낙폭 계산 (간단한 버전)
            max_drawdown = 0.1  # 임시값
            
            # 샤프 비율 계산 (간단한 버전)
            sharpe_ratio = 0.5  # 임시값
            
            return PerformanceMetrics(
                period_type='daily',
                period_start=period_start,
                period_end=period_end,
                total_trades=total_trades,
                winning_trades=winning_trades,
                losing_trades=losing_trades,
                win_rate=win_rate,
                total_profit_loss=total_profit_loss,
                total_profit_loss_percentage=total_profit_loss_percentage,
                max_drawdown=max_drawdown,
                sharpe_ratio=sharpe_ratio,
                average_trade_duration=0,
                best_trade_profit=0,
                worst_trade_loss=0,
                market_condition_performance={},
                strategy_performance={}
            )
            
        except Exception as e:
            self.logger.error(f"성과 지표 계산 오류: {e}")
            return None
    
    def _perform_period_ai_analysis(self, trades: List[Dict[str, Any]], 
                                  metrics: PerformanceMetrics) -> str:
        """기간별 AI 분석"""
        try:
            return f"기간 분석 결과: 총 {metrics.total_trades}건 거래, 승률 {metrics.win_rate:.2%}, 수익률 {metrics.total_profit_loss_percentage:.2f}%"
        except Exception as e:
            self.logger.error(f"기간별 AI 분석 오류: {e}")
            return "기간별 분석을 수행할 수 없습니다."
    
    def _generate_period_improvements(self, trades: List[Dict[str, Any]], 
                                    metrics: PerformanceMetrics) -> str:
        """기간별 개선 제안"""
        try:
            improvements = []
            
            if metrics.win_rate < 0.5:
                improvements.append("승률 개선을 위한 진입 조건 강화")
            
            if metrics.max_drawdown > 0.1:
                improvements.append("리스크 관리 강화")
            
            if metrics.total_profit_loss < 0:
                improvements.append("손익비 개선을 위한 청산 전략 조정")
            
            return "\n".join(improvements) if improvements else "현재 전략이 양호합니다."
            
        except Exception as e:
            self.logger.error(f"기간별 개선 제안 오류: {e}")
            return "개선 제안을 생성할 수 없습니다."
    
    def _extract_period_lessons(self, trades: List[Dict[str, Any]], 
                               metrics: PerformanceMetrics) -> str:
        """기간별 교훈 추출"""
        try:
            return f"기간 교훈: {metrics.total_trades}건의 거래를 통해 시장 상황별 대응 전략의 중요성을 확인했습니다."
        except Exception as e:
            self.logger.error(f"기간별 교훈 추출 오류: {e}")
            return "교훈을 추출할 수 없습니다."
    
    def _suggest_period_actions(self, trades: List[Dict[str, Any]], 
                               metrics: PerformanceMetrics) -> str:
        """기간별 다음 행동 제안"""
        try:
            return "다음 기간을 위한 전략 조정 및 시장 모니터링 강화"
        except Exception as e:
            self.logger.error(f"기간별 행동 제안 오류: {e}")
            return "다음 행동을 제안할 수 없습니다."
    
    def _save_performance_metrics(self, metrics: PerformanceMetrics) -> bool:
        """성과 지표 저장"""
        try:
            cursor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO performance_metrics (
                period_type, period_start, period_end, total_trades, winning_trades, losing_trades,
                win_rate, total_profit_loss, total_profit_loss_percentage, max_drawdown, sharpe_ratio,
                average_trade_duration, best_trade_profit, worst_trade_loss,
                market_condition_performance, strategy_performance
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                metrics.period_type, metrics.period_start, metrics.period_end,
                metrics.total_trades, metrics.winning_trades, metrics.losing_trades,
                metrics.win_rate, metrics.total_profit_loss, metrics.total_profit_loss_percentage,
                metrics.max_drawdown, metrics.sharpe_ratio, metrics.average_trade_duration,
                metrics.best_trade_profit, metrics.worst_trade_loss,
                json.dumps(metrics.market_condition_performance, ensure_ascii=False),
                json.dumps(metrics.strategy_performance, ensure_ascii=False)
            ))
            
            self.connection.commit()
            cursor.close()
            
            return True
            
        except Error as e:
            self.logger.error(f"성과 지표 저장 오류: {e}")
            return False
    
    def _analyze_success_patterns(self, trades: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """성공 패턴 분석"""
        try:
            successful_trades = [trade for trade in trades if self._calculate_profit_loss(trade) > 0]
            
            insights = []
            if successful_trades:
                insight = {
                    'insight_type': 'pattern',
                    'insight_title': '성공 거래 패턴 발견',
                    'insight_description': f'{len(successful_trades)}건의 성공 거래에서 공통 패턴을 발견했습니다.',
                    'confidence_level': 0.7,
                    'supporting_data': {'successful_trades_count': len(successful_trades)},
                    'applicable_conditions': {'market_condition': 'bullish'},
                    'action_items': '성공 패턴을 기반으로 한 진입 조건 강화',
                    'priority_level': 'high'
                }
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            self.logger.error(f"성공 패턴 분석 오류: {e}")
            return []
    
    def _analyze_failure_patterns(self, trades: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """실패 패턴 분석"""
        try:
            failed_trades = [trade for trade in trades if self._calculate_profit_loss(trade) < 0]
            
            insights = []
            if failed_trades:
                insight = {
                    'insight_type': 'pattern',
                    'insight_title': '실패 거래 패턴 발견',
                    'insight_description': f'{len(failed_trades)}건의 실패 거래에서 개선점을 발견했습니다.',
                    'confidence_level': 0.6,
                    'supporting_data': {'failed_trades_count': len(failed_trades)},
                    'applicable_conditions': {'market_condition': 'bearish'},
                    'action_items': '실패 패턴을 피하기 위한 조건 추가',
                    'priority_level': 'high'
                }
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            self.logger.error(f"실패 패턴 분석 오류: {e}")
            return []
    
    def _analyze_market_condition_performance(self, trades: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """시장 상황별 성과 분석"""
        try:
            insight = {
                'insight_type': 'market',
                'insight_title': '시장 상황별 성과 분석',
                'insight_description': '다양한 시장 상황에서의 거래 성과를 분석했습니다.',
                'confidence_level': 0.5,
                'supporting_data': {'total_trades': len(trades)},
                'applicable_conditions': {'market_condition': 'all'},
                'action_items': '시장 상황별 전략 최적화',
                'priority_level': 'medium'
            }
            
            return [insight]
            
        except Exception as e:
            self.logger.error(f"시장 상황별 성과 분석 오류: {e}")
            return []
    
    def _analyze_timing_patterns(self, trades: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """타이밍 패턴 분석"""
        try:
            insight = {
                'insight_type': 'timing',
                'insight_title': '거래 타이밍 패턴 분석',
                'insight_description': '최적의 거래 타이밍 패턴을 분석했습니다.',
                'confidence_level': 0.6,
                'supporting_data': {'total_trades': len(trades)},
                'applicable_conditions': {'timing': 'optimal'},
                'action_items': '타이밍 개선을 위한 조건 추가',
                'priority_level': 'medium'
            }
            
            return [insight]
            
        except Exception as e:
            self.logger.error(f"타이밍 패턴 분석 오류: {e}")
            return []
    
    def _save_learning_insight(self, insight: Dict[str, Any]) -> bool:
        """학습 인사이트 저장"""
        try:
            cursor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO learning_insights (
                insight_type, insight_title, insight_description, confidence_level,
                supporting_data, applicable_conditions, action_items, priority_level
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                insight['insight_type'], insight['insight_title'], insight['insight_description'],
                insight['confidence_level'], json.dumps(insight['supporting_data'], ensure_ascii=False),
                json.dumps(insight['applicable_conditions'], ensure_ascii=False),
                insight['action_items'], insight['priority_level']
            ))
            
            self.connection.commit()
            cursor.close()
            
            return True
            
        except Error as e:
            self.logger.error(f"학습 인사이트 저장 오류: {e}")
            return False
    
    def _analyze_performance_for_improvements(self) -> List[Dict[str, Any]]:
        """성과 분석을 통한 개선점 도출"""
        try:
            improvements = []
            
            # 승률 개선 제안
            improvement = {
                'improvement_type': 'condition',
                'old_value': '기존 진입 조건',
                'new_value': '강화된 진입 조건',
                'reason': '승률 개선을 위한 조건 강화',
                'expected_impact': '승률 10% 향상 예상',
                'implementation_date': datetime.now(),
                'validation_period_days': 30,
                'performance_before': {'win_rate': 0.5},
                'performance_after': {'win_rate': 0.6},
                'success_metric': 0.6,
                'status': 'proposed'
            }
            improvements.append(improvement)
            
            return improvements
            
        except Exception as e:
            self.logger.error(f"성과 분석 개선점 도출 오류: {e}")
            return []
    
    def _generate_ai_improvements(self) -> List[Dict[str, Any]]:
        """AI 기반 개선 제안"""
        try:
            improvements = []
            
            # AI 분석 기반 개선 제안
            improvement = {
                'improvement_type': 'parameter',
                'old_value': '기존 파라미터',
                'new_value': 'AI 최적화 파라미터',
                'reason': 'AI 분석을 통한 파라미터 최적화',
                'expected_impact': '수익률 15% 향상 예상',
                'implementation_date': datetime.now(),
                'validation_period_days': 30,
                'performance_before': {'profit_rate': 0.05},
                'performance_after': {'profit_rate': 0.06},
                'success_metric': 0.7,
                'status': 'proposed'
            }
            improvements.append(improvement)
            
            return improvements
            
        except Exception as e:
            self.logger.error(f"AI 개선 제안 생성 오류: {e}")
            return []
    
    def _generate_risk_improvements(self) -> List[Dict[str, Any]]:
        """리스크 관리 개선 제안"""
        try:
            improvements = []
            
            # 리스크 관리 개선 제안
            improvement = {
                'improvement_type': 'risk',
                'old_value': '기존 리스크 관리',
                'new_value': '강화된 리스크 관리',
                'reason': '최대 낙폭 감소를 위한 리스크 관리 강화',
                'expected_impact': '최대 낙폭 20% 감소 예상',
                'implementation_date': datetime.now(),
                'validation_period_days': 30,
                'performance_before': {'max_drawdown': 0.15},
                'performance_after': {'max_drawdown': 0.12},
                'success_metric': 0.8,
                'status': 'proposed'
            }
            improvements.append(improvement)
            
            return improvements
            
        except Exception as e:
            self.logger.error(f"리스크 개선 제안 생성 오류: {e}")
            return []
    
    def _save_strategy_improvement(self, improvement: Dict[str, Any]) -> bool:
        """전략 개선 제안 저장"""
        try:
            cursor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO strategy_improvements (
                improvement_type, old_value, new_value, reason, expected_impact,
                implementation_date, validation_period_days, performance_before,
                performance_after, success_metric, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                improvement['improvement_type'], improvement['old_value'], improvement['new_value'],
                improvement['reason'], improvement['expected_impact'], improvement['implementation_date'],
                improvement['validation_period_days'], json.dumps(improvement['performance_before'], ensure_ascii=False),
                json.dumps(improvement['performance_after'], ensure_ascii=False),
                improvement['success_metric'], improvement['status']
            ))
            
            self.connection.commit()
            cursor.close()
            
            return True
            
        except Error as e:
            self.logger.error(f"전략 개선 제안 저장 오류: {e}")
            return False

# 전역 반성 시스템 객체
reflection_system = TradingReflectionSystem()

def create_immediate_reflection(trade_id: int, trade_data: Dict[str, Any], 
                              market_data: Dict[str, Any]) -> bool:
    """즉시 반성 생성 (편의 함수)"""
    return reflection_system.create_immediate_reflection(trade_id, trade_data, market_data)

def create_periodic_reflection(reflection_type: str, period_start: datetime, 
                             period_end: datetime) -> bool:
    """주기적 회고 생성 (편의 함수)"""
    return reflection_system.create_periodic_reflection(reflection_type, period_start, period_end)

def analyze_learning_patterns() -> List[Dict[str, Any]]:
    """학습 패턴 분석 (편의 함수)"""
    return reflection_system.analyze_learning_patterns()

def generate_strategy_improvements() -> List[Dict[str, Any]]:
    """전략 개선 제안 생성 (편의 함수)"""
    return reflection_system.generate_strategy_improvements()
