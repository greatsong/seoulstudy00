import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 불러오기
data = pd.read_csv('age.csv')

# Streamlit 제목
st.title('📊 행정구역별 연령대별 인구 시각화')

# 행정구역 선택
selected_area = st.selectbox('🏙️ 행정구역을 선택하세요:', data['행정구역'].unique())

# 선택된 행정구역의 데이터 필터링
filtered_data = data[data['행정구역'] == selected_area]

# 인구 수 추출
age_population = filtered_data.iloc[0, 3:103].values  # 0~99세
age_population_100_plus = filtered_data.iloc[0, 103]  # 100세 이상

# 레이블 및 데이터 구성
age_labels = [f"{i}세" for i in range(100)] + ['100세 이상']
full_population = list(age_population) + [age_population_100_plus]

# 가장 많은 인구 수 기준으로 강조 범위 설정
max_population = max(full_population)
threshold = max_population * 0.9

# 색상 설정
bar_colors = ['lightcoral' if pop >= threshold else 'skyblue' for pop in full_population]
bar_colors[-1] = 'gold'  # 100세 이상 강조

# 시각화
fig, ax = plt.subplots(figsize=(16, 8))
bars = ax.bar(age_labels, full_population, color=bar_colors, edgecolor='black', alpha=0.9)

# 제목 및 축 레이블
ax.set_title(f'{selected_area} 연령대별 인구 분포', fontsize=20, fontweight='bold')
ax.set_xlabel('연령대', fontsize=14)
ax.set_ylabel('인구 수', fontsize=14)

# X축 눈금 조정
ax.set_xticks(range(0, 101, 5))
ax.set_xticklabels([f"{i}세" for i in range(0, 101, 5)] + ['100세 이상'], rotation=45, fontsize=10)

# Y축 그리드 추가
ax.grid(axis='y', linestyle='--', alpha=0.6)

# 막대에 수치 표시
for bar in bars:
    height = bar.get_height()
    if height > 0:
        ax.text(bar.get_x() + bar.get_width()/2, height + max_population * 0.01, 
                f'{int(height):,}', ha='center', va='bottom', fontsize=9)

# Streamlit에 출력
st.pyplot(fig)
