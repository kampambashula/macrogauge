def what_changed(fx_mom, infl_mom, liq_mom):
    notes = []

    if fx_mom > 0:
        notes.append("Kwacha weakened on monthly basis")
    if infl_mom > 0:
        notes.append("Inflation momentum picked up")
    if liq_mom > 0:
        notes.append("Liquidity conditions loosened")

    return notes
