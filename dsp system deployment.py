import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Petrol Station Issue Tracker", layout="wide")

st.title(" Petrol Station Technical Issue Reporting & Technician Tracking")

# ---------------- INPUT SECTION ----------------
st.sidebar.header("Report Technical Issue")

station_name = st.sidebar.text_input("Petrol Station Name")
problem = st.sidebar.text_area("Technical Problem Faced")

station_lat = st.sidebar.number_input("Station Latitude", value=12.9716)
station_lon = st.sidebar.number_input("Station Longitude", value=77.5946)

submit = st.sidebar.button("Submit Issue")

# ---------------- TECHNICIAN INPUT ----------------
st.sidebar.header("Technician Tracking")

tech_name = st.sidebar.text_input("Technician Name")
tech_lat = st.sidebar.number_input("Technician Latitude", value=12.9750)
tech_lon = st.sidebar.number_input("Technician Longitude", value=77.6000)

status = st.sidebar.selectbox(
    "Technician Status",
    ["Assigned", "On the Way", "Reached Station"]
)

# ---------------- MAIN DISPLAY ----------------
if submit:
    st.success("Issue reported successfully!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Station Details")
        st.write(f"**Station:** {station_name}")
        st.write(f"**Problem:** {problem}")

    with col2:
        st.subheader("👨‍🔧 Technician Details")
        st.write(f"**Technician:** {tech_name}")
        st.write(f"**Status:** {status}")

    # ---------------- MAP ----------------
    st.subheader("🗺 Live Technician Tracking")

    m = folium.Map(location=[station_lat, station_lon], zoom_start=13)

    # Station Marker
    folium.Marker(
        [station_lat, station_lon],
        popup="Petrol Station",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    # Technician Marker
    folium.Marker(
        [tech_lat, tech_lon],
        popup=f"Technician: {tech_name}",
        icon=folium.Icon(color="green", icon="wrench")
    ).add_to(m)

    # Line showing movement
    folium.PolyLine(
        locations=[[tech_lat, tech_lon], [station_lat, station_lon]],
        color="blue",
        tooltip="Technician Route"
    ).add_to(m)

    st_folium(m, width=1000, height=500)

else:
    st.info("Please submit a technical issue to start tracking.")
