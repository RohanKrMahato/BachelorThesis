import pandas as pd
import yfinance as yf
import time

# 1. Load your finalized ticker list
input_file = './get_ticker/company_tickers_final.csv'
output_file = './get_ticker/company_tickers_with_sectors.csv'

df = pd.read_csv(input_file)
tickers = df['Ticker'].tolist()

results = []

print(f"Fetching metadata for {len(tickers)} tickers...")

for index, row in df.iterrows():
    ticker_symbol = row['Ticker']
    company_name = row['Company Name']
    
    print(f"[{index+1}/{len(tickers)}] Processing: {ticker_symbol}")
    
    try:
        ticker_obj = yf.Ticker(ticker_symbol)
        info = ticker_obj.info
        
        # Extract sector and industry, default to 'N/A' if not found
        sector = info.get('sector', 'N/A')
        industry = info.get('industry', 'N/A')
        
        results.append({
            'Company Name': company_name,
            'Ticker': ticker_symbol,
            'Sector': sector,
            'Industry': industry
        })
        
    except Exception as e:
        print(f"Error fetching {ticker_symbol}: {e}")
        results.append({
            'Company Name': company_name,
            'Ticker': ticker_symbol,
            'Sector': 'Error',
            'Industry': 'Error'
        })
    
    # Small delay to respect rate limits
    time.sleep(0.2)

# 2. Create the new DataFrame and save
sector_df = pd.DataFrame(results)
sector_df.to_csv(output_file, index=False)

print(f"\nSector mapping complete! Saved to {output_file}")