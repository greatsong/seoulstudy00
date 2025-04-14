import streamlit as st
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("age.csv")

# 전처리
df = df.rename(columns={df.columns[0]: '행정구역'})
age_columns = [col for col in df.columns if '세' in col]

# 🎈 Streamlit 앱 시작
st.set_page_config(page_title="연령별 인구 분석", layout="wide")
st.title("👶👦👨‍🦳 2025년 3월 연령별 인구 분석 대시보드")
st.markdown("🔎 원하는 **지역**을 선택하면 **연령별 인구 분포**를 확인할 수 있어요!")

# 지역 선택
region = st.selectbox("🏙️ 분석할 지역을 선택하세요", df['행정구역'].unique())
filtered = df[df['행정구역'] == region]

# 연령별 데이터 추출 및 가공
age_data = filtered[age_columns].T
age_data.columns = ['인구수']
age_data = age_data.reset_index()
age_data.columns = ['연령_원본', '인구수']

# ✅ 연령 텍스트 정제: '2025년03월_계_0세' → '0세', '100세 이상'
age_data['연령'] = age_data['연령_원본'].str.extract(r'_(\d+세|100세 이상)$')[0]

# ✅ 정렬용 숫자 추출: '0세' → 0, '100세 이상' → 100
age_data['연령숫자'] = age_data['연령'].apply(lambda x: int(x.replace('세', '').replace('이상', '')))

# 숫자 순 정렬 후 시각화
age_data = age_data.sort_values(by='연령숫자')

# 📊 바 차트 출력
st.bar_chart(data=age_data, x='연령', y='인구수', use_container_width=True)

# 🎉 마무리 멘트
st.markdown("📌 **팁:** 고령화나 유소년 인구비율을 비교하면서 지역 간 특성을 파악해보세요!")
