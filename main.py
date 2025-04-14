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

# 0세부터 99세까지의 인구 수 데이터 추출
age_population = filtered_data.iloc[0, 3:103].values  # 0세부터 99세까지
age_population_100_plus = filtered_data.iloc[0, 103]  # 100세 이상 인구 수

# 연령대 라벨 생성
age_labels = [f"{i}세" for i in range(100)] + ['100세 이상']

# 데이터프레임 생성
age_data = pd.DataFrame({
    '연령대': age_labels,
    '인구 수': list(age_population) + [age_population_100_plus]
})

# Streamlit에서 바 차트 시각화
st.bar_chart(age_data.set_index('연령대'))

# 연령대별 인구 수 제목
st.write(f'{selected_area}의 연령대별 인구 수')
