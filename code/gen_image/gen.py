import pandas as pd
import matplotlib.pyplot as plt
import io

# 1. Load the data
# If you have a file, use: df = pd.read_csv('your_file.csv')

df = pd.read_csv("get_ticker\company_tickers_with_sectors.csv")

# 2. Calculate the distribution of Sectors
sector_counts = df['Sector'].value_counts()

# 3. Create the Plot
plt.figure(figsize=(10, 7))
colors = plt.get_cmap('Pastel1').colors # Using a nice color palette

plt.pie(
    sector_counts, 
    labels=sector_counts.index, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=colors,
    wedgeprops={'edgecolor': 'white'}
)

# 4. Formatting
plt.title('', fontsize=14, pad=20)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Save or Show
# plt.savefig('nifty500_sector_distribution.png', dpi=300, bbox_inches='tight')
plt.show()