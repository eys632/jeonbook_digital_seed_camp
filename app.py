"""
전주 한옥마을 혼잡/주차 난이도 MVP - Backend
==============================================
FastAPI + Uvicorn 기반 백엔드

실행:
    python -m uvicorn app:app --host 0.0.0.0 --port 8000

실데이터 연동 시:
    get_realtime_features() 함수만 교체하면 됨.
    현재는 더미(룰 기반) 데이터로 동작.
"""

import math
import random
from datetime import datetime, timedelta, timezone
from typing import Tuple

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# ============================================================
# FastAPI 앱 설정
# ============================================================
app = FastAPI(
    title="전주 한옥마을 혼잡/주차 난이도 MVP",
    description="실시간 혼잡도 및 주차 난이도를 제공하는 API",
    version="1.0.0",
)

# 정적 파일 서빙 (CSS, JS 등 추가 시 사용)
app.mount("/static", StaticFiles(directory="static"), name="static")

# KST 타임존
KST = timezone(timedelta(hours=9))


# ============================================================
# 더미 데이터 생성 함수들
# ※ 실데이터 연동 시 get_realtime_features()만 교체하면 됨
# ============================================================

def get_realtime_features() -> Tuple[float, float]:
    """
    실시간 특성값을 반환합니다.
    
    Returns:
        Tuple[float, float]: (traffic_index, parking_pressure)
        - traffic_index: 0.0 ~ 1.0 (0=한산, 1=매우혼잡)
        - parking_pressure: 0.0 ~ 1.0 (0=여유, 1=만차)
    
    ※ 실데이터 연동 시 이 함수만 교체:
       - 실시간 교통 API (네이버, 카카오 등)
       - 주차장 API (전주시 공공데이터)
       - 방문객 수 데이터 등
    """
    now = datetime.now(KST)
    hour = now.hour
    weekday = now.weekday()  # 0=월, 6=일
    
    # 시간대별 기본 혼잡도 (더미 룰)
    if 10 <= hour < 12:
        base_traffic = 0.4
    elif 12 <= hour < 14:
        base_traffic = 0.6
    elif 14 <= hour < 18:
        base_traffic = 0.7
    elif 18 <= hour < 20:
        base_traffic = 0.5
    else:
        base_traffic = 0.2
    
    # 주말 가중치
    if weekday >= 5:  # 토, 일
        base_traffic = min(1.0, base_traffic * 1.3)
    
    # 약간의 랜덤 변동 추가
    traffic_index = max(0.0, min(1.0, base_traffic + random.uniform(-0.1, 0.1)))
    
    # 주차 압박도 (교통량에 비례 + 랜덤)
    parking_pressure = max(0.0, min(1.0, traffic_index * 0.9 + random.uniform(0, 0.15)))
    
    return traffic_index, parking_pressure


def forecast_30min(traffic_index: float) -> float:
    """
    30분 뒤 교통 지수를 예측합니다.
    
    Args:
        traffic_index: 현재 교통 지수 (0.0 ~ 1.0)
    
    Returns:
        float: 30분 뒤 예측 교통 지수 (0.0 ~ 1.0)
    
    ※ 실데이터 연동 시:
       - ML 모델 예측값으로 교체
       - 시계열 예측 (ARIMA, LSTM 등)
    """
    now = datetime.now(KST)
    hour = now.hour
    
    # 단순 룰: 피크타임 진입 시 증가, 이탈 시 감소
    if 11 <= hour < 13:
        trend = 0.1  # 점심 피크 진입
    elif 14 <= hour < 17:
        trend = 0.05  # 오후 유지
    elif 17 <= hour < 19:
        trend = -0.1  # 저녁 감소
    else:
        trend = 0.0
    
    # 랜덤 노이즈
    noise = random.uniform(-0.05, 0.05)
    
    forecast = traffic_index + trend + noise
    return max(0.0, min(1.0, forecast))


def score_difficulty(traffic_index: float, parking_pressure: float) -> int:
    """
    혼잡도와 주차 압박도를 종합하여 난이도 점수를 계산합니다.
    
    Args:
        traffic_index: 교통 지수 (0.0 ~ 1.0)
        parking_pressure: 주차 압박도 (0.0 ~ 1.0)
    
    Returns:
        int: 난이도 점수 (0 ~ 100)
    
    시그모이드 함수로 중간값 강조
    """
    # 가중 평균
    combined = traffic_index * 0.6 + parking_pressure * 0.4
    
    # 시그모이드 변환 (0~1 → 0~100)
    # 중앙값(0.5)에서 50점, 극단값에서 0/100에 가까워짐
    sigmoid_input = (combined - 0.5) * 8  # 스케일 조정
    sigmoid_value = 1 / (1 + math.exp(-sigmoid_input))
    
    return int(round(sigmoid_value * 100))


