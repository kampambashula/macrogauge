# pages/home.py
import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data
from utils.economic_analysis import (
    classify_fx_pressure,
    classify_inflation_trend,
    classify_yield_curve_simple,
    classify_fiscal_stress_simple,
    classify_commodity_pressure
)

def run():
    st.set_page_config(page_title="MacroGauge | Home", layout="wide")

    st.title("🧭 MacroGauge")
    st.caption("Zambia’s macroeconomic dashboard that talks")

    DATA = load_all_data()

    # ===============================
    # Latest snapshot date
    # ===============================
    latest_dates = []
    for key in DATA:
        col = "Date" if "Date" in DATA[key].columns else "Month"
        latest_dates.append(
            pd.to_datetime(DATA[key][col], errors="coerce").max()
        )

    latest_date = max(d for d in latest_dates if pd.notna(d))

    st.markdown(f"📅 **Live Snapshot:** Februray 2026")
    st.divider()

    # ===============================
    # SIGNALS
    # ===============================
    st.subheader("🚦 Macro Signals — At a Glance")

    fx_status, fx_note = classify_fx_pressure(DATA["forex"])
    inf_status, inf_note = classify_inflation_trend(DATA["inflation"])
    yc_status, yc_note = classify_yield_curve_simple(DATA["bill_rates"])
    fiscal_status, fiscal_note = classify_fiscal_stress_simple(DATA["bills"])
    comm_status, comm_note = classify_commodity_pressure(DATA["commodity"])

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("FX Pressure", fx_status)
    c2.metric("Inflation Trend", inf_status)
    c3.metric("Yield Curve", yc_status)
    c4.metric("Fiscal Stress", fiscal_status)
    c5.metric("Commodities", comm_status)

    st.divider()

    # ===============================
    # AUTO NARRATIVE
    # ===============================
    st.subheader("🗣️ What changed this month?")

    for note in [fx_note, inf_note, yc_note, fiscal_note, comm_note]:
        st.markdown(f"- {note}")

    st.divider()

    # ===============================
    # NAVIGATION (SESSION STATE)
    # ===============================
    st.subheader("🧭 Explore the System with Navigation bar - Left")

    col1, col2, col3 = st.columns(3)

    if col1.button("📄 Monthly Macro Snapshot", use_container_width=True):
        st.session_state.page = "Macro Snapshot"

    if col2.button("🧠 Macro Risk Monitor", use_container_width=True):
        st.session_state.page = "Macro Risk Indicator"

    if col3.button("🏛️ Fiscal Dashboard", use_container_width=True):
        st.session_state.page = "Fiscal Dashboard"

    col4, col5 = st.columns(2)

    if col4.button("📈 Commodities", use_container_width=True):
        st.session_state.page = "Commodities Dashboard"

    col5.button(
        "📊 Data Explorer (Coming Soon)",
        use_container_width=True,
        disabled=True
    )

    st.caption(
        "MacroGauge is a macro intelligence system and sovereign risk terminal."
    )

    st.divider()

    # ===============================
    # ABOUT
    # ===============================
    st.markdown("### 👤 About the Author")
    st.write(
        "MacroGauge is built and maintained by **Kampamba Shula** — "
        "economist, technologist, and macro systems builder."
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.link_button(
            "🌍 kampambashula.com",
            "https://kampambashula.com"
        )

if __name__ == "__main__":
    run()