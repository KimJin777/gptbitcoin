#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이미지 최적화 기능 테스트
"""

from screenshot_capture import capture_upbit_screenshot

def test_image_optimization():
    """
    이미지 최적화 기능 테스트
    """
    print("=" * 60)
    print("🔧 이미지 최적화 기능 테스트")
    print("=" * 60)
    
    try:
        # 스크린샷 캡처 및 최적화
        print("📸 차트 스크린샷을 캡처하고 최적화합니다...")
        result = capture_upbit_screenshot()
        
        if result:
            filepath, image_base64 = result
            print(f"\n✅ 테스트 성공!")
            print(f"📁 파일 위치: {filepath}")
            print(f"🔗 Base64 길이: {len(image_base64)} 문자")
            print(f"📊 최적화된 크기: {len(image_base64) * 3 / 4 / (1024*1024):.2f} MB (추정)")
            
            # 최적화 효과 확인
            import os
            original_size = os.path.getsize(filepath) / (1024*1024)  # MB
            optimized_size = len(image_base64) * 3 / 4 / (1024*1024)  # MB (추정)
            compression_ratio = (1 - optimized_size / original_size) * 100
            
            print(f"\n📊 최적화 효과:")
            print(f"   📏 원본 크기: {original_size:.2f} MB")
            print(f"   📏 최적화 크기: {optimized_size:.2f} MB")
            print(f"   📊 압축률: {compression_ratio:.1f}%")
            
            if compression_ratio > 10:
                print("✅ 이미지 최적화가 성공적으로 작동합니다!")
            else:
                print("⚠️ 압축률이 낮습니다. 설정을 확인해주세요.")
                
        else:
            print("❌ 스크린샷 캡처에 실패했습니다.")
            
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_image_optimization()
