import pandas as pd
import numpy as np

# --- FX Traffic Light
def fx_traffic_light(df_fx, lookback_months=1):
    df = df_fx.copy().sort_values('Date')
    last_value = df['USDZMW'].iloc[-1]
    prev_value = df['USDZMW'].iloc[-lookback_months-1]
    mom_change = (last_value - prev_value) / prev_value * 100

    # Down = good (appreciation), Up = bad (depreciation)
    if mom_change < 0:
        status = 'green'
    elif 0 <= mom_change < 3:
        status = 'amber'
    else:
        status = 'red'

    note = f"{lookback_months}-month % change: {mom_change:.2f}%"
    return status, note, mom_change, last_value


# --- Inflation Traffic Light
def inflation_traffic_light(df_inflation, target_rate=7.0):
    df = df_inflation.copy().sort_values('Month')
    last_value = df['Inflation_Annual'].iloc[-1]
    prev_value = df['Inflation_Annual'].iloc[-2]
    mom_change = last_value - prev_value

    # Down = good (inflation slowing), Up = bad
    if last_value <= target_rate:
        status = 'green'
    elif target_rate < last_value <= target_rate + 3:
        status = 'amber'
    else:
        status = 'red'

    note = f"Latest inflation: {last_value:.2f}%"
    return status, note, mom_change, last_value


# --- Liquidity Traffic Light
def liquidity_traffic_light(df_liquidity):
    df = df_liquidity.copy().sort_values('Date')
    last_value = df['Total_Reserves'].iloc[-1]
    prev_value = df['Total_Reserves'].iloc[-2]
    mom_change = (last_value - prev_value) / prev_value * 100 if prev_value != 0 else np.nan

    # Up = good, Down = bad
    if mom_change > 0:
        status = 'green'
    elif 0 >= mom_change > -5:
        status = 'amber'
    else:
        status = 'red'

    note = f"MoM % change in reserves: {mom_change:.2f}%" if not np.isnan(mom_change) else "MoM change: n/a"
    return status, note, mom_change, last_value


# --- Policy / Lending Traffic Light
def policy_traffic_light(df_policy):
    df = df_policy.copy().sort_values('Date')
    last_value = df['BoZ_Policy_Rate'].iloc[-1]
    prev_value = df['BoZ_Policy_Rate'].iloc[-2]
    mom_change = last_value - prev_value

    # Higher rate = tight, can keep as-is
    if last_value <= 7:
        status = 'green'
    elif 7 < last_value <= 10:
        status = 'amber'
    else:
        status = 'red'

    note = f"BoZ policy rate: {last_value:.2f}%"
    return status, note, mom_change, last_value


# --- Fiscal / T-bills Traffic Light
def fiscal_traffic_light(df_bills):
    df = df_bills.copy().sort_values('Date')
    this_month_sales = df['Total_Sales'].iloc[-1]
    prev_month_sales = df['Total_Sales'].iloc[-2] if len(df) > 1 else np.nan
    mom_change = (this_month_sales - prev_month_sales)/prev_month_sales*100 if prev_month_sales else np.nan

    ratio = this_month_sales / df['Opening _Balance'].iloc[-1] if df['Opening _Balance'].iloc[-1] else 0

    # Down = good (lower spending/pressure), Up = bad
    if ratio < 0.2:
        status = 'green'
    elif 0.2 <= ratio < 0.4:
        status = 'amber'
    else:
        status = 'red'

    note = f"MoM T-bills sales change: {mom_change:.2f}%" if not np.isnan(mom_change) else "MoM change: n/a"
    return status, note, mom_change, this_month_sales


# --- External Sector / Gross Reserves Traffic Light
def external_traffic_light(df_forex):
    df = df_forex.copy().sort_values('Date')
    last_value = df['Gross_International_Reserves'].iloc[-1] / 1e3  # billions
    prev_value = df['Gross_International_Reserves'].iloc[-2] / 1e3
    mom_change = (last_value - prev_value)/prev_value*100

    # Up = good, Down = bad
    if last_value >= 5.0:
        status = 'green'
    elif 4.0 <= last_value < 5.0:
        status = 'amber'
    else:
        status = 'red'

    note = f"Gross reserves: {last_value:.1f} B ZMW"
    return status, note, mom_change, last_value


# --- Commodity Traffic Lights (Separate)
def copper_traffic_light(df_commodity, copper_base=8000):
    df = df_commodity.copy().sort_values('Date')
    last_value = df['Copper_US_Tonne'].iloc[-1]
    prev_value = df['Copper_US_Tonne'].iloc[-2]
    mom_change = (last_value - prev_value)/prev_value*100

    # Up = good
    if last_value >= copper_base:
        status = 'green'
    elif last_value >= copper_base*0.9:
        status = 'amber'
    else:
        status = 'red'

    note = f"Copper: {last_value:.2f} USD/Tonne"
    return status, note, mom_change, last_value


def oil_traffic_light(df_commodity, oil_base=70):
    df = df_commodity.copy().sort_values('Date')
    last_value = df['Oil_US_barrel'].iloc[-1]
    prev_value = df['Oil_US_barrel'].iloc[-2]
    mom_change = (last_value - prev_value)/prev_value*100

    # Up = good
    if last_value <= oil_base:
        status = 'green'
    elif last_value <= oil_base*1.1:
        status = 'amber'
    else:
        status = 'red'

    note = f"Oil: {last_value:.2f} USD/barrel"
    return status, note, mom_change, last_value


# --- Plotly Gauge Wrapper
def traffic_light_gauge(title, value, min_val, max_val, status, mom_change=None, confidence=None):
    import plotly.graph_objects as go

    color_map = {
        "green": "#2ecc71",
        "amber": "#f39c12",
        "red": "#e74c3c"
    }

    delta_config = None
    if mom_change is not None:
        delta_config = {
            "reference": value - mom_change,
            "position": "top",
            "increasing": {"color": "#2ecc71", "symbol": "▲"},   # Up = good
            "decreasing": {"color": "#e74c3c", "symbol": "▼"},   # Down = bad
        }

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta" if mom_change is not None else "gauge+number",
            value=value,
            delta=delta_config,
            title={"text": title},
            gauge={
                "axis": {"range": [min_val, max_val]},
                "bar": {"color": color_map.get(status, "gray")},
                "steps": [
                    {"range": [min_val, min_val + (max_val - min_val)*0.5], "color": "#ecf0f1"},
                    {"range": [min_val + (max_val - min_val)*0.5, min_val + (max_val - min_val)*0.75], "color": "#fef5e7"},
                    {"range": [min_val + (max_val - min_val)*0.75, max_val], "color": "#fdecea"},
                ],
            },
            number={"suffix": "%"} if "%" in title else {}
        )
    )

    if confidence is not None:
        fig.add_annotation(
            text=f"Confidence: {confidence}%",
            x=0.5,
            y=-0.25,
            showarrow=False,
            font=dict(size=12),
            xref="paper",
            yref="paper",
        )

    fig.update_layout(height=280, margin=dict(l=20, r=20, t=60, b=40))
    return fig
