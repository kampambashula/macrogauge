# utils/economic_analysis.py
import pandas as pd
import numpy as np
import plotly.express as px

def analyze_money_supply(df: pd.DataFrame):
    """
    Analyze money supply aggregates (M0, M1, M2, M3) and provide IMF-style commentary
    based on Year-over-Year (YoY) changes.

    Returns:
        commentary: str
        df_agg: pd.DataFrame with Date, M0, M1, M2, M3, and YoY changes
    """

    df = df.copy().sort_values('Date')
    df['Date'] = pd.to_datetime(df['Date'])

    # --- Map CSV columns to standard monetary aggregates
    df['M0'] = df['Currency_with_non_Bank']
    df['M1'] = df['Narrow_Money_M1']
    df['M2'] = df['Broad_Money_M2']
    df['M3'] = df['Broad_Money_M3']

    # --- Compute YoY % changes
    for col in ['M0', 'M1', 'M2', 'M3']:
        df[f'{col}_YoY'] = df[col].pct_change(periods=12) * 100

    # --- Generate dynamic commentary based on latest changes and trends
    last_row = df.iloc[-1]
    commentary_lines = []

    # Basic YoY changes commentary
    for col in ['M1', 'M2', 'M3']:
        yoy = last_row[f'{col}_YoY']
        trend = "increased" if yoy > 0 else "decreased" if yoy < 0 else "stable"
        commentary_lines.append(f"{col} has {trend} by {yoy:.2f}% YoY to {last_row[col]:,.0f} ZMW.")

    # Compare broad vs narrow money trends
    if last_row['M2_YoY'] > last_row['M1_YoY'] and last_row['M3_YoY'] > last_row['M1_YoY']:
        commentary_lines.append(
            "Broad money (M2, M3) is expanding faster than narrow money (M1), "
            "indicating increased bank deposits and liquidity in the financial system."
        )
    elif last_row['M1_YoY'] > last_row['M2_YoY'] and last_row['M1_YoY'] > last_row['M3_YoY']:
        commentary_lines.append(
            "Narrow money (M1) is growing faster than broad aggregates (M2, M3), "
            "which may indicate stronger transactional demand rather than deposits."
        )

    # Detect unusually high changes
    for col in ['M0', 'M1', 'M2', 'M3']:
        yoy = last_row[f'{col}_YoY']
        if yoy > 20:
            commentary_lines.append(f"{col} is rising sharply (+{yoy:.2f}% YoY), signaling rapid liquidity growth.")
        elif yoy < -10:
            commentary_lines.append(f"{col} has contracted significantly (-{yoy:.2f}% YoY), signaling tightening liquidity.")

    commentary = "\n".join(commentary_lines)

    # Return commentary and DataFrame for plotting
    df_plot = df[['Date', 'M0', 'M1', 'M2', 'M3', 'M0_YoY', 'M1_YoY', 'M2_YoY', 'M3_YoY']].copy()

    return commentary, df_plot


def analyze_liquidity(df: pd.DataFrame, start_year=2016):
    """
    Analyze liquidity trends using Total Reserves with YoY % change.
    Returns commentary and DataFrame filtered from start_year.
    """

    df = df.copy().sort_values('Date')
    df['Date'] = pd.to_datetime(df['Date'])

    # --- Filter for a long-term view (default: from 2016)
    df['Year'] = df['Date'].dt.year # type: ignore
    df_plot = df[df['Year'] >= start_year].copy()

    # Compute YoY % change
    df_plot['Total_Reserves_YoY'] = df_plot['Total_Reserves'].pct_change(periods=12) * 100

    # --- Generate dynamic commentary
    last_row = df_plot.iloc[-1]
    yoy_change = last_row['Total_Reserves_YoY']
    value = last_row['Total_Reserves']
    trend = "increased" if yoy_change > 0 else "decreased" if yoy_change < 0 else "stable"

    commentary = (
        f"Total reserves have {trend} by {yoy_change:.2f}% YoY to {value:,.0f} ZMW. "
        f"Over the period from {start_year}, liquidity trends show accumulation or drawdown in reserves."
    )

    return commentary, df_plot[['Date', 'Total_Reserves', 'Total_Reserves_YoY']]


