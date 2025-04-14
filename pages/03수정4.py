import streamlit as st
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("age.csv")
df = df.rename(columns={df.columns[0]: '행정구역'})

# ✅ 연령대 열만 인덱스로 슬라이싱 (3번째부터 103번째 열까지 → 0세~100세 이상)
age_columns = df.columns[3:104]

# 🎈 Streamlit UI
st.set_page_config(page_title="연령별 인구 분석", layout="wide")
st.title("👶👦👨‍🦳 2025년 3월 연령별 인구 분석 대시보드")
st.markdown("📊 원하는 지역을 선택하면 **연령별 인구 분포**를 확인할 수 있어요!")

# 지역 선택
region = st.selectbox("🏙️ 분석할 지역을 선택하세요", df['행정구역'].unique())

# 해당 지역 필터링 후 연령대별 인구 추출
region_data = df[df['행정구역'] == region]
pop_by_age = region_data[age_columns].T
pop_by_age.columns = ['인구수']

# 연령 라벨 추가
pop_by_age['연령'] = age_columns.str.extract(r'계_(.*)')  # '계_0세' → '0세'
pop_by_age = pop_by_age.reset_index(drop=True)

# 시각화 (연령을 인덱스로 설정)
st.bar_chart(data=pop_by_age.set_index('연령'))
