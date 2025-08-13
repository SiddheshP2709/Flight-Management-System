# pages/view_graph.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

def load_data():
    return pd.read_csv("flights_data.csv")

def build_graph(df):
    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(
            row['source'],
            row['destination'],
            weight=row['price'],
            time=row['time'],
            airline=row['airline']
        )
    return G

def app():
    st.header("📊 Flight Route Graph")
    df = load_data()
    G = build_graph(df)

    st.subheader("Graph Visualization (Price-based Edges)")
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', ax=ax, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    st.pyplot(fig)