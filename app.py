import streamlit as st
from myeongsik import get_myeongsik
from ohaeng import calc_ohaeng
from ai_interpreter import get_result
import datetime

MIN_DATE = datetime.date(1900, 1, 1)

if 'result' not in st.session_state:
  st.session_state['result'] = ''

if 'loading' not in st.session_state:
  st.session_state['loading'] = False

st.title('사주 AI')

date = st.date_input('생년/월/일', value=None, min_value=MIN_DATE)
time = st.time_input('시/분', value=None)

if st.button('사주 보기'):
  if date and time:
    with st.spinner('해석 중...'):
      myeongsik = get_myeongsik(date.year, date.month, date.day, time.hour, time.minute)
      ohaeng = calc_ohaeng(myeongsik)
      st.session_state['result'] = get_result(ohaeng)

st.divider()
st.subheader('결과')

if st.session_state['result']:
  st.write(st.session_state['result'])
else:
  st.write('내용이 없습니다.')