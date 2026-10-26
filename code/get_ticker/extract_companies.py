import pandas as pd

# 1. Load your Excel file
file_path = 'IndexInclExcl.xls'
df = pd.read_excel(file_path, sheet_name='Nifty 500')

# 2. Process dates and sort
df['Event Date'] = pd.to_datetime(df['Event Date'], dayfirst=True)
df = df.sort_values(by='Event Date')

# 3. Filter for data until the end of 2004
target_date = pd.Timestamp(2004, 12, 31)
df_until_2004 = df[df['Event Date'] <= target_date]

# 4. Apply Inclusion/Exclusion logic
nifty_500_set = set()
for _, row in df_until_2004.iterrows():
    company = str(row['Scrip Name']).strip()
    description = str(row['Description']).lower()
    
    if "inclusion" in description:
        nifty_500_set.add(company)
    elif "exclusion" in description:
        nifty_500_set.discard(company)

# 5. Create a DataFrame from the final list
final_list = sorted(list(nifty_500_set))
result_df = pd.DataFrame(final_list, columns=['Company Name'])

# 6. Save to CSV
result_df.to_csv('nifty_500_end_2004.csv', index=False)

print(f"Successfully saved {len(final_list)} companies to 'nifty_500_end_2004.csv'")