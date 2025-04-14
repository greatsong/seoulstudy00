import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
data = pd.read_csv('age.csv')

# 스트림릿 제목
st.title("👵 연령대별 인구 수")

# 행정구역 선택
selected_area = st.selectbox("행정구역을 선택하세요:", data['행정구역'].unique())

# 선택된 행정구역에 대한 데이터 필터링
filtered_data = data[data['행정구역'] == selected_area]

# 데이터 전처리
age_columns = filtered_data.columns[3:]  # 연령대별 인구 수 열
age_data = filtered_data[age_columns].values.flatten()

# 5세 단위로 x축 레이블 수정
filtered_age_columns = [age for age in age_columns if age.endswith('세') and int(age.split('계_')[1].strip('세')) % 5 == 0]

# 해당 5세 단위의 데이터만 추출
filtered_age_data = [age_data[i] for i, age in enumerate(age_columns) if age.endswith('세') and int(age.split('계_')[1].strip('세')) % 5 == 0]

# 시각화
st.write(f"{selected_area}의 연령대별 인구 수:")
fig, ax = plt.subplots()
ax.bar(filtered_age_columns, filtered_age_data)
ax.set_xlabel("연령대")
ax.set_ylabel("인구 수")
ax.set_title(f"{selected_area}의 연령대별 인구 수")
plt.xticks(rotation=45)
plt.tight_layout()

# 그래프 출력
st.pyplot(fig)
