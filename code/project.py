import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ──────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────

def preview_data(frequencies, sector_path):
    """Prints a preview of the datasets to the console."""
    print("\n" + "="*50)
    print("DATA PREVIEW")
    print("="*50)

    for freq in frequencies:
        returns_path = f'./standardized_return/standardized_returns_{freq}.csv'
        print(f"\n--- {freq.upper()} STANDARDIZED RETURNS PREVIEW ---")
        
        if os.path.exists(returns_path):
            df_returns = pd.read_csv(returns_path, index_col='Date', parse_dates=True)
            print(f"Shape: {df_returns.shape} (Rows: Time Periods, Columns: Tickers)")
            print(df_returns.head(3))
            print(f"\n{freq.capitalize()} Summary Statistics (first 5 stocks):")
            print(df_returns.iloc[:, :5].describe())
        else:
            print(f"Error: Could not find {returns_path}")
        print("-" * 30)

    print("\n--- SECTOR MAPPING PREVIEW ---")
    if os.path.exists(sector_path):
        df_sectors = pd.read_csv(sector_path)
        print(f"Shape: {df_sectors.shape}")
        print(df_sectors.head())
        print("\nValue Counts by Sector:")
        print(df_sectors['Sector'].value_counts())
    else:
        print(f"Error: Could not find {sector_path}")


