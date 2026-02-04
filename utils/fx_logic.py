def fx_state(df):
    latest = df.iloc[-1]

    z = latest["Z_Score"]
    mom = latest["FX_MoM"]

    if z > 2 or (z > 1.5 and mom > 2):
        status = "red"
        note = "Kwacha under stress with sharp depreciation and elevated volatility"
        confidence = 85

    elif z > 1 or mom > 1:
        status = "amber"
        note = "FX pressures elevated amid seasonal demand and volatility"
        confidence = 70

    else:
        status = "green"
        note = "FX trading within normal volatility bands"
        confidence = 90

    return {
        "status": status,
        "commentary": note,
        "confidence": confidence,
        "metrics": {
            "rate": round(latest["USDZMW"], 2),
            "MoM": round(mom, 2),
            "z_score": round(z, 2),
        },
    }
