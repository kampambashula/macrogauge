def macro_headline(
    fx_gauge,
    inflation,
    liquidity,
    fiscal,
    external,
    commodity,
    policy_value=None
):
    """
    Generate an IMF-style macro summary paragraph with separate copper and oil commentary.

    Parameters
    ----------
    fx_gauge : dict with keys ['status', 'mom_change']
    inflation : dict with keys ['status', 'value', 'mom_change']
    liquidity : dict with keys ['status', 'value', 'mom_change']
    fiscal : dict with keys ['status', 'value', 'mom_change']
    external : dict with keys ['status', 'value', 'mom_change']
    commodity : dict with keys ['status_copper', 'value_copper', 'mom_copper', 
                               'status_oil', 'value_oil', 'mom_oil']
    policy_value : float, optional

    Returns
    -------
    headline : str, single paragraph
    details : dict of dict, keyed by metric, with commentary and MoM
    """

    details = {}

    # --- FX
    if fx_gauge['status'] == "red":
        fx_text = f"The Kwacha experienced **significant depreciation** ({fx_gauge['mom_change']:+.2f}% MoM), reflecting elevated FX market pressures"
    elif fx_gauge['status'] == "amber":
        fx_text = f"The Kwacha traded with **moderate depreciation** ({fx_gauge['mom_change']:+.2f}% MoM) amid seasonal FX demand"
    else:
        fx_text = f"FX conditions remained broadly **stable** ({fx_gauge['mom_change']:+.2f}% MoM)"
    details['FX'] = {"commentary": fx_text, "mom": fx_gauge.get('mom_change', None)}

    # --- Inflation
    if inflation['status'] == "red":
        infl_text = f"Inflation remains **elevated** at {inflation['value']:.1f}%, above the central bank target, with {inflation['mom_change']:+.2f}% MoM pressure"
    elif inflation['status'] == "amber":
        infl_text = f"Inflation slightly **exceeds target** at {inflation['value']:.1f}%, with persistent MoM price pressures ({inflation['mom_change']:+.2f}%)"
    else:
        infl_text = f"Inflation is **within target** at {inflation['value']:.1f}%, with MoM trends easing ({inflation['mom_change']:+.2f}%)"
    details['Inflation'] = {"commentary": infl_text, "mom": inflation['mom_change']}

    # --- Liquidity
    if liquidity['status'] == "red":
        liq_text = f"Banking system liquidity remains **strained**, with total reserves changing {liquidity['mom_change']:+.2f}% MoM"
    elif liquidity['status'] == "amber":
        liq_text = f"Liquidity conditions are **somewhat tight**, total reserves moved {liquidity['mom_change']:+.2f}% MoM"
    else:
        liq_text = f"Liquidity is broadly **stable**, total reserves changed {liquidity['mom_change']:+.2f}% MoM"
    details['Liquidity'] = {"commentary": liq_text, "mom": liquidity['mom_change']}

    # --- Fiscal
    if fiscal['status'] == "red":
        fiscal_text = f"Fiscal operations show **high pressure**, with T-bills sales increasing {fiscal['mom_change']:+.2f}% MoM"
    elif fiscal['status'] == "amber":
        fiscal_text = f"Fiscal position is **moderately tight**, T-bills sales moved {fiscal['mom_change']:+.2f}% MoM"
    else:
        fiscal_text = f"Fiscal flows remain **manageable**, T-bills sales changed {fiscal['mom_change']:+.2f}% MoM"
    details['Fiscal'] = {"commentary": fiscal_text, "mom": fiscal['mom_change']}

    # --- External
    if external['status'] == "red":
        ext_text = f"External sector under **significant pressure**, gross reserves {external['value']:.1f} B ZMW ({external['mom_change']:+.2f}% MoM)"
    elif external['status'] == "amber":
        ext_text = f"External sector shows **moderate stress**, gross reserves {external['value']:.1f} B ZMW ({external['mom_change']:+.2f}% MoM)"
    else:
        ext_text = f"External sector is **stable**, gross reserves {external['value']:.1f} B ZMW ({external['mom_change']:+.2f}% MoM)"
    details['External'] = {"commentary": ext_text, "mom": external['mom_change']}

    # --- Commodity: Copper
    if commodity['status_copper'] == "red":
        comm_text_copper = f"Copper prices show **significant volatility**, changing {commodity['mom_copper']:+.2f}% MoM"
    elif commodity['status_copper'] == "amber":
        comm_text_copper = f"Copper prices **moderately volatile**, MoM change {commodity['mom_copper']:+.2f}%"
    else:
        comm_text_copper = f"Copper prices remain **stable**, MoM change {commodity['mom_copper']:+.2f}%"
    details['Copper'] = {"commentary": comm_text_copper, "mom": commodity['mom_copper']}

    # --- Commodity: Oil
    if commodity['status_oil'] == "red":
        comm_text_oil = f"Oil prices show **significant volatility**, changing {commodity['mom_oil']:+.2f}% MoM"
    elif commodity['status_oil'] == "amber":
        comm_text_oil = f"Oil prices **moderately volatile**, MoM change {commodity['mom_oil']:+.2f}%"
    else:
        comm_text_oil = f"Oil prices remain **stable**, MoM change {commodity['mom_oil']:+.2f}%"
    details['Oil'] = {"commentary": comm_text_oil, "mom": commodity['mom_oil']}

    # --- Policy / Lending
    if policy_value is not None:
        policy_text = f"Monetary policy remains accommodative with BoZ policy rate at {policy_value:.2f}%"
        details['Policy'] = {"commentary": policy_text}

    # --- Combine into one IMF-style paragraph
    headline = (
        f"{fx_text}. {infl_text}. {liq_text}. {fiscal_text}. {ext_text}. {comm_text_copper}. {comm_text_oil}."
    )
    if policy_value is not None:
        headline += f" {policy_text}."

    return headline, details
