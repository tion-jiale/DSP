import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from geopy.distance import geodesic

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Technician Auto Assignment", layout="wide")
st.title("⛽ Petrol Station Issue → Auto Technician Assignment")

# ---------------- AUTO STATION LOCATION ----------------
st.subheader("📍 Detecting Petrol Station Location")

location = streamlit_geolocation()

if location:
    station_lat = float(location["latitude"])
    station_lon = float(location["longitude"])
    st.success("Station location detected")
else:
    station_lat, station_lon = 12.9716, 77.5946
    st.warning("Using default location")

# ---------------- STATION INPUT ----------------
st.sidebar.header("Report Technical Issue")

station_name = st.sidebar.text_input("Petrol Station Name")
problem = st.sidebar.text_area("Technical Problem")

submit = st.sidebar.button("Submit Issue")

# ---------------- TECHNICIAN DATABASE (Sample) ----------------
technicians = pd.DataFrame({
    "name": ["Ravi", "Kumar", "Amit", "Suresh"],
    "lat": [12.9750, 12.9650, 12.9800, 12.9600],
    "lon": [77.6000, 77.5900, 77.6100, 77.5850],
    "status": ["Available", "Available", "Busy", "Available"]
})

# ---------------- ASSIGN TECHNICIAN ----------------
if submit:
    st.success("Issue submitted")

    available_techs = technicians[technicians["status"] == "Available"].copy()

    if available_techs.empty:
        st.error("No technicians available")
        st.stop()

    # Calculate distance
    available_techs["distance_km"] = available_techs.apply(
        lambda row: geodesic(
            (station_lat, station_lon),
            (row["lat"], row["lon"])
        ).km,
        axis=1
    )

    assigned_tech = available_techs.sort_values("distance_km").iloc[0]

    # ---------------- DISPLAY ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Station Details")
        st.write(f"**Name:** {station_name}")
        st.write(f"**Issue:** {problem}")
        st.write(f"**Location:** {station_lat}, {station_lon}")

    with col2:
        st.subheader("👨‍🔧 Assigned Technician")
        st.write(f"**Name:** {assigned_tech['name']}")
        st.write(f"**Distance:** {assigned_tech['distance_km']:.2f} km")
        st.write("**Status:** On the way")

    # ---------------- MAP ----------------
    st.subheader("🗺 Technician Assignment Map")

    m = folium.Map(location=[station_lat, station_lon], zoom_start=13)

    # Station Marker
    folium.Marker(
        [station_lat, station_lon],
        popup="Petrol Station",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    # Technician Marker
    folium.Marker(
        [assigned_tech["lat"], assigned_tech["lon"]],
        popup=f"Technician: {assigned_tech['name']}",
        icon=folium.Icon(color="green", icon="wrench")
    ).add_to(m)

    # Route
    folium.PolyLine(
        locations=[
            [assigned_tech["lat"], assigned_tech["lon"]],
            [station_lat, station_lon]
        ],
        color="blue"
    ).add_to(m)

    st_folium(m, width=1000, height=500)

else:
    st.info("Submit an issue to auto-assign a technician.")
