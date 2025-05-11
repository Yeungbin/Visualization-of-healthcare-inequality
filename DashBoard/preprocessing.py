import pandas as pd
import streamlit as st

def load_data():
    url = "https://raw.githubusercontent.com/seungjuniper/koreamedicalDash/main/final.xlsx"
    df = pd.read_excel(url)

    numeric_cols = [
        "인구 10만명 당 병상수", "인구 10만명 당 병원수",
        "인구 10만명 당 의사수", "미충족의료율",
        "의료접근성지표", "전공불균형지표"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", "").astype(float)

    return df

def filter_data(df):
    selected_region = st.selectbox("시도 선택", options=["전국"] + df["시도"].unique().tolist(), index=0)
    selected_city = None
    if selected_region == "전국":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["시도"] == selected_region]
        selected_city = st.selectbox("시군구 선택", options=["전체"] + filtered_df["시군구"].unique().tolist(), index=0)
        if selected_city != "전체":
            filtered_df = filtered_df[filtered_df["시군구"] == selected_city]

    return selected_region, selected_city, filtered_df