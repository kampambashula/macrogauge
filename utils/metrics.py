def mom_change(series):
    return series.iloc[-1] - series.iloc[-2]

def yoy_change(series):
    return series.iloc[-1] - series.iloc[-13]

def trend_label(value, thresholds):
    low, high = thresholds
    if value < low:
        return "low"
    elif value < high:
        return "moderate"
    return "high"
