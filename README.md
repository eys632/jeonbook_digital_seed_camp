# 전주 한옥마을 혼잡/주차 난이도 MVP

전주 한옥마을의 실시간 혼잡도와 주차 난이도를 확인할 수 있는 대시보드입니다.

## 📋 기능

- **실시간 혼잡도 표시**: 현재 한옥마을의 혼잡 상태를 확인
- **30분 뒤 예측**: 향후 혼잡도 예측 정보 제공
- **난이도 점수**: 0~100 점수로 방문 난이도 표시
- **자동 갱신**: 5초마다 데이터 자동 업데이트
- **레벨 표시**: EASY / MODERATE / HARD / VERY_HARD

## 🚀 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

접속: http://localhost:8000/

## ☁️ Kakao Cloud VM (ver1) 배포

### 1. SSH 접속

```bash
ssh -i ver1_key.pem ubuntu@<PUBLIC_IP>
```

### 2. 환경 설정 및 실행

```bash
# 시스템 업데이트 및 패키지 설치
sudo apt update
sudo apt install -y python3-pip git

# 레포지토리 클론
git clone https://github.com/<USERNAME>/camp.git
cd camp

# 의존성 설치
pip3 install -r requirements.txt

# 서버 실행
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### 3. 보안 그룹 설정

Kakao Cloud 콘솔에서 인바운드 규칙 추가:
- **프로토콜**: TCP
- **포트**: 8000
- **소스**: 0.0.0.0/0 (또는 특정 IP)

### 4. 접속

```
http://<PUBLIC_IP>:8000/
```

## 🔄 백그라운드 실행

```bash
nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

로그 확인:
```bash
tail -f server.log
```

프로세스 종료:
```bash
pkill -f uvicorn
```

## 🛠️ (선택) systemd 서비스 등록

```bash
# 서비스 파일 생성
sudo nano /etc/systemd/system/hanok-mvp.service
```

```ini
[Unit]
Description=Jeonju Hanok Village MVP
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/camp
ExecStart=/usr/bin/python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 서비스 활성화 및 시작
sudo systemctl daemon-reload
sudo systemctl enable hanok-mvp
sudo systemctl start hanok-mvp

# 상태 확인
sudo systemctl status hanok-mvp
```

## 📁 프로젝트 구조

```
camp/
├── app.py              # FastAPI 백엔드
├── requirements.txt    # Python 의존성
├── static/
│   └── index.html      # 프론트엔드 대시보드
└── README.md           # 이 문서
```

## 📡 API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/` | GET | 대시보드 HTML 페이지 |
| `/api/status` | GET | 혼잡도/난이도 JSON 데이터 |
| `/health` | GET | 헬스체크 |

### `/api/status` 응답 예시

```json
{
  "area": "Jeonju Hanok Village",
  "area_kr": "전주 한옥마을",
  "now_kst": "2026-02-03T14:30:00+09:00",
  "traffic_index_now": 0.65,
  "traffic_index_forecast_30m": 0.72,
  "parking_pressure_now": 0.58,
  "difficulty_now_0_100": 68,
  "difficulty_30m_0_100": 74,
  "level_now": "HARD",
  "level_30m": "HARD",
  "message": "현재 한옥마을이 혼잡합니다. 대중교통 이용을 권장합니다. 🟠",
  "message_30m": "30분 뒤 한옥마을이 혼잡합니다. 대중교통 이용을 권장합니다. 🟠",
  "notes": "현재 더미(룰 기반) 데이터로 동작 중입니다. 추후 실시간 교통/주차 API 연동 예정."
}
```

## 🔮 향후 계획 (실데이터 연동)

현재는 더미(룰 기반) 데이터로 동작합니다. 
실데이터 연동 시 `app.py`의 `get_realtime_features()` 함수만 교체하면 됩니다:

```python
def get_realtime_features() -> Tuple[float, float]:
    """
    실데이터 연동 시 이 함수를 수정:
    - 네이버/카카오 실시간 교통 API
    - 전주시 공공데이터 주차장 API
    - 방문객 수 실시간 데이터
    """
    # API 호출 로직
    traffic_index = call_traffic_api()
    parking_pressure = call_parking_api()
    return traffic_index, parking_pressure
```

## 📝 라이선스

MIT License
