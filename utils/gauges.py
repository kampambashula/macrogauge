from utils.plotly_gauges import traffic_light_gauge

def inflation_gauge(
    yoy,
    mom,
    status,
    confidence,
    target=7,
    lower=6,
    upper=8,
    max_val=20
):
    steps = [
        {"range": [0, lower], "color": "#ecf0f1"},        # Below target
        {"range": [lower, upper], "color": "#2ecc71"},   # Target band
        {"range": [upper, 12], "color": "#f39c12"},      # Above target
        {"range": [12, max_val], "color": "#e74c3c"},    # Elevated risk
    ]

    return traffic_light_gauge(
        title="Inflation (YoY)",
        value=yoy,
        min_val=0,
        max_val=max_val,
        status=status,
        mom_change=mom,
        confidence=confidence,
        steps=steps
    )

def fx_volatility_gauge(
    rate,
    mean,
    std,
    status,
    mom,
    confidence
):
    min_val = mean - 3 * std
    max_val = mean + 3 * std

    steps = [
        {"range": [mean - std, mean + std], "color": "#ecf0f1"},   # Normal
        {"range": [mean + std, mean + 2 * std], "color": "#fef5e7"},
        {"range": [mean + 2 * std, max_val], "color": "#fdecea"},
    ]

    return traffic_light_gauge(
        title="FX (USD/ZMW)",
        value=rate,
        min_val=min_val,
        max_val=max_val,
        status=status,
        mom_change=mom,
        confidence=confidence,
        steps=steps
    )

def fx_stress_gauge(value, status, confidence):
    return traffic_light_gauge(
        title="FX Stress Index",
        value=value,
        min_val=-1,
        max_val=3,
        status=status,
        confidence=confidence,
    )