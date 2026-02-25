"""
Plot Clinical Validation: Model vs Historical Cohorts.

This script generates a comparison between the "Energy Deficit Window" predicted by
the computational model and historical clinical data for AIS onset and progression.

Data Sources:
    - Weinstein & Ponseti (1983): Curve progression in idiopathic scoliosis.
    - Lonstein & Carlson (1984): Prediction of curve progression.

Model Mapping:
    - Spinal Length L is mapped to Age based on growth charts.
    - L = 0.35m corresponds to Age ~ 10y (Onset of risk).
    - L = 0.45m corresponds to Age ~ 14y (Peak progression).
    - Mapping: Age = 10 + 40 * (L - 0.35)

Usage:
    python scripts/reporting/plot_clinical_validation.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def load_clinical_data(filepath):
    """Load clinical cohort data."""
    if not os.path.exists(filepath):
        print(f"Warning: Data file {filepath} not found.")
        return None
    return pd.read_csv(filepath)

def length_to_age(L):
    """Map spinal length (m) to Age (years)."""
    return 10 + 40 * (L - 0.35)

def age_to_length(Age):
    """Map Age (years) to spinal length (m)."""
    return 0.35 + (Age - 10) / 40.0

def plot_validation(data, output_path):
    """Generate validation plot."""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 1. Plot Clinical Data
    if data is not None:
        sources = data['source'].unique()
        markers = {'Weinstein_1983': 'o', 'Lonstein_1984': 's'}
        colors = {'Weinstein_1983': 'blue', 'Lonstein_1984': 'green'}

        for source in sources:
            subset = data[data['source'] == source]
            # Group by age to handle multiple points or just plot scatter
            ax1.scatter(subset['age'], subset['cobb_angle'],
                        label=f"Clinical: {source}",
                        marker=markers.get(source, 'o'),
                        color=colors.get(source, 'black'),
                        s=100, alpha=0.7)

            # Connect points if logical
            subset_sorted = subset.sort_values('age')
            ax1.plot(subset_sorted['age'], subset_sorted['cobb_angle'],
                     color=colors.get(source, 'black'), linestyle='--', alpha=0.5)

    # 2. Plot Model Prediction (Energy Deficit Window)
    # Define spinal length range
    L_range = np.linspace(0.25, 0.50, 100)
    Age_range = length_to_age(L_range)

    # Calculate Theoretical Deficit (Toy Model)
    # Demand ~ L^4, Supply ~ L^2
    # Deficit Ratio R = (L/L_crit)^2
    L_crit = 0.35
    R_deficit = (L_range / L_crit)**2

    # Instability starts when R > 1 (L > 0.35)
    # Assume Cobb Angle is proportional to excess deficit for visualization
    # Cobb ~ k * (R - 1) if R > 1 else 0
    k_cobb = 40.0 # Tuning parameter to match scale
    predicted_cobb = np.maximum(0, k_cobb * (R_deficit - 1))

    # Filter for realistic age range (e.g., 8-16)
    mask = (Age_range >= 8) & (Age_range <= 16)

    ax1.plot(Age_range[mask], predicted_cobb[mask],
             color='red', linewidth=3, label='Model Prediction (Energy Deficit)')

    # Shade the "Energy Deficit Window"
    ax1.fill_between(Age_range[mask], 0, predicted_cobb[mask],
                     where=(Age_range[mask] >= 10),
                     color='red', alpha=0.1, label='Instability Window')

    # Formatting
    ax1.set_xlabel('Age (Years)', fontsize=12)
    ax1.set_ylabel('Cobb Angle (Degrees) / Risk Score', fontsize=12)
    ax1.set_title('Clinical Validation: Model vs Cohort Data', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left')

    # Add secondary x-axis for Spinal Length
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())

    # Create ticks for Length
    age_ticks = ax1.get_xticks()
    length_ticks = [age_to_length(a) for a in age_ticks]

    ax2.set_xticks(age_ticks)
    ax2.set_xticklabels([f"{l:.2f}m" for l in length_ticks])
    ax2.set_xlabel('Equivalent Spinal Length (m)', fontsize=10, color='gray')

    # Add annotation for L_crit
    ax1.axvline(x=10, color='k', linestyle=':', alpha=0.5)
    ax1.text(10.1, 5, 'Onset (L_crit=0.35m)', rotation=90, verticalalignment='bottom')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    data_path = "data/clinical_cohort_targets.csv"
    output_dir = "manuscript/figures"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "fig_clinical_validation.png")

    data = load_clinical_data(data_path)
    plot_validation(data, output_path)
