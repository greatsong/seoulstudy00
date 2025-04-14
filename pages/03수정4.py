import streamlit as st
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("age.csv")
df = df.rename(columns={df.columns[0]: '행정구역'})

# 연령대 열 인덱스 (0세~100세 이상)
age_columns = df.columns[3:104]

# Streamlit UI
st.set_page_config(page_title="연령별 인구 분석", layout="wide")
st.title("👶👦👨‍🦳 2025년 3월 연령별 인구 분석 대시보드")
st.markdown("📊 원하는 지역을 선택하면 **연령별 인구 분포**를 확인할 수 있어요!")

# 지역 선택
region = st.selectbox("🏙️ 분석할 지역을 선택하세요", df['행정구역'].unique())

# 연령별 인구 데이터 추출
region_data = df[df['행정구역'] == region]
pop_by_age = region_data[age_columns].T
pop_by_age.columns = ['인구수']

# 연령 라벨과 정렬용 숫자 컬럼 추가
pop_by_age['연령'] = [col.split('_')[-1] for col in age_columns]
pop_by_age['정렬용숫자'] = pop_by_age['연령'].apply(lambda x: int(x.replace('세', '').replace('이상', '')))

# 정렬 후 인덱스 설정
pop_by_age = pop_by_age.sort_values(by='정렬용숫자').reset_index(drop=True)
pop_by_age = pop_by_age.set_index('연령')

# 시각화
st.bar_chart(pop_by_age['인구수'])

# 마무리
st.markdown("🧠 **Tip:** 유소년 인구 또는 고령 인구 집중 구간을 비교해보세요!")
