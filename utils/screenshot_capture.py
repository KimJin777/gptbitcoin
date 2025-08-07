"""
차트 스크린샷 캡처 유틸리티 (AWS 환경 최적화)
"""

import os
import time
import base64
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging

logger = logging.getLogger(__name__)

def setup_chrome_driver():
    """AWS 환경에 최적화된 Chrome 드라이버 설정"""
    chrome_options = Options()
    
    # AWS 환경 최적화 설정
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--disable-images')
    chrome_options.add_argument('--disable-javascript')
    chrome_options.add_argument('--disable-background-timer-throttling')
    chrome_options.add_argument('--disable-backgrounding-occluded-windows')
    chrome_options.add_argument('--disable-renderer-backgrounding')
    chrome_options.add_argument('--disable-features=TranslateUI')
    chrome_options.add_argument('--disable-ipc-flooding-protection')
    
    # 헤드리스 모드 (AWS 서버 환경)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maximized')
    
    # 메모리 최적화
    chrome_options.add_argument('--memory-pressure-off')
    chrome_options.add_argument('--max_old_space_size=4096')
    
    # 사용자 에이전트 설정
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        # Chrome 드라이버 생성
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        logger.error(f"Chrome 드라이버 생성 실패: {e}")
        return None

def capture_tradingview_chart(symbol="BTCUSD", interval="60", indicators="BB"):
    """
    TradingView 차트 스크린샷 캡처 (AWS 최적화)
    
    Args:
        symbol (str): 거래 심볼 (기본값: BTCUSD)
        interval (str): 시간 간격 (기본값: 60분)
        indicators (str): 지표 (기본값: BB - 볼린저 밴드)
    
    Returns:
        str: Base64 인코딩된 이미지 또는 None
    """
    driver = None
    try:
        # Chrome 드라이버 설정
        driver = setup_chrome_driver()
        if not driver:
            logger.error("Chrome 드라이버 초기화 실패")
            return None
        
        # TradingView URL 구성
        url = f"https://www.tradingview.com/chart/?symbol={symbol}&interval={interval}&indicator={indicators}"
        
        logger.info(f"차트 캡처 시작: {url}")
        
        # 페이지 로드
        driver.get(url)
        
        # 페이지 로딩 대기
        wait = WebDriverWait(driver, 20)
        
        # 차트 컨테이너 대기
        try:
            chart_container = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "chart-container"))
            )
        except TimeoutException:
            logger.warning("차트 컨테이너를 찾을 수 없습니다. 전체 페이지를 캡처합니다.")
        
        # 차트 로딩 대기 (추가 시간)
        time.sleep(5)
        
        # 스크린샷 캡처
        screenshot = driver.get_screenshot_as_png()
        
        # 이미지 최적화
        optimized_image = optimize_image_for_aws(screenshot)
        
        # Base64 인코딩
        img_base64 = base64.b64encode(optimized_image).decode('utf-8')
        
        logger.info("차트 캡처 완료")
        return img_base64
        
    except WebDriverException as e:
        logger.error(f"웹드라이버 오류: {e}")
        return None
    except Exception as e:
        logger.error(f"차트 캡처 중 오류: {e}")
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logger.error(f"드라이버 종료 오류: {e}")

def optimize_image_for_aws(image_data):
    """
    AWS 환경에 최적화된 이미지 압축
    
    Args:
        image_data (bytes): 원본 이미지 데이터
    
    Returns:
        bytes: 최적화된 이미지 데이터
    """
    try:
        # PIL로 이미지 로드
        image = Image.open(BytesIO(image_data))
        
        # 이미지 크기 조정 (AWS 메모리 절약)
        max_width = 1600
        max_height = 900
        
        # 비율 유지하면서 크기 조정
        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # JPEG로 변환 및 압축
        output_buffer = BytesIO()
        image.save(output_buffer, format='JPEG', quality=85, optimize=True)
        
        optimized_data = output_buffer.getvalue()
        
        # 파일 크기 확인 (2MB 이하로 제한)
        if len(optimized_data) > 2 * 1024 * 1024:
            # 더 강한 압축
            output_buffer = BytesIO()
            image.save(output_buffer, format='JPEG', quality=70, optimize=True)
            optimized_data = output_buffer.getvalue()
        
        logger.info(f"이미지 최적화 완료: {len(image_data)} -> {len(optimized_data)} bytes")
        return optimized_data
        
    except Exception as e:
        logger.error(f"이미지 최적화 오류: {e}")
        return image_data

def test_screenshot_capture():
    """스크린샷 캡처 테스트"""
    logger.info("스크린샷 캡처 테스트 시작")
    
    # 테스트 실행
    result = capture_tradingview_chart("BTCUSD", "60", "BB")
    
    if result:
        logger.info("스크린샷 캡처 테스트 성공")
        return True
    else:
        logger.error("스크린샷 캡처 테스트 실패")
        return False

if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 테스트 실행
    test_screenshot_capture()
