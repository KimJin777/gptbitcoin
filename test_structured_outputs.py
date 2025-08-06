#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Structured Outputs 테스트
"""

import os
from dotenv import load_dotenv
load_dotenv()

from autotrading import (
    get_market_data_with_indicators, 
    create_market_analysis_data_with_indicators, 
    ai_trading_decision_with_indicators,
    ai_trading_decision_with_vision,
    capture_upbit_screenshot
)

def test_structured_outputs():
    """
    Structured Outputs 기능 테스트
    """
    print("=" * 60)
    print("🔧 Structured Outputs 기능 테스트")
    print("=" * 60)
    
    try:
        # 1. 시장 데이터 수집
        print("\n📊 시장 데이터를 수집합니다...")
        daily_df, minute_df, current_price, orderbook, fear_greed_data, analyzed_news = get_market_data_with_indicators()
        
        # 2. AI 분석용 데이터 생성
        print("🤖 AI 분석용 데이터를 생성합니다...")
        market_data = create_market_analysis_data_with_indicators(daily_df, minute_df, current_price, orderbook, fear_greed_data, analyzed_news)
        
        # 3. Structured Outputs를 사용한 AI 분석 (기술적 지표만)
        print("\n🤖 Structured Outputs를 사용한 AI 분석을 시작합니다...")
        decision = ai_trading_decision_with_indicators(market_data)
        
        if decision:
            print("\n✅ Structured Outputs 테스트 성공!")
            print(f"📈 매매 결정: {decision.get('decision', 'N/A')}")
            print(f"🎯 신뢰도: {decision.get('confidence', 'N/A')}")
            print(f"⚠️ 위험도: {decision.get('risk_level', 'N/A')}")
            
            # Structured output 구조 확인
            required_fields = ['decision', 'reason', 'confidence', 'risk_level', 'expected_price_range', 'key_indicators']
            missing_fields = [field for field in required_fields if field not in decision]
            
            if missing_fields:
                print(f"⚠️ 누락된 필드: {missing_fields}")
            else:
                print("✅ 모든 필수 필드가 포함되어 있습니다!")
                
        else:
            print("❌ Structured Outputs 분석에 실패했습니다.")
            
        # 4. Vision API + Structured Outputs 테스트 (선택사항)
        print("\n📸 Vision API + Structured Outputs 테스트를 시작합니다...")
        screenshot_result = capture_upbit_screenshot()
        
        if screenshot_result:
            filepath, chart_image_base64 = screenshot_result
            print(f"✅ 차트 스크린샷 캡처 완료: {filepath}")
            
            vision_decision = ai_trading_decision_with_vision(market_data, chart_image_base64)
            
            if vision_decision:
                print("\n✅ Vision API + Structured Outputs 테스트 성공!")
                print(f"📈 매매 결정: {vision_decision.get('decision', 'N/A')}")
                print(f"🎯 신뢰도: {vision_decision.get('confidence', 'N/A')}")
                
                # Vision API 구조 확인
                vision_fields = ['decision', 'reason', 'confidence', 'risk_level', 'expected_price_range', 'key_indicators', 'chart_analysis']
                vision_missing_fields = [field for field in vision_fields if field not in vision_decision]
                
                if vision_missing_fields:
                    print(f"⚠️ Vision API 누락된 필드: {vision_missing_fields}")
                else:
                    print("✅ Vision API 모든 필수 필드가 포함되어 있습니다!")
                    
            else:
                print("❌ Vision API + Structured Outputs 분석에 실패했습니다.")
        else:
            print("⚠️ 차트 스크린샷 캡처 실패, Vision API 테스트를 건너뜁니다.")
            
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_structured_outputs()
