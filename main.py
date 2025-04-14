import streamlit as st
import pandas as pd

# 데이터 불러오기
file_path = 'age.csv'  # 파일 경로를 올바르게 설정해주세요.
data = pd.read_csv(file_path)

# 스트림릿 애플리케이션 코드
def run_app():
    st.title('2025년 3월 한국 인구 통계 데이터 분석')

    # 데이터 선택
    st.sidebar.header("데이터 선택")
    selected_region = st.sidebar.selectbox("행정구역을 선택하세요", data['행정구역'].unique())

    # 선택한 지역의 데이터 필터링
    region_data = data[data['행정구역'] == selected_region].iloc[:, 3:]  # 연령대별 데이터 추출

    # 연령대 이름 정의
    age_labels = [f"{i}세" for i in range(0, 101)] + ['100세 이상']

    # 연령대별 인구 수를 데이터프레임으로 변환
    population_counts = region_data.values.flatten()
    population_df = pd.DataFrame({
        '연령대': age_labels,
        '인구수': population_counts
    })

    # Streamlit의 바 차트로 시각화
    st.bar_chart(population_df.set_index('연령대'))

if __name__ == "__main__":
    run_app()
