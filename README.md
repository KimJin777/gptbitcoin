# 🚀 비트코인 AI 자동매매 시스템

최신 기술적 지표, 공포탐욕지수, 뉴스 분석을 통합한 고급 비트코인 자동매매 시스템입니다.

## 📋 주요 기능

### 🔧 기술적 분석
- **이동평균선**: SMA(20, 50), EMA(12, 26)
- **모멘텀 지표**: RSI, MACD, 스토캐스틱, 윌리엄스 %R
- **변동성 지표**: 볼린저 밴드, ATR
- **추세 지표**: ADX, CCI, ROC
- **거래량 지표**: OBV

### 🧠 시장 심리 분석
- **공포탐욕지수**: Alternative.me API 연동
- **뉴스 감정 분석**: Google News API + SerpAPI 연동
- **실시간 시장 심리 모니터링**

### 🤖 AI 기반 매매 결정
- **GPT-4o** 기반 지능형 매매 결정
- **GPT Vision API** 차트 이미지 분석
- **Structured Outputs** 안정적인 JSON 응답
- **다중 지표 종합 분석**
- **리스크 관리** 및 보수적 접근

### 📸 차트 이미지 분석
- **실시간 차트 스크린샷 캡처**
- **Pillow 라이브러리 이미지 최적화**
- **1시간 차트 + 볼린저 밴드 설정**
- **Base64 인코딩으로 OpenAI 전송**

### 🗄️ 데이터베이스 관리
- **MySQL 8.0 데이터베이스 연동**
- **거래 기록 자동 저장**
- **시장 데이터 히스토리 관리**
- **거래 통계 및 수익률 분석**
- **시스템 로그 저장 및 조회**

### 🤔 자동 반성 및 회고 시스템
- **거래 직후 즉시 반성 생성**
- **일/주/월 주기적 회고 분석**
- **AI 기반 성과 분석 및 개선점 도출**
- **학습 패턴 자동 발견**
- **전략 개선 제안 자동 생성**
- **재귀적 성능 향상 시스템**

### 📊 실시간 모니터링 대시보드
- **Streamlit 기반 웹 대시보드**
- **실시간 거래 기록 모니터링**
- **성과 지표 시각화 (승률, 수익률, 샤프 비율)**
- **반성 시스템 데이터 조회**
- **학습 인사이트 및 전략 개선 제안**
- **가격 차트 및 거래량 분석**
- **자동 새로고침 기능**

## 🛠️ 설치 및 설정

### 1. 필요한 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 2. MySQL 데이터베이스 설정

