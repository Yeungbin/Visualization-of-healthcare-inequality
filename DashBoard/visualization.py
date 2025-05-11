import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import folium
import plotly.express as px
import streamlit as st

def display_metrics(df, filtered_df, selected_region, selected_city):
    st.markdown("### 주요 지표")
    cols = st.columns(3)
    
    metrics = [
        ("인구 10만명 당 의사수", "인구 10만명 당 의사수"),
        ("인구 10만명 당 병원수", "인구 10만명 당 병원수"),
        ("인구 10만명 당 병상수", "인구 10만명 당 병상수"),
        ("미충족의료율", "미충족의료율"),
        ("의료접근성 지표", "의료접근성지표"),
        ("전공불균형 지표", "전공불균형지표"),
    ]

    for i, (label, col_name) in enumerate(metrics):
        col = cols[i % 3]
        if col_name not in filtered_df.columns:
            col.error(f"{col_name} 데이터가 없습니다.")
            continue
        if filtered_df[col_name].isna().all():
            col.error(f"{label} 데이터가 없습니다.")
            continue

        if selected_city == "전체" and selected_region != "전국":
            avg = df[col_name].mean()
            val = filtered_df[col_name].mean()
            help_text = f"전국 평균 {avg:.2f}"
        elif selected_city != "전체":
            avg = df[df["시도"] == selected_region][col_name].mean()
            val = filtered_df[col_name].mean()
            help_text = f"{selected_region} 평균 {avg:.2f}"
        else:
            avg = df[col_name].mean()
            val = filtered_df[col_name].mean()
            help_text = f"전국 평균 {avg:.2f}"

        delta = val - avg
        delta_text = f"+{delta:.2f}" if delta > 0 else f"{delta:.2f}"
        if pd.isna(val):
            col.metric(label=label, value="N/A", delta="N/A", help=help_text)
        else:
            col.metric(label=label, value=f"{val:.2f}", delta=delta_text, help=help_text)

def create_map(filtered_df, selected_region, selected_city, indicator):
    if selected_region == "전국":
        center = [37.5665, 126.978]; zoom = 7
    elif selected_city == "전체":
        center = [filtered_df["위도"].mean(), filtered_df["경도"].mean()]; zoom = 10
    else:
        center = [filtered_df["위도"].iloc[0], filtered_df["경도"].iloc[0]]; zoom = 12

    m = folium.Map(location=center, zoom_start=zoom)

    def get_color(value, vmin, vmax):
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        cmap = plt.cm.get_cmap('coolwarm')
        return mcolors.to_hex(cmap(norm(value)))

    vmin, vmax = filtered_df[indicator].min(), filtered_df[indicator].max()
    for _, row in filtered_df.iterrows():
        lat, lon, val = row["위도"], row["경도"], row[indicator]
        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color=get_color(val, vmin, vmax),
            fill=True,
            fill_color=get_color(val, vmin, vmax),
            fill_opacity=0.7,
            popup=f"{row['시도']} {row['시군구']} - {val:.2f}"
        ).add_to(m)
    return m

def create_charts(filtered_df, selected_region, selected_city):
    mandatory_cols = ["내과", "외과", "심장혈관흉부외과", "산부인과", "소아청소년과"]
    filtered_df[mandatory_cols] = filtered_df[mandatory_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
    total_mandatory = filtered_df[mandatory_cols].sum().sum()
    total_optional = filtered_df["비필수과"].sum()

    labels = ["비필수과"] + mandatory_cols
    values = [total_optional] + [filtered_df[col].sum() for col in mandatory_cols]
    title1 = f"{selected_city if selected_city and selected_city != '전체' else selected_region}의 필수과/비필수과 비율"
    fig1 = px.pie(names=labels, values=values, title=title1)

    group_col = "시도" if selected_region == "전국" else "시군구"
    pop_data = filtered_df.groupby(group_col)["인구수"].sum().reset_index()
    title2 = f"{selected_city if selected_city and selected_city != '전체' else selected_region}의 인구 분포"
    fig2 = px.bar(pop_data, x=group_col, y="인구수", labels={"인구수": "인구수"}, title=title2)

    return fig1, fig2