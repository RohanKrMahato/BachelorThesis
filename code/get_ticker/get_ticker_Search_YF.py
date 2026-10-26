import pandas as pd
import yfinance as yf
import time
import re

INPUT_FILE = "nifty_500_end_2004.csv"
OUTPUT_FILE = "company_tickers_Search_YF.csv"


def clean_name(name):
    name = re.sub(r"\b(Ltd|Limited|Co|Corporation|Corp)\b\.?", "", name)
    name = re.sub(r"\(.*?\)", "", name)
    name = re.sub(r"-.*", "", name)
    return name.strip()

def get_ticker(company):
    try:
        search = yf.Search(clean_name(company))
        quotes = search.quotes

        if not quotes:
            return None

        for q in quotes:
            symbol = q.get("symbol", "")

            # Prefer NSE tickers
            if symbol.endswith(".NS"):
                return symbol

        # fallback
        return quotes[0].get("symbol")

    except Exception:
        return None


def verify_ticker(symbol):
    try:
        t = yf.Ticker(symbol)
        info = t.history(period="1d")
        return not info.empty
    except:
        return False


def main():

    df = pd.read_csv(INPUT_FILE)
    companies = df["Company Name"].dropna().tolist()

    results = []

    for company in companies:

        print("Searching:", company)

        ticker = get_ticker(company)

        if ticker and verify_ticker(ticker):
            print("  Found:", ticker)
            results.append({
                "Company Name": company,
                "Ticker": ticker
            })
        else:
            print("  No ticker found")

        time.sleep(0.5)

    pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)

    print("\nSaved:", len(results), "tickers")


if __name__ == "__main__":
    main()