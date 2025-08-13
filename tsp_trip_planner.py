# pages/tsp_trip_planner.py

import streamlit as st
import pandas as pd
import itertools

def load_data():
    return pd.read_csv("flights_data.csv")

def build_graph(df, cities, weight_type):
    graph = {}
    for src in cities:
        graph[src] = {}
        for dst in cities:
            if src == dst:
                continue
            flights = df[(df['source'] == src) & (df['destination'] == dst)]
            if not flights.empty:
                best = flights.sort_values(by=weight_type).iloc[0]
                graph[src][dst] = best
    return graph

def tsp_solver(graph, cities):
    best_path = None
    min_total = float('inf')
    best_segments = []

    for perm in itertools.permutations(cities):
        total = 0
        valid = True
        path_segments = []
        for i in range(len(perm) - 1):
            src = perm[i]
            dst = perm[i + 1]
            if dst not in graph.get(src, {}):
                valid = False
                break
            flight = graph[src][dst]
            total += flight['price']  # we'll switch this later if needed
            path_segments.append(flight)
        if valid and total < min_total:
            min_total = total
            best_path = perm
            best_segments = path_segments

    return best_path, best_segments, min_total

def app():
    st.header("🧭 Trip Optimizer (Visit All Cities, Any Order)")

    df = load_data()
    all_cities = sorted(set(df['source']).union(df['destination']))
    selected_cities = st.multiselect("Select Cities to Visit", all_cities)

    optimization = st.radio("Optimize For", ['Cheapest', 'Quickest'])
    weight_type = 'price' if optimization == 'Cheapest' else 'time'

    if st.button("Find Optimal Trip"):
        if len(selected_cities) < 2:
            st.warning("Select at least two cities.")
            return
        if len(selected_cities) > 8:
            st.warning("Too many cities! Limit to 8 for now due to computation.")
            return

        graph = build_graph(df, selected_cities, weight_type)
        path, segments, total = tsp_solver(graph, selected_cities)

        if not path:
            st.error("No valid complete trip found between selected cities.")
            return

        st.success(f"Optimal Trip Found ({optimization})!")
        st.markdown("** → **".join(path))
        st.metric(f"Total {weight_type}", total)
        st.subheader("Flight Segments")
        st.dataframe(pd.DataFrame(segments))
