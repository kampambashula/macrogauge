def generate_closing_summary(snapshot_month, gauges):
    risks = []

    for key, (status, _) in gauges.items():
        if status == "red":
            risks.append(key.replace("_", " "))

    if not risks:
        return f"### 🔎 MacroGauge Summary — {snapshot_month}\nRisks remain broadly contained."

    risk_list = ", ".join(risks)
    return f"""
### 🔎 MacroGauge Summary — {snapshot_month}
- Elevated risks observed in **{risk_list}**
- Policy coordination remains critical
"""
