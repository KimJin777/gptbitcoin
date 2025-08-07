"""
AWS 환경 설정 스크립트
"""

import subprocess
import sys
import os
import logging

logger = logging.getLogger(__name__)

def run_command(command, description=""):
    """명령어 실행"""
    try:
        logger.info(f"실행 중: {description or command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"성공: {description or command}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"실패: {description or command}")
        logger.error(f"오류: {e.stderr}")
        return False

def install_python_packages():
    """Python 패키지 설치"""
    logger.info("Python 패키지 설치 시작")
    
    packages = [
        "selenium",
        "webdriver-manager",
        "Pillow",
        "requests",
        "beautifulsoup4",
        "lxml",
        "mysql-connector-python",
        "schedule",
        "streamlit",
        "plotly",
        "pandas",
        "numpy",
        "ta",
        "pyupbit",
        "openai",
        "pydantic",
        "python-dotenv"
    ]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"패키지 설치: {package}"):
            logger.error(f"패키지 설치 실패: {package}")
            return False
    
    logger.info("Python 패키지 설치 완료")
    return True

def install_chrome_driver():
    """Chrome 드라이버 설치"""
    logger.info("Chrome 드라이버 설치 시작")
    
    # Chrome 드라이버 다운로드
    if not run_command("wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/LATEST_RELEASE", "Chrome 드라이버 버전 확인"):
        return False
    
    # 최신 버전 확인
    try:
        with open('/tmp/chromedriver.zip', 'r') as f:
            version = f.read().strip()
    except:
        version = "120.0.6099.109"  # 기본 버전
    
    # Chrome 드라이버 다운로드
    download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_linux64.zip"
    
    if not run_command(f"wget -q -O /tmp/chromedriver.zip {download_url}", "Chrome 드라이버 다운로드"):
        return False
    
    # 압축 해제 및 설치
    commands = [
        "unzip -q /tmp/chromedriver.zip -d /tmp/",
        "sudo mv /tmp/chromedriver /usr/local/bin/",
        "sudo chmod +x /usr/local/bin/chromedriver",
        "rm /tmp/chromedriver.zip"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Chrome 드라이버 설치: {cmd}"):
            return False
    
    logger.info("Chrome 드라이버 설치 완료")
    return True

def setup_mysql():
    """MySQL 설정"""
    logger.info("MySQL 설정 시작")
    
    commands = [
        "sudo apt update",
        "sudo apt install -y mysql-server",
        "sudo systemctl start mysql",
        "sudo systemctl enable mysql"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"MySQL 설정: {cmd}"):
            return False
    
    logger.info("MySQL 설정 완료")
    return True

def create_environment_file():
    """환경 변수 파일 생성"""
    logger.info("환경 변수 파일 생성")
    
    env_content = """# AWS 환경 설정
# 업비트 API 키
UPBIT_ACCESS_KEY=your_upbit_access_key_here
UPBIT_SECRET_KEY=your_upbit_secret_key_here

# OpenAI API 키
OPENAI_API_KEY=your_openai_api_key_here

# SerpAPI 키 (뉴스 분석용)
SERP_API_KEY=your_serpapi_key_here

# MySQL 데이터베이스 설정
DB_HOST=localhost
DB_PORT=3306
DB_NAME=gptbitcoin
DB_USER=root
DB_PASSWORD=your_mysql_password_here

# AWS 환경 설정
AWS_ENVIRONMENT=true
HEADLESS_MODE=true
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        logger.info("환경 변수 파일 생성 완료")
        return True
    except Exception as e:
        logger.error(f"환경 변수 파일 생성 실패: {e}")
        return False

def setup_database():
    """데이터베이스 초기화"""
    logger.info("데이터베이스 초기화 시작")
    
    # MySQL 접속 및 데이터베이스 생성
    mysql_commands = [
        "mysql -u root -e \"CREATE DATABASE IF NOT EXISTS gptbitcoin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\"",
        "mysql -u root -e \"CREATE USER IF NOT EXISTS 'gptbitcoin'@'localhost' IDENTIFIED BY 'your_password_here';\"",
        "mysql -u root -e \"GRANT ALL PRIVILEGES ON gptbitcoin.* TO 'gptbitcoin'@'localhost';\"",
        "mysql -u root -e \"FLUSH PRIVILEGES;\""
    ]
    
    for cmd in mysql_commands:
        if not run_command(cmd, f"데이터베이스 설정: {cmd}"):
            logger.warning(f"데이터베이스 설정 경고: {cmd}")
    
    logger.info("데이터베이스 초기화 완료")
    return True

def create_service_file():
    """시스템 서비스 파일 생성"""
    logger.info("시스템 서비스 파일 생성")
    
    service_content = """[Unit]
Description=GPT Bitcoin Trading Bot
After=network.target mysql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/gptbitcoin
Environment=PATH=/home/ubuntu/.local/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/usr/bin/python3 /home/ubuntu/gptbitcoin/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    try:
        with open('/tmp/gptbitcoin.service', 'w') as f:
            f.write(service_content)
        
        # 서비스 파일 복사
        commands = [
            "sudo cp /tmp/gptbitcoin.service /etc/systemd/system/",
            "sudo systemctl daemon-reload",
            "sudo systemctl enable gptbitcoin.service"
        ]
        
        for cmd in commands:
            if not run_command(cmd, f"서비스 설정: {cmd}"):
                logger.warning(f"서비스 설정 경고: {cmd}")
        
        logger.info("시스템 서비스 파일 생성 완료")
        return True
    except Exception as e:
        logger.error(f"서비스 파일 생성 실패: {e}")
        return False

def main():
    """메인 설정 함수"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    logger.info("AWS 환경 설정 시작")
    
    # 1. Python 패키지 설치
    if not install_python_packages():
        logger.error("Python 패키지 설치 실패")
        return False
    
    # 2. Chrome 드라이버 설치
    if not install_chrome_driver():
        logger.error("Chrome 드라이버 설치 실패")
        return False
    
    # 3. MySQL 설정
    if not setup_mysql():
        logger.error("MySQL 설정 실패")
        return False
    
    # 4. 환경 변수 파일 생성
    if not create_environment_file():
        logger.error("환경 변수 파일 생성 실패")
        return False
    
    # 5. 데이터베이스 초기화
    if not setup_database():
        logger.error("데이터베이스 초기화 실패")
        return False
    
    # 6. 서비스 파일 생성
    if not create_service_file():
        logger.error("서비스 파일 생성 실패")
        return False
    
    logger.info("AWS 환경 설정 완료!")
    logger.info("다음 단계:")
    logger.info("1. .env 파일에서 API 키를 설정하세요")
    logger.info("2. sudo systemctl start gptbitcoin.service로 서비스를 시작하세요")
    logger.info("3. sudo systemctl status gptbitcoin.service로 상태를 확인하세요")
    
    return True

if __name__ == "__main__":
    main()
