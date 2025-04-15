import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 데이터 로드
data = pd.read_csv('/path/to/your/age.csv')  # 실제로는 올바른 파일 경로를 입력해야 합니다.

# 스트림릿 제목
st.title("👶 만 16~18세 인구 수 비교")

# 행정구역 선택
selected_area = st.selectbox("행정구역을 선택하세요:", data['행정구역'].unique())

# 만 16~18세에 해당하는 열 이름을 정의합니다.
age_selectors = ['2025년03월_계_16세', '2025년03월_계_17세', '2025년03월_계_18세']

# 선택한 행정구역의 인구 수 추출
selected_population = data.loc[data['행정구역'] == selected_area, age_selectors]

# 선택된 행정구역의 인구 수가 있는지 확인
if not selected_population.empty:
    selected_population = selected_population.values.flatten()

    # 다른 행정구역의 인구 수 추출
    other_populations = data.loc[data['행정구역'] != selected_area, age_selectors]

    # 데이터프레임에 행정구역 이름 추가
    other_populations['행정구역'] = data.loc[data['행정구역'] != selected_area, '행정구역'].values

    # 선택된 행정구역과 다른 행정구역의 인구 수 비교 데이터 생성
    comparison_data = {
        '행정구역': [selected_area, *other_populations['행정구역'].values],
        '16세': [selected_population[0], *other_populations['2025년03월_계_16세'].values],
        '17세': [selected_population[1], *other_populations['2025년03월_계_17세'].values],
        '18세': [selected_population[2], *other_populations['2025년03월_계_18세'].values],
    }

    # 결과를 데이터프레임으로 변환
    comparison_df = pd.DataFrame(comparison_data)

    # 시각화
    fig = go.Figure()

    # 각 연령대별 인구 수 추가
    for age in age_selectors:
        fig.add_trace(go.Bar(
            x=comparison_df['행정구역'],
            y=comparison_df[age],
            name=age.split('_')[-1].replace('세', '세'),
            hoverinfo='text',
            text=comparison_df[age],
        ))

    # 레이아웃 설정
    fig.update_layout(
        title=f"{selected_area}와 다른 행정구역의 만 16세~18세 인구 수 비교",
        xaxis_title="행정구역",
        yaxis_title="인구 수",
        barmode='group',
    )

    # 스트림릿에서 그래프 출력
    st.plotly_chart(fig)
else:
    st.warning("선택한 행정구역의 데이터가 없습니다.")
