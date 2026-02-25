# pages/inflation_analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px

def load_inflation_data(csv_path="data/raw/inflation.csv"):
    """Load and preprocess inflation data"""
    df = pd.read_csv(csv_path)
    # Convert 'Month' to datetime
    df['Month'] = pd.to_datetime(df['Month'], format='%d-%b-%y')
    # Sort by Month in case CSV is not sorted
    df = df.sort_values('Month')
    # Extract last 12 months
    df_last12 = df.tail(12)
    return df_last12

def run():
    st.set_page_config(page_title="MacroGauge | Inflation Analysis", layout="wide")
    st.title("📊 MacroGauge — Inflation Analysis")
    st.caption("Visualize CPI trends over the last 12 months")

    # --- Load data
    inflation_df = load_inflation_data()

    # --- Total CPI Plot
    st.subheader("📈 Total Consumer Price Index (CPI)")
    fig_total = px.line(
        inflation_df,
        x='Month',
        y='Total_Consumer_Price_Index',
        labels={'Month': 'Month', 'Total_Consumer_Price_Index': 'CPI'},
        title="Total Consumer Price Index (Last 12 Months)",
        markers=True
    )
    fig_total.update_layout(
        xaxis=dict(title='Month'),
        yaxis=dict(title='CPI'),
    )
    st.plotly_chart(fig_total, use_container_width=True)

    # --- Food vs Non-Food CPI Plot
    st.subheader("🍎 Food vs Non-Food CPI")
    fig_food = px.line(
        inflation_df,
        x='Month',
        y=['Food_Consumer_Price_Index', 'Non_Food_Consumer_Price_Index'],
        labels={'value': 'CPI', 'Month': 'Month', 'variable': 'Category'},
        title="Food vs Non-Food Consumer Price Index (Last 12 Months)",
        markers=True
    )
    fig_food.update_layout(
        xaxis=dict(title='Month'),
        yaxis=dict(title='CPI'),
        legend_title_text='Category'
    )
    st.plotly_chart(fig_food, use_container_width=True)

# --- Optional standalone run
if __name__ == "__main__":
    run()