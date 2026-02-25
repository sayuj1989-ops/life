"""
Master reproducible execution script for the Code Ocean capsule.
This script runs the core analysis pipeline for the
"Metabolic Buckling: An Energy Deficit Window Explains Adolescent Idiopathic Scoliosis" manuscript.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_script(script_path):
    print(f"--- Running {script_path.name} ---")
    result = subprocess.run([sys.executable, str(script_path)], capture_output=False)
    if result.returncode != 0:
        print(f"Error running {script_path.name}")
        # We continue even if one fails for documentation purposes in logs
    print(f"--- Finished {script_path.name} ---\n")


def main():
    # Set the results directory if not already set (Code Ocean uses ../results)
    if "RESULTS_DIR" not in os.environ:
        # Check if running in Code Ocean (typical dir structure)
        if Path("../results").exists():
            os.environ["RESULTS_DIR"] = "../results"
        else:
            os.environ["RESULTS_DIR"] = "outputs"

    results_dir = Path(os.environ["RESULTS_DIR"])
    results_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting master analysis pipeline.")
    print(f"Results will be saved to: {results_dir.absolute()}\n")

    # 1. Integrated Bio-Gravitational Simulation
    integrated_sim = Path("scripts/experiments/experiment_integrated_simulation.py")
    if integrated_sim.exists():
        run_script(integrated_sim)

    # 2. Energy Deficit Bifurcation Mapping
    bifurcation_sim = Path("scripts/experiments/weekly_sim_energy_deficit_bifurcation.py")
    if bifurcation_sim.exists():
        run_script(bifurcation_sim)

    # 3. Thermodynamic Cost Protein Analysis
    protein_cost_sim = Path("scripts/experiments/experiment_thermodynamic_cost_proteins.py")
    if protein_cost_sim.exists():
        run_script(protein_cost_sim)

    print("Pipeline execution complete.")


if __name__ == "__main__":
    main()
