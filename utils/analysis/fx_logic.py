from utils.metrics import mom_change

def fx_signal(df):
    rate = df["Weighted_Rate"].dropna()
    delta = mom_change(rate)

    if delta > 0.5:
        condition = "pressure"
    elif delta < -0.3:
        condition = "relief"
    else:
        condition = "stable"

    return {
        "level": rate.iloc[-1],
        "mom": delta,
        "condition": condition
    }
