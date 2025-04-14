import streamlit as st
import pandas as pd

# 데이터 불러오기
data = pd.read_csv('age.csv')

# Streamlit 제목
st.title('행정구역별 인구 시각화')

# 행정구역 선택
selected_area = st.selectbox('행정구역을 선택하세요:', data['행정구역'].unique())

# 선택된 행정구역의 데이터 필터링
filtered_data = data[data['행정구역'] == selected_area]

# 0세부터 100세 이상의 인구 수 데이터 추출
age_population = filtered_data.iloc[0, 3:104].values  # 3번 인덱스부터 103번 인덱스까지
age_labels = [f"{i}세" for i in range(101)] + ['100세 이상']

# Streamlit의 바 차트 시각화
st.bar_chart(age_population, x=age_labels, width=700, height=400)

# 연령대별 인구 수 제목
st.write(f'{selected_area}의 연령대별 인구 수')
