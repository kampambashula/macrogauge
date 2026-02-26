# pages/external_sector.py
import streamlit as st
import plotly.express as px
from utils.data_loader import load_all_data
from utils.economic_analysis import analyze_forex, analyze_reserves

def run():
    st.set_page_config(page_title="MacroGauge | External Sector", layout="wide")
    st.title("🌐 MacroGauge — External Sector")
    st.caption("Track external sector indicators in real time")

    # --- Load preprocessed data
    DATA = load_all_data()
    df_forex = DATA['boz_forex']

    # --- FX Analysis
    fx_commentary, fx_plot_df = analyze_forex(df_forex)

    st.subheader("💱 Foreign Exchange Inflows / Outflows")
    st.markdown(f"**Commentary:** {fx_commentary}")

    fig_fx = px.line(
        fx_plot_df,
        x='Date',
        y=['Total_FX_Inflows', 'Total_FX_Outflows', 'Net_FX'],
        title="FX Inflows, Outflows, and Net FX",
        labels={'value': 'Amount (ZMW)', 'variable': 'FX Indicator'},
        markers=True
    )
    fig_fx.update_layout(xaxis_title="Date", yaxis_title="ZMW", legend_title="Indicator")
    st.plotly_chart(fig_fx, use_container_width=True)

    # --- Gross International Reserves Analysis
    reserves_commentary, reserves_plot_df = analyze_reserves(df_forex)

    st.subheader("💰 Gross International Reserves")
    st.markdown(f"**Commentary:** {reserves_commentary}")

    fig_reserves = px.line(
        reserves_plot_df,
        x='Date',
        y=['Gross_International_Reserves', 'GIR_YoY'],
        title="Gross International Reserves & YoY Change",
        labels={'value': 'ZMW', 'variable': 'Indicator'},
        markers=True
    )
    fig_reserves.update_layout(
        xaxis_title="Date",
        yaxis_title="ZMW / YoY %",
        legend_title="Indicator"
    )
    st.plotly_chart(fig_reserves, use_container_width=True)

# --- Optional standalone run
if __name__ == "__main__":
    run()
