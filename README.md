# Jeonju Hanok Village Traffic & Crowd Insight  
## 전북 디지털 시드 캠프 · 우수상(2등)

![Poster](./assets/poster.png)

> 수상: 전북 디지털 시드 캠프 우수상(2등)  
> 대회 특징: 하루(1-day) 안에 문제 정의 → 솔루션 제시 → (가능 범위) 구현 → 발표 까지 완료하는 실전 프로젝트  
> 노션(팀 공유 페이지): https://www.notion.so/1-2fc42fd1015480b3aebbe214374dd528?source=copy_link

![Award](./assets/award.jpg)

---

## 0) Quick Links
- 발표자료(대회 발표본으로 간주): [presentation_mid.pdf](./assets/presentation_mid.pdf)  
- 발표자료(대회 이후 보완본/확장본): [AI_Mobility_Tourism_Transformation.pdf](C:\Users\eys63\GitHub\camp\assets\AI_Mobility_Tourism_Transformation.pdf)

---

## 1) 프로젝트 한 줄 요약
전주 한옥마을의 **교통 혼잡·주차난**이 관광 경험에 미치는 불편을 문제로 정의하고,  
**실시간 혼잡 예측 + 대안 이동(MaaS) 유도 + 보행 안전/혼잡 관리**까지 확장 가능한  
“스마트 모빌리티 & AI IoT 플랫폼” 컨셉의 솔루션을 제안했습니다.

---

## 2) 문제 정의(Why)
한옥마을은 피크 시간대에 반복적으로
- 진입로 정체 및 불법 주정차
- 주차난(공영/민영 가격·수용 한계)
- 관광 동선 혼잡
이 발생해 관광객 만족도/재방문/소비에 영향을 줄 수 있습니다.

본 프로젝트는 이를 **교통 정보 제공과 수요 분산 전략**으로 완화하여,  
“교통이 풀리면 지역 경제의 혈관이 뚫린다”라는 메시지로 지역 관광 활성화를 목표로 했습니다.

---

## 3) 대회 제약과 MVP 범위(1-day 해커톤 현실)
이 대회는 하루 안에 문제 정의부터 솔루션 제시, 최소 구현, 발표까지 끝내야 했습니다.  
물리적으로 시간이 부족하여, 본 레포에서는 **프론트엔드 중심 MVP(서비스 틀)**을 우선 구현했고,  
발표에서는 아래 “향후 구현 계획”을 구체적인 실행 단계로 제시했습니다.

---

## 4) MVP(대회 당일 구현한 것)
- 사용자가 “현재/예측 혼잡”을 직관적으로 볼 수 있는 **프론트엔드 프로토타입(틀)** 구현
- 클라우드(VM) 환경에서 실행 가능하도록 구성하여 동작 확인

> NOTE: 이 레포의 구현은 ‘실데이터 연동/모델 학습’ 이전 단계에서  
> “서비스 형태(UX/흐름/배포 가능성)”를 빠르게 증명하기 위한 MVP입니다.

---

## 5) 솔루션 컨셉(발표안)
발표자료 기준 솔루션은 3개 축으로 구성했습니다.

1) **AI Traffic Prediction (지능형 수요 관리)**  
- IoT 센서/영상 기반으로 정체를 예측하고 사전 분산

2) **Smart MaaS (관광 연계 이동)**  
- 외곽 주차장 + 셔틀/공유 모빌리티로 한옥마을 접근 최적화

3) **Safe Walking Zone (보행자 안전·혼잡)**  
- 사고 다발/혼잡 구역을 인지해 보행 안전 확보

---

## 6) My Role (Tech Lead & Engineering)
3인 팀 프로젝트에서 **아이디어 구상/문제 정의부터 1-day MVP 개발 및 클라우드 배포까지 기술 구현을 주도**했습니다.

1) **기획 구체화 (Planning & Pivot)**  
- 포괄적인 ‘여행’ 주제를 데이터 기반 해결이 가능한 ‘관광지 교통 문제 해결’로 구체화(Pivot) 제안  
- ‘문제 정의 → 분석 → 솔루션’으로 이어지는 논리적 흐름 설계

2) **개발 총괄 (End-to-End Dev)**  
- 제한된 시간(1-day)에서 결과물을 내기 위해 **MVP 설계/구현/클라우드 배포를 전담**  
- 프론트엔드부터 서버 환경 구성까지 단독 수행(구현 파트 전담)

