import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

# Helper to parse dates safely
def parse_dates(df, date_col='Date'):
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce', dayfirst=True)
    return df

# Load each dataset individually
def load_bill_rates():
    path = os.path.join(DATA_DIR, 'bill_rates.csv')
    df = pd.read_csv(path)
    df = parse_dates(df, 'Date')
    return df

def load_bills():
    path = os.path.join(DATA_DIR, 'bills.csv')
    df = pd.read_csv(path)
    df = parse_dates(df, 'Date')
    return df

def load_bonds():
    path = os.path.join(DATA_DIR, 'bonds.csv')
    df = pd.read_csv(path)
    df = parse_dates(df, 'Date')
    return df

def load_boz_forex():
    path = os.path.join(DATA_DIR, 'boz_forex.csv')
    df = pd.read_csv(path)
    df = parse_dates(df, 'Date')
    return df

def load_forex():
    path = os.path.join(DATA_DIR, 'forex_rates.csv')
    df = pd.read_csv(path)
    df = parse_dates(df, 'Date')
    return df

def load_commodity():
    path = os.path.join(DATA_DIR, 'commodity.csv')
    df = pd.read_csv(path)
    df = parse_dates(df, 'Date')
    return df

def load_inflation():
    path = os.path.join(DATA_DIR, 'inflation.csv')
    df = pd.read_csv(path)

    # Parse dates
    df['Month'] = pd.to_datetime(df['Month'], dayfirst=True)

    # Create YoY column from Total_Annual_Inflation_Rate if it exists
    if 'Inflation_Annual' in df.columns:
        df['YoY'] = df['Inflation_Annual']
    else:
        # fallback: calculate from index if needed
        df['YoY'] = df['Total_Consumer_Price_Index'].pct_change(periods=12) * 100

    # Optional: create MoM column
    df['MoM'] = df['Total_Consumer_Price_Index'].pct_change() * 100

    return df


def load_lending_rates():
    path = os.path.join(DATA_DIR, 'lending_rates.csv')
    df = pd.read_csv(path)
    df = parse_dates(df, 'Date')
    return df

def load_liabilities():
    path = os.path.join(DATA_DIR, 'liabilities.csv')
    df = pd.read_csv(path)
    df = parse_dates(df, 'Date')
    return df

def load_liquidity():
    path = os.path.join(DATA_DIR, 'liquidity.csv')
    df = pd.read_csv(path)
    df = parse_dates(df, 'Date')
    return df

def load_money_supply():
    path = os.path.join(DATA_DIR, 'money_supply.csv')
    df = pd.read_csv(path)
    df = parse_dates(df, 'Date')
    return df

# Master loader to get all datasets in a dictionary
def load_all_data():
    data = {
        'bill_rates': load_bill_rates(),
        'bills': load_bills(),
        'bonds': load_bonds(),
        'boz_forex': load_boz_forex(),
        'commodity': load_commodity(),
        'inflation': load_inflation(),
        'lending_rates': load_lending_rates(),
        'liabilities': load_liabilities(),
        'liquidity': load_liquidity(),
        'money_supply': load_money_supply(),
        'forex': load_forex()
    }
    return data
