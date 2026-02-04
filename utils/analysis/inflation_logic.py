from utils.metrics import mom_change, yoy_change, trend_label

def inflation_signal(df):
    yoy = df["Total_Annual_Inflation_Rate"].dropna()
    mom = df["Total_Monthly_Inflation_Rate"].dropna()

    yoy_delta = yoy_change(yoy)
    mom_delta = mom_change(mom)

    pressure = trend_label(yoy.iloc[-1], thresholds=(6, 10))

    return {
        "level": yoy.iloc[-1],
        "mom": mom_delta,
        "yoy": yoy_delta,
        "pressure": pressure
    }
