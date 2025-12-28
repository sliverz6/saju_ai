FIVE_ELEMENTS = ["목", "화", "토", "금", "수"]

STEM_TO_ELEMENT = {
    "갑": "목", "을": "목",
    "병": "화", "정": "화",
    "무": "토", "기": "토",
    "경": "금", "신": "금",
    "임": "수", "계": "수",
}

BRANCH_TO_ELEMENT = {
    "자": "수",
    "축": "토",
    "인": "목",
    "묘": "목",
    "진": "토",
    "사": "화",
    "오": "화",
    "미": "토",
    "신": "금",
    "유": "금",
    "술": "토",
    "해": "수",
}

def calc_ohaeng(myeongsik: dict) -> dict:
    """
    myeongsik 예:
    {"year":"계해","month":"을축","day":"병인","hour":"무자"}  (hour는 '??' 가능)

    반환:
    {
      "counts": {"목":2,"화":1,"토":2,"금":0,"수":3},
      "details": {"stems":[...],"branches":[...]}
    }
    """
    counts = {e: 0 for e in FIVE_ELEMENTS}
    stem_elems = []
    branch_elems = []

    for key in ("year", "month", "day", "hour"):
        ganji = myeongsik.get(key)
        if not ganji or ganji == "??":
            continue

        stem = ganji[0]
        branch = ganji[1]

        se = STEM_TO_ELEMENT.get(stem)
        be = BRANCH_TO_ELEMENT.get(branch)

        if se:
            counts[se] += 1
            stem_elems.append((key, stem, se))

        if be:
            counts[be] += 1
            branch_elems.append((key, branch, be))

    return {
        "counts": counts,
        # "details": {
        #     "stems": stem_elems,
        #     "branches": branch_elems,
        # }
    }
