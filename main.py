import streamlit as st
import pandas as pd

# 데이터 불러오기
file_path = 'age.csv'  # 여기에 실제 CSV 파일 경로 입력
data = pd.read_csv(file_path)

# Streamlit 애플리케이션
def run_app():
    st.title('2025년 3월 한국 인구 통계 데이터 분석')

    # 사이드바에서 행정구역 선택
    st.sidebar.header("데이터 선택")
    selected_region = st.sidebar.selectbox("행정구역을 선택하세요", data['행정구역'].unique())

    # 연령대별 열 이름만 필터링
    age_columns = [col for col in data.columns if '2025년03월_계_' in col and '세' in col]
    region_data = data[data['행정구역'] == selected_region][age_columns]

    # 연령대 이름 가공 (열 이름에서 '0세', '1세', ..., '100세 이상'만 추출)
    age_labels = [col.split('_')[-1] for col in age_columns]

    # 연령대별 인구 수 추출
    population_counts = region_data.values.flatten()

    if len(population_counts) == 101:
        population_df = pd.DataFrame({
            '연령대': age_labels,
            '인구수': population_counts
        })

        # 결측값을 0으로 처리
        population_df['인구수'] = population_df['인구수'].fillna(0)

        # 정렬을 위한 숫자형 연령대
        population_df['연령대 순서'] = population_df['연령대'].apply(
            lambda x: int(x.replace('세', '')) if x != '100세 이상' else 100
        )
        population_df = population_df.sort_values(by='연령대 순서')

        # 시각화
        st.bar_chart(population_df.set_index('연령대'))

    else:
        st.error("연령대별 인구 데이터 형식이 잘못되었습니다. 0세부터 100세 이상의 모든 구간이 포함되어야 합니다.")

if __name__ == "__main__":
    run_app()
