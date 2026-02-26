# pages/monetary_engine.py
import streamlit as st
import plotly.express as px
from utils.data_loader import load_all_data
from utils.economic_analysis import analyze_money_supply, analyze_liquidity

def run():
    st.set_page_config(page_title="MacroGauge | Monetary Engine", layout="wide")
    st.title("💰 MacroGauge — Monetary Engine")
    st.caption("Track monetary sector indicators in real time")

    # --- Load preprocessed data
    DATA = load_all_data()

    # --- Money Supply Analysis (M0, M1, M2, M3)
    m_supply_commentary, m_supply_df = analyze_money_supply(DATA['money_supply'])
    st.subheader("📈 Money Supply Overview (YoY)")
    st.markdown(f"**Analysis:** {m_supply_commentary}")

    # --- Plot Money Supply Aggregates (M0, M1, M2, M3)
    fig_money = px.line(
        m_supply_df,
        x='Date',
        y=['M0_YoY', 'M1_YoY', 'M2_YoY', 'M3_YoY'],
        labels={'value': 'YoY % Change', 'Date': 'Date', 'variable': 'Aggregate'},
        title="Money Supply YoY Changes (%)",
        markers=True
    )
    fig_money.update_layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='YoY % Change'),
        legend_title_text='Aggregate'
    )
    st.plotly_chart(fig_money, use_container_width=True)

    # --- Liquidity Analysis (Total Reserves)
    liquidity_commentary, liquidity_df = analyze_liquidity(DATA['liquidity'], start_year=2016)
    st.subheader("💧 Liquidity Overview (Total Reserves YoY)")
    st.markdown(f"**Analysis:** {liquidity_commentary}")

    fig_liq = px.line(
        liquidity_df,
        x='Date',
        y='Total_Reserves_YoY',
        labels={'Total_Reserves_YoY': 'YoY % Change', 'Date': 'Date'},
        title='Total Reserves YoY Changes (%)',
        markers=True
    )
    fig_liq.update_layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='YoY % Change')
    )
    st.plotly_chart(fig_liq, use_container_width=True)

# --- Optional standalone run
if __name__ == "__main__":
    run()
