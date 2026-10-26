import pandas as pd

# files
yf_file = "company_tickers_Search_YF.csv"
nse_file = "company_tickers_NSE_List.csv"

output_file = "company_tickers_final.csv"

# load data
yf_df = pd.read_csv(yf_file)
nse_df = pd.read_csv(nse_file)

# normalize company names
yf_df["Company Name"] = yf_df["Company Name"].str.strip()
nse_df["Company Name"] = nse_df["Company Name"].str.strip()

# create dictionary from NSE list (priority source)
nse_dict = dict(zip(nse_df["Company Name"], nse_df["Ticker"]))

# start with YF dataframe
final_df = yf_df.copy()

# overwrite ticker if company exists in NSE list
final_df["Ticker"] = final_df.apply(
    lambda row: nse_dict[row["Company Name"]] if row["Company Name"] in nse_dict else row["Ticker"],
    axis=1
)

# add companies that exist only in NSE list
extra = nse_df[~nse_df["Company Name"].isin(final_df["Company Name"])]

final_df = pd.concat([final_df, extra], ignore_index=True)

# save result
final_df.to_csv(output_file, index=False)

print("Merged file saved as:", output_file)
print("Total companies:", len(final_df))