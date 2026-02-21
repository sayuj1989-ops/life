import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

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

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

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
    ax.axhline(y=0.1, color='r', linestyle='--', label='Critical Stability Threshold')
    ax.fill_between(df['Mass_kg'], 0, 0.1, color='red', alpha=0.1, label='Unstable / Metabolic Buckling Zone')

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
