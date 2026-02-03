"""
관광지 혼잡/주차 난이도 MVP - Backend
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
from typing import Tuple, Optional, List

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# ============================================================
# FastAPI 앱 설정
# ============================================================
app = FastAPI(
    title="관광지 혼잡/주차 난이도 MVP",
    description="실시간 혼잡도 및 주차 난이도를 제공하는 API",
    version="2.0.0",
)

# 정적 파일 서빙 (CSS, JS 등 추가 시 사용)
app.mount("/static", StaticFiles(directory="static"), name="static")

# KST 타임존
KST = timezone(timedelta(hours=9))

# ============================================================
# 지원 지역 데이터베이스
# ※ 실데이터 연동 시 DB 또는 외부 API로 교체
# ============================================================
AREAS = {
    # ===== 전주시 =====
    "jeonju-hanok": {
        "id": "jeonju-hanok",
        "name": "Jeonju Hanok Village",
        "name_kr": "전주 한옥마을",
        "region": "전주시",
        "category": "전통마을",
        "base_popularity": 0.85,
        "emoji": "🏘️",
    },
    "jeonju-nambu": {
        "id": "jeonju-nambu",
        "name": "Jeonju Nambu Market",
        "name_kr": "남부시장",
        "region": "전주시",
        "category": "전통시장",
        "base_popularity": 0.7,
        "emoji": "🏪",
    },
    "jeonju-gaeksa": {
        "id": "jeonju-gaeksa",
        "name": "Jeonju Gaeksa",
        "name_kr": "전주객사",
        "region": "전주시",
        "category": "문화유적",
        "base_popularity": 0.5,
        "emoji": "🏛️",
    },
    "jeonju-omokdae": {
        "id": "jeonju-omokdae",
        "name": "Omokdae Pavilion",
        "name_kr": "오목대",
        "region": "전주시",
        "category": "전망대",
        "base_popularity": 0.6,
        "emoji": "🏯",
    },
    "jeonju-gyeonggijeon": {
        "id": "jeonju-gyeonggijeon",
        "name": "Gyeonggijeon Shrine",
        "name_kr": "경기전",
        "region": "전주시",
        "category": "문화유적",
        "base_popularity": 0.75,
        "emoji": "⛩️",
    },
    "jeonju-pungnammun": {
        "id": "jeonju-pungnammun",
        "name": "Pungnammun Gate",
        "name_kr": "풍남문",
        "region": "전주시",
        "category": "문화유적",
        "base_popularity": 0.55,
        "emoji": "🚪",
    },
    "jeonju-deokjin": {
        "id": "jeonju-deokjin",
        "name": "Deokjin Park",
        "name_kr": "덕진공원",
        "region": "전주시",
        "category": "공원",
        "base_popularity": 0.6,
        "emoji": "🌳",
    },
    # ===== 전북 기타 지역 =====
    "jeonbuk-maisan": {
        "id": "jeonbuk-maisan",
        "name": "Maisan Mountain",
        "name_kr": "마이산",
        "region": "진안군",
        "category": "자연경관",
        "base_popularity": 0.7,
        "emoji": "⛰️",
    },
    "jeonbuk-naejangsan": {
        "id": "jeonbuk-naejangsan",
        "name": "Naejangsan National Park",
        "name_kr": "내장산",
        "region": "정읍시",
        "category": "국립공원",
        "base_popularity": 0.75,
        "emoji": "🍁",
    },
    "jeonbuk-byeonsan": {
        "id": "jeonbuk-byeonsan",
        "name": "Byeonsanbando National Park",
        "name_kr": "변산반도",
        "region": "부안군",
        "category": "국립공원",
        "base_popularity": 0.65,
        "emoji": "🏖️",
    },
    "jeonbuk-gunsan": {
        "id": "jeonbuk-gunsan",
        "name": "Gunsan Modern History Museum",
        "name_kr": "군산 근대역사박물관",
        "region": "군산시",
        "category": "박물관",
        "base_popularity": 0.6,
        "emoji": "🏛️",
    },
    "jeonbuk-imsil": {
        "id": "jeonbuk-imsil",
        "name": "Imsil Cheese Village",
        "name_kr": "임실치즈마을",
        "region": "임실군",
        "category": "체험마을",
        "base_popularity": 0.55,
        "emoji": "🧀",
    },
    "jeonbuk-gochang": {
        "id": "jeonbuk-gochang",
        "name": "Gochang Dolmen Site",
        "name_kr": "고창 고인돌",
        "region": "고창군",
        "category": "세계유산",
        "base_popularity": 0.5,
        "emoji": "🪨",
    },
    "jeonbuk-sunchang": {
        "id": "jeonbuk-sunchang",
        "name": "Sunchang Gochujang Village",
        "name_kr": "순창 고추장마을",
        "region": "순창군",
        "category": "체험마을",
        "base_popularity": 0.45,
        "emoji": "🌶️",
    },
}


# ============================================================
# 더미 데이터 생성 함수들
# ※ 실데이터 연동 시 get_realtime_features()만 교체하면 됨
# ============================================================

def get_realtime_features(area_id: str = "jeonju-hanok") -> Tuple[float, float]:
    """
    실시간 특성값을 반환합니다.
    
    Args:
        area_id: 지역 ID
    
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
    
    # 지역별 기본 인기도 반영
    area_info = AREAS.get(area_id, AREAS["jeonju-hanok"])
    popularity = area_info["base_popularity"]
    
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
    
    # 지역 인기도 반영
    base_traffic = base_traffic * popularity
    
    # 주말 가중치
    if weekday >= 5:  # 토, 일
        base_traffic = min(1.0, base_traffic * 1.3)
    
    # 약간의 랜덤 변동 추가 (지역별 시드로 일관성 유지)
    random.seed(hash(area_id + str(hour) + str(now.minute // 5)))
    traffic_index = max(0.0, min(1.0, base_traffic + random.uniform(-0.1, 0.1)))
    
    # 주차 압박도 (교통량에 비례 + 랜덤)
    parking_pressure = max(0.0, min(1.0, traffic_index * 0.9 + random.uniform(0, 0.15)))
    
    # 시드 초기화
    random.seed()
    
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


def message_from_level(level: str, area_name: str = "한옥마을", is_forecast: bool = False) -> str:
    """
    레벨에 따른 사용자 안내 문구를 반환합니다.
    
    Args:
        level: 레벨 문자열
        area_name: 지역 이름
        is_forecast: 예측 메시지 여부
    
    Returns:
        str: 안내 문구
    """
    prefix = "30분 뒤 " if is_forecast else "현재 "
    
    messages = {
        "EASY": f"{prefix}{area_name}은(는) 여유롭습니다. 방문하기 좋은 시간입니다! 🟢",
        "MODERATE": f"{prefix}{area_name}은(는) 적당히 붐빕니다. 주차 공간을 미리 확인하세요. 🟡",
        "HARD": f"{prefix}{area_name}이(가) 혼잡합니다. 대중교통 이용을 권장합니다. 🟠",
        "VERY_HARD": f"{prefix}{area_name}이(가) 매우 혼잡합니다. 방문 시간 조정을 권장합니다. 🔴",
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
async def get_status(area: str = Query(default="jeonju-hanok", description="지역 ID")):
    """
    현재 혼잡도 + 30분 뒤 예측 + 난이도 점수 반환
    
    Args:
        area: 지역 ID (예: jeonju-hanok, gyeongbokgung, haeundae 등)
    
    Returns:
        JSON 응답:
        - area: 지역명 (영문)
        - area_kr: 지역명 (한글)
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
    # 지역 정보 조회
    area_info = AREAS.get(area)
    if not area_info:
        return {
            "error": "지역을 찾을 수 없습니다.",
            "available_areas": list(AREAS.keys())
        }
    
    # 현재 시각
    now = datetime.now(KST)
    
    # 실시간 특성값 조회 (※ 실데이터 연동 시 이 함수만 교체)
    traffic_index_now, parking_pressure_now = get_realtime_features(area)
    
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
    message_now = message_from_level(level_now, area_info["name_kr"], is_forecast=False)
    message_30m = message_from_level(level_30m, area_info["name_kr"], is_forecast=True)
    
    return {
        "area_id": area_info["id"],
        "area": area_info["name"],
        "area_kr": area_info["name_kr"],
        "region": area_info["region"],
        "category": area_info["category"],
        "emoji": area_info["emoji"],
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


@app.get("/api/areas")
async def get_areas(search: Optional[str] = Query(default=None, description="검색어")):
    """
    지원하는 지역 목록 반환
    
    Args:
        search: 검색어 (선택, 지역명/카테고리로 필터링)
    
    Returns:
        지역 목록
    """
    areas_list = list(AREAS.values())
    
    # 검색어 필터링
    if search:
        search_lower = search.lower()
        areas_list = [
            area for area in areas_list
            if search_lower in area["name"].lower()
            or search_lower in area["name_kr"]
            or search_lower in area["region"]
            or search_lower in area["category"]
        ]
    
    return {
        "total": len(areas_list),
        "areas": areas_list
    }


@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {"status": "healthy", "timestamp": datetime.now(KST).isoformat()}