def analyze_forex(df_forex: pd.DataFrame):
    """
    Analyze FX inflows and outflows, compute YoY changes, net FX, and generate dynamic commentary.

    Parameters
    ----------
    df_forex : pd.DataFrame
        BOZ Forex data with inflow/outflow columns.

    Returns
    -------
    commentary : str
        Dynamic IMF-style commentary on FX flows.
    df_plot : pd.DataFrame
        DataFrame for plotting: Total inflows, Total outflows, Net FX.
    """
    df = df_forex.copy().sort_values('Date')

    # --- Aggregate inflows and outflows
    inflow_cols = [
        'BOZ_Inflows_Mines',
        'BOZ_Inflows_Other_Non-GRZ',
        'BOZ_Inflows_Mining_Taxes',
        'BOZ_Inflows_Donor_Inflows'
    ]
    outflow_cols = [
        'BOZ_Outflows_Dealing_Net_Sales',
        'BOZ_Outflows_Other_Non-GRZ',
        'BOZ_Outflows_GRZ_Debt_Servicing',
        'BOZ_Outflows_GRZ_Other_Uses'
    ]

    df['Total_FX_Inflows'] = df[inflow_cols].sum(axis=1)
    df['Total_FX_Outflows'] = df[outflow_cols].sum(axis=1)
    df['Net_FX'] = df['Total_FX_Inflows'] - df['Total_FX_Outflows']

    # --- Compute YoY % changes
    df['Total_FX_Inflows_YoY'] = df['Total_FX_Inflows'].pct_change(periods=12) * 100
    df['Total_FX_Outflows_YoY'] = df['Total_FX_Outflows'].pct_change(periods=12) * 100
    df['Net_FX_YoY'] = df['Net_FX'].pct_change(periods=12) * 100

    # --- Dynamic commentary
    last_net_fx = df['Net_FX'].iloc[-1]
    last_net_fx_yoy = df['Net_FX_YoY'].iloc[-1]

    commentary = f"Latest Net FX position: {last_net_fx/1e3:.2f} B ZMW "
    commentary += f"with a YoY change of {last_net_fx_yoy:.2f}%. "

    inflow_dominant = df[inflow_cols].iloc[-1].idxmax().replace('BOZ_Inflows_', '').replace('_', ' ') # type: ignore
    outflow_dominant = df[outflow_cols].iloc[-1].idxmax().replace('BOZ_Outflows_', '').replace('_', ' ') # type: ignore

    if last_net_fx_yoy > 0:
        commentary += f"FX inflows exceeded outflows, primarily driven by {inflow_dominant}. This supports external stability."
    elif last_net_fx_yoy < 0:
        commentary += f"FX outflows exceeded inflows, mainly due to {outflow_dominant}. This may exert pressure on the exchange rate."
    else:
        commentary += "FX inflows and outflows are broadly balanced."

    # --- Prepare df for plotting
    df_plot = df[['Date', 'Total_FX_Inflows', 'Total_FX_Outflows', 'Net_FX']].copy()

    return commentary, df_plot


# -------------------------------
# Gross International Reserves (GIR) Analysis
# -------------------------------
def analyze_reserves(df_forex: pd.DataFrame):
    """
    Analyze Gross International Reserves, compute YoY changes, and generate dynamic commentary.

    Parameters
    ----------
    df_forex : pd.DataFrame
        BOZ Forex data with 'Gross_International_Reserves' column.

    Returns
    -------
    commentary : str
        IMF-style commentary on reserves trends.
    df_plot : pd.DataFrame
        DataFrame for plotting GIR YoY changes.
    """
    df = df_forex.copy().sort_values('Date')

    # --- Compute YoY % change
    df['GIR_YoY'] = df['Gross_International_Reserves'].pct_change(periods=12) * 100

    last_value = df['Gross_International_Reserves'].iloc[-1]
    last_yoy = df['GIR_YoY'].iloc[-1]

    commentary = f"Gross International Reserves stand at {last_value/1e3:.2f} B ZMW "
    commentary += f"with a YoY change of {last_yoy:.2f}%. "

    if last_yoy > 5:
        commentary += "This robust growth indicates a strong external buffer and improved liquidity."
    elif last_yoy < 0:
        commentary += "Declining reserves may signal pressure on external stability and require monitoring."
    else:
        commentary += "Reserves remain broadly stable, supporting exchange rate stability."

    # --- Prepare df for plotting
    df_plot = df[['Date', 'Gross_International_Reserves', 'GIR_YoY']].copy()

    return commentary, df_plot

