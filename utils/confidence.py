import numpy as np

def compute_confidence(mom_change, yoy_change=None, volatility=None):
    """
    Returns confidence score between 0 and 100
    """

    score = 50  # neutral baseline

    # --- Strength of move
    score += min(abs(mom_change) * 10, 20)

    # --- Confirmation from YoY trend
    if yoy_change is not None:
        if np.sign(mom_change) == np.sign(yoy_change):
            score += 10
        else:
            score -= 10

    # --- Volatility penalty
    if volatility is not None:
        if volatility > 2:
            score -= 10

    return int(max(10, min(score, 95)))
