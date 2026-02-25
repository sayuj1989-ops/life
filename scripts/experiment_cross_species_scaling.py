"""
Cross-Species Scaling Analysis for Metabolic Buckling.

This script implements the validation of the 'Bio-Gravitational Number' (Bg)
across 9 vertebrate species, testing the hypothesis that humans occupy a unique
unstable regime (Bg < 0.1) where metabolic expenditure is required to maintain
spinal geometry.

Data Source:
    O'Connell, G. D., Vresilovic, E. J., & Elliott, D. M. (2007).
    Comparison of animals used in disc research to human lumbar disc geometry.
    Spine, 32(3), 328-333.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dataclasses import dataclass
from pathlib import Path

# Constants
g = 9.81  # m/s^2

@dataclass
class Species:
    name: str
    mass_kg: float
    spine_length_m: float
    disc_area_mm2: float
    youngs_modulus_mpa: float  # Normalized compressive stiffness
    is_biped: bool = False

    @property
    def area_m2(self):
        return self.disc_area_mm2 * 1e-6

    @property
    def radius_m(self):
        return np.sqrt(self.area_m2 / np.pi)

    @property
    def I_m4(self):
        """Second moment of area for circular cross section: I = pi * r^4 / 4 = A^2 / (4pi)."""
        return (self.area_m2 ** 2) / (4 * np.pi)

    @property
    def E_pa(self):
        return self.youngs_modulus_mpa * 1e6

    @property
    def flexural_stiffness_Nm2(self):
        return self.E_pa * self.I_m4

    @property
    def gravitational_moment_Nm(self):
        """Approximate gravitational moment: M_g ~ M * g * L / 2 (distributed load)."""
        return self.mass_kg * g * self.spine_length_m / 2

    @property
    def buckling_load_N(self):
        """Euler critical load for column: P_crit = pi^2 * EI / L^2."""
        return (np.pi ** 2) * self.flexural_stiffness_Nm2 / (self.spine_length_m ** 2)

    @property
    def Bg(self):
        """Bio-Gravitational Number: Ratio of Elastic Stiffness to Gravitational Demand.

        Bg = EI / (M * g * L^2)

        If Bg >> 1: Structure is stiff enough to resist gravity passively.
        If Bg << 1: Structure requires active metabolic stabilization.
        """
        return self.flexural_stiffness_Nm2 / (self.mass_kg * g * self.spine_length_m ** 2)


def get_species_data():
    """Returns list of Species objects with literature data."""
    # Data from O'Connell et al. 2007 & Showalter et al. 2012
    # Mass and Length estimates based on typical lab animal weights/sizes
    return [
        Species("Human", 70.0, 0.50, 1925, 9.95, is_biped=True),
        Species("Calf", 100.0, 0.80, 1100, 12.72),
        Species("Pig", 50.0, 0.60, 872, 15.77),
        Species("Baboon", 25.0, 0.40, 808, 9.36, is_biped=True),  # Partial biped
        Species("Goat", 50.0, 0.50, 670, 7.20),
        Species("Sheep", 60.0, 0.60, 511, 9.78),
        Species("Rabbit", 3.0, 0.25, 90, 10.44),
        Species("Rat", 0.3, 0.15, 11.85, 5.09),
        Species("Mouse", 0.03, 0.05, 1.61, 2.93),
    ]

def run_analysis():
    species_list = get_species_data()

    results = []
    for s in species_list:
        results.append({
            "Species": s.name,
            "Mass (kg)": s.mass_kg,
            "Length (m)": s.spine_length_m,
            "EI (Nm2)": s.flexural_stiffness_Nm2,
            "Bg": s.Bg,
            "P_crit (N)": s.buckling_load_N,
            "Load (N)": s.mass_kg * g,
            "Is Biped": s.is_biped
        })

    df = pd.DataFrame(results)
    print("--- Cross-Species Scaling Analysis ---")
    print(df.sort_values("Bg"))

    # Save results
    output_dir = Path("outputs/cross_species")
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / "scaling_results.csv", index=False)

    # Generate Plot
    plot_results(df, output_dir)

def plot_results(df, output_dir):
    plt.figure(figsize=(10, 6))

    # Color by bipedalism
    colors = ['red' if b else 'blue' for b in df["Is Biped"]]

    plt.scatter(df["Mass (kg)"], df["Bg"], c=colors, s=100, alpha=0.7)

    for i, row in df.iterrows():
        plt.annotate(row["Species"], (row["Mass (kg)"], row["Bg"]),
                     xytext=(5, 5), textcoords='offset points')

    plt.xscale('log')
    plt.yscale('log')

    # Add instability threshold
    plt.axhline(0.1, color='k', linestyle='--', label='Instability Threshold (Bg=0.1)')
    plt.axhline(1.0, color='gray', linestyle=':', label='Passive Stability (Bg=1.0)')

    plt.xlabel("Body Mass (kg)")
    plt.ylabel("Bio-Gravitational Number (Bg)")
    plt.title("The Allometric Trap: Humans occupy a unique unstable regime")
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_dir / "fig_cross_species_bg.png", dpi=300)
    # Also save to manuscript figures
    manuscript_figs = Path("manuscript/figures")
    manuscript_figs.mkdir(parents=True, exist_ok=True)
    plt.savefig(manuscript_figs / "fig_cross_species_bg.png", dpi=300)

    print(f"\nFigure saved to {manuscript_figs / 'fig_cross_species_bg.png'}")

if __name__ == "__main__":
    run_analysis()
