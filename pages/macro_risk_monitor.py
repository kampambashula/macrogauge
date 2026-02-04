# pages/macro_risk_monitor.py
import streamlit as st
from utils.data_loader import load_all_data
from utils.economic_analysis import (
    compute_recession_probability,
    classify_policy_stance,
    get_latest_valid_term_spread
)
import pandas as pd


# -------------------------------
def run():
    st.set_page_config(
        page_title="MacroGauge | Macro Risk Monitor",
        layout="wide"
    )

    st.title("🧠 Macro Risk Monitor")
    st.caption("Market-implied recession risk and policy stance assessment")

    # --- Load data
    DATA = load_all_data()
    bill_rates_df = DATA["bill_rates"]

    # ================================
    # 1️⃣ Recession Probability Gauge
    # ================================
    st.subheader("📉 Recession Risk Indicator")

    recession = compute_recession_probability(bill_rates_df)

    # Compute last valid term spread
    date_spread, latest_spread = get_latest_valid_term_spread(bill_rates_df)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Recession Probability",
            f"{recession['probability']:.0f}%",
            recession["band"]
        )
    with col2:
        if latest_spread is not None:
            st.metric(
                "Yield Curve Spread (10Y–3M)",
                f"{latest_spread:.2f} pp",
                help=f"Computed from last valid observation ({date_spread.strftime('%b %Y')})" # type: ignore
            )
        else:
            st.metric(
                "Yield Curve Spread (10Y–3M)",
                "Data unavailable"
            )
    with col3:
        st.metric(
            "Inversion Duration",
            f"{int(recession['inversion_months'])} months"
        )

    st.markdown(recession["commentary"])
    st.divider()

    # ================================
    # 2️⃣ Policy Stance Classification
    # ================================
    st.subheader("🏦 Policy Stance Assessment")

    policy = classify_policy_stance(bill_rates_df)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Policy Stance", policy["stance"])
    with col2:
        st.metric(
            "Short-Term Yield YoY",
            f"{policy['short_rate_yoy']:.1f}%"
        )

    st.markdown(policy["commentary"])

    # ================================
    # Interpretation box
    # ================================
    with st.expander("📝 How to interpret this page"):
        st.markdown(
            """
            **Recession Risk** reflects market-implied expectations derived from yield curve behavior.
            It is not a forecast, but an early-warning signal based on financial conditions.

            **Policy Stance** classifies the current macro environment as:
            - **Tight**: Restrictive conditions, elevated downside risk
            - **Neutral**: Balanced policy environment
            - **Accommodative**: Supportive of growth and credit expansion

            These indicators are best interpreted together rather than in isolation.
            """
        )

# --- Optional standalone run
if __name__ == "__main__":
    run()
