# fiscal_dashboard.py
import streamlit as st
from utils.data_loader import load_all_data
from utils.economic_analysis import (
    analyze_bills,
    analyze_bonds,
    analyze_bill_rates,
    analyze_yield_curve,
    analyze_fiscal_stress
)

def run():
    st.set_page_config(page_title="MacroGauge | Fiscal Dashboard", layout="wide")
    st.title("🏛️ MacroGauge — Fiscal Dashboard")
    st.caption("Track fiscal indicators in real time with  analysis")

    # --- Load all data
    DATA = load_all_data()
    bills_df = DATA['bills']
    bill_rates_df = DATA['bill_rates']
    bonds_df = DATA['bonds']

    # ================================
    # 1️⃣ T-Bill Analysis
    # ================================
    st.subheader("💵 T-Bill Market")
    tbill_commentary, tbill_fig_total, tbill_fig_latest = analyze_bills(bills_df)
    st.markdown(tbill_commentary)
    st.plotly_chart(tbill_fig_total, use_container_width=True)
    st.plotly_chart(tbill_fig_latest, use_container_width=True)

    # ================================
    # 2️⃣ Bond Analysis
    # ================================
    st.subheader("📈 Government Bonds")
    bond_commentary, bond_fig_total, bond_fig_latest = analyze_bonds(bonds_df)
    st.markdown(bond_commentary)
    st.plotly_chart(bond_fig_total, use_container_width=True)
    st.plotly_chart(bond_fig_latest, use_container_width=True)

    # ================================
    # 3️⃣ T-Bill Rates Analysis
    # ================================
    st.subheader("📊 T-Bill Yields")
    yield_commentary, yield_fig_total, yield_fig_latest = analyze_bill_rates(bill_rates_df)
    st.markdown(yield_commentary)
    st.plotly_chart(yield_fig_total, use_container_width=True)
    st.plotly_chart(yield_fig_latest, use_container_width=True)

    # ================================
    # 4️⃣ Yield Curve Analysis
    # ================================
    st.subheader("📉 Yield Curve Analysis")
    yc_commentary, yc_fig_annual, yc_fig_latest = analyze_yield_curve(bill_rates_df)
    st.markdown(yc_commentary)
    st.plotly_chart(yc_fig_annual, use_container_width=True)
    st.plotly_chart(yc_fig_latest, use_container_width=True)

    # ================================
    # 5️⃣ Fiscal Stress Index
    # ================================
    st.subheader("⚠️ Fiscal Stress Index")
    stress_commentary, stress_df, fig_stress = analyze_fiscal_stress(
        bills_df=bills_df,
        bill_rates_df=bill_rates_df
    )
    st.markdown(stress_commentary)
    st.plotly_chart(fig_stress, use_container_width=True)

    # ================================
    # Optional: Show latest values in columns
    # ================================
    st.subheader("📌 Key Latest Metrics")
    latest_bill = bills_df.sort_values('Date').iloc[-1]
    latest_bond = bonds_df.sort_values('Date').iloc[-1]
    latest_yield = bill_rates_df.sort_values('Date').iloc[-1]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Latest Total T-Bill Sales", f"{latest_bill['Total_Sales']:,.0f}")
        st.metric("Outstanding Balance", f"{latest_bill['Outstanding_Balance']:,.0f}")
    with col2: 
        st.metric("Latest Weighted Avg Yield (%)", f"{latest_yield['Weighted Av.']:.2f}")

# --- Optional standalone run
if __name__ == "__main__":
    run()
