import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from utils.data_loader import load_all_data

# --- Helper to generate custom lags
def create_lags(df, col, lags=[1,3,6]):
    df_lags = df[[col]].copy()
    for lag in lags:
        df_lags[f'{col}_lag{lag}'] = df_lags[col].shift(lag)
    df_lags = df_lags.dropna()
    return df_lags

# --- Train simple ML models and predict next month
def forecast_next_month(df, col):
    df_lags = create_lags(df, col)
    X = df_lags.drop(columns=[col])
    y = df_lags[col]

    # Linear Regression
    lr = LinearRegression()
    lr.fit(X, y)
    lr_pred = lr.predict([X.iloc[-1]])[0] # type: ignore

    # Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    rf_pred = rf.predict([X.iloc[-1]])[0]

    # XGBoost
    xgb = XGBRegressor(n_estimators=100, random_state=42)
    xgb.fit(X, y)
    xgb_pred = xgb.predict([X.iloc[-1]])[0]

    # Average prediction as base case
    base = (lr_pred + rf_pred + xgb_pred) / 3
    bull = base * 0.95  # optimistic scenario
    bear = base * 1.05  # pessimistic scenario

    df_out = pd.DataFrame({
        'Scenario': ['Base', 'Bull', 'Bear'],
        'Forecast': [base, bull, bear]
    })
    return df_out

# --- Master function to build all scenario tables
def build_base_bull_bear():
    data = load_all_data()
    scenario_tables = {}

    # Inflation forecast
    df_infl = data['inflation'].sort_values('Month')
    df_infl = df_infl.rename(columns={'Inflation_Annual':'value'})
    scenario_tables['Inflation'] = forecast_next_month(df_infl, 'value')

    # FX forecast (USD/ZMW)
    df_fx = data['boz_forex'].sort_values('Date')
    if 'USD/ZMW' in df_fx.columns:
        df_fx = df_fx.rename(columns={'USD/ZMW':'value'})
        scenario_tables['USD/ZMW'] = forecast_next_month(df_fx, 'value')

    # Liquidity forecast (Total Reserves)
    df_liq = data['liquidity'].sort_values('Date')
    df_liq = df_liq.rename(columns={'Total_Reserves':'value'})
    scenario_tables['Total Reserves'] = forecast_next_month(df_liq, 'value')

    # Policy / Lending forecast (Policy Rate)
    df_policy = data['lending_rates'].sort_values('Date')
    df_policy = df_policy.rename(columns={'BoZ_Policy_Rate':'value'})
    scenario_tables['Policy Rate'] = forecast_next_month(df_policy, 'value')

    # Fiscal / Debt forecast (Total Sales)
    df_fiscal = data['bills'].sort_values('Date')
    df_fiscal = df_fiscal.rename(columns={'Total_Sales':'value'})
    scenario_tables['Fiscal Sales'] = forecast_next_month(df_fiscal, 'value')

    # External Sector forecast (Gross International Reserves)
    df_ext = data['boz_forex'].sort_values('Date')
    df_ext = df_ext.rename(columns={'Gross_International_Reserves':'value'})
    scenario_tables['Gross Reserves'] = forecast_next_month(df_ext, 'value')

    # Commodity forecast (Copper_US_Tonne)
    df_comm = data['commodity'].sort_values('Date')
    df_comm = df_comm.rename(columns={'Copper_US_Tonne':'value'})
    scenario_tables['Copper Price'] = forecast_next_month(df_comm, 'value')

    return scenario_tables