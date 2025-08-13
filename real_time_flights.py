# Authour: SIDDHESH PATIL
# pages/real_time_flights.py

import streamlit as st
import requests
import pandas as pd

def fetch_flights(dep_iata, arr_iata, api_key):
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": api_key,
        "dep_iata": dep_iata,
        "arr_iata": arr_iata
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        return data.get('data', [])
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return []

def app():
    st.header("🛰️ Real-Time Flights Search (AviationStack API)")

    api_key = st.secrets.get("AVIATIONSTACK_API_KEY", "")
    if not api_key:
        st.error("API key not found in secrets. Please add it to .streamlit/secrets.toml")
        return

    col1, col2 = st.columns(2)
    with col1:
        dep_iata = st.text_input("Departure IATA Code", value="DEL")
    with col2:
        arr_iata = st.text_input("Arrival IATA Code", value="BOM")

    if st.button("Search Flights"):
        st.info("Fetching real-time flight data...")
        flights = fetch_flights(dep_iata, arr_iata, api_key)

        if not flights:
            st.warning("No flights found or API limit reached.")
            return

        st.success(f"Found {len(flights)} flights")

        rows = []
        for flight in flights:
            rows.append({
                "Airline": flight['airline']['name'],
                "Flight": flight['flight']['iata'],
                "Departure": flight['departure']['scheduled'],
                "Arrival": flight['arrival']['scheduled'],
                "Status": flight['flight_status']
            })

        st.dataframe(pd.DataFrame(rows))