def analyze_bills(df_bills: pd.DataFrame):
    """
    Analyze T-Bill issuance, compute YoY changes, tenor composition, and generate plots.

    Returns:
        commentary: str
        fig_total: px.line - total sales over time
        fig_latest: px.bar - latest T-Bill sales composition
    """
    df = df_bills.copy().sort_values('Date')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # --- Compute YoY changes for Total Sales and Outstanding Balance
    df['Total_Sales_YoY'] = df['Total_Sales'].pct_change(periods=12) * 100
    df['Outstanding_Balance_YoY'] = df['Outstanding_Balance'].pct_change(periods=12) * 100

    # --- Tenor composition percentages
    for tenor in ['91_days', '182_days', '273_days', '364_days']:
        # Ensure numeric
        df[tenor] = pd.to_numeric(df[tenor], errors='coerce')
        df['Total_Sales'] = pd.to_numeric(df['Total_Sales'], errors='coerce')
        df[f'{tenor}_pct'] = df[tenor] / df['Total_Sales'] * 100

    # --- Dynamic commentary
    last_row = df.iloc[-1]
    commentary = (
        f"Total T-Bill sales changed {last_row['Total_Sales_YoY']:.2f}% YoY, "
        f"with outstanding balances changing {last_row['Outstanding_Balance_YoY']:.2f}% YoY. "
    )
    # Top tenor
    tenor_cols_pct = ['91_days_pct','182_days_pct','273_days_pct','364_days_pct']
    top_tenor = last_row[tenor_cols_pct].idxmax().replace('_pct','') # type: ignore
    commentary += f"The {top_tenor} tenor dominates recent issuance."

    # --- Figures
    # 1. Total T-Bill sales over time
    fig_total = px.line(
        df,
        x='Date',
        y='Total_Sales',
        title="Total T-Bill Sales Over Time",
        markers=True
    )

    # 2. Latest T-Bill composition (bar)
    latest_row_tenors = last_row[['91_days','182_days','273_days','364_days']]
    df_plot = latest_row_tenors.reset_index()
    df_plot.columns = ['Tenor', 'Value']

    fig_latest = px.bar(
        df_plot,
        x='Tenor',
        y='Value',
        title=f"Latest T-Bill Sales Composition — {last_row['Date'].strftime('%b %Y')}"
    )

    return commentary, fig_total, fig_latest


# -------------------------------
# T-Bill Rates Analysis
# -------------------------------
def analyze_bill_rates(df_rates: pd.DataFrame):
    df = df_rates.copy().sort_values('Date')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Ensure numeric
    rate_cols = ['91 days','182 days','273 days','364 days','Weighted Av.']
    df[rate_cols] = df[rate_cols].apply(pd.to_numeric, errors='coerce')

    # YoY change
    df['Weighted_Avg_YoY'] = df['Weighted Av.'].pct_change(periods=12) * 100
    last_yoy = df['Weighted_Avg_YoY'].iloc[-1]

    commentary = f"Weighted average T-Bill yields changed {last_yoy:.2f}% YoY, indicating market cost of short-term funding."

    # --- Figures
    # 1. Weighted Avg over time
    fig_total = px.line(df, x='Date', y='Weighted Av.',
                        title="Weighted Avg T-Bill Yields Over Time", markers=True)

    # 2. Latest yields composition (long format for Plotly)
    last_row = df.iloc[-1]
    df_plot = last_row[rate_cols].reset_index()
    df_plot.columns = ['Tenor', 'Yield']
    fig_latest = px.bar(df_plot, x='Tenor', y='Yield',
                        title=f"Latest T-Bill Yields — {last_row['Date'].strftime('%b %Y')}")

    return commentary, fig_total, fig_latest


