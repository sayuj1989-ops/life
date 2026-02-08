"""
Reproducible minimal experiment demonstrating integration of PyElastica
with protein metrics via the afcc.simulation module.

This experiment simulates the mechanical response of "virtual proteins"
with different structural properties (Anisotropy, Curvature, Torsion).
"""

import sys
import csv
import time
from pathlib import Path
from pprint import pprint

# Ensure we can import from research/alphafold_countercurvature/src
# In a real installed environment this wouldn't be needed if installed
src_path = Path(__file__).parent.parent / "research/alphafold_countercurvature/src"
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

try:
    from afcc.simulation import simulate_protein_mechanics
except ImportError:
    print("Error: Could not import afcc.simulation. Check python path.")
    sys.exit(1)

def run_experiment():
    print("Running Integrated Protein Mechanics Experiment...")

    # 1. Define Virtual Protein Profiles (Mock Metrics)
    profiles = {
        "Control": {
            'anisotropy_index': 1.0,
            'curvature_summary': 0.0,
            'torsion_summary': 0.0,
            'PAE_domain_blockiness_score': 0.0
        },
        "High_Vector_Strength": {
            'anisotropy_index': 5.0, # Highly aligned/fibrous
            'curvature_summary': 0.0,
            'torsion_summary': 0.0,
            'PAE_domain_blockiness_score': 0.0
        },
        "High_Curvature_Drive": {
            'anisotropy_index': 1.0,
            'curvature_summary': 1.0, # Active bending
            'torsion_summary': 0.0,
            'PAE_domain_blockiness_score': 0.0
        },
        "Twisted_Scaffold": {
            'anisotropy_index': 2.0,
            'curvature_summary': 0.5,
            'torsion_summary': 0.5, # Torsional coupling
            'PAE_domain_blockiness_score': 0.0
        },
        "Blocky_Linker": {
            'anisotropy_index': 1.0,
            'curvature_summary': 0.5,
            'torsion_summary': 0.0,
            'PAE_domain_blockiness_score': 2.0 # Modulated stiffness
        }
    }

    # Output file
    output_dir = Path("outputs/integrated_sim")
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "results.csv"

    results = []

    print(f"{'Profile':<25} | {'Max Curv':<10} | {'Max Tor':<10} | {'S_lat':<10} | {'Time (s)':<8}")
    print("-" * 80)

    for name, metrics in profiles.items():
        # Run Simulation
        # We use a standard "rod unit" setup
        # length=0.5m, n_elements=50, duration=2.0s

        sim_out = simulate_protein_mechanics(
            metrics,
            length=0.5,
            n_elements=50,
            duration=2.0,
            dt=1e-4, # 1e-4 is stable
            boundary_condition="fixed"
        )

        if not sim_out.get('success', False):
            print(f"Error running {name}: {sim_out.get('error')}")
            continue

        # Collect results
        row = {
            "profile_name": name,
            **metrics,
            **sim_out
        }
        results.append(row)

        print(f"{name:<25} | {sim_out.get('max_curvature', 0):<10.4f} | {sim_out.get('max_torsion', 0):<10.4f} | {sim_out.get('S_lat', 0):<10.4f} | {sim_out.get('runtime_sec', 0):<8.4f}")

    # Save to CSV
    if results:
        fieldnames = list(results[0].keys())
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"\nResults saved to {csv_path}")

if __name__ == "__main__":
    run_experiment()
