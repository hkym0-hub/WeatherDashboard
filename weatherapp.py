# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Open-Meteo Interactive Weather Dashboard", layout="centered")

st.title("🌤️ Open-Meteo Interactive Weather Dashboard")
st.caption("지도를 클릭하면 해당 지역의 시간별 기온 데이터를 불러옵니다.")

# Step 1: Create an interactive map
m = folium.Map(location=[36.5, 127.8], zoom_start=5)  # center of Korea
st.markdown("### ① 지역 선택 (지도를 클릭하세요)")
map_data = st_folium(m, width=700, height=500)

# Step 2: Get coordinates from click
if map_data and map_data["last_clicked"]:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.success(f"선택된 위치: 위도 {lat:.3f}, 경도 {lon:.3f}")

    # Step 3: Call Open-Meteo API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    # Step 4: Extract temperature data
    hourly = pd.DataFrame({
        "time": data["hourly"]["time"],
        "temperature (°C)": data["hourly"]["temperature_2m"]
    })

    # Step 5: Show temperature chart
    st.markdown("### ② 시간별 기온 변화")
    fig = px.line(hourly, x="time", y="temperature (°C)", title="Hourly Temperature")
    st.plotly_chart(fig, use_container_width=True)

    # Optional: Show data table
    with st.expander("데이터 보기"):
        st.dataframe(hourly)
else:
    st.info("지도를 클릭하면 해당 지역의 날씨 데이터를 가져옵니다.")