# -------------------------------
# Bond Analysis
# -------------------------------
def analyze_bonds(df_bonds: pd.DataFrame):
    df = df_bonds.copy().sort_values('Date')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Ensure numeric for sales and maturities
    for tenor in ['3_Year', '5_Year', '7_Year', '10_Year', '15_Year']:
        df[f'{tenor}_Sales'] = pd.to_numeric(df[f'{tenor}_Sales'], errors='coerce')
        df[f'{tenor}_Maturities'] = pd.to_numeric(df[f'{tenor}_Maturities'], errors='coerce')
        df[f'{tenor}_Net'] = df[f'{tenor}_Sales'] - df[f'{tenor}_Maturities']

    # Total Bond Stock
    bond_cols = ['Bonds_24_months', 'Bonds_3_year', 'Bonds_5_year',
                 'Bonds_7_year', 'Bonds_10_year', 'Bonds_15_year']
    df[bond_cols] = df[bond_cols].apply(pd.to_numeric, errors='coerce')
    df['Bonds_TOTAL'] = df[bond_cols].sum(axis=1)
    df['Bonds_TOTAL_YoY'] = df['Bonds_TOTAL'].pct_change(periods=12) * 100

    # Dynamic commentary
    last_row = df.iloc[-1]
    last_total_yoy = last_row['Bonds_TOTAL_YoY']
    largest_tenor = last_row[bond_cols].idxmax()
    commentary = (
        f"Total government bond stock changed {last_total_yoy:.2f}% YoY. "
        f"The {largest_tenor} tenor represents the largest portion of outstanding bonds."
    )

    # --- Figures
    # Total Bonds over time
    fig_total = px.line(df, x='Date', y='Bonds_TOTAL',
                        title="Total Outstanding Bonds Over Time", markers=True)

    # Latest bond composition (long format for Plotly)
    df_plot = last_row[bond_cols].reset_index()
    df_plot.columns = ['Tenor', 'Value']
    fig_latest = px.bar(df_plot, x='Tenor', y='Value',
                        title=f"Latest Bond Outstanding by Tenor — {last_row['Date'].strftime('%b %Y')}")

    return commentary, fig_total, fig_latest


def analyze_yield_curve(df_rates: pd.DataFrame):
    df = df_rates.copy()

    # --- Date handling
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.sort_values('Date')

    # --- Tenors and maturity mapping
    tenors = [
        '91 days', '182 days', '273 days', '364 days',
        '24 months', '3 year', '5 year', '7 year', '10 year', '15 year'
    ]
    tenor_months = {
        '91 days': 3,
        '182 days': 6,
        '273 days': 9,
        '364 days': 12,
        '24 months': 24,
        '3 year': 36,
        '5 year': 60,
        '7 year': 84,
        '10 year': 120,
        '15 year': 180
    }

    # --- Force numeric
    for t in tenors:
        if t in df.columns:
            df[t] = pd.to_numeric(df[t], errors='coerce')

    # Drop rows with no valid yields at all
    df = df.dropna(subset=[t for t in tenors if t in df.columns], how='all')

    # =========================
    # Latest Yield Curve
    # =========================
    latest = df.iloc[-1]

    df_latest = (
        pd.DataFrame({
            'Tenor': tenors,
            'Yield (%)': [latest.get(t, None) for t in tenors]
        })
        .dropna(subset=['Yield (%)'])
    )

    df_latest['Maturity (Months)'] = df_latest['Tenor'].map(tenor_months)

    # --- Safe curve shape detection using first vs last yield
    if len(df_latest) >= 2:
        slope = df_latest['Yield (%)'].iloc[-1] - df_latest['Yield (%)'].iloc[0]
        if slope > 0.25:
            shape_comment = (
                "The yield curve is upward sloping (normal), "
                "indicating positive growth and moderate inflation expectations."
            )
        elif slope < -0.25:
            shape_comment = (
                "The yield curve is inverted, signaling expectations of slowing growth "
                "or potential recession."
            )
        else:
            shape_comment = (
                "The yield curve is relatively flat, suggesting uncertainty in the economic outlook."
            )
    else:
        shape_comment = "Insufficient data to determine the yield curve shape."

    commentary_latest = (
        f"As of {latest['Date'].strftime('%b %Y')}, the yield curve shows:\n"
        + ", ".join(
            f"{row.Tenor}: {row['Yield (%)']:.2f}%"
            for _, row in df_latest.iterrows()
        )
        + ".\n"
        + shape_comment
    )

    # --- Latest curve figure
    fig_latest = px.line(
        df_latest,
        x='Maturity (Months)',
        y='Yield (%)',
        markers=True,
        text='Tenor',
        title=f"Latest Yield Curve — {latest['Date'].strftime('%b %Y')}"
    )
    fig_latest.update_traces(textposition="top center")
    fig_latest.update_layout(height=420, margin=dict(l=20, r=20, t=60, b=40))

    # =========================
    # Annual Average Yield Curve
    # =========================
    df['Year'] = df['Date'].dt.year # type: ignore
    annual_avg = (
        df.groupby('Year')[tenors]
        .mean()
        .reset_index()
        .dropna(how='all', subset=tenors)
    )

    latest_year = annual_avg['Year'].iloc[-1]

    df_annual_latest = (
        annual_avg[annual_avg['Year'] == latest_year]
        .melt(id_vars='Year', var_name='Tenor', value_name='Yield (%)')
        .dropna(subset=['Yield (%)'])
    )

    df_annual_latest['Maturity (Months)'] = df_annual_latest['Tenor'].map(tenor_months)

    fig_annual = px.line(
        df_annual_latest,
        x='Maturity (Months)',
        y='Yield (%)',
        markers=True,
        text='Tenor',
        title=f"Annual Average Yield Curve — {latest_year}"
    )
    fig_annual.update_traces(textposition="top center")
    fig_annual.update_layout(height=420, margin=dict(l=20, r=20, t=60, b=40))

    return commentary_latest, fig_annual, fig_latest





