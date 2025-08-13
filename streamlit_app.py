# Authour: SIDDHESH PATIL
# streamlit_app.py
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

# Import pages
import pages.search_flights as search_flights_manual
import pages.view_graph as view_graph
import pages.view_mst as view_mst
import pages.tsp_trip_planner as tsp_trip_planner
import pages.real_time_flights as real_time_flights

# --- PAGE CONFIG ---
st.set_page_config(page_title="Flight Management System", layout="wide")

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    selected = option_menu(
        "Flight Management",
        ["Search Flights", "Flight Graph", "MST - Prim's", "Trip Planner", "Real Time Flights"],
        menu_icon="airplane",
        default_index=0
    )

    # Show all flights button
    if st.button("📋 Show All Flights"):
        try:
            df = pd.read_csv("flights_data.csv")
            st.title("📋 All Flights Data")
            st.dataframe(df)
        except FileNotFoundError:
            st.error("flights_data.csv not found. Please upload the file.")

# --- PAGE ROUTING ---
if selected == "Search Flights":
    search_flights_manual.app()
elif selected == "Flight Graph":
    view_graph.app()
elif selected == "MST - Prim's":
    view_mst.app()
elif selected == "Trip Planner":
    tsp_trip_planner.app()
elif selected == "Real Time Flights":
    real_time_flights.app()