# analyze_myeongsik.py (혹은 analysis.py)

FIVE_ELEMENTS = ["목", "화", "토", "금", "수"]

STEM_TO_ELEMENT = {
    "갑": "목", "을": "목",
    "병": "화", "정": "화",
    "무": "토", "기": "토",
    "경": "금", "신": "금",
    "임": "수", "계": "수",
}

BRANCH_TO_ELEMENT = {
    "자": "수", "축": "토", "인": "목", "묘": "목",
    "진": "토", "사": "화", "오": "화", "미": "토",
    "신": "금", "유": "금", "술": "토", "해": "수",
}

# 월지(지지) -> 계절/기운 요약 (MVP용 간단 매핑)
BRANCH_TO_SEASON = {
    "인": "봄", "묘": "봄", "진": "봄(환절)",
    "사": "여름", "오": "여름", "미": "여름(환절)",
    "신": "가을", "유": "가을", "술": "가을(환절)",
    "해": "겨울", "자": "겨울", "축": "겨울(환절)",
}

def _level(count: int) -> str:
    """오행 개수를 사람이 읽기 쉽게 등급화 (MVP 규칙)"""
    if count <= 0:
        return "없음"
    if count == 1:
        return "약함"
    if count == 2:
        return "보통"
    if count == 3:
        return "강함"
    return "매우 강함"

def analyze_myeongsik(myeongsik: dict, ohaeng_counts: dict | None = None) -> dict:
    """
    입력:
      myeongsik: {"year":"계해","month":"을축","day":"병인","hour":"무자" or "??"}
      ohaeng_counts: {"목":1,"화":1,"토":3,"금":0,"수":3} (없으면 내부에서 계산)

    출력(예):
      {
        "pillars": {...},
        "day_master": {"stem":"병","element":"화"},
        "month": {"branch":"축","season":"겨울(환절)"},
        "ohaeng": {
          "counts": {...},
          "levels": {...},
          "most": ["토","수"],
          "least": ["금"],
          "missing": ["금"],
          "weak": ["목","화"],
          "strong": ["토","수"]
        },
        "notes": [...]
      }
    """
    # --- 기본 검증 ---
    for k in ("year", "month", "day"):
        if k not in myeongsik or not myeongsik[k] or myeongsik[k] == "??":
            raise ValueError(f"myeongsik['{k}'] 값이 필요합니다.")

    year_gj = myeongsik["year"]
    month_gj = myeongsik["month"]
    day_gj = myeongsik["day"]
    hour_gj = myeongsik.get("hour", "??")

    day_stem = day_gj[0]
    if day_stem not in STEM_TO_ELEMENT:
        raise ValueError(f"일간(일주의 천간) '{day_stem}'을 해석할 수 없습니다.")

    day_elem = STEM_TO_ELEMENT[day_stem]

    # --- 월지/계절 ---
    month_branch = month_gj[1]
    season = BRANCH_TO_SEASON.get(month_branch, "알 수 없음")

    # --- 오행 카운트 없으면 내부 계산(천간+지지 8글자 기준) ---
    if ohaeng_counts is None:
        # 아주 간단 계산: 각 기둥의 천간+지지 각각 1점
        ohaeng_counts = {e: 0 for e in FIVE_ELEMENTS}
        for key in ("year", "month", "day", "hour"):
            gj = myeongsik.get(key)
            if not gj or gj == "??":
                continue
            stem, branch = gj[0], gj[1]
            ohaeng_counts[STEM_TO_ELEMENT[stem]] += 1
            ohaeng_counts[BRANCH_TO_ELEMENT[branch]] += 1
    else:
        # 누락 키 보정
        ohaeng_counts = {e: int(ohaeng_counts.get(e, 0)) for e in FIVE_ELEMENTS}

    # --- 오행 요약/등급 ---
    levels = {e: _level(ohaeng_counts[e]) for e in FIVE_ELEMENTS}

    max_v = max(ohaeng_counts.values()) if ohaeng_counts else 0
    min_v = min(ohaeng_counts.values()) if ohaeng_counts else 0

    most = [e for e, v in ohaeng_counts.items() if v == max_v and max_v > 0]
    least = [e for e, v in ohaeng_counts.items() if v == min_v]

    missing = [e for e, v in ohaeng_counts.items() if v == 0]
    weak = [e for e, v in ohaeng_counts.items() if v == 1]
    strong = [e for e, v in ohaeng_counts.items() if v >= 3]

    notes = []
    if hour_gj == "??":
        notes.append("태어난 시간이 없어 시주/오행 분포가 일부 달라질 수 있습니다.")
    if missing:
        notes.append(f"부족 오행(0): {', '.join(missing)}")
    if strong:
        notes.append(f"강한 오행(3+): {', '.join(strong)}")

    return {
        "pillars": {
            "year": year_gj,
            "month": month_gj,
            "day": day_gj,
            "hour": hour_gj,
        },
        "day_master": {
            "stem": day_stem,          # 일간
            "element": day_elem,       # 일간 오행
        },
        "month": {
            "branch": month_branch,    # 월지
            "season": season,          # 계절 요약
        },
        "ohaeng": {
            "counts": ohaeng_counts,
            "levels": levels,
            "most": most,
            "least": least,
            "missing": missing,
            "weak": weak,
            "strong": strong,
        },
        "notes": notes,
    }


