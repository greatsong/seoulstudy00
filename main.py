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

    # 연령대 이름 정의 (0세부터 99세, 그리고 100세 이상)
    age_labels = [f"{i}세" for i in range(100)] + ['100세 이상']

    # 연령대별 인구 수를 배열로 변환
    population_counts = region_data.values.flatten()

    # 모든 연령대 구간이 존재하도록 보장
    if len(population_counts) == 101:
        population_df = pd.DataFrame({
            '연령대': age_labels,
            '인구수': population_counts
        })

        # 인구 수치가 결측치인 경우 0으로 처리
        population_df['인구수'] = population_df['인구수'].fillna(0)

        # 연령대에 대한 정렬 작업
        population_df['연령대 순서'] = population_df['연령대'].apply(
            lambda x: int(x[:-1]) if x != '100세 이상' else 100
        )
        population_df = population_df.sort_values(by='연령대 순서')

        # Streamlit의 바 차트로 시각화
        st.bar_chart(population_df.set_index('연령대'))

    else:
        st.error("연령대별 인구 데이터 형식이 잘못되었습니다. 0세부터 100세 이상의 모든 구간이 포함되어야 합니다.")

if __name__ == "__main__":
    run_app()
