# utils/macro_brief_exporter_text.py
import os
import pandas as pd
from utils.data_loader import load_all_data
from utils.economic_analysis import (
    summarize_fx,
    summarize_inflation,
    analyze_fiscal_stress,
    analyze_bills,
    analyze_bonds,
    analyze_yield_curve,
    summarize_commodities
)

def generate_macro_brief_text(DATA, year=None, month=None):
    """
    Generate macro brief text for different platforms.
    Returns a dictionary with keys: 'blog', 'whatsapp', 'linkedin'
    """
    # Determine latest snapshot if not provided
    if year is None or month is None:
        latest_dates = [
            pd.to_datetime(DATA['forex']['Date'], errors='coerce').max(),
            pd.to_datetime(DATA['inflation']['Month'], errors='coerce').max(),
            pd.to_datetime(DATA['bills']['Date'], errors='coerce').max(),
            pd.to_datetime(DATA['bill_rates']['Date'], errors='coerce').max(),
            pd.to_datetime(DATA['bonds']['Date'], errors='coerce').max(),
            pd.to_datetime(DATA['commodity']['Date'], errors='coerce').max()
        ]
        latest_dates = [d for d in latest_dates if pd.notna(d)]
        latest_date = max(latest_dates)
        year = latest_date.year
        month = latest_date.month
    else:
        latest_date = pd.to_datetime(f"{year}-{month}-01")

    snapshot_str = latest_date.strftime('%B %Y')
    snapshot_file_str = latest_date.strftime('%b_%Y')  # for filenames

    # --- FX
    fx_comment, _ = summarize_fx(DATA['forex'])
    
    # --- Inflation
    inf_comment, _ = summarize_inflation(DATA['inflation'])

    # --- Fiscal
    fiscal_comment, _, _ = analyze_fiscal_stress(
        bills_df=DATA['bills'],
        bill_rates_df=DATA['bill_rates']
    )

    # --- T-Bills & Bonds
    tbill_comment, _, _ = analyze_bills(DATA['bills'])
    bond_comment, _, _ = analyze_bonds(DATA['bonds'])

    # --- Commodities
    comm_comment, _ = summarize_commodities(DATA['commodity'])

    # --- Yield Curve
    yc_comment, _, _ = analyze_yield_curve(DATA['bill_rates'])

    # -------------------------------
    # Compose base text
    # -------------------------------
    base_text = (
        f"MacroGauge — Zambia Macro Brief ({snapshot_str})\n\n"
        f"💱 FX Overview:\n{fx_comment}\n\n"
        f"📊 Inflation:\n{inf_comment}\n\n"
        f"🏛️ Fiscal Overview:\n{fiscal_comment}\n\n"
        f"💵 T-Bills & Bonds:\n{tbill_comment}\n{bond_comment}\n\n"
        f"📈 Commodities:\n{comm_comment}\n\n"
        f"📉 Yield Curve:\n{yc_comment}\n"
    )

    # -------------------------------
    # Format for different platforms
    # -------------------------------
    brief_blog = base_text  # blog: full text with headings
    brief_whatsapp = base_text.replace("\n\n", "\n")  # short, mobile-friendly
    brief_linkedin = base_text.replace("\n\n", " | ").replace("\n", " ")  # condensed for social media

    return {
        "blog": (brief_blog, snapshot_file_str),
        "whatsapp": (brief_whatsapp, snapshot_file_str),
        "linkedin": (brief_linkedin, snapshot_file_str)
    }


# -------------------------------
# Standalone terminal run
# -------------------------------
if __name__ == "__main__":
    # Load data
    DATA = load_all_data()

    # Generate briefs
    briefs = generate_macro_brief_text(DATA)

    # Ensure output folder exists
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Write files dynamically with month-year in filenames
    for key, (text, snapshot_file_str) in briefs.items():
        filename = f"macro_brief_{key}_{snapshot_file_str}.txt"
        path = os.path.join(output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    print(f"✅ Macro briefs exported to {output_dir}:")
    for key, (_, snapshot_file_str) in briefs.items():
        print(f" - macro_brief_{key}_{snapshot_file_str}.txt")