#### MySQL 8.0 설치 (Windows)
1. [MySQL Community Server](https://dev.mysql.com/downloads/mysql/) 다운로드
2. 설치 시 root 비밀번호 설정
3. MySQL 서비스 시작

#### 데이터베이스 생성
```sql
CREATE DATABASE gptbitcoin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 환경 변수 설정 (.env 파일)
```env
# 업비트 API 키
UPBIT_ACCESS_KEY=your_upbit_access_key
UPBIT_SECRET_KEY=your_upbit_secret_key

# OpenAI API 키
OPENAI_API_KEY=your_openai_api_key

# SerpAPI 키 (뉴스 분석용)
SERP_API_KEY=your_serpapi_key

# MySQL 데이터베이스 설정
DB_HOST=localhost
DB_PORT=3306
DB_NAME=gptbitcoin
DB_USER=root
DB_PASSWORD=your_mysql_password
```

### 3. API 키 발급 방법

#### 업비트 API 키
1. [업비트](https://upbit.com) 로그인
2. 마이페이지 → Open API 관리
3. API 키 발급 (읽기/주문 권한 필요)

#### OpenAI API 키
1. [OpenAI Platform](https://platform.openai.com) 가입
2. API Keys → Create new secret key

#### SerpAPI 키 (선택사항)
1. [SerpAPI](https://serpapi.com) 가입
2. API 키 발급 (뉴스 분석 기능 사용시)

## 🚀 사용 방법

### 메인 자동매매 시스템 실행
```bash
python main.py
```

### 거래 기록 조회
```bash
python view_trades.py
```

### 반성 시스템 데이터 조회
```bash
python reflection_viewer.py
```

### 반성 스케줄러 실행 (별도 프로세스)
```bash
python scheduler.py
```

### 실시간 모니터링 대시보드
```bash
python run_dashboard.py
```
또는
```bash
streamlit run dashboard.py
```

웹 브라우저에서 http://localhost:8501 으로 접속하여 실시간 모니터링을 확인할 수 있습니다.

### 거래 기록 조회
```bash
python view_trades.py
```

### 뉴스 분석 시스템 실행 (독립 실행)
```bash
python news_analyzer.py
```

### 차트 스크린샷 캡처 테스트
```bash
python screenshot_capture.py
```

### 최적화된 Vision API 통합 테스트
```bash
python test_optimized_vision.py
```

### 이미지 최적화 기능 테스트
```bash
python test_image_optimization.py
```

### Structured Outputs 테스트
```bash
python test_structured_outputs.py
```

## 📊 시스템 구성

### 1. 데이터 수집 모듈
- **시장 데이터**: 30일 일봉 + 24시간 분봉
- **기술적 지표**: 10개 주요 지표 자동 계산
- **시장 심리**: 공포탐욕지수 실시간 수집
- **뉴스 분석**: Google News API 연동

### 2. AI 분석 엔진
- **GPT-4o** 기반 지능형 분석
- **GPT Vision API** 차트 이미지 분석
- **다중 지표 종합 평가**
- **시장 심리 + 뉴스 감정 통합 분석**

### 3. 이미지 처리 모듈
- **Selenium** 웹 자동화로 차트 캡처
- **Pillow** 라이브러리 이미지 최적화
- **자동 차트 설정** (1시간 + 볼린저 밴드)
- **Base64 인코딩** OpenAI 전송용

### 4. 매매 실행 모듈
- **자동 매수/매도/보유 결정**
- **최소 거래금액 확인**
- **수수료 고려한 거래량 계산**

## 📈 분석 지표

### 기술적 지표
| 지표 | 설명 | 매매 신호 |
|------|------|-----------|
| RSI | 상대강도지수 | 70↑ 과매수, 30↓ 과매도 |
| MACD | 이동평균수렴확산 | 골든크로스/데드크로스 |
| 볼린저밴드 | 변동성 밴드 | 상단/하단 터치 |
| 스토캐스틱 | 모멘텀 지표 | K/D선 교차 |

### 시장 심리 지표
| 지수 범위 | 분류 | 투자 전략 |
|-----------|------|-----------|
| 0-25 | Extreme Fear | 과매도, 매수 기회 |
| 26-45 | Fear | 신중한 접근 |
| 46-55 | Neutral | 균형잡힌 시장 |
| 56-75 | Greed | 과매수 주의 |
| 76-100 | Extreme Greed | 과매수, 매도 기회 |

## 🔧 이미지 최적화 기능

### 최적화 프로세스
1. **원본 스크린샷 캡처**: Selenium으로 전체 페이지 캡처
2. **이미지 크기 조정**: 최대 1920px로 리사이즈
3. **JPEG 압축**: 품질 85%로 최적화
4. **파일 크기 제한**: 2MB 이하로 압축
5. **Base64 인코딩**: OpenAI API 전송용

### 최적화 효과
- **파일 크기 감소**: 평균 20-30% 압축률
- **전송 속도 향상**: 최적화된 이미지로 빠른 API 호출
- **API 비용 절약**: 작은 파일 크기로 토큰 사용량 감소
- **안정성 향상**: 네트워크 오류 위험 감소

## 🔧 Structured Outputs 기능

### 구조화된 응답 모델
- **TradingDecision**: 매매 결정, 신뢰도, 위험도, 예상 가격 범위
- **KeyIndicators**: RSI, MACD, 볼린저 밴드, 트렌드 강도, 시장 심리, 뉴스 감정
- **ChartAnalysis**: 가격 액션, 지지선/저항선, 차트 패턴, 거래량 분석
- **ExpectedPriceRange**: 예상 최저/최고 가격

### Structured Outputs 장점
- **안정적인 JSON 응답**: Pydantic 모델로 타입 안전성 보장
- **일관된 데이터 구조**: 항상 동일한 필드와 형식
- **오류 처리 강화**: 잘못된 응답 구조 자동 감지
- **개발 효율성**: IDE 자동완성 및 타입 힌트 지원

### 뉴스 감정 분석
- **긍정적 뉴스**: 상승 압력 예상
- **부정적 뉴스**: 하락 압력 예상
- **중립적 뉴스**: 횡보 예상

## ⚠️ 주의사항

### 리스크 관리
- **실제 거래 전 충분한 테스트 필요**
- **소액으로 시작하여 점진적 확대**
- **손절매 전략 필수 설정**

### API 사용량
- **OpenAI API**: GPT-4o 사용량 모니터링
- **SerpAPI**: 월간 요청 한도 확인
- **업비트 API**: 초당 요청 제한 준수

### 시스템 안정성
- **네트워크 오류 대응**
- **API 응답 지연 처리**
- **예외 상황 로깅**

## 📁 파일 구조

```
gptbitcoin/
├── advanced_ai_trading.py    # 메인 자동매매 시스템
├── news_analyzer.py          # 뉴스 분석 시스템
├── mvp.py                    # 기본 버전
├── requirements.txt          # 필요한 라이브러리
├── .env                      # 환경 변수 (직접 생성)
└── README.md                # 사용 설명서
```

## 🔄 실행 주기

### 메인 시스템
- **분석 주기**: 5분마다
- **데이터 수집**: 실시간
- **AI 분석**: 매 사이클마다
- **매매 실행**: 조건 충족시

### 뉴스 분석 시스템
- **분석 주기**: 30분마다
- **뉴스 수집**: Google News API
- **감정 분석**: 키워드 기반
- **결과 저장**: JSON 파일

## 📊 출력 예시

```
============================================================
비트코인 AI 자동매매 시스템 시작 (기술적 지표 + 공포탐욕지수 + 뉴스 분석 포함)
============================================================

=== 시장 데이터 수집 중 (기술적 지표 포함) ===
30일 일봉 데이터 수집 완료: 30개
24시간 분봉 데이터 수집 완료: 1440개
현재 비트코인 가격: 45,000,000원
공포탐욕지수: 65 (Greed)
📰 최신 뉴스 분석 결과:
  긍정: 3개
  중립: 5개
  부정: 2개

=== AI 매매 결정 분석 중 (기술적 지표 포함) ===
AI 결정: hold
신뢰도: 0.75
위험도: medium
RSI 신호: neutral
MACD 신호: bullish
볼린저밴드 신호: middle
트렌드 강도: strong
시장 심리: greed
뉴스 감정: positive
```

## 🤝 기여하기

버그 리포트나 기능 제안은 언제든 환영합니다!

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다. 실제 거래에 사용하기 전에 충분한 테스트가 필요합니다.

---

**⚠️ 투자 경고**: 암호화폐 투자는 높은 위험을 수반합니다. 투자 결정은 본인의 판단에 따라 신중하게 이루어져야 합니다.
