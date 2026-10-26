import pandas as pd
import yfinance as yf

# 1. Load the ticker list
df_tickers = pd.read_csv('./get_ticker/company_tickers_final.csv')
tickers = df_tickers['Ticker'].tolist()

# 2. Define the study period
start_date = "2005-01-01"
end_date = "2020-12-31"

def create_market_dataset(ticker_list, start, end):
    print(f"Downloading data for {len(ticker_list)} tickers...")
    
    # Download data with group_by='ticker' to make iteration easier
    raw_data = yf.download(ticker_list, start=start, end=end, group_by='ticker', auto_adjust=False)
    
    valid_series = {}
    total_days = None

    for ticker in ticker_list:
        try:
            # Extract Adjusted Close for the specific ticker 
            # Handle potential missing tickers in the download object
            if ticker in raw_data.columns.levels[0]:
                series = raw_data[ticker]['Adj Close']
                
                # Calculate missing data ratio
                missing_ratio = series.isnull().mean()
                
                # Requirement: Discard if missing data > 10% 
                if missing_ratio <= 0.10:
                    valid_series[ticker] = series
                    if total_days is None:
                        total_days = len(series)
        except KeyError:
            continue

    # Create the T x N matrix [cite: 43]
    if not valid_series:
        print("No stocks met the criteria.")
        return pd.DataFrame()

    filtered_data = pd.DataFrame(valid_series)
    
    # Drop rows where ALL stocks are NA (market holidays) 
    filtered_data = filtered_data.dropna(how='all')

    print(f"Initial stocks: {len(ticker_list)}")
    print(f"Stocks retained (N): {len(filtered_data.columns)}")
    print(f"Trading days (T): {len(filtered_data)}")
    
    return filtered_data

# Create the T x N matrix
market_matrix = create_market_dataset(tickers, start_date, end_date)

if not market_matrix.empty:
    print("\nSample of the Matrix:")
    print(market_matrix.head())
    # Save the result
    market_matrix.to_csv('./get_price/nifty500_raw_matrix.csv')