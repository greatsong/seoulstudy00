import streamlit as st
import pandas as pd

# 데이터 불러오기
file_path = 'age.csv'  # ← 여기에 실제 CSV 파일 경로 입력
data = pd.read_csv(file_path)

# 애플리케이션 본문
def run_app():
    st.title('2025년 3월 한국 인구 통계 데이터 분석')

    # 사이드바 - 행정구역 선택
    st.sidebar.header("데이터 선택")
    selected_region = st.sidebar.selectbox("행정구역을 선택하세요", data['행정구역'].unique())

    # 연령대 열만 추출 ('2025년03월_계_0세' ~ '2025년03월_계_100세 이상')
    age_columns = [col for col in data.columns if '2025년03월_계_' in col and '세' in col]

    # 연령대 열 이름 정렬 (0세 ~ 100세 이상)
    age_columns_sorted = sorted(
        age_columns,
        key=lambda x: int(x.split('_')[-1].replace('세 이상', '100').replace('세', ''))
    )

    # 선택한 지역의 연령대 데이터만 추출
    region_data = data[data['행정구역'] == selected_region][age_columns_sorted]

    # 연령대 이름 리스트 (ex. '0세', '1세', ..., '100세 이상')
    age_labels = [col.split('_')[-1] for col in age_columns_sorted]

    # 인구 수 데이터
    population_counts = region_data.values.flatten()

    # 데이터프레임 생성
    population_df = pd.DataFrame({
        '연령대': age_labels,
        '인구수': population_counts
    })

    # 결측값은 0으로 처리
    population_df['인구수'] = population_df['인구수'].fillna(0)

    # 차트 출력
    st.bar_chart(population_df.set_index('연령대'))

# 메인 실행
if __name__ == "__main__":
    run_app()
