from unittest import result
from myeongsik import get_myeongsik
from ohaeng import calc_ohaeng
from analysis_myeongsik import analyze_myeongsik
from ai_interpreter import storytelling_from_ohaeng


m = get_myeongsik(1986, 6, 8, 8, 20)  # 형
# m = get_myeongsik(1993, 6, 16, 13, 30)
# m = get_myeongsik(1961, 1, 4, 12)
print(m)
o = calc_ohaeng(m)  # 네가 만든 counts 형태(목/화/토/금/수)
print(o)
# result = storytelling_from_ohaeng(o)
# print(result)
