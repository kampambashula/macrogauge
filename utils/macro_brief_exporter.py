# utils/macro_brief_exporter.py
import pandas as pd
from io import BytesIO
from fpdf import FPDF
from utils.economic_analysis import (
    summarize_fx,
    summarize_inflation,
    analyze_fiscal_stress,
    analyze_bills,
    analyze_bonds,
    analyze_bill_rates,
    analyze_yield_curve,
    summarize_commodities
)

# -------------------------------
# Helper to clean text for PDF
# -------------------------------
def clean_text(text: str) -> str:
    replacements = {
        "—": "-",  # em-dash → dash
        "–": "-",  # en-dash → dash
        "“": '"',
        "”": '"',
        "’": "'"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

# -------------------------------
# PDF Generator
# -------------------------------
def generate_brief_file(DATA, year, month):
    """
    Generate a branded PDF macro brief summarizing key metrics
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- Unicode-safe font
    # Place a TTF font like "ARIALUNI.TTF" in your project folder
    # For simplicity here, fallback to default Arial but clean text
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "MacroGauge — Zambia Macro Brief", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Snapshot: {pd.to_datetime(f'{year}-{month}-01').strftime('%B %Y')}", ln=True, align="C")
    pdf.ln(5)
    
    # --- FX
    fx_comment, _ = summarize_fx(DATA['forex'])
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "FX Overview", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 6, clean_text(fx_comment))
    pdf.ln(3)
    
    # --- Inflation
    inf_comment, _ = summarize_inflation(DATA['inflation'])
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Inflation", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 6, clean_text(inf_comment))
    pdf.ln(3)
    
    # --- Fiscal
    fiscal_comment, _, _ = analyze_fiscal_stress(
        bills_df=DATA['bills'],
        bill_rates_df=DATA['bill_rates']
    )
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Fiscal Overview", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 6, clean_text(fiscal_comment))
    pdf.ln(3)
    
    # --- Bills & Bonds
    tbill_comment, _, _ = analyze_bills(DATA['bills'])
    bond_comment, _, _ = analyze_bonds(DATA['bonds'])
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "T-Bills & Bonds", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 6, clean_text(tbill_comment))
    pdf.multi_cell(0, 6, clean_text(bond_comment))
    pdf.ln(3)
    
    # --- Commodities
    comm_comment, _ = summarize_commodities(DATA['commodity'])
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Commodities", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 6, clean_text(comm_comment))
    pdf.ln(3)
    
    # --- Yield Curve
    yc_comment, _, _ = analyze_yield_curve(DATA['bill_rates'])
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Yield Curve", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 6, clean_text(yc_comment))
    
    # --- Return PDF as bytes
    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)  # type: ignore
    pdf_bytes.seek(0)
    return pdf_bytes.read()
