import pandas as pd
import numpy as np

def compute_fx_stress_components(fx_df, reserves_df=None, window=12):
    """
    Compute FX stress components.
    
    fx_df expects:
    - Date
    - USDZMW
    
    reserves_df optional:
    - Date
    - Gross_International_Reserves
    """
    df = fx_df.copy().sort_values("Date").reset_index(drop=True)
    price_col = "USDZMW"

    # --- MoM % change
    df["FX_MoM"] = df[price_col].pct_change() * 100

    # --- Rolling mean & std for Z-score
    df["FX_Mean"] = df[price_col].rolling(window, min_periods=1).mean()
    df["FX_Std"] = df[price_col].rolling(window, min_periods=1).std().replace(0, 1e-6)

    df["Z_Price"] = (df[price_col] - df["FX_Mean"]) / df["FX_Std"]
    df["Z_Vol"] = df["FX_Std"] / df["FX_Std"].rolling(window, min_periods=1).mean().replace(0, 1e-6)
    df["Z_MoM"] = df["FX_MoM"] / df["FX_MoM"].rolling(window, min_periods=1).std().replace(0, 1e-6)

    # --- Reserves stress (inverse relation: lower reserves = higher stress)
    if reserves_df is not None:
        r = reserves_df.copy().sort_values("Date").reset_index(drop=True)
        r["Res_Mean"] = r["Gross_International_Reserves"].rolling(window, min_periods=1).mean()
        r["Res_Std"] = r["Gross_International_Reserves"].rolling(window, min_periods=1).std().replace(0, 1e-6)
        r["Z_Reserves"] = (r["Res_Mean"] - r["Gross_International_Reserves"]) / r["Res_Std"]
        df = df.merge(r[["Date", "Z_Reserves"]], on="Date", how="left")
    else:
        df["Z_Reserves"] = 0.0

    return df

def compute_fx_stress_index(df):
    """
    Compute weighted FX Stress Index.
    """
    weights = {
        "Z_Price": 0.35,
        "Z_Vol": 0.25,
        "Z_MoM": 0.25,
        "Z_Reserves": 0.15,
    }
    df = df.copy()
    df["FX_Stress_Index"] = (
        df["Z_Price"] * weights["Z_Price"] +
        df["Z_Vol"] * weights["Z_Vol"] +
        df["Z_MoM"] * weights["Z_MoM"] +
        df["Z_Reserves"] * weights["Z_Reserves"]
    )
    # Normalize index to ~[-3,3] for plotting if needed
    df["FX_Stress_Index"] = df["FX_Stress_Index"].clip(-3, 3)
    return df

def fx_stress_state(df):
    """
    Return dictionary for plotting gauge:
    - status: green/amber/red
    - label: text for gauge
    - commentary: IMF-style statement
    - confidence: approximate confidence score %
    - value: latest FX stress index
    - mom_change: last month change for delta arrow
    """
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest

    value = latest["FX_Stress_Index"]
    mom_change = value - prev["FX_Stress_Index"]

    if value >= 2:
        status = "red"
        label = "Severe FX Stress"
        commentary = "Severe FX stress with disorderly market dynamics and elevated volatility."
        confidence = 85
    elif value >= 1:
        status = "amber"
        label = "Elevated FX Pressure"
        commentary = "FX pressures elevated with rising volatility and moderate currency depreciation."
        confidence = 70
    else:
        status = "green"
        label = "FX Stable"
        commentary = "FX conditions stable within historical norms, manageable volatility."
        confidence = 90

    return {
        "status": status,
        "label": label,
        "commentary": commentary,
        "confidence": confidence,
        "value": value,
        "mom_change": mom_change
    }
