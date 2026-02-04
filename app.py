import streamlit as st

# --- Import all pages
from pages import (
    home,
    macro_snapshot,
    monetary_engine,
    external_sector,
    fiscal_dashboard,
    commodities_dashboard,
    macro_risk_monitor,
    macro_brief_dashboard
)

# --- Sidebar Navigation
st.sidebar.title("🧭 MacroGauge")

page_options = [
    "Home",
    "Macro Snapshot",
    "Monetary Engine",
    "External Sector",
    "Fiscal Dashboard",
    "Commodities Dashboard",
    "Macro Risk Indicator",
    "Macro Brief"
]

# Default loads Home (index=0)
selected_page = st.sidebar.selectbox(
    "Navigate",
    page_options,
    index=0
)

# --- Page Routing
if selected_page == "Home":
    home.run()
elif selected_page == "Macro Snapshot":
    macro_snapshot.run()
elif selected_page == "Monetary Engine":
    monetary_engine.run()
elif selected_page == "External Sector":
    external_sector.run()
elif selected_page == "Fiscal Dashboard":
    fiscal_dashboard.run()
elif selected_page == "Commodities Dashboard":
    commodities_dashboard.run()
elif selected_page == "Macro Risk Indicator":
    macro_risk_monitor.run()
elif selected_page == "Macro Brief":
    macro_brief_dashboard.run()
