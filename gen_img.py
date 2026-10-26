import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist

def generate_concentration_hist():
    # 1. Setup Parameters
    np.random.seed(42)
    n_days = 1000       # Number of data points (days)
    n_dims = 500        # Number of dimensions (stocks)
    
    # 2. Generate "Purely Random" Market Data
    # Just Gaussian noise in 500 dimensions
    random_data = np.random.randn(n_days, n_dims)
    
    # 3. Generate "Real" (Structured) Market Data
    # A market driven by a few strong factors (e.g., Market Trend + Sectors)
    n_factors = 5
    factors = np.random.randn(n_days, n_factors) # Latent economic drivers
    loadings = np.random.randn(n_factors, n_dims) # How stocks react
    
    # Mix Factors + Noise
    noise_level = 3.0
    structured_data = np.dot(factors, loadings) + np.random.randn(n_days, n_dims) * noise_level
    
    # IMPORTANT: Normalize both datasets (Z-score)
    # We want to compare the SHAPE of distances, not the magnitude driven by price scale
    random_data = (random_data - np.mean(random_data)) / np.std(random_data)
    structured_data = (structured_data - np.mean(structured_data)) / np.std(structured_data)

    # 4. Calculate Pairwise Euclidean Distances
    # This computes distance between Day 1 & Day 2, Day 1 & Day 3... etc.
    dist_random = pdist(random_data, metric='euclidean')
    dist_structure = pdist(structured_data, metric='euclidean')

    # 5. Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot Random Histogram (The "Curse")
    ax.hist(dist_random, bins=50, density=True, alpha=0.5, color='gray', 
            label='Purely Random Market (Concentrated)', edgecolor='black')

    # Plot Structured Histogram (The "Reality")
    ax.hist(dist_structure, bins=50, density=True, alpha=0.6, color='#1f77b4', 
            label='Real Market Structure (Differentiated)', edgecolor='black')

    # 6. Styling & Annotations
    ax.set_title('Concentration of Distances in High-Dimensional Space', fontsize=14, fontweight='bold')
    ax.set_xlabel('Euclidean Distance between Daily Vectors', fontsize=12)
    ax.set_ylabel('Frequency Density', fontsize=12)
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.3)

    # Annotation pointing to the spike
    peak_x = np.mean(dist_random)
    peak_y = 0.6 # Approx height
    ax.annotate('Differentiation is Tough:\nAll days look "equally far apart"', 
                xy=(peak_x, 0.4), xytext=(peak_x + 10, 0.5),
                arrowprops=dict(facecolor='black', shrink=0.05),
                fontsize=10, ha='left')

    # 7. Save
    output_filename = 'distance_concentration_histogram.png'
    plt.savefig(output_filename, dpi=300)
    print(f"Image saved as {output_filename}")
    plt.show()

if __name__ == "__main__":
    generate_concentration_hist()