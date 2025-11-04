import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import pandas as pd

st.set_page_config(page_title="Open-Meteo Interactive Weather Dashboard", page_icon="🌤️", layout="centered")

st.title("🌤️ Open-Meteo Interactive Weather Dashboard")
st.write("지도에서 위치를 클릭하면 해당 지역의 시간별 기온 데이터를 불러옵니다.")

# Step 1: Create an interactive map
st.subheader("1️⃣ 지역 선택 (지도를 클릭하세요)")
m = folium.Map(location=[37.5665, 126.9780], zoom_start=5)  # center near Korea
clicked_point = st_folium(m, height=400, width=700)

# Step 2: Fetch weather if a point was clicked
if clicked_point and clicked_point.get("last_clicked"):
    lat = clicked_point["last_clicked"]["lat"]
    lon = clicked_point["last_clicked"]["lng"]

    st.success(f"선택된 위치: 위도 {lat:.2f}, 경도 {lon:.2f}")
    
    # Step 3: Call Open-Meteo API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&timezone=auto"
    response = requests.get(url)
    data = response.json()

    # Step 4: Prepare temperature data
    hourly = data.get("hourly", {})
    if hourly:
        df = pd.DataFrame({
            "Time": hourly["time"],
            "Temperature (°C)": hourly["temperature_2m"]
        })
        df["Time"] = pd.to_datetime(df["Time"])
        
        st.subheader("2️⃣ 시간별 기온 변화")
        st.line_chart(df.set_index("Time"))
    else:
        st.warning("이 위치의 기상 데이터를 불러올 수 없습니다.")
else:
    st.info("지도를 클릭하면 데이터를 불러옵니다.")
