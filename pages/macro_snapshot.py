import streamlit as st
from datetime import datetime, timedelta

from utils.data_loader import load_all_data
from utils.transformations import (
    fx_traffic_light,
    inflation_traffic_light,
    liquidity_traffic_light,
    policy_traffic_light,
    fiscal_traffic_light,
    external_traffic_light,
    copper_traffic_light,
    oil_traffic_light
)
from utils.plotly_gauges import traffic_light_gauge
from utils.commentary_engine import macro_headline

def run():
    st.set_page_config(page_title="MacroGauge | Macro Snapshot", layout="wide")

    # --- Determine snapshot month (previous month)
    today = datetime.today()
    snapshot_date = today.replace(day=1) - timedelta(days=1)
    snapshot_month_name = snapshot_date.strftime('%B %Y')

    st.title(f"🧭 MacroGauge — {snapshot_month_name} Macro Snapshot")
    st.caption("Reading the economy in real time")

    # --- Load preprocessed data
    DATA = load_all_data()

    # --- Compute gauges and MoM
    fx_status, fx_note, fx_mom, fx_val = fx_traffic_light(DATA['forex'])
    infl_status, infl_note, infl_mom, infl_val = inflation_traffic_light(DATA['inflation'])
    liq_status, liq_note, liq_mom, liq_val = liquidity_traffic_light(DATA['liquidity'])
    policy_status, policy_note, policy_mom, policy_val = policy_traffic_light(DATA['lending_rates'])
    fiscal_status, fiscal_note, fiscal_mom, fiscal_val = fiscal_traffic_light(DATA['bills'])
    ext_status, ext_note, ext_mom, ext_val = external_traffic_light(DATA['boz_forex'])
    copper_status, copper_note, copper_mom, copper_val = copper_traffic_light(DATA['commodity'])
    oil_status, oil_note, oil_mom, oil_val = oil_traffic_light(DATA['commodity'])

    # --- Gauge Grid
    st.subheader("📊 Economic Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.plotly_chart(traffic_light_gauge(
            "FX Gauge (USD/ZMW)", fx_val, fx_val*0.9, fx_val*1.1, fx_status,
            mom_change=fx_mom, is_good_up=False
        ))
    with col2:
        st.plotly_chart(traffic_light_gauge(
            "Inflation Gauge (%)", infl_val, 0, max(15, infl_val*1.2), infl_status,
            mom_change=infl_mom, is_good_up=False
        ))
    with col3:
        st.plotly_chart(traffic_light_gauge(
            "Liquidity Gauge (Reserves)", liq_val, liq_val*0.9, liq_val*1.1, liq_status,
            mom_change=liq_mom, is_good_up=True
        ))
    with col4:
        st.plotly_chart(traffic_light_gauge(
            "Policy & Lending Rate (%)", policy_val, 0, max(20, policy_val*1.2), policy_status,
            mom_change=policy_mom, is_good_up=True
        ))

    col5, col6, col7 = st.columns(3)
    with col5:
        st.plotly_chart(traffic_light_gauge(
            "Fiscal & T-bills", fiscal_val, 0, fiscal_val*1.5, fiscal_status,
            mom_change=fiscal_mom, is_good_up=False
        ))
    with col6:
        st.plotly_chart(traffic_light_gauge(
            "External Sector (Reserves B ZMW)", ext_val, 0, ext_val*1.5, ext_status,
            mom_change=ext_mom, is_good_up=True
        ))
    with col7:
        st.plotly_chart(traffic_light_gauge(
            "Copper (USD/Tonne)", copper_val, copper_val*0.8, copper_val*1.2, copper_status,
            mom_change=copper_mom, is_good_up=True
        ))
    col8 = st.columns(1)
    with col8[0]:
        st.plotly_chart(traffic_light_gauge(
            "Oil (USD/Barrel)", oil_val, oil_val*0.8, oil_val*1.2, oil_status,
            mom_change=oil_mom, is_good_up=False
        ))

    # --- What changed this month
    st.subheader(f"🔄 What Changed in {snapshot_month_name}")
    st.markdown(f"""
    - FX: {fx_note}
    - Inflation: {infl_note}, MoM {infl_mom:+.2f}%
    - Liquidity: {liq_note}, MoM {liq_mom:+.2f}%
    - Policy: {policy_note}, MoM {policy_mom:+.2f}%
    - Fiscal: {fiscal_note}, MoM {fiscal_mom:+.2f}%
    - External: {ext_note}, MoM {ext_mom:+.2f}%
    - Copper: {copper_note}, MoM {copper_mom:+.2f}%
    - Oil: {oil_note}, MoM {oil_mom:+.2f}%
    """)

    # --- IMF-style headline at the bottom
    headline, details = macro_headline(
        fx_gauge={'status': fx_status, 'mom_change': fx_mom},
        inflation={'status': infl_status, 'value': infl_val, 'mom_change': infl_mom},
        liquidity={'status': liq_status, 'value': liq_val, 'mom_change': liq_mom},
        fiscal={'status': fiscal_status, 'value': fiscal_val, 'mom_change': fiscal_mom},
        external={'status': ext_status, 'value': ext_val, 'mom_change': ext_mom},
        commodity={
            'status_copper': copper_status, 'value_copper': copper_val, 'mom_copper': copper_mom,
            'status_oil': oil_status, 'value_oil': oil_val, 'mom_oil': oil_mom
        },
        policy_value=policy_val
    )
    st.subheader("📝 Macro Headline")
    st.markdown(headline)
