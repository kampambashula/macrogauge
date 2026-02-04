# pages/macro_brief_dashboard.py
import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data
from utils.economic_analysis import (
    summarize_fx,
    summarize_inflation,
    analyze_fiscal_stress,
    analyze_bills,
    analyze_bonds,
    analyze_yield_curve,
    summarize_commodities
)

def run():
    st.set_page_config(
        page_title="MacroGauge | Macro Brief",
        layout="wide"
    )

    st.title("📄 MacroGauge — Monthly Macro Brief")
    st.caption("Snapshot of Zambia's key macroeconomic indicators")

    # --- Load all data
    DATA = load_all_data()

    # --- Determine latest snapshot month & year dynamically
    latest_dates = [
        pd.to_datetime(DATA['forex']['Date'], errors='coerce').max(),
        pd.to_datetime(DATA['inflation']['Month'], errors='coerce').max(),
        pd.to_datetime(DATA['bills']['Date'], errors='coerce').max(),
        pd.to_datetime(DATA['bill_rates']['Date'], errors='coerce').max(),
        pd.to_datetime(DATA['bonds']['Date'], errors='coerce').max(),
        pd.to_datetime(DATA['commodity']['Date'], errors='coerce').max()
    ]
    # Remove NaT values
    latest_dates = [d for d in latest_dates if pd.notna(d)]
    latest_date = max(latest_dates)
    latest_year = latest_date.year
    latest_month = latest_date.month

    st.subheader(f"📅 Snapshot — {latest_date.strftime('%B %Y')}")

    # -------------------------------
    # FX Overview
    # -------------------------------
    fx_comment, fx_fig = summarize_fx(DATA['forex'])
    st.markdown("### 💱 FX Overview")
    st.markdown(fx_comment)
    if fx_fig is not None:
        st.plotly_chart(fx_fig, use_container_width=True)
        st.markdown("📌 *Commentary: The graph shows the USD/ZMW trend over the last 5 years. Rising values indicate local currency depreciation, which may impact import costs and inflation.*")

    # -------------------------------
    # Inflation Overview
    # -------------------------------
    inf_comment, inf_fig = summarize_inflation(DATA['inflation'])
    st.markdown("### 📊 Inflation")
    st.markdown(inf_comment)
    if inf_fig is not None:
        st.plotly_chart(inf_fig, use_container_width=True)
        st.markdown("📌 *Commentary: Year-on-year CPI movements indicate price pressure. Persistent increases highlight cost-of-living concerns, while moderation suggests policy effectiveness.*")

    # -------------------------------
    # Fiscal Overview
    # -------------------------------
    fiscal_comment, fiscal_df, fiscal_fig = analyze_fiscal_stress(
        bills_df=DATA['bills'],
        bill_rates_df=DATA['bill_rates']
    )
    st.markdown("### 🏛️ Fiscal Overview")
    st.markdown(fiscal_comment)
    if fiscal_fig is not None:
        st.plotly_chart(fiscal_fig, use_container_width=True)
        st.markdown("📌 *Commentary: The fiscal stress index illustrates liquidity and debt pressure in the government. Peaks may indicate tighter funding conditions.*")

    # -------------------------------
    # T-Bills & Bonds
    # -------------------------------
    tbill_comment, tbill_fig_total, tbill_fig_latest = analyze_bills(DATA['bills'])
    bond_comment, bond_fig_total, bond_fig_latest = analyze_bonds(DATA['bonds'])
    st.markdown("### 💵 T-Bills & Bonds")
    st.markdown(tbill_comment)
    st.plotly_chart(tbill_fig_total, use_container_width=True)
    st.plotly_chart(tbill_fig_latest, use_container_width=True)
    st.markdown("📌 *Commentary: Total T-bill sales and outstanding balances show short-term funding trends and market appetite. The latest issuance may indicate government borrowing needs.*")
    st.markdown(bond_comment)
    st.plotly_chart(bond_fig_total, use_container_width=True)
    st.plotly_chart(bond_fig_latest, use_container_width=True)
    st.markdown("📌 *Commentary: Government bond stock by tenor reveals debt structure and rollover risks. Longer tenors dominate if the government is locking funding for future years.*")

    # -------------------------------
    # Commodities
    # -------------------------------
    comm_comment, comm_fig = summarize_commodities(DATA['commodity'])
    st.markdown("### 📈 Commodities")
    st.markdown(comm_comment)
    if comm_fig is not None:
        st.plotly_chart(comm_fig, use_container_width=True)
        st.markdown("📌 *Commentary: Copper prices drive Zambia's export revenue, while maize prices reflect local food security and inflation pressure. Oil prices affect production costs.*")

    # -------------------------------
    # Yield Curve
    # -------------------------------
    yc_comment, yc_fig_annual, yc_fig_latest = analyze_yield_curve(DATA['bill_rates'])
    st.markdown("### 📉 Yield Curve")
    st.markdown(yc_comment)
    if yc_fig_annual is not None:
        st.plotly_chart(yc_fig_annual, use_container_width=True)
    if yc_fig_latest is not None:
        st.plotly_chart(yc_fig_latest, use_container_width=True)
    st.markdown("📌 *Commentary: The shape of the yield curve signals market expectations. Normal curves indicate growth optimism; inverted curves warn of potential slowdowns.*")

    # -------------------------------
    # Key Metrics Summary
    # -------------------------------
    st.subheader("📌 Key Metrics — Latest Values")
    latest_fx = DATA['forex'].sort_values('Date').iloc[-1]
    latest_inf = DATA['inflation'].sort_values('Month').iloc[-1]
    latest_fiscal = fiscal_df.sort_values('Date').iloc[-1] if fiscal_df is not None else None
    latest_copper = DATA['commodity'].sort_values('Date').iloc[-1]['Copper_US_Tonne']
    latest_maize = DATA['commodity'].sort_values('Date').iloc[-1]['Maize_K_50Kg']

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("USD/ZMW Exchange Rate", f"{latest_fx['USDZMW']:.2f}")
        st.markdown("💡 *Exchange rate trends reflect currency strength and external pressures.*")
    with col2:
        if latest_fiscal is not None:
            st.metric("T-Bills Total Sales", f"{latest_fiscal['Total_Sales']:,.0f}")
            
        st.markdown("💡 *Fiscal metrics indicate government funding conditions and debt sustainability.*")
    with col3:
        st.metric("Copper (US$/Tonne)", f"{latest_copper:,.0f}")
        st.metric("Maize (K/50Kg)", f"{latest_maize:,.0f}")
        st.markdown("💡 *Copper is Zambia's main export; maize prices affect food security and inflation.*")