def analyze_yield_curve_stress(df_rates: pd.DataFrame):
    """
    Computes yield curve slope and stress signal over time.
    """

    df = df_rates.copy().sort_values("Date")
    df["Date"] = pd.to_datetime(df["Date"])

    short_tenors = ["91 days", "182 days", "273 days", "364 days"]
    long_tenors = ["5 year", "7 year", "10 year", "15 year"]

    df["Short_Yield_Avg"] = df[short_tenors].mean(axis=1)
    df["Long_Yield_Avg"] = df[long_tenors].mean(axis=1)

    # Positive = inverted
    df["Yield_Curve_Slope"] = df["Short_Yield_Avg"] - df["Long_Yield_Avg"]

    def label_curve(slope):
        if slope > 0.5:
            return "Inverted"
        elif slope > -0.5:
            return "Flat"
        else:
            return "Normal"

    df["Yield_Curve_Regime"] = df["Yield_Curve_Slope"].apply(label_curve)

    latest = df.iloc[-1]

    commentary = (
        f"The yield curve is currently **{latest['Yield_Curve_Regime'].lower()}**, "
        f"with short-term yields averaging {latest['Short_Yield_Avg']:.2f}% "
        f"and long-term yields at {latest['Long_Yield_Avg']:.2f}%. "
    )

    if latest["Yield_Curve_Regime"] == "Inverted":
        commentary += (
            "This configuration increases rollover risk and amplifies fiscal stress, "
            "especially where short-term issuance dominates."
        )
    elif latest["Yield_Curve_Regime"] == "Flat":
        commentary += (
            "This suggests uncertainty in market expectations and limited scope "
            "for cost-efficient debt terming."
        )
    else:
        commentary += (
            "This supports stable financing conditions and reduces short-term refinancing pressure."
        )

    return commentary, df

