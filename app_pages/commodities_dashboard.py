# commodities_dashboard.py
import streamlit as st
from utils.data_loader import load_all_data
from utils.economic_analysis import (
    analyze_copper,
    analyze_oil,
    analyze_maize
)

def run():
    st.set_page_config(page_title="MacroGauge | Commodities Dashboard", layout="wide")
    st.title("📈 MacroGauge — Commodities Dashboard")
    st.caption("Commodity price dynamics and macroeconomic implications")

    DATA = load_all_data()
    df = DATA['commodity']

    # ================================
    # 🔶 Copper
    # ================================
    st.subheader("🔶 Copper")
    copper_commentary, copper_fig = analyze_copper(df)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(copper_fig, use_container_width=True)
    with col2:
        st.markdown(copper_commentary)

    # ================================
    # 🛢️ Oil
    # ================================
    st.subheader("🛢️ Oil")
    oil_commentary, oil_fig = analyze_oil(df)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(oil_fig, use_container_width=True)
    with col2:
        st.markdown(oil_commentary)

    # ================================
    # 🌽 Maize (Zambia)
    # ================================
    st.subheader("🌽 Maize (Domestic)")
    maize_commentary, maize_fig = analyze_maize(df)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(maize_fig, use_container_width=True)
    with col2:
        st.markdown(maize_commentary)


if __name__ == "__main__":
    run()
