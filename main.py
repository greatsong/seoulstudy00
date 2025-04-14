import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

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

# 인구 수 배열 생성
full_population = list(age_population) + [age_population_100_plus]

# 슬라이더를 사용하여 범위 선택
min_age = 0
max_age = 100

age_range = st.slider(
    '인구 수를 보고 싶은 연령대 선택하기:',
    min_value=min_age,
    max_value=max_age,
    value=(0, 100),
    step=1
)

# 선택한 연령대 범위에 따른 인구 수 필터링
filter_indices = range(age_range[0], age_range[1] + 1)
filtered_labels = [age_labels[i] for i in filter_indices]
filtered_population = [full_population[i] for i in filter_indices]

# Matplotlib를 이용한 시각화
plt.figure(figsize=(14, 7))
bars = plt.bar(filtered_labels, filtered_population, color='skyblue', edgecolor='black')

# 그래프 제목 및 축 레이블
plt.title(f'{selected_area} 연령대별 인구 수 ({age_range[0]}세 ~ {age_range[1]}세)', fontsize=18, fontweight='bold')
plt.xlabel('연령대', fontsize=14)
plt.ylabel('인구 수', fontsize=14)

# X축 레이블 회전 조정
plt.xticks(rotation=45, fontsize=10)

# Y축 그리드 추가
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 막대에 수치 표시
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 100, int(yval), ha='center', fontsize=9)

# Streamlit에서 Matplotlib 그래프 표시
st.pyplot(plt)

# 빈 차트 초기화
plt.clf()