def analyze_fiscal_stress(
    bills_df: pd.DataFrame,
    bill_rates_df: pd.DataFrame
):
    """
    Construct a Fiscal Stress Index using:
    1. Yield pressure (latest Weighted Avg T-Bill YoY)
    2. Rollover risk
    3. Issuance intensity

    Returns:
        commentary: str
        df: pd.DataFrame with Fiscal_Stress_Index and Fiscal_Regime
        fig: plotly Figure showing stress index over time with regimes
    """

    bills = bills_df.copy()
    rates = bill_rates_df.copy()

    bills['Date'] = pd.to_datetime(bills['Date'], errors='coerce')
    rates['Date'] = pd.to_datetime(rates['Date'], errors='coerce')

    bills = bills.sort_values('Date')
    rates = rates.sort_values('Date')

    # -----------------------------
    # 1. Yield pressure (Weighted Avg YoY)
    # -----------------------------
    rates['Weighted_Yield_YoY'] = rates['Weighted Av.'].pct_change(12) * 100

    # -----------------------------
    # 2. Rollover risk (short-term concentration)
    # -----------------------------
    bills['Short_Term_Ratio'] = (
        bills['Outstanding_Balance_91_days'] +
        bills['Outstanding_Balance_182_days']
    ) / bills['Outstanding_Balance']

    # -----------------------------
    # 3. Issuance intensity (12m sales vs stock)
    # -----------------------------
    bills['Issuance_12m'] = bills['Total_Sales'].rolling(12).sum()
    bills['Issuance_Pressure'] = bills['Issuance_12m'] / bills['Outstanding_Balance']

    # -----------------------------
    # Merge yield info
    # -----------------------------
    df = bills.merge(
        rates[['Date', 'Weighted_Yield_YoY']],
        on='Date',
        how='inner'
    ).dropna()

    # -----------------------------
    # Standardisation (z-score)
    # -----------------------------
    def zscore(series):
        return (series - series.mean()) / series.std()

    df['z_yield'] = zscore(df['Weighted_Yield_YoY']).clip(-3, 3)
    df['z_rollover'] = zscore(df['Short_Term_Ratio']).clip(-3, 3)
    df['z_issuance'] = zscore(df['Issuance_Pressure']).clip(-3, 3)

    # -----------------------------
    # Fiscal Stress Index
    # -----------------------------
    df['Fiscal_Stress_Index'] = (
        df['z_yield'] +
        df['z_rollover'] +
        df['z_issuance']
    ) / 3

    # -----------------------------
    # Automatic regime labeling
    # -----------------------------
    def label_stress(x):
        if x <= -0.5:
            return "Accommodative"
        elif x <= 0.5:
            return "Neutral"
        elif x <= 1.5:
            return "Tightening"
        elif x <= 2.5:
            return "Stressed"
        else:
            return "Critical"

    df['Fiscal_Regime'] = df['Fiscal_Stress_Index'].apply(label_stress)

    # -----------------------------
    # Commentary (latest observation)
    # -----------------------------
    latest = df.iloc[-1]

    commentary = (
        f"The Fiscal Stress Index currently stands at "
        f"{latest['Fiscal_Stress_Index']:.2f}, placing the domestic "
        f"financing environment in a **{latest['Fiscal_Regime']}** regime. "
    )

    if latest['Fiscal_Regime'] in ["Stressed", "Critical"]:
        commentary += (
            "This reflects rising funding costs, elevated rollover exposure, "
            "and increased issuance pressure, which together signal "
            "heightened vulnerability in domestic debt markets."
        )
    elif latest['Fiscal_Regime'] == "Tightening":
        commentary += (
            "Financing conditions are tightening, suggesting emerging cost "
            "and liquidity pressures that warrant close monitoring."
        )
    else:
        commentary += (
            "Domestic financing conditions remain broadly supportive, "
            "with manageable costs and refinancing risks."
        )

    # -----------------------------
    # Figure for stress index over time
    # -----------------------------
    import plotly.express as px
    fig = px.line(
        df,
        x="Date",
        y="Fiscal_Stress_Index",
        color="Fiscal_Regime",
        title="Fiscal Stress Index Over Time with Regime Labels"
    )

    return commentary, df, fig


def compute_recession_probability(df_rates: pd.DataFrame):
    """
    Computes a probability-weighted recession risk using yield curve signals.
    Returns probability, risk band, and commentary.
    """

    df = df_rates.copy().sort_values("Date")
    df["Date"] = pd.to_datetime(df["Date"])

    # --- Core spread (10Y - 3M proxy)
    df["Term_Spread"] = df["10 year"] - df["91 days"]

    latest_spread = df["Term_Spread"].iloc[-1]

    # --- Inversion duration (months)
    inversion_months = (df["Term_Spread"] < 0).rolling(6).sum().iloc[-1]

    # --- Short rate momentum (YoY)
    df["Short_Rate_YoY"] = df["91 days"].pct_change(12) * 100
    short_rate_yoy = df["Short_Rate_YoY"].iloc[-1]

    # ============================
    # Scoring
    # ============================

    # 1. Inversion depth score
    if latest_spread < -1.0:
        depth_score = 1.0
    elif latest_spread < -0.5:
        depth_score = 0.7
    elif latest_spread < 0:
        depth_score = 0.4
    else:
        depth_score = 0.0

    # 2. Duration score
    if inversion_months >= 4:
        duration_score = 1.0
    elif inversion_months >= 2:
        duration_score = 0.6
    else:
        duration_score = 0.0

    # 3. Policy pressure score
    policy_score = 0.0
    if short_rate_yoy > 30:
        policy_score = 1.0
    elif short_rate_yoy > 15:
        policy_score = 0.5

    # ============================
    # Probability aggregation
    # ============================
    probability = (
        0.4 * depth_score +
        0.4 * duration_score +
        0.2 * policy_score
    ) * 100

    # ============================
    # Risk band
    # ============================
    if probability >= 60:
        band = "High"
    elif probability >= 40:
        band = "Elevated"
    elif probability >= 20:
        band = "Moderate"
    else:
        band = "Low"

    commentary = (
        f"Market-implied recession probability is estimated at {probability:.0f}%. "
        f"The yield curve term spread stands at {latest_spread:.2f} percentage points, "
        f"with inversion persisting for approximately {int(inversion_months)} months. "
        f"Overall recession risk is assessed as {band.lower()}."
    )

    return {
        "probability": probability,
        "band": band,
        "latest_spread": latest_spread,
        "inversion_months": inversion_months,
        "commentary": commentary
    }


