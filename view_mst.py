# Authour: SIDDHESH PATIL
# pages/view_mst.py
import streamlit as st
import pandas as pd
import heapq
from collections import defaultdict

def app():
    st.header("🌐 Minimum Spanning Tree using Prim's Algorithm (with Return Flights)")

    try:
        df = pd.read_csv("flights_data.csv")
        cities = list(set(df['source']).union(set(df['destination'])))
        selected_cities = st.multiselect("Select Cities for MST", cities)

        if st.button("Generate MST") and len(selected_cities) > 1:
            # Filter edges for selected cities and ensure both directions exist
            edges = []
            seen_edges = set()
            for _, row in df.iterrows():
                u, v, w = row['source'], row['destination'], row['price']
                if u in selected_cities and v in selected_cities:
                    if (u, v) not in seen_edges and (v, u) not in seen_edges:
                        edges.append((u, v, w))
                        edges.append((v, u, w))  # Return flight
                        seen_edges.add((u, v))

            # Build graph
            graph = defaultdict(list)
            for u, v, w in edges:
                graph[u].append((w, v))

            # Prim's algorithm
            mst = []
            visited = set()
            min_heap = [(0, selected_cities[0], None)]  # (weight, current_node, parent)

            while min_heap and len(visited) < len(selected_cities):
                weight, u, parent = heapq.heappop(min_heap)
                if u in visited:
                    continue
                visited.add(u)
                if parent:
                    mst.append((parent, u, weight))
                for next_weight, v in graph[u]:
                    if v not in visited:
                        heapq.heappush(min_heap, (next_weight, v, u))

            if len(mst) != len(selected_cities) - 1:
                st.error("Selected cities are not fully connected.")
            else:
                # Include return paths
                bidirectional_mst = mst + [(to, frm, wt) for frm, to, wt in mst]
                total_bidirectional_price = sum(row[2] for row in bidirectional_mst)
                total_oneway_price = sum(row[2] for row in mst)
                st.success("Minimum Spanning Tree with Return Flights Generated!")
                mst_df = pd.DataFrame(bidirectional_mst, columns=["From", "To", "Price"])
                st.dataframe(mst_df)
                st.metric("Total Price (one-way only)", total_oneway_price)
                st.metric("Total Price (including return flights)", total_bidirectional_price)

    except FileNotFoundError:
        st.error("flights_data.csv not found. Please upload the file.")
