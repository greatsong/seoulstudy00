import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 불러오기
data = pd.read_csv('age.csv')

# Streamlit 제목
st.title('📊 2025년 3월 기준, 행정구역별 연령대 인구 시각화')

# 행정구역 선택
selected_area = st.selectbox('🏙️ 행정구역을 선택하세요:', data['행정구역'].unique())

# 선택된 행정구역 필터링
filtered = data[data['행정구역'] == selected_area]

# 연령 컬럼 추출
age_columns = [col for col in data.columns if '세' in col]
age_labels = [col.replace('2025년03월_계_', '') for col in age_columns]
age_values = filtered.iloc[0][age_columns].values

# 색상 설정
max_value = max(age_values)
threshold = max_value * 0.9
colors = ['lightcoral' if v >= threshold else 'skyblue' for v in age_values]
colors[-1] = 'gold'  # 100세 이상 강조

# 그래프 그리기
fig, ax = plt.subplots(figsize=(16, 8))
bars = ax.bar(age_labels, age_values, color=colors, edgecolor='black', alpha=0.9)

ax.set_title(f'{selected_area} 연령대별 인구 분포 (2025년 3월)', fontsize=20, fontweight='bold')
ax.set_xlabel('연령대', fontsize=14)
ax.set_ylabel('인구 수', fontsize=14)
ax.set_xticks(range(len(age_labels)))
ax.set_xticklabels(age_labels, rotation=45, fontsize=9)
ax.grid(axis='y', linestyle='--', alpha=0.6)

for bar in bars:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x() + bar.get_width() / 2, h + max_value * 0.01, f'{int(h):,}', 
                ha='center', va='bottom', fontsize=9)

st.pyplot(fig)