def run_pca_analysis(start_year, end_year,
                     base_dir='./standardized_return/',
                     sector_path='./get_ticker/company_tickers_with_sectors.csv'):
    """    
    Comprehensive PCA Analysis across Daily, Weekly, and Monthly frequencies.
    - Displays full-shape data previews and statistical tables.
    - Compares Scree and Cumulative plots (Linear & Log) across all frequencies.
    - High-res heatmaps for stocks and sectors with grid styling.
    """
    print(f"\n{'='*100}")
    print(f"MULTI-FREQUENCY PCA ANALYSIS: {start_year} – {end_year}")
    print(f"{'='*100}\n")
    
    frequencies = ['daily', 'weekly', 'monthly']
    pca_results = {}
    
    # Load Sector Mapping
    sector_df = pd.read_csv(sector_path)
    sector_map = sector_df.set_index('Ticker')['Sector'].to_dict()
    
    # ──────────────────────────────────────────────────────────────────────────
    # 1. LOAD, FILTER, AND COMPUTE PCA
    # ──────────────────────────────────────────────────────────────────────────
    for freq in frequencies:
        path = f"{base_dir}standardized_returns_{freq}.csv"
        try:
            df_full = pd.read_csv(path, index_col='Date', parse_dates=True)
            mask = (df_full.index.year >= start_year) & (df_full.index.year <= end_year)
            std_ret = df_full.loc[mask].copy()
            
            if std_ret.empty:
                print(f"No data available for {freq} in the selected period.")
                continue

            T, N = std_ret.shape
            
            # Core PCA Computation
            cov_matrix = std_ret.cov()
            eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
            
            # Sort descending
            idx = eigenvalues.argsort()[::-1]
            eigenvalues = eigenvalues[idx]
            eigenvectors = eigenvectors[:, idx]
            
            loadings_df = pd.DataFrame(
                eigenvectors,
                index=std_ret.columns,
                columns=[f'PC{i+1}' for i in range(N)]
            )
            
            total_var = np.sum(eigenvalues)
            cumulative_variance = np.cumsum(eigenvalues / total_var) * 100
            
            pca_results[freq] = {
                'std_ret': std_ret,
                'eigenvalues': eigenvalues,
                'cumulative_variance': cumulative_variance,
                'loadings_df': loadings_df,
                'N': N, 'T': T, 'total_var': total_var
            }
        except FileNotFoundError:
            print(f"Error: Could not find {path}")

    if not pca_results:
        return

    # ──────────────────────────────────────────────────────────────────────────
    # 2. STATISTICAL TABLES AND DATA PREVIEWS (PER FREQUENCY)
    # ──────────────────────────────────────────────────────────────────────────
    for freq in frequencies:
        if freq not in pca_results: continue
        res = pca_results[freq]
        
        print(f"\n{'#'*45} {freq.upper()} ANALYSIS {'#'*45}")
        
        # A. Full Dataset Shape & Preview
        print(f"\n[1] DATASET STRUCTURE ({freq.upper()}):")
        print(f"Total Rows (Trading Periods): {res['T']}")
        print(f"Total Columns (Stocks):       {res['N']}")
        print(f"Full Data Shape: {res['std_ret'].shape}")
        print(res['std_ret'].head(5))
        
        # B. Top 10 Eigenvalues
        print(f"\n[2] TOP 10 EIGENVALUES & VARIANCE EXPLAINED ({freq.upper()}):")
        top_10_ev = res['eigenvalues'][:10]
        eigen_table = pd.DataFrame({
            'Component': [f'PC{i+1}' for i in range(10)],
            'Eigenvalue ($\lambda$)': top_10_ev,
            '\% Variance Explained': (top_10_ev / res['total_var']) * 100,
            'Cumulative Variance ($\%$)': res['cumulative_variance'][:10]
        })
        print(eigen_table)

        # C. Variance Threshold Table
        thresholds = [70, 75, 80, 85]
        comp_needed = [np.argmax(res['cumulative_variance'] >= t) + 1 for t in thresholds]
        thresh_df = pd.DataFrame({
            'Target Variance ($\%$)': thresholds,
            'Components Required': comp_needed,
            'Actual Explained ($\%$)': [round(res['cumulative_variance'][k-1], 2) for k in comp_needed]
        })
        print(f"\n[3] VARIANCE THRESHOLD SUMMARY:")
        print(thresh_df)

        # D. Top 10 Eigenvectors (Loadings) & Summary Stats
        print(f"\n[4] EIGENVECTORS (LOADINGS) - TOP 10 PCs (First 10 Stocks shown):")
        top_10_loadings = res['loadings_df'].iloc[:, :10]
        print(top_10_loadings.head(10))
        
        print(f"\n[5] EIGENVECTOR SUMMARY STATISTICS (TOP 10 PCs):")
        print(top_10_loadings.describe().loc[['mean', 'std', 'min', 'max']])

        # E. Dominant Sectors (Text)
        loadings_with_sectors = res['loadings_df'].copy()
        loadings_with_sectors['Sector'] = loadings_with_sectors.index.map(sector_map)
        sector_abs = (
            loadings_with_sectors.dropna(subset=['Sector'])
            .drop(columns='Sector').abs()
            .groupby(loadings_with_sectors['Sector']).mean()
        )
        print(f"\n[6] DOMINANT SECTORS (TOP 3 PCs):")
        for pc in ['PC1', 'PC2', 'PC3']:
            top_s = sector_abs[pc].idxmax()
            print(f" - {pc}: {top_s:25} | Avg Abs Loading: {sector_abs[pc].max():.4f}")

    # ──────────────────────────────────────────────────────────────────────────
    # 3. COMPARATIVE VISUALIZATIONS (ALL FREQUENCIES)
    # ──────────────────────────────────────────────────────────────────────────
    styles = {'daily': ('royalblue', '-'), 'weekly': ('darkorange', '--'), 'monthly': ('forestgreen', '-.')}
    
    # A. Scree Plots (Linear vs Log)
    plt.figure(figsize=(12, 6))
    for freq, res in pca_results.items():
        c, s = styles[freq]
        plt.plot(range(1, res['N']+1), res['eigenvalues'], label=freq.capitalize(), color=c, linestyle=s)
    plt.title(f"Scree Plot Comparison – Linear Scale ({start_year}–{end_year})", fontsize=15)
    plt.xlabel("Principal Component (PC)"); plt.ylabel("Eigenvalue ($\lambda$)")
    plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout(); plt.show()

    plt.figure(figsize=(12, 6))
    for freq, res in pca_results.items():
        c, s = styles[freq]
        plt.plot(range(1, res['N']+1), res['eigenvalues'], label=freq.capitalize(), color=c, linestyle=s)
    plt.yscale('log')
    plt.title(f"Scree Plot Comparison – Log Scale ({start_year}–{end_year})", fontsize=15)
    plt.xlabel("Principal Component (PC)"); plt.ylabel("Eigenvalue ($\lambda$) - Log")
    plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout(); plt.show()

    # B. Scree Plot (First 30 PCs Zoomed) - NEWLY ADDED
    plt.figure(figsize=(12, 6))
    for freq, res in pca_results.items():
        c, _ = styles[freq]
        n_p = min(15, res['N'])
        plt.plot(range(1, n_p+1), res['eigenvalues'][:n_p], marker='o', label=freq.capitalize(), color=c)
    plt.title(f'Scree Plot (First 15 PCs)', fontsize=15)
    plt.ylabel('Eigenvalue ($\lambda$)'); plt.xlabel('Principal Component (PC)')
    plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout(); plt.show()

    # C. Cumulative Variance (ALL PCs)
    plt.figure(figsize=(12, 6))
    for freq, res in pca_results.items():
        c, s = styles[freq]
        plt.plot(range(1, res['N']+1), res['cumulative_variance'], label=freq.capitalize(), color=c, linestyle=s)
    plt.title(f"Cumulative Variance Explained – All PCs ({start_year}–{end_year})", fontsize=15)
    plt.xlabel("Number of Principal Components"); plt.ylabel("Cumulative Variance ($\%$)")
    plt.axhline(y=80, color='red', linestyle=':', alpha=0.6, label='80$\%$ Threshold')
    plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout(); plt.show()

    # D. Cumulative Variance (First 30 PCs Zoomed)
    plt.figure(figsize=(12, 6))
    for freq, res in pca_results.items():
        c, _ = styles[freq]
        n_p = min(30, res['N'])
        plt.plot(range(1, n_p+1), res['cumulative_variance'][:n_p], marker='o', label=freq.capitalize(), color=c)
    plt.title(f'Cumulative Variance Explained (First 30 PCs)', fontsize=15)
    plt.ylabel('Cumulative $\%$'); plt.xlabel('Number of Components'); plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout(); plt.show()

    # ──────────────────────────────────────────────────────────────────────────
    # 4. INDIVIDUAL HEATMAPS (STOCKS & SECTORS)
    # ──────────────────────────────────────────────────────────────────────────
    n_plot_heat = 30 

    for freq, res in pca_results.items():
        # A. Stock Loadings Heatmap
        loadings_df = res['loadings_df']
        abs_l = loadings_df.iloc[:, :n_plot_heat].abs()
        max_abs_per_stock = abs_l.max(axis=1)
        top_indices = max_abs_per_stock.sort_values(ascending=False).head(45).index
        loadings_subset = loadings_df.loc[top_indices, loadings_df.columns[:n_plot_heat]]
        
        plt.figure(figsize=(14, 10))
        sns.heatmap(
            loadings_subset,
            cmap='coolwarm',
            center=0,
            vmin=-0.4, vmax=0.4,
            linewidths=0.3,
            cbar_kws={'label': 'Loading (weight)'},
            xticklabels=[f'PC{i+1}' for i in range(n_plot_heat)],
            yticklabels=loadings_subset.index,
        )
        plt.title(f'PCA Loadings Heatmap [{freq.upper()}] – Top Stocks × First {n_plot_heat} PCs', fontsize=16, pad=20)
        plt.xlabel('Principal Component', fontsize=13)
        plt.ylabel('Stock Ticker', fontsize=13)
        plt.xticks(rotation=0)
        plt.tight_layout(); plt.show()
        
        # B. Sectoral Dominance Heatmap
        loadings_with_sectors = res['loadings_df'].copy()
        loadings_with_sectors['Sector'] = loadings_with_sectors.index.map(sector_map)
        sector_abs = (
            loadings_with_sectors.dropna(subset=['Sector'])
            .drop(columns='Sector').abs()
            .groupby(loadings_with_sectors['Sector']).mean()
        )
        plt.figure(figsize=(14, 8))
        sns.heatmap(
            sector_abs.iloc[:, :10],
            cmap='YlGnBu',
            annot=True,
            fmt=".3f",
            linewidths=0.3,
            cbar_kws={'label': 'Avg Absolute Loading'}
        )
        plt.title(f'Sectoral Dominance Heatmap [{freq.upper()}] ({start_year}–{end_year})', fontsize=16, pad=20)
        plt.xlabel('Principal Component', fontsize=12)
        plt.ylabel('Sector', fontsize=12)
        plt.tight_layout(); plt.show()

    print(f"\nMulti-Frequency Analysis Complete for {start_year}–{end_year}.")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN EXECUTION BLOCK
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Setup paths
    freqs = ['daily', 'weekly', 'monthly']
    s_path = './get_ticker/company_tickers_with_sectors.csv'
    
    # Run Preview
    preview_data(freqs, s_path)
    
    # Run Analyses
    analysis_periods = [
        (2005, 2020),
        (2005, 2010),
        (2010, 2015),
        (2015, 2020)
    ]
    
    for start, end in analysis_periods:
        run_pca_analysis(start, end)