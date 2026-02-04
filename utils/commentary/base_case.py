from utils.analysis.inflation_logic import inflation_signal
from utils.analysis.fx_logic import fx_signal

def generate_base_case(snapshot_month, DATA):
    infl = inflation_signal(DATA["inflation"])
    fx = fx_signal(DATA["forex"])

    statements = []

    # FX narrative
    if fx["condition"] == "pressure":
        statements.append("gradual FX pressure")
    elif fx["condition"] == "relief":
        statements.append("improving FX conditions")
    else:
        statements.append("stable FX conditions")

    # Inflation narrative
    if infl["pressure"] == "high":
        statements.append("sticky inflation")
    elif infl["pressure"] == "moderate":
        statements.append("easing inflation")
    else:
        statements.append("contained inflation")

    return f"**{', '.join(statements).capitalize()}.**"