def level_from_score(score: int) -> str:
    """
    점수를 레벨 문자열로 변환합니다.
    
    Args:
        score: 난이도 점수 (0 ~ 100)
    
    Returns:
        str: "EASY" | "MODERATE" | "HARD" | "VERY_HARD"
    """
    if score < 30:
        return "EASY"
    elif score < 55:
        return "MODERATE"
    elif score < 75:
        return "HARD"
    else:
        return "VERY_HARD"


def message_from_level(level: str, is_forecast: bool = False) -> str:
    """
    레벨에 따른 사용자 안내 문구를 반환합니다.
    
    Args:
        level: 레벨 문자열
        is_forecast: 예측 메시지 여부
    
    Returns:
        str: 안내 문구
    """
    prefix = "30분 뒤 " if is_forecast else "현재 "
    
    messages = {
        "EASY": f"{prefix}한옥마을은 여유롭습니다. 방문하기 좋은 시간입니다! 🟢",
        "MODERATE": f"{prefix}한옥마을은 적당히 붐빕니다. 주차 공간을 미리 확인하세요. 🟡",
        "HARD": f"{prefix}한옥마을이 혼잡합니다. 대중교통 이용을 권장합니다. 🟠",
        "VERY_HARD": f"{prefix}한옥마을이 매우 혼잡합니다. 방문 시간 조정을 권장합니다. 🔴",
    }
    
    return messages.get(level, "정보를 확인할 수 없습니다.")


# ============================================================
# API 엔드포인트
# ============================================================

@app.get("/")
async def root():
    """
    메인 페이지 (대시보드 HTML) 반환
    """
    return FileResponse("static/index.html")


@app.get("/api/status")
async def get_status():
    """
    현재 혼잡도 + 30분 뒤 예측 + 난이도 점수 반환
    
    Returns:
        JSON 응답:
        - area: 지역명
        - now_kst: 현재 시각 (ISO 8601)
        - traffic_index_now: 현재 교통 지수
        - traffic_index_forecast_30m: 30분 뒤 예측 교통 지수
        - difficulty_now_0_100: 현재 난이도 점수 (0~100)
        - difficulty_30m_0_100: 30분 뒤 난이도 점수 (0~100)
        - level_now: 현재 레벨
        - level_30m: 30분 뒤 레벨
        - message: 사용자 안내 문구
        - notes: 데이터 출처 안내
    """
    # 현재 시각
    now = datetime.now(KST)
    
    # 실시간 특성값 조회 (※ 실데이터 연동 시 이 함수만 교체)
    traffic_index_now, parking_pressure_now = get_realtime_features()
    
    # 30분 뒤 예측
    traffic_index_30m = forecast_30min(traffic_index_now)
    parking_pressure_30m = parking_pressure_now * 0.9 + random.uniform(0, 0.1)  # 단순 추정
    
    # 난이도 점수 계산
    difficulty_now = score_difficulty(traffic_index_now, parking_pressure_now)
    difficulty_30m = score_difficulty(traffic_index_30m, parking_pressure_30m)
    
    # 레벨 결정
    level_now = level_from_score(difficulty_now)
    level_30m = level_from_score(difficulty_30m)
    
    # 안내 메시지
    message_now = message_from_level(level_now, is_forecast=False)
    message_30m = message_from_level(level_30m, is_forecast=True)
    
    return {
        "area": "Jeonju Hanok Village",
        "area_kr": "전주 한옥마을",
        "now_kst": now.isoformat(),
        "traffic_index_now": round(traffic_index_now, 3),
        "traffic_index_forecast_30m": round(traffic_index_30m, 3),
        "parking_pressure_now": round(parking_pressure_now, 3),
        "difficulty_now_0_100": difficulty_now,
        "difficulty_30m_0_100": difficulty_30m,
        "level_now": level_now,
        "level_30m": level_30m,
        "message": message_now,
        "message_30m": message_30m,
        "notes": "현재 더미(룰 기반) 데이터로 동작 중입니다. 추후 실시간 교통/주차 API 연동 예정.",
    }


@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {"status": "healthy", "timestamp": datetime.now(KST).isoformat()}
