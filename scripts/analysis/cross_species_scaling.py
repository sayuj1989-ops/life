import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats

# Ensure output directory exists
os.makedirs('outputs/figures', exist_ok=True)

def main():
    # Load data
    df = pd.read_csv('data/species_parameters.csv')

    # Constants
    g = 9.81

    # Calculate Bg = EI / (M * g * L^2)
    # Note: For quadrupeds, this relates to beam stiffness vs sag.
    # For bipeds, this relates to column buckling vs load.
    # Low Bg means "Floppy/Unstable". High Bg means "Stiff/Stable".
    df['Weight_N'] = df['Mass_kg'] * g
    df['Bg'] = df['EI_Nm2'] / (df['Weight_N'] * df['Length_m']**2)

    # Calculate Kleiber-Euler Number (Ke)
    # Supply S ~ M^0.75 (Metabolic Rate)
    # Demand D ~ L^4 (Active Moment to maintain straightness against gravity M_g ~ L^4)
    # We normalize to Human Adult = 1.0 for comparison

    # Base metabolic rate BMR = 70 * M^0.75 (kcal/day approx) -> Watts
    # Specific Supply Density sigma ~ M^-0.25
    # Total Supply Capacity ~ Volume * sigma ~ L^3 * L^-0.75 ~ L^2.25?
    # Let's just use M^0.75 as the supply proxy.

    # Demand Proxy:
    # Moment M_g ~ Weight * Eccentricity. Eccentricity ~ L. Weight ~ L^3.
    # So Moment ~ L^4.
    # Active Power P ~ Moment * Rate.
    # So Demand ~ L^4.

    human_adult = df[df['Species'] == 'Human_Adult'].iloc[0]

    supply_ref = human_adult['Mass_kg']**0.75
    demand_ref = human_adult['Length_m']**4

    df['Supply_Index'] = df['Mass_kg']**0.75 / supply_ref
    df['Demand_Index'] = df['Length_m']**4 / demand_ref

    df['Ke'] = df['Supply_Index'] / df['Demand_Index']

    print(df[['Species', 'Bg', 'Ke']])

    # Perform Regression
    df_filtered = df[~df['Species'].isin(['Giraffe', 'Dolphin'])].copy()
    log_mass = np.log10(df_filtered['Mass_kg'])
    log_bg = np.log10(df_filtered['Bg'])

    slope, intercept, r_value, p_value, std_err = stats.linregress(log_mass, log_bg)

    # Bootstrap for 95% CI
    np.random.seed(42)
    n_iterations = 10000
    boot_slopes = []

    for _ in range(n_iterations):
        indices = np.random.choice(len(df_filtered), len(df_filtered), replace=True)
        sample_log_mass = log_mass.iloc[indices]
        sample_log_bg = log_bg.iloc[indices]
        bslope, _, _, _, _ = stats.linregress(sample_log_mass, sample_log_bg)
        boot_slopes.append(bslope)

    ci_lower, ci_upper = np.percentile(boot_slopes, [2.5, 97.5])

    print(f"\n--- Statistical Results ---")
    print(f"Allometric Exponent (slope): {slope:.3f} ± {std_err:.3f}")
    print(f"R^2: {r_value**2:.3f}")
    print(f"p-value: {p_value:.3e}")
    print(f"95% CI from Bootstrap: [{ci_lower:.3f}, {ci_upper:.3f}]")
    print(f"Deviation from -0.25 (Metabolic Scaling): {abs(slope - (-0.25)):.3f}")

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot Regression Line and CI
    x_vals = np.linspace(df_filtered['Mass_kg'].min() * 0.5, df_filtered['Mass_kg'].max() * 2, 100)
    log_x_vals = np.log10(x_vals)
    y_vals = 10**(intercept + slope * log_x_vals)

    # CI lines
    y_lower = 10**(intercept + ci_lower * log_x_vals)
    y_upper = 10**(intercept + ci_upper * log_x_vals)

    ax.plot(x_vals, y_vals, 'k--', linewidth=2, label=f'Allometric Fit: $B_g \\propto M^{{{slope:.3f}}}$')
    ax.fill_between(x_vals, y_lower, y_upper, color='gray', alpha=0.2, label='95% Confidence Interval')

    # Plot Points
    colors = {'Quadruped': 'blue', 'Biped': 'red', 'Facultative_Biped': 'orange'}
    markers = {'Quadruped': 'o', 'Biped': '^', 'Facultative_Biped': 's'}

    for i, row in df.iterrows():
        posture = row['Posture']
        color = colors.get(posture, 'gray')
        marker = markers.get(posture, 'o')

        ax.scatter(row['Mass_kg'], row['Bg'], c=color, marker=marker, s=150, label=posture if posture not in ax.get_legend_handles_labels()[1] else "")
        ax.annotate(row['Species'], (row['Mass_kg'], row['Bg']), xytext=(5, 5), textcoords='offset points', fontsize=9)

    # Add Stability Zones
    # Critical Bg ~ 0.1 (Euler limit approx 1/pi^2)
    ax.axhline(y=0.1, color='r', linestyle='--', label='Critical Stability Threshold ($B_g=0.1$)')
    ax.fill_between(x_vals, 1e-4, 0.1, color='red', alpha=0.1, label='Unstable / Metabolic Buckling Zone')

    # Add stats text box
    stats_text = (f"Exponent: {slope:.3f} $\\pm$ {std_err:.3f}\n"
                  f"$R^2$: {r_value**2:.3f}\n"
                  f"$p$-value: {p_value:.1e}\n"
                  f"95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]\n"
                  f"Kleiber deviation: {abs(slope - (-0.25)):.3f}")

    props = dict(boxstyle='round', facecolor='white', alpha=0.8)
    ax.text(0.05, 0.15, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Body Mass (kg)')
    ax.set_ylabel('Bio-Gravitational Number (Bg)')
    ax.set_title('Cross-Species Scaling: The Allometric Trap')
    ax.grid(True, which="both", ls="-", alpha=0.2)
    ax.legend()

    plt.tight_layout()
    plt.savefig('outputs/figures/cross_species_scaling.png')
    print("Figure saved to outputs/figures/cross_species_scaling.png")

if __name__ == "__main__":
    main()
