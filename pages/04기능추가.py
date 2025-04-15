import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 데이터 로드 - 이미 존재하는 age.csv 파일을 사용
data = pd.read_csv('age.csv')  # 'age.csv'의 경로를 올바르게 지정해야 합니다.

# 스트림릿 제목
st.title("👶 만 16~18세 인구 수 비교")

# 두 개의 행정구역 선택
selected_area_1 = st.selectbox("첫 번째 행정구역을 선택하세요:", data['행정구역'].unique())
selected_area_2 = st.selectbox("두 번째 행정구역을 선택하세요:", data['행정구역'].unique())

# 만 16~18세에 해당하는 열 이름을 정의합니다.
age_selectors = ['2025년03월_계_16세', '2025년03월_계_17세', '2025년03월_계_18세']

# 첫 번째 행정구역의 인구 수 추출
selected_population_1 = data.loc[data['행정구역'] == selected_area_1, age_selectors]

# 두 번째 행정구역의 인구 수 추출
selected_population_2 = data.loc[data['행정구역'] == selected_area_2, age_selectors]

# 두 행정구역의 인구 수가 유효한지 확인
if not selected_population_1.empty and not selected_population_2.empty:
    population_1 = selected_population_1.values.flatten()
    population_2 = selected_population_2.values.flatten()

    # 비교 데이터 생성
    comparison_data = {
        '행정구역': [selected_area_1, selected_area_2],
        '16세': [population_1[0], population_2[0]],
        '17세': [population_1[1], population_2[1]],
        '18세': [population_1[2], population_2[2]]
    }

    # 데이터프레임으로 변환
    comparison_df = pd.DataFrame(comparison_data)

    # 시각화
    fig = go.Figure()

    # 각 연령대별 인구 수 추가
    for age in ['16세', '17세', '18세']:
        fig.add_trace(go.Bar(
            x=comparison_df['행정구역'],
            y=comparison_df[age],
            name=age,
            hoverinfo='text',
            text=comparison_df[age],
        ))

    # 레이아웃 설정
    fig.update_layout(
        title="각 지역의 만 16세~18세 인구 수 비교",
        xaxis_title="행정구역",
        yaxis_title="인구 수",
        barmode='group',
    )

    # 스트림릿에서 그래프 출력
    st.plotly_chart(fig)
else:
    st.warning("선택한 행정구역 중 하나의 데이터가 없습니다.")
