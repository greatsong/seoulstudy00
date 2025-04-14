import streamlit as st
import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv('age.csv')

# 연령별 컬럼만 추출
age_columns = [col for col in df.columns if '2025년03월_계_' in col and '세' in col]

# 나이 정보 정렬용 숫자 추출
def extract_age(col_name):
    if '100세 이상' in col_name:
        return 100
    return int(col_name.split('_')[-1].replace('세', ''))

# 정렬된 연령 컬럼
age_columns_sorted = sorted(age_columns, key=extract_age)

# 연령 데이터를 Long 형식으로 변환
data_long = df.melt(
    id_vars=['행정구역'],
    value_vars=age_columns_sorted,
    var_name='연령',
    value_name='인구수'
)

# 연령 라벨 정리
data_long['연령'] = data_long['연령'].apply(lambda x: '100세 이상' if '100세 이상' in x else f"{int(x.split('_')[-1].replace('세', ''))}세")

# Streamlit 앱 시작
st.set_page_config(page_title="연령별 인구 대시보드", layout="wide")

st.title("📊 2025년 3월 연령별 인구 대시보드")
st.markdown("🧑‍🤝‍🧑 **행정구역별 인구 구조를 확인해보세요!**")

# 행정구역 선택
selected_region = st.selectbox("📍 행정구역을 선택하세요:", df['행정구역'].unique())

# 선택한 행정구역의 데이터 필터링
filtered = data_long[data_long['행정구역'] == selected_region]

# 시각화
st.bar_chart(filtered.set_index('연령')['인구수'])
