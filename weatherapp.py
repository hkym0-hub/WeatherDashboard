import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import pandas as pd

st.set_page_config(page_title="Open-Meteo Interactive Weather Dashboard", page_icon="🌤️", layout="centered")

st.title("🌤️ Open-Meteo Interactive Weather Dashboard")
st.write("지도에서 위치를 클릭하거나, 직접 위도/경도를 입력하면 해당 지역의 시간별 기온 데이터를 불러옵니다.")

# --- Step 1: Choose input method ---
st.subheader("1️⃣ 지역 선택 방법")
input_method = st.radio("위치를 선택하는 방법을 고르세요:", ("지도를 클릭", "직접 입력"))

lat, lon = None, None

# --- Option 1: Choose on map ---
if input_method == "지도를 클릭":
    st.info("지도를 클릭하여 위도와 경도를 선택하세요.")
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=5)
    clicked_point = st_folium(m, height=400, width=700)

    if clicked_point and clicked_point.get("last_clicked"):
        lat = clicked_point["last_clicked"]["lat"]
        lon = clicked_point["last_clicked"]["lng"]
        st.success(f"선택된 위치: 위도 {lat:.2f}, 경도 {lon:.2f}")

# --- Option 2: Manual input ---
else:
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("위도 (Latitude)", min_value=-90.0, max_value=90.0, value=37.57, step=0.01)
    with col2:
        lon = st.number_input("경도 (Longitude)", min_value=-180.0, max_value=180.0, value=126.98, step=0.01)
    st.info(f"입력된 위치: 위도 {lat:.2f}, 경도 {lon:.2f}")

# --- Step 2: Fetch and display weather ---
if lat is not None and lon is not None:
    if st.button("📡 기상 데이터 불러오기"):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation,wind_speed_10m&timezone=auto"
        response = requests.get(url)
        data = response.json()

        hourly = data.get("hourly", {})
        if hourly:
            df = pd.DataFrame({
                "Time": hourly["time"],
                "Temperature (°C)": hourly["temperature_2m"],
                "Precipitation (mm)": hourly["precipitation"],
                "Wind Speed (m/s)": hourly["wind_speed_10m"],
            })
            df["Time"] = pd.to_datetime(df["Time"])

            st.subheader("2️⃣ 시간별 기상 변화")
            st.line_chart(df.set_index("Time"))
        else:
            st.warning("이 위치의 기상 데이터를 불러올 수 없습니다.")
