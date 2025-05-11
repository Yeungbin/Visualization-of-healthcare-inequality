import streamlit as st
from streamlit_folium import folium_static
from preprocessing import load_data, filter_data
from visualization import display_metrics, create_map, create_charts

st.set_page_config(page_title="의료 현황 대시보드", layout="wide", page_icon="\U0001F3E5")
st.header('전국 의료 현황 대시보드\U0001F4C8', divider='gray')

# Data Load
df = load_data()
selected_region, selected_city, filtered_df = filter_data(df)

# Category to Visualize
indicator = st.radio("지표를 선택하세요:", ['의료접근성지표', '전공불균형지표'],
                     help="의료접근성 지표 계산 방법: 인구 10만 명 당 의사수/병원수/병상수/미충족 의료율 정규화 후 25점씩 가중치 부여해 100점 만점 | 전공불균형 지표 계산 방법: 해당 지역의 필수과 비율 - 0.38",
                     label_visibility="visible")

# Legend
display_metrics(df, filtered_df, selected_region, selected_city)

# Map Construction
m = create_map(filtered_df, selected_region, selected_city, indicator)
fig1, fig2 = create_charts(filtered_df, selected_region, selected_city)

# Visualization 
with st.container():
    st.markdown("---")
    st.markdown("#### 지표 시각화",
                help="색상은 선택한 지표 값에 따라 표시됩니다. 값이 높을수록 빨간색에 가깝고, 낮을수록 파란색에 가깝습니다.")
    folium_static(m, width=1200, height=600)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        st.plotly_chart(fig1, use_container_width=True)
