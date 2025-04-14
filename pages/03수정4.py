import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

# 1살 단위의 x축 레이블 생성
ages = [int(age.split('계_')[1].strip('세')) for age in age_columns]

# Plotly를 사용하여 시각화
fig = go.Figure()

# 바 차트 추가
fig.add_trace(go.Bar(
    x=ages,  # x축: 연령대
    y=age_data,  # y축: 인구 수
    hoverinfo='text',
    text=[f"{age}세: {population}명" for age, population in zip(ages, age_data)],  # 마우스를 올렸을 때 보여줄 텍스트
))

# 레이아웃 설정
fig.update_layout(
    title=f"{selected_area}의 연령대별 인구 수",
    xaxis_title="연령대",
    yaxis_title="인구 수",
    xaxis_tickvals=[age for age in ages if age % 5 == 0],  # x축 레이블을 5세 단위로 표시
    xaxis_ticktext=[f"{age}세" for age in ages if age % 5 == 0],  # x축 텍스트
)

# 스트림릿에서 그래프 출력
st.plotly_chart(fig)
