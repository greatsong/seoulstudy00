import streamlit as st
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("age.csv")

# 첫 번째 열 이름 정리
df = df.rename(columns={df.columns[0]: '행정구역'})
age_columns = [col for col in df.columns if '세' in col]

# 🎈 앱 설정
st.set_page_config(page_title="연령별 인구 분석", layout="wide")
st.title("👶👦👨‍🦳 2025년 3월 연령별 인구 분석 대시보드")
st.markdown("📊 원하는 지역을 선택하면 **연령별 인구 분포**를 확인할 수 있어요!")

# 지역 선택
region = st.selectbox("🏙️ 분석할 지역을 선택하세요", df['행정구역'].unique())
filtered = df[df['행정구역'] == region]

# 연령대 데이터 정리
age_data = filtered[age_columns].T
age_data.columns = ['인구수']
age_data = age_data.reset_index()
age_data.columns = ['연령_원본', '인구수']

# ✅ 연령 텍스트 정제
# '2025년03월_계_0세' → '0세', '2025년03월_계_100세 이상' → '100세 이상'
age_data['연령'] = age_data['연령_원본'].str.extract(r'_(\d+세|100세 이상)$')[0]

# ✅ 정렬용 숫자 컬럼 생성
age_data['연령숫자'] = age_data['연령'].apply(lambda x: int(x.replace('세', '').replace('이상', '')))

# ✅ 숫자 순으로 정렬 후 인덱스를 '연령'으로 설정
age_data = age_data.sort_values(by='연령숫자').reset_index(drop=True)
age_data = age_data.set_index('연령')

# ✅ 시각화: 완전히 정렬된 상태로 출력
st.bar_chart(age_data['인구수'])

# 🎉 마무리 멘트
st.markdown("✅ **팁:** 고령화 추이, 유소년 비율을 지역별로 비교해보세요!")
