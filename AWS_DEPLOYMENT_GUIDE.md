# 🚀 AWS EC2 자동매매 시스템 배포 가이드

## 📋 사전 준비사항

### 1. AWS EC2 인스턴스 생성
- **인스턴스 타입**: t3.medium 이상 권장 (2GB RAM 이상)
- **OS**: Ubuntu 22.04 LTS
- **스토리지**: 20GB 이상
- **보안 그룹**: SSH(22), HTTP(80), HTTPS(443), 커스텀 포트(8501)

### 2. 필요한 패키지 설치
```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 필수 패키지 설치
sudo apt install -y python3 python3-pip python3-venv git wget unzip

# Chrome 설치 (이미 완료됨)
# wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
# sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# sudo apt update
# sudo apt install -y google-chrome-stable
```

## 🔧 배포 단계

### 1. 프로젝트 클론
```bash
cd /home/ubuntu
git clone https://github.com/KimJin777/gptbitcoin.git
cd gptbitcoin
```

### 2. 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. AWS 환경 설정 스크립트 실행
```bash
python3 aws_setup.py
```

### 4. 환경 변수 설정
```bash
# .env 파일 편집
nano .env

# 다음 내용으로 수정:
UPBIT_ACCESS_KEY=your_actual_upbit_access_key
UPBIT_SECRET_KEY=your_actual_upbit_secret_key
OPENAI_API_KEY=your_actual_openai_api_key
SERP_API_KEY=your_actual_serpapi_key
DB_HOST=localhost
DB_PORT=3306
DB_NAME=gptbitcoin
DB_USER=root
DB_PASSWORD=your_mysql_password
AWS_ENVIRONMENT=true
HEADLESS_MODE=true
```

### 5. 데이터베이스 초기화
```bash
# MySQL 접속
sudo mysql -u root

# 데이터베이스 생성
CREATE DATABASE gptbitcoin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gptbitcoin'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON gptbitcoin.* TO 'gptbitcoin'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Python 스크립트로 테이블 생성
python3 -c "from database.connection import init_database; init_database()"
```

### 6. 서비스 시작
```bash
# 시스템 서비스 시작
sudo systemctl start gptbitcoin.service

# 서비스 상태 확인
sudo systemctl status gptbitcoin.service

# 로그 확인
sudo journalctl -u gptbitcoin.service -f
```

## 🌐 대시보드 접속

### 1. Streamlit 대시보드 실행
```bash
# 대시보드 실행
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0

# 또는 백그라운드에서 실행
nohup streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 > dashboard.log 2>&1 &
```

### 2. 방화벽 설정
```bash
# AWS 보안 그룹에서 포트 8501 열기
# 또는 UFW 설정
sudo ufw allow 8501
```

### 3. 접속 확인
- **URL**: `http://your-ec2-public-ip:8501`
- **예시**: `http://3.25.123.45:8501`

## 🔍 모니터링 및 관리

### 1. 서비스 관리 명령어
```bash
# 서비스 시작
sudo systemctl start gptbitcoin.service

# 서비스 중지
sudo systemctl stop gptbitcoin.service

# 서비스 재시작
sudo systemctl restart gptbitcoin.service

# 서비스 상태 확인
sudo systemctl status gptbitcoin.service

# 자동 시작 설정
sudo systemctl enable gptbitcoin.service
```

### 2. 로그 확인
```bash
# 실시간 로그 확인
sudo journalctl -u gptbitcoin.service -f

# 최근 로그 확인
sudo journalctl -u gptbitcoin.service -n 100

# 특정 시간 로그 확인
sudo journalctl -u gptbitcoin.service --since "2024-01-01 00:00:00"
```

### 3. 프로세스 모니터링
```bash
# 실행 중인 프로세스 확인
ps aux | grep python

# 메모리 사용량 확인
free -h

# 디스크 사용량 확인
df -h
```

## 🛠️ 문제 해결

### 1. Chrome 드라이버 문제
```bash
# Chrome 버전 확인
google-chrome --version

# Chrome 드라이버 버전 확인
chromedriver --version

# 드라이버 재설치
wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/LATEST_RELEASE
unzip -q /tmp/chromedriver.zip -d /tmp/
sudo mv /tmp/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

### 2. MySQL 연결 문제
```bash
# MySQL 서비스 상태 확인
sudo systemctl status mysql

# MySQL 재시작
sudo systemctl restart mysql

# MySQL 접속 테스트
mysql -u root -p
```

### 3. 메모리 부족 문제
```bash
# 스왑 메모리 추가
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 영구 설정
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## 📊 성능 최적화

### 1. 시스템 최적화
```bash
# 시스템 파라미터 최적화
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### 2. Python 최적화
```bash
# 가상환경에서 최적화
pip install --upgrade pip
pip install --upgrade setuptools wheel
```

### 3. 로그 로테이션 설정
```bash
# 로그 로테이션 설정
sudo nano /etc/logrotate.d/gptbitcoin

# 다음 내용 추가:
/home/ubuntu/gptbitcoin/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
}
```

## 🔒 보안 설정

### 1. 방화벽 설정
```bash
# UFW 활성화
sudo ufw enable

# 필요한 포트만 열기
sudo ufw allow ssh
sudo ufw allow 8501
sudo ufw allow 3306
```

### 2. SSL 인증서 설정 (선택사항)
```bash
# Certbot 설치
sudo apt install -y certbot python3-certbot-nginx

# SSL 인증서 발급
sudo certbot --nginx -d your-domain.com
```

## 📈 백업 및 복구

### 1. 데이터베이스 백업
```bash
# 백업 스크립트 생성
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u root -p gptbitcoin > /home/ubuntu/backup/gptbitcoin_$DATE.sql
gzip /home/ubuntu/backup/gptbitcoin_$DATE.sql
EOF

chmod +x backup.sh

# 백업 디렉토리 생성
mkdir -p /home/ubuntu/backup

# 자동 백업 설정 (crontab)
crontab -e
# 다음 줄 추가: 0 2 * * * /home/ubuntu/gptbitcoin/backup.sh
```

### 2. 코드 백업
```bash
# Git 원격 저장소 설정
git remote add origin https://github.com/KimJin777/gptbitcoin.git
git add .
git commit -m "AWS 배포 완료"
git push origin main
```

## 🎯 완료 확인

### 1. 시스템 상태 확인
```bash
# 모든 서비스 상태 확인
sudo systemctl status gptbitcoin.service
sudo systemctl status mysql
sudo systemctl status nginx  # (선택사항)

# 포트 확인
sudo netstat -tlnp | grep -E ':(8501|3306|80|443)'
```

### 2. 기능 테스트
```bash
# 자동매매 시스템 테스트
python3 test_trading_with_reflection.py

# 대시보드 테스트
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
```

## 📞 지원 및 문의

문제가 발생하면 다음을 확인하세요:
1. 로그 파일 확인: `sudo journalctl -u gptbitcoin.service -f`
2. 시스템 리소스 확인: `htop`, `df -h`, `free -h`
3. 네트워크 연결 확인: `ping google.com`
4. 포트 상태 확인: `sudo netstat -tlnp`

---

**⚠️ 주의사항**: 실제 거래에 사용하기 전에 충분한 테스트가 필요합니다.
