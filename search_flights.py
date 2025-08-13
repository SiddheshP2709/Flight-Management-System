# Authour: SIDDHESH PATIL
# pages/search_flights.py
import streamlit as st
import pandas as pd
import heapq

# --- Build Graph from DataFrame ---
def build_graph(df, weight_type):
    graph = {}
    for _, row in df.iterrows():
        src, dst = row['source'], row['destination']
        weight = row[weight_type]
        graph.setdefault(src, []).append({
            'destination': dst,
            'weight': weight,
            'airline': row['airline'],
            'price': row['price'],
            'time': row['time']
        })
    return graph

# --- Dijkstra Algorithm ---
def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        if node == end:
            return cost, path
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor['destination'] not in visited:
                heapq.heappush(queue, (
                    cost + neighbor['weight'],
                    neighbor['destination'],
                    path
                ))
    return None, None

# --- Extract Path Details ---
def display_path_details(df, path):
    segments = []
    for i in range(len(path) - 1):
        row = df[(df['source'] == path[i]) & (df['destination'] == path[i+1])].iloc[0]
        segments.append(row)
    return pd.DataFrame(segments)

# --- Streamlit App ---
def app():
    st.header("🔍 Search Flights (Manual Dijkstra)")

    try:
        df = pd.read_csv("flights_data.csv")
    except FileNotFoundError:
        st.error("flights_data.csv not found.")
        return

    st.subheader("Filter Options")

    # --- Airline filter ---
    airlines = sorted(df["airline"].dropna().unique().tolist())
    selected_airlines = st.multiselect(
        "Select Preferred Airlines",
        airlines,
        default=airlines
    )

    # --- Cost filter ---
    min_cost, max_cost = int(df["price"].min()), int(df["price"].max())
    cost_range = st.slider(
        "Select Price Range",
        min_cost, max_cost,
        (min_cost, max_cost),
        step=50
    )

    # --- Duration filter ---
    min_time, max_time = int(df["time"].min()), int(df["time"].max())
    time_range = st.slider(
        "Select Duration Range (minutes)",
        min_time, max_time,
        (min_time, max_time),
        step=10
    )

    # --- Apply filters to dataset ---
    filtered_df = df[
        (df["airline"].isin(selected_airlines)) &
        (df["price"] >= cost_range[0]) & (df["price"] <= cost_range[1]) &
        (df["time"] >= time_range[0]) & (df["time"] <= time_range[1])
    ]

    # --- Source/Destination ---
    airports = sorted(set(filtered_df['source']).union(filtered_df['destination']))
    if not airports:
        st.error("No flights available with the selected filters.")
        return

    source = st.selectbox("Select Source Airport", airports)
    destination = st.selectbox("Select Destination Airport", airports)

    option = st.radio("Optimization Preference", ('Cheapest', 'Quickest'))

    if st.button("Find Best Route"):
        if filtered_df.empty:
            st.error("No flights match your filters.")
            return

        weight_type = 'price' if option == 'Cheapest' else 'time'
        graph = build_graph(filtered_df, weight_type)
        total, path = dijkstra(graph, source, destination)

        if path:
            st.success(f"Best route found ({option}): {' -> '.join(path)}")
            st.metric(label=f"Total {weight_type}", value=total)
            st.subheader("Flight Segments")
            path_df = display_path_details(filtered_df, path)
            st.dataframe(path_df)
        else:
            st.error("No path available between selected airports.")