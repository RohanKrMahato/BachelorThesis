import pandas as pd
import requests
import io
import re
from rapidfuzz import process, fuzz

INPUT_FILE = "nifty_500_end_2004.csv"
OUTPUT_FILE = "company_tickers_NSE_List.csv"

# NSE equity list
NSE_URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"


def clean_name(name):
    name = name.lower()

    # remove common suffix
    name = re.sub(r"\b(ltd|limited|corp|corporation|co)\b\.?", "", name)

    # remove brackets
    name = re.sub(r"\(.*?\)", "", name)

    # remove punctuation
    name = re.sub(r"[^a-z0-9 ]", " ", name)

    name = re.sub(r"\s+", " ", name)

    return name.strip()


def download_nse_list():
    r = requests.get(NSE_URL)
    df = pd.read_csv(io.StringIO(r.text))

    df["clean_name"] = df["NAME OF COMPANY"].apply(clean_name)

    return df


def main():

    print("Downloading NSE symbol list...")
    nse_df = download_nse_list()

    nse_names = nse_df["clean_name"].tolist()

    input_df = pd.read_csv(INPUT_FILE)

    results = []

    for company in input_df["Company Name"].dropna():

        clean_company = clean_name(company)

        match = process.extractOne(
            clean_company,
            nse_names,
            scorer=fuzz.token_sort_ratio
        )

        if match and match[1] > 85:

            matched_row = nse_df[nse_df["clean_name"] == match[0]].iloc[0]

            ticker = matched_row["SYMBOL"] + ".NS"

            print(f"{company}  ->  {ticker}")

            results.append({
                "Company Name": company,
                "Ticker": ticker
            })

    pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)

    print("\nSaved", len(results), "tickers")


if __name__ == "__main__":
    main()