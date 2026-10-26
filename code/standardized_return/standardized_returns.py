import pandas as pd
import numpy as np
import os

# Configuration
INPUT_PATH = './get_price/nifty500_raw_matrix.csv'
OUTPUT_DIR = './standardized_return/'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_returns():
    print("Loading raw price matrix...")
    df = pd.read_csv(INPUT_PATH, index_col='Date', parse_dates=True)

    # 1. Professional Imputation (Common for all frequencies)
    # Forward fill (LOCF) then backfill for initial gaps
    df_imputed = df.ffill().bfill()

    # --- DAILY RETURNS (with Calendar-Day scaling) ---
    print("Processing Daily Returns...")
    date_series = pd.to_datetime(df_imputed.index).to_series()
    day_diffs = date_series.diff().dt.days
    
    daily_log_ret = np.log(df_imputed).diff()
    # Apply your professional sqrt(n) scaling
    daily_scaled = daily_log_ret.div(np.sqrt(day_diffs), axis=0).dropna()
    # Z-score standardization
    daily_final = (daily_scaled - daily_scaled.mean()) / daily_scaled.std()
    daily_final.to_csv(os.path.join(OUTPUT_DIR, 'standardized_returns_daily.csv'))

    # --- WEEKLY RETURNS (Friday-to-Friday) ---
    print("Processing Weekly Returns...")
    # Resample to last trading day of the week (Friday anchor)
    df_weekly = df_imputed.resample('W-FRI').last()
    weekly_log_ret = np.log(df_weekly).diff().dropna()
    # Professional Z-score (Standard for PCA at this horizon)
    weekly_final = (weekly_log_ret - weekly_log_ret.mean()) / weekly_log_ret.std()
    weekly_final.to_csv(os.path.join(OUTPUT_DIR, 'standardized_returns_weekly.csv'))

    # --- MONTHLY RETURNS (Month-End) ---
    print("Processing Monthly Returns...")
    # Resample to Month End
    df_monthly = df_imputed.resample('ME').last()
    monthly_log_ret = np.log(df_monthly).diff().dropna()
    # Professional Z-score
    monthly_final = (monthly_log_ret - monthly_log_ret.mean()) / monthly_log_ret.std()
    monthly_final.to_csv(os.path.join(OUTPUT_DIR, 'standardized_returns_monthly.csv'))

    print(f"\nSuccess! Files generated in {OUTPUT_DIR}:")
    print(f" - Daily:   {daily_final.shape}")
    print(f" - Weekly:  {weekly_final.shape}")
    print(f" - Monthly: {monthly_final.shape}")

if __name__ == "__main__":
    generate_returns()