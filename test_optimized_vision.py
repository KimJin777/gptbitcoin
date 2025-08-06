#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최적화된 이미지 캡처 및 Vision API 통합 테스트
"""

import os
from dotenv import load_dotenv
load_dotenv()

from screenshot_capture import capture_upbit_screenshot
from advanced_ai_trading import create_market_analysis_data_with_indicators, get_market_data_with_indicators, ai_trading_decision_with_vision

def test_optimized_vision_integration():
    """
    최적화된 이미지 캡처 및 Vision API 통합 테스트
    """
    print("=" * 60)
    print("🔧 최적화된 이미지 캡처 및 Vision API 통합 테스트")
    print("=" * 60)
    
    try:
        # 1. 시장 데이터 수집
        print("\n📊 시장 데이터를 수집합니다...")
        daily_df, minute_df, current_price, orderbook, fear_greed_data, analyzed_news = get_market_data_with_indicators()
        
        # 2. AI 분석용 데이터 생성
        print("🤖 AI 분석용 데이터를 생성합니다...")
        market_data = create_market_analysis_data_with_indicators(daily_df, minute_df, current_price, orderbook, fear_greed_data, analyzed_news)
        
        # 3. 최적화된 차트 스크린샷 캡처
        print("\n📸 최적화된 차트 스크린샷을 캡처합니다...")
        screenshot_result = capture_upbit_screenshot()
        
        if screenshot_result:
            filepath, chart_image_base64 = screenshot_result
            print(f"✅ 최적화된 스크린샷 캡처 완료!")
            print(f"📁 파일 위치: {filepath}")
            print(f"🔗 Base64 길이: {len(chart_image_base64)} 문자")
            print(f"📊 최적화된 크기: {len(chart_image_base64) * 3 / 4 / (1024*1024):.2f} MB (추정)")
            
            # 4. Vision API를 사용한 AI 분석
            print("\n🤖 Vision API를 사용한 AI 분석을 시작합니다...")
            decision = ai_trading_decision_with_vision(market_data, chart_image_base64)
            
            # 5. 결과 출력
            print("\n" + "=" * 60)
            print("🎉 테스트 결과")
            print("=" * 60)
            print(f"📈 매매 결정: {decision.get('decision', 'N/A')}")
            print(f"🎯 신뢰도: {decision.get('confidence', 'N/A')}")
            print(f"⚠️ 위험도: {decision.get('risk_level', 'N/A')}")
            print(f"💰 예상 가격 범위: {decision.get('expected_price_range', 'N/A')}")
            
            if 'chart_analysis' in decision:
                chart_analysis = decision['chart_analysis']
                print(f"📊 차트 분석:")
                print(f"   - 가격 액션: {chart_analysis.get('price_action', 'N/A')}")
                print(f"   - 지지선: {chart_analysis.get('support_level', 'N/A')}")
                print(f"   - 저항선: {chart_analysis.get('resistance_level', 'N/A')}")
                print(f"   - 차트 패턴: {chart_analysis.get('chart_pattern', 'N/A')}")
                print(f"   - 거래량 분석: {chart_analysis.get('volume_analysis', 'N/A')}")
            
            print("\n✅ 최적화된 이미지와 Vision API 통합이 성공적으로 작동합니다!")
            
        else:
            print("❌ 스크린샷 캡처에 실패했습니다.")
            
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_optimized_vision_integration()
