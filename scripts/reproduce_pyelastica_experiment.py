#!/usr/bin/env python3
"""
Reproducible minimal experiment mapping protein/ECM-inspired parameters
to emergent curvature/torsion outputs using PyElastica.
"""

import sys
import os
import time
import json
import numpy as np

# Ensure src is in path to import spinalmodes package
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

try:
    from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation, verify_pyelastica_installation
except ImportError as e:
    print(f"Error importing spinalmodes: {e}")
    sys.exit(1)

def run_experiment():
    print(">>> Verifying PyElastica installation...")
    if not verify_pyelastica_installation(exit_on_fail=False):
        print("PyElastica is missing. Please install it via pip install pyelastica")
        sys.exit(1)
    print(">>> PyElastica is available.")

    # Define test cases (Protein/ECM proxies)
    experiments = [
        {
            "name": "Control",
            "anisotropy": 1.0,           # Isotropic stiffness
            "active_curvature": 0.0,     # No active drive
            "stiffness_modulation": 0.0,
            "boundary_condition": "fixed",
            "initial_lateral_defect": 0.0,
            "natural_kyphosis": 2.0      # Normal kyphosis
        },
        {
            "name": "High_Stiffness_Anisotropy (PIEZO2-like)",
            "anisotropy": 5.0,           # Strong lateral stiffness (resists scoliosis)
            "active_curvature": 2.0,     # Moderate active drive
            "stiffness_modulation": 0.1,
            "boundary_condition": "fixed",
            "initial_lateral_defect": 0.5, # Perturbation to test resistance
            "natural_kyphosis": 2.0
        },
        {
            "name": "High_Active_Curvature (Instability)",
            "anisotropy": 1.0,           # Isotropic (weak lateral stiffness)
            "active_curvature": 10.0,    # Strong active drive (destabilizing)
            "stiffness_modulation": 0.0,
            "boundary_condition": "fixed",
            "initial_lateral_defect": 0.5, # Perturbation to trigger instability
            "natural_kyphosis": 2.0
        }
    ]

    results = []

    print(f"\n>>> Running {len(experiments)} experiments...")

    for exp in experiments:
        name = exp["name"]
        print(f"\n--- Running Experiment: {name} ---")

        # Prepare parameters, excluding 'name'
        params = {k: v for k, v in exp.items() if k != "name"}

        # Run simulation with standard settings
        # Using n_elements=30 and duration=2.0s for a quick but meaningful test
        sim_result = run_protein_simulation(
            n_elements=30,
            duration=2.0,
            dt=2e-4,
            show_progress=True,
            **params
        )

        # Collect metrics
        metrics = {
            "max_curvature": sim_result.get("max_curvature"),
            "cobb_angle": sim_result.get("cobb_angle"),
            "S_lat": sim_result.get("S_lat"),
            "U_CC": sim_result.get("U_CC"),
            "U_info": sim_result.get("U_info"),
            "U_gravity": sim_result.get("U_gravity"),
            "runtime_sec": sim_result.get("runtime_sec"),
            "peak_memory_mb": sim_result.get("peak_memory_mb"),
            "success": sim_result.get("success"),
            "error": sim_result.get("error")
        }

        outcome = {
            "name": name,
            "input_parameters": params,
            "metrics": metrics
        }
        results.append(outcome)

        if metrics["success"]:
            print(f"    Success!")
            print(f"    Cobb Angle: {metrics['cobb_angle']:.2f} deg")
            print(f"    Max Curvature: {metrics['max_curvature']:.4f}")
            print(f"    S_lat: {metrics['S_lat']:.4f}")
            print(f"    U_CC (Cost): {metrics['U_CC']:.4f}")
            print(f"    Runtime: {metrics['runtime_sec']:.4f} s")
        else:
            print(f"    Failed: {metrics['error']}")

    # Save results
    output_dir = os.path.join(os.path.dirname(__file__), '../outputs')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "pyelastica_experiment_results.json")

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n>>> Results saved to {output_file}")

if __name__ == "__main__":
    run_experiment()
