import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울의 100년 연평균 기온 변화")
st.write("서울의 일별 기온 데이터를 연도별로 평균 내어, 장기간의 기온 변화를 살펴봅니다.")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8")

    # 날짜 열을 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 결측값 제거
    df = df.dropna(subset=["날짜", "평균기온"])

    return df


try:
    df = load_data()

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    # 연도별 평균기온 계산
    yearly_temp = (
        df.groupby("연도")["평균기온"]
        .mean()
        .reset_index()
    )

    # 데이터에 포함된 전체 기간 중 최대 100년 표시
    yearly_temp = yearly_temp.sort_values("연도").tail(100)

    st.subheader("연도별 연평균 기온")

    st.line_chart(
        yearly_temp.set_index("연도"),
        y="평균기온",
        x_label="연도",
        y_label="연평균 기온 (℃)"
    )

    # 간단한 요약 정보
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "분석 기간",
            f"{yearly_temp['연도'].min()}~{yearly_temp['연도'].max()}"
        )

    with col2:
        st.metric(
            "가장 낮은 연평균 기온",
            f"{yearly_temp['평균기온'].min():.1f} ℃"
        )

    with col3:
        st.metric(
            "가장 높은 연평균 기온",
            f"{yearly_temp['평균기온'].max():.1f} ℃"
        )

    with st.expander("연도별 데이터 보기"):
        display_df = yearly_temp.copy()
        display_df["평균기온"] = display_df["평균기온"].round(2)
        display_df.columns = ["연도", "연평균 기온 (℃)"]
        st.dataframe(display_df, use_container_width=True)

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.write(f"오류 내용: {e}")