3) **기술 커뮤니케이션**  
- 구현 내용이 발표자료/발표 흐름에 정확히 반영되도록 팀 내 조율  
- 발표에서 구현 파트 발표 및 기술 Q&A 대응

> 팀원들은 발표자료 제작 및 발표 진행을 담당했습니다.

---

## 7) (향후 구현) 실제 서비스로 확장하는 로드맵
### 7.1 데이터 확보
- 학과 GPU 서버로 학습 환경 확보
- Roboflow / Kaggle / 오픈 데이터셋에서 차량 바운딩박스 이미지 확보
- 가능하다면 전주 지역 CCTV 프레임을 추가 수집하여 도메인 적합성 강화

### 7.2 모델 학습(차량/보행자 객체탐지)
- 차량 탐지 → 프레임 내 차량 수(방향별) 추정 → 도로 혼잡 지표로 변환
- 사람 탐지(확장) → 보행 혼잡/웨이팅(줄 서 있는 사람) 추정

### 7.3 실시간 운영(영상 입력)
- 카카오/네이버 지도 등에서 제공되는 CCTV 영상 또는 지자체 CCTV 소스/API 확보(가능한 방식 탐색)
- 실시간 영상에서 일부 프레임만 샘플링하여 추론 비용 최소화
- CCTV 메타정보(위치/도로 방향/관광지 유입 방향)를 함께 관리하여  
  “어느 방향의 증가가 한옥마을 혼잡을 유발하는지”까지 반영

### 7.4 사용자 행동 추천(서비스 핵심)
- 목적지가 혼잡하면 외곽 주차 + 도보/대중교통 등 대안 추천
- 보행 혼잡/웨이팅이 높은 구간은 혼잡 회피 동선 안내

### 7.5 안전/상황 확장(사고·기상)
- 실시간 교통사고 접수/발생 구간 API 연동이 가능하다면, 사고 구간 안내 및 우회 추천
- 눈/비 등 기상 악화 시 사고 위험을 함께 경고하여 안전한 이동을 지원

---

## 8) How to Run (Local / VM)

### 8.1 Requirements
- Python 3.9+ (권장: 3.10+)
- pip

### 8.2 Run locally
```bash
git clone https://github.com/eys632/jeonbook_digital_seed_camp.git
cd jeonbook_digital_seed_camp

python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

브라우저에서 접속:
- http://localhost:8000/

### 8.3 Run on Kakao Cloud VM (예시)
```bash
sudo apt update
sudo apt install -y git python3-pip

git clone https://github.com/eys632/jeonbook_digital_seed_camp.git
cd jeonbook_digital_seed_camp

pip3 install -r requirements.txt
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
```

- VM 보안그룹 인바운드에 TCP 8000 오픈 필요
- 접속: http://<VM_PUBLIC_IP>:8000/


## 9) Repository Structure
```text
.
├── app.py                 # 백엔드(서버) 엔트리
├── requirements.txt       # 의존성
├── static/                # 대회 당일 제작한 프론트 MVP(틀)
└── assets/                # 포스터/수상사진/발표자료(PDF)
```

- `static/`에는 대회 시간 제약 내에서 만든 **프론트엔드 프로토타입(서비스 화면/구조)**가 포함되어 있습니다.
- `assets/presentation_mid.pdf`는 **대회 발표 흐름/핵심 메시지**를 담은 발표자료로 사용했습니다(슬라이드 1장 정도 차이는 있으나 메시지 동일).
- `assets/AI_Mobility_Tourism_Transformation.pdf`는 **대회 이후 팀원이 완성도를 높이기 위해 보완/수정한 버전**입니다.


## 10) Presentation / Docs
- 발표자료(PDF, 대회 발표본으로 간주): [presentation_mid.pdf](./assets/presentation_mid.pdf)
- 발표자료(PDF, 대회 이후 보완본): [AI_Mobility_Tourism_Transformation.pdf](C:\Users\eys63\GitHub\camp\assets\AI_Mobility_Tourism_Transformation.pdf)


## Links
- Team Notion: https://www.notion.so/1-2fc42fd1015480b3aebbe214374dd528?source=copy_link
