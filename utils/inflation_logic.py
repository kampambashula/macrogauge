def inflation_state(df, target=7, band=(6, 8)):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    yoy = latest["YoY"]
    mom = latest["MoM"]

    if yoy > 12 or (mom > 0.4 and yoy > band[1]):
        status = "red"
        note = "Inflation is materially above target and re-accelerating"
        confidence = 85
    elif band[1] < yoy <= 12:
        status = "amber"
        note = "Inflation remains above target with limited disinflation progress"
        confidence = 70
    elif band[0] <= yoy <= band[1]:
        status = "green"
        note = "Inflation is within the central bank target range"
        confidence = 90
    else:
        status = "green"
        note = "Inflation is below target with easing price pressures"
        confidence = 75

    return {
        "status": status,
        "commentary": note,
        "confidence": confidence,
        "metrics": {
            "YoY": round(yoy, 2),
            "MoM": round(mom, 2),
        },
    }
