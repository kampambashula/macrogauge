from utils.analysis.inflation_logic import inflation_signal
from utils.analysis.fx_logic import fx_signal

def generate_what_changed(snapshot_month, DATA):
    infl = inflation_signal(DATA["inflation"])
    fx = fx_signal(DATA["forex"])

    bullets = []

    if fx["mom"] > 0:
        bullets.append("Kwacha weakened on month-on-month basis")
    else:
        bullets.append("Kwacha stabilized compared to previous month")

    if infl["mom"] > 0:
        bullets.append("Monthly inflation accelerated")
    else:
        bullets.append("Monthly inflation eased")

    return "\n".join([f"- {b}" for b in bullets])
