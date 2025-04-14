import streamlit as st
import pandas as pd

# 데이터 불러오기
data = pd.read_csv('age.csv')  # 여기에 파일 경로를 적절히 입력하세요.

# Streamlit 제목
st.title('한국 인구 통계 시각화')

# 지역 선택 (드롭다운)
지역들 = data['행정구역'].unique()
선택된_지역 = st.selectbox('지역을 선택하세요:', 지역들)

# 선택한 지역의 데이터 필터링
선택한_데이터 = data[data['행정구역'] == 선택된_지역]

# 연령대 데이터 추출
연령대_열 = 선택한_데이터.columns[3:]  # 3열 이후의 인구 통계 데이터
인구수 = 선택한_데이터.iloc[0, 3:].astype(int)

# Streamlit에서 막대 그래프 시각화
st.bar_chart(인구수)

# 선택된 연령대의 레이블 설정
st.write(f"{선택된_지역}의 연령대별 인구 수")
st.write(pd.DataFrame({'연령대': 연령대_열, '인구 수': 인구수}).set_index('연령대'))
