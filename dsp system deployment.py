import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from geopy.distance import geodesic

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
st.set_page_config(page_title="Technician Auto Assignment", layout="wide")

# ---------------- SESSION STATE ----------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "assigned_tech" not in st.session_state:
    st.session_state.assigned_tech = None

# ---------------- TITLE ----------------
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

st.write(f"Latitude: {station_lat}")
st.write(f"Longitude: {station_lon}")

# ---------------- STATION INPUT ----------------
st.sidebar.header("Report Technical Issue")

station_name = st.sidebar.text_input("Petrol Station Name")
problem = st.sidebar.text_area("Technical Problem")

if st.sidebar.button("Submit Issue"):
    st.session_state.submitted = True

# ---------------- TECHNICIAN DATABASE ----------------
technicians = pd.DataFrame({
    "name": ["Ravi", "Kumar", "Amit", "Suresh"],
    "lat": [12.9750, 12.9650, 12.9800, 12.9600],
    "lon": [77.6000, 77.5900, 77.6100, 77.5850],
    "status": ["Available", "Available", "Busy", "Available"]
})

# ---------------- ASSIGN TECHNICIAN ----------------
if st.session_state.submitted:

    st.success("Issue submitted")

    available_techs = technicians[technicians["status"] == "Available"].copy()

    available_techs["distance_km"] = available_techs.apply(
        lambda row: geodesic(
            (station_lat, station_lon),
            (row["lat"], row["lon"])
        ).km,
        axis=1
    )

    st.session_state.assigned_tech = (
        available_techs.sort_values("distance_km").iloc[0]
    )

# ---------------- DISPLAY RESULT ----------------
if st.session_state.assigned_tech is not None:

    tech = st.session_state.assigned_tech

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Station Details")
        st.write(f"**Name:** {station_name}")
        st.write(f"**Issue:** {problem}")

    with col2:
        st.subheader("👨‍🔧 Assigned Technician")
        st.write(f"**Name:** {tech['name']}")
        st.write(f"**Distance:** {tech['distance_km']:.2f} km")
        st.write("**Status:** On the way")

    # ---------------- MAP ----------------
    st.subheader("🗺 Technician Assignment Map")

    m = folium.Map(location=[station_lat, station_lon], zoom_start=13)

    folium.Marker(
        [station_lat, station_lon],
        popup="Petrol Station",
        icon=folium.Icon(color="red")
    ).add_to(m)

    folium.Marker(
        [tech["lat"], tech["lon"]],
        popup=f"Technician: {tech['name']}",
        icon=folium.Icon(color="green", icon="wrench")
    ).add_to(m)

    folium.PolyLine(
        locations=[[tech["lat"], tech["lon"]], [station_lat, station_lon]],
        color="blue"
    ).add_to(m)

    st_folium(m, width=1000, height=500)

else:
    st.info("Submit an issue to auto-assign a technician.")

# ---------------- RESET ----------------
if st.sidebar.button("Reset"):
    st.session_state.submitted = False
    st.session_state.assigned_tech = None


