import pandas as pd

def compute_fx_metrics(df, window=12):
    """
    Expects df with columns:
    - Date
    - USDZMW (or Close)
    """

    df = df.copy()
    df = df.sort_values("Date")

    price_col = "USDZMW" if "USDZMW" in df.columns else "Close"

    df["FX_MoM"] = df[price_col].pct_change() * 100
    df["FX_Mean"] = df[price_col].rolling(window).mean()
    df["FX_Std"] = df[price_col].rolling(window).std()

    df["Z_Score"] = (df[price_col] - df["FX_Mean"]) / df["FX_Std"]

    return df
