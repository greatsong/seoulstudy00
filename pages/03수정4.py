import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="나이대별 인구 시각화", layout="wide")
st.title("나이대별 인구 시각화 앱 😊")

# 0. 데이터 경로: 'age.csv'
@st.cache_data
def load_data():
    # CSV 파일 읽기
    df = pd.read_csv('age.csv')
    return df

df = load_data()

st.subheader("데이터 미리보기 👀")
st.dataframe(df.head())

# 1. 나이(또는 연령) 관련 컬럼 자동 탐색하기
# "나이", "연령", "Age" 등이 포함된 컬럼명을 우선탐색
age_col_candidates = [col for col in df.columns if "나이" in col or "연령" in col or "Age" in col]
if age_col_candidates:
    age_col = age_col_candidates[0]
else:
    # 없으면 첫 번째 컬럼을 나이 컬럼으로 가정
    age_col = df.columns[0]
    
st.write(f"**선택된 나이대 컬럼**: `{age_col}`")

# 2. 나이대 문자열을 숫자 순서대로 정렬할 수 있도록 처리
def extract_age_value(age_str):
    """
    문자열에서 숫자를 추출하여 정렬 기준으로 사용.
    "100세 이상"의 경우에도 "100"을 추출하여 올바르게 정렬합니다.
    """
    match = re.search(r'(\d+)', str(age_str))
    if match:
        return int(match.group(1))
    else:
        return 0

# 새로운 정렬용 컬럼 추가
df['age_order'] = df[age_col].apply(extract_age_value)

# 정렬 진행 (숫자 기준 오름차순)
df_sorted = df.sort_values(by='age_order').reset_index(drop=True)

st.subheader("정렬된 데이터 🔢")
st.dataframe(df_sorted)

# 3. 인터랙티브 차트 생성: 스트림릿 내장 시각화 함수 활용
st.sidebar.header("📊 차트 설정")
chart_type = st.sidebar.selectbox("시각화 유형 선택", ("바 차트", "라인 차트", "면적 차트"))

# 수치형 컬럼 선택 (정렬용 컬럼 제외)
numeric_cols = df_sorted.select_dtypes(include=['int64','float64']).columns.tolist()
if "age_order" in numeric_cols:
    numeric_cols.remove("age_order")

if numeric_cols:
    num_col = st.sidebar.selectbox("수치형 데이터 선택", numeric_cols)
else:
    st.error("수치형 데이터가 발견되지 않았습니다!")
    num_col = None

if num_col:
    st.subheader("📈 선택한 차트")
    # 인덱스를 나이대 컬럼으로 지정하여 차트를 그립니다.
    plot_data = df_sorted.set_index(age_col)[[num_col]]
    
    if chart_type == "바 차트":
        st.bar_chart(plot_data)
    elif chart_type == "라인 차트":
        st.line_chart(plot_data)
    elif chart_type == "면적 차트":
        st.area_chart(plot_data)
    
    st.success("차트가 성공적으로 로드되었습니다! 🎉")
    
# 추가 옵션: 사용자가 원하는 범위의 나이대만 필터링할 수 있는 슬라이더 (옵션)
st.sidebar.header("나이대 필터링")
min_age = int(df_sorted['age_order'].min())
max_age = int(df_sorted['age_order'].max())
age_range = st.sidebar.slider("나이대 범위 선택", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# 필터링 진행
filtered_df = df_sorted[(df_sorted['age_order'] >= age_range[0]) & (df_sorted['age_order'] <= age_range[1])]
st.subheader("필터링된 데이터 보기")
st.dataframe(filtered_df)

if num_col in filtered_df.columns:
    filtered_plot = filtered_df.set_index(age_col)[[num_col]]
    st.subheader("필터링된 데이터 차트 📊")
    if chart_type == "바 차트":
        st.bar_chart(filtered_plot)
    elif chart_type == "라인 차트":
        st.line_chart(filtered_plot)
    elif chart_type == "면적 차트":
        st.area_chart(filtered_plot)
else:
    st.info("선택된 수치형 데이터가 필터링 후에 존재하지 않습니다.")
