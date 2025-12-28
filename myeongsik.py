from datetime import date

HEAVENLY_STEMS = ["갑","을","병","정","무","기","경","신","임","계"]
EARTHLY_BRANCHES = ["자","축","인","묘","진","사","오","미","신","유","술","해"]
INWOL_STEM_BY_YEAR_STEM = {
    "갑": "병", "기": "병",
    "을": "무", "경": "무",
    "병": "경", "신": "경",
    "정": "임", "임": "임",
    "무": "갑", "계": "갑",
}
# 일간(=일주의 천간) -> 자시(子時)의 시각(시간 천간) 시작값
ZI_STEM_BY_DAY_STEM = {
    "갑": "갑", "기": "갑",
    "을": "병", "경": "병",
    "병": "무", "신": "무",
    "정": "경", "임": "경",
    "무": "임", "계": "임",
}



def get_year_ganji(year, month, day):
    """
    month, day 기준으로 입춘 이전이면 자동 보정
    """
    # 입춘 이전이면 전년도 사용
    is_before_ipchun = (month < 2) or (month == 2 and day < 4)
    if is_before_ipchun:
        year -= 1

    BASE_YEAR = 1924  # 갑자년
    diff = year - BASE_YEAR
    idx = diff % 60

    stem = HEAVENLY_STEMS[idx % 10]
    branch = EARTHLY_BRANCHES[idx % 12]

    return stem + branch


def get_month_branch(month, day):
    """
    절기 기준 월지 (간단 버전)
    """
    if (month == 2 and day >= 4) or (month == 3 and day < 6):
        return "인"
    elif (month == 3 and day >= 6) or (month == 4 and day < 5):
        return "묘"
    elif (month == 4 and day >= 5) or (month == 5 and day < 6):
        return "진"
    elif (month == 5 and day >= 6) or (month == 6 and day < 6):
        return "사"
    elif (month == 6 and day >= 6) or (month == 7 and day < 7):
        return "오"
    elif (month == 7 and day >= 7) or (month == 8 and day < 8):
        return "미"
    elif (month == 8 and day >= 8) or (month == 9 and day < 8):
        return "신"
    elif (month == 9 and day >= 8) or (month == 10 and day < 8):
        return "유"
    elif (month == 10 and day >= 8) or (month == 11 and day < 7):
        return "술"
    elif (month == 11 and day >= 7) or (month == 12 and day < 7):
        return "해"
    elif (month == 12 and day >= 7) or (month == 1 and day < 6):
        return "자"
    else:
        return "축"
    

def get_month_ganji(year_stem, month, day):
    """
    year_stem : 연주의 천간 (ex. '갑', '을')
    """
    # 월지 구하기
    month_branch = get_month_branch(month, day)

    # 인월의 천간 결정
    inwol_stem = INWOL_STEM_BY_YEAR_STEM[year_stem]

    # 인월 기준으로 몇 번째 달인지 계산
    branch_index = EARTHLY_BRANCHES.index(month_branch)
    inwol_index = EARTHLY_BRANCHES.index("인")
    offset = (branch_index - inwol_index) % 12

    # 월간 계산
    stem_index = (HEAVENLY_STEMS.index(inwol_stem) + offset) % 10
    month_stem = HEAVENLY_STEMS[stem_index]

    return month_stem + month_branch


def get_day_ganji(year, month, day):
    """
    일주(日柱) 계산
    기준일: 1900-01-31 = 갑자일
    """
    base_date = date(1900, 1, 31)  # 갑자일
    target_date = date(year, month, day)

    diff_days = (target_date - base_date).days
    idx = diff_days % 60

    stem = HEAVENLY_STEMS[idx % 10]
    branch = EARTHLY_BRANCHES[idx % 12]

    return stem + branch


def hour_to_branch(hour: int, minute: int = 0) -> str:
    """
    시지(지지) 결정 (2시간 단위)
    - 자시: 23:00~00:59
    - 축시: 01:00~02:59
    - ...
    """
    if not (0 <= hour <= 23) or not (0 <= minute <= 59):
        raise ValueError("hour(0~23), minute(0~59) 범위여야 합니다.")

    # 23시는 자시로 취급
    if hour == 23:
        return "자"

    # 0~22시는 2시간 단위로 나눔: 0~0:59=자, 1~2=축, 3~4=인 ...
    idx = ((hour + 1) // 2) % 12
    return EARTHLY_BRANCHES[idx]


def get_hour_ganji(day_stem: str, hour: int, minute: int = 0) -> str:
    """
    시주(時柱) 계산
    day_stem: 일간(예: '갑','을'...)  -> 일주의 천간만 넣으면 됨
    hour, minute: 출생 시각 (24시간제)
    """
    if day_stem not in ZI_STEM_BY_DAY_STEM:
        raise ValueError(f"day_stem은 {list(ZI_STEM_BY_DAY_STEM.keys())} 중 하나여야 합니다.")

    branch = hour_to_branch(hour, minute)

    # 자시를 기준으로 몇 번째 시지인지(자=0, 축=1, ... 해=11)
    offset = EARTHLY_BRANCHES.index(branch)

    # 자시의 시각 천간에서 offset만큼 천간을 순환
    zi_stem = ZI_STEM_BY_DAY_STEM[day_stem]
    stem_idx = (HEAVENLY_STEMS.index(zi_stem) + offset) % 10
    stem = HEAVENLY_STEMS[stem_idx]

    return stem + branch


def get_myeongsik(year, month, day, hour=None, minute=0):
    """
    사주 명식(연주·월주·일주·시주) 통합 계산
    hour가 None이면 시주는 '??' 처리
    """

    # 1. 연주
    year_ganji = get_year_ganji(year, month, day)
    year_stem = year_ganji[0]

    # 2. 월주
    month_ganji = get_month_ganji(year_stem, month, day)

    # 3. 일주
    day_ganji = get_day_ganji(year, month, day)
    day_stem = day_ganji[0]

    # 4️. 시주
    if hour is None:
        hour_ganji = "??"
    else:
        hour_ganji = get_hour_ganji(day_stem, hour, minute)

    return {
        "year": year_ganji,
        "month": month_ganji,
        "day": day_ganji,
        "hour": hour_ganji,
    }


# print(get_myeongsik(1984, 2, 2, 23))