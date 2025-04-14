import streamlit as st
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("age.csv")
df = df.rename(columns={df.columns[0]: '행정구역'})

# 연령 열만 추출
age_columns = [col for col in df.columns if '2025년03월_계_' in col and '세' in col]

# 연령 순서를 숫자 기준으로 정렬
def extract_age(col):
    if '100세 이상' in col:
        return 100
    else:
        return int(col.split('_')[-1].replace('세', ''))

# 정렬된 열 리스트
sorted_age_columns = sorted(age_columns, key=extract_age)

# Streamlit UI
st.set_page_config(page_title="연령별 인구 분석", layout="wide")
st.title("👶👦👨‍🦳 2025년 3월 연령별 인구 분석 대시보드")
st.markdown("📊 원하는 지역을 선택하면 **연령별 인구 분포**를 확인할 수 있어요!")

# 지역 선택
region = st.selectbox("🏙️ 분석할 지역을 선택하세요", df['행정구역'].unique())

# 해당 지역 데이터 가져오기
filtered = df[df['행정구역'] == region]
pop_by_age = filtered[sorted_age_columns].T
pop_by_age.columns = ['인구수']
pop_by_age['연령'] = [col.split('_')[-1] for col in sorted_age_columns]
pop_by_age = pop_by_age.reset_index(drop=True)

# 시각화
st.bar_chart(data=pop_by_age.set_index('연령'))