def classify_policy_stance(df_rates: pd.DataFrame):
    """
    Classifies current monetary/fiscal stance using yield behavior.
    """

    df = df_rates.copy().sort_values("Date")
    df["Date"] = pd.to_datetime(df["Date"])

    # Metrics
    short_rate = df["91 days"].iloc[-1]
    short_rate_yoy = df["91 days"].pct_change(12).iloc[-1] * 100
    term_spread = df["10 year"].iloc[-1] - df["91 days"].iloc[-1]

    # Classification
    if short_rate_yoy > 20 and term_spread < 0:
        stance = "Tight"
        signal = "Restrictive financial conditions with elevated recession risk."
    elif abs(term_spread) < 0.5 and abs(short_rate_yoy) < 10:
        stance = "Neutral"
        signal = "Balanced policy stance with no strong directional pressure."
    else:
        stance = "Accommodative"
        signal = "Supportive policy stance aimed at stimulating growth."

    commentary = (
        f"Current policy stance is assessed as **{stance}**. "
        f"Short-term yields are changing at {short_rate_yoy:.1f}% YoY, "
        f"while the yield curve spread stands at {term_spread:.2f} percentage points. "
        f"{signal}"
    )

    return {
        "stance": stance,
        "short_rate_yoy": short_rate_yoy,
        "term_spread": term_spread,
        "commentary": commentary
    }

def get_latest_valid_term_spread(df: pd.DataFrame):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # Ensure numeric
    df['91 days'] = pd.to_numeric(df['91 days'], errors='coerce')
    df['10 year'] = pd.to_numeric(df['10 year'], errors='coerce')

    # Keep only rows where BOTH exist
    valid = df.dropna(subset=['91 days', '10 year'])

    if valid.empty:
        return None, None  # graceful failure

    latest = valid.iloc[-1]

    spread = latest['10 year'] - latest['91 days']

    return latest['Date'], spread

def analyze_copper(df: pd.DataFrame):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    df['YoY_Change'] = df['Copper_US_Tonne'].pct_change(12) * 100
    latest = df.iloc[-1]
    yoy = latest['YoY_Change']

    commentary = (
        f"Copper prices averaged USD {latest['Copper_US_Tonne']:,.0f} per tonne in "
        f"{latest['Date'].strftime('%B %Y')}. "
        f"Prices are {'higher' if yoy > 0 else 'lower'} by {abs(yoy):.1f}% year-on-year, "
        "with implications for export earnings, fiscal revenues, and foreign exchange inflows."
    )

    fig = px.line(
        df,
        x='Date',
        y='Copper_US_Tonne',
        title="Copper Prices (USD per tonne)",
        markers=True
    )
    fig.update_layout(height=350)

    return commentary, fig



def analyze_oil(df: pd.DataFrame):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    df['MoM_Change'] = df['Oil_US_barrel'].pct_change() * 100
    latest = df.iloc[-1]
    mom = latest['MoM_Change']

    commentary = (
        f"Global oil prices stood at USD {latest['Oil_US_barrel']:.2f} per barrel in "
        f"{latest['Date'].strftime('%B %Y')}. "
        f"Month-on-month prices moved {mom:+.1f}%, "
        "with direct pass-through risks to fuel prices, transport costs, and headline inflation."
    )

    fig = px.line(
        df,
        x='Date',
        y='Oil_US_barrel',
        title="Oil Prices (USD per barrel)",
        markers=True
    )
    fig.update_layout(height=350)

    return commentary, fig


def analyze_maize(df: pd.DataFrame):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    df['YoY_Change'] = df['Maize_K_50Kg'].pct_change(12) * 100
    latest = df.iloc[-1]
    yoy = latest['YoY_Change']

    commentary = (
        f"Maize prices averaged K {latest['Maize_K_50Kg']:.2f} per 50kg bag in "
        f"{latest['Date'].strftime('%B %Y')}. "
        f"Prices are {'up' if yoy > 0 else 'down'} {abs(yoy):.1f}% year-on-year, "
        "reflecting domestic supply conditions, seasonal factors, and food security dynamics. "
        "Elevated maize prices increase risks to food inflation and household welfare."
    )

    fig = px.line(
        df,
        x='Date',
        y='Maize_K_50Kg',
        title="Maize Prices (Kwacha per 50kg bag)",
        markers=True
    )
    fig.update_layout(height=350)

    return commentary, fig



