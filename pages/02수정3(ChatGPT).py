import streamlit as st
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("age.csv")

# 전처리
df = df.copy()
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

# 연령 텍스트에서 숫자만 추출, '100세 이상'은 100으로 처리
age_data['연령'] = age_data['연령_원본'].str.extract(r'(\d+세|100세 이상)')[0]
age_data['연령숫자'] = age_data['연령'].apply(lambda x: int(x.replace('세', '').replace('이상', '')))

# 숫자 순 정렬 후 시각화
age_data = age_data.sort_values(by='연령숫자')
st.bar_chart(data=age_data, x='연령', y='인구수', use_container_width=True)

# 🎉 마무리 멘트
st.markdown("🧠 Tip: **고령화 현상**을 확인하거나 **유소년 인구** 비율을 지역별로 비교해보세요!")