# -------------------------------
# FX Summary
# -------------------------------
def summarize_fx(df: pd.DataFrame):
    """
    Summarize FX trends for Zambia (USD/ZMW) with month-on-month change.

    Returns:
        commentary (str): summary text
        fig (plotly.graph_objects.Figure): time series plot of FX rates
    """
    df = df.copy()
    
    # Ensure Date column is datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.sort_values('Date')
    
    if 'USDZMW' not in df.columns:
        return "USD/ZMW data not available.", None

    # Latest and previous month
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) >= 2 else latest
    
    # Month-on-month % change
    mom_change = (latest['USDZMW'] - prev['USDZMW']) / prev['USDZMW'] * 100
    
    # Direction wording
    if mom_change > 0:
        direction = "weakened"
    elif mom_change < 0:
        direction = "strengthened"
    else:
        direction = "remained stable"
    
    commentary = (
        f"As of {latest['Date'].strftime('%b %Y')}, the ZMW vs USD stands at {latest['USDZMW']:.2f}. "
        f"Compared to last month the ZMW {direction} "
        f"by {abs(mom_change):.2f}%."
    )

    # Optional: last 5 years for plotting
    five_years_ago = latest['Date'] - pd.DateOffset(years=5)
    df_plot = df[df['Date'] >= five_years_ago]

    fig = px.line(
        df_plot, x='Date', y='USDZMW', 
        title="USD/ZMW Exchange Rate — Last 5 Years",
        markers=True
    )
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=60, b=40))
    
    return commentary, fig


# -------------------------------
# Inflation Summary
# -------------------------------
def summarize_inflation(df_inf: pd.DataFrame):
    df = df_inf.copy().sort_values('Month')
    df['Month'] = pd.to_datetime(df['Month'])
    latest = df.iloc[-1]

    commentary = (
        f"As of {latest['Month'].strftime('%b %Y')}, headline inflation is "
        f"{latest['Inflation_Annual']:.2f}%. "
        f"Month-on-month change: {(latest['Inflation_Annual']-df['Inflation_Annual'].iloc[-2]):.2f}%."
    )

    fig = px.line(df, x='Month', y='Inflation_Annual', markers=True, title="Headline Inflation (%)")
    fig.update_layout(height=400, margin=dict(l=20,r=20,t=40,b=40))

    return commentary, fig

# -------------------------------
# Reserves Summary
# -------------------------------
def summarize_reserves(df_res: pd.DataFrame):
    df = df_res.copy().sort_values('Date')
    df['Date'] = pd.to_datetime(df['Date'])
    latest = df.iloc[-1]

    commentary = (
        f"As of {latest['Date'].strftime('%b %Y')}, international reserves are USD "
        f"{latest['Reserves_USD']:.2f} million, covering "
        f"{latest['Months_Import_Cover']:.2f} months of import."
    )

    fig = px.line(df, x='Date', y='Reserves_USD', markers=True, title="International Reserves (USD million)")
    fig.update_layout(height=400, margin=dict(l=20,r=20,t=40,b=40))

    return commentary, fig

# -------------------------------
# Commodities Summary (Copper, Oil, Maize)
# -------------------------------
def summarize_commodities(df_comm: pd.DataFrame):
    df = df_comm.copy().sort_values('Date')
    df['Date'] = pd.to_datetime(df['Date'])
    latest = df.iloc[-1]

    commentary = (
        f"As of {latest['Date'].strftime('%b %Y')}, commodity prices are:\n"
        f"- Copper: ${latest['Copper_US_Tonne']:.2f}/t\n"
        f"- Oil: ${latest['Oil_US_barrel']:.2f}/barrel\n"
        f"- Maize (Zambia, 50Kg): K{latest['Maize_K_50Kg']:.2f}"
    )

    # Melt for plotly
    df_plot = df.melt(id_vars='Date', value_vars=['Copper_US_Tonne','Oil_US_barrel','Maize_K_50Kg'],
                      var_name='Commodity', value_name='Price')
    fig = px.line(df_plot, x='Date', y='Price', color='Commodity', markers=True, title="Commodity Prices")
    fig.update_layout(height=400, margin=dict(l=20,r=20,t=40,b=40))

    return commentary, fig