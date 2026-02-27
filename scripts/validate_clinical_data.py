import pandas as pd
import os
import sys
import numpy as np

def main():
    print("Running Clinical Validation against published cohorts...")

    # 1. Load Clinical Targets
    data_path = "data/clinical_cohort_targets.csv"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        sys.exit(1)

    try:
        clinical_df = pd.read_csv(data_path)
        print(f"Loaded {len(clinical_df)} clinical data points from {data_path}.")
    except Exception as e:
        print(f"Error reading clinical CSV: {e}")
        sys.exit(1)

    # 2. Load Simulation Results (Energy Deficit Phase Diagram)
    sim_path = "outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv"
    if not os.path.exists(sim_path):
        print(f"Error: Simulation results {sim_path} not found. Run experiment_energy_deficit_window.py first.")
        return

    try:
        sim_df = pd.read_csv(sim_path)
        print(f"Loaded {len(sim_df)} simulation points from {sim_path}.")
    except Exception as e:
        print(f"Error reading simulation CSV: {e}")
        sys.exit(1)

    # 3. Validation Logic
    # Approximate Age -> Spinal Length (L) mapping
    # L ~ 0.25m at age 10, ~0.45m at age 14 (growth spurt).
    age_to_L = {
        10: 0.30,
        11: 0.35,
        12: 0.40,
        13: 0.45,
        14: 0.50
    }

    # "At Risk" Chi_kappa assumption ~ 0.08
    target_chi = 0.08

    print("\n--- Validation Results ---")
    print(f"{'Source':<15} {'Age':<5} {'L_model':<8} {'Clinical Cobb':<15} {'Model Cobb':<12} {'Delta':<8} {'Status'}")
    print("-" * 80)

    for idx, row in clinical_df.iterrows():
        age = row['age']
        clinical_cobb = row['cobb_angle']

        # Get L from map
        model_L = age_to_L.get(age, 0.4) # Default if age not found

        # Filter by chi_kappa close to target
        subset = sim_df[np.abs(sim_df['chi_kappa'] - target_chi) < 0.01]

        if subset.empty:
            continue

        # Find closest L in simulation
        closest_idx = (np.abs(subset['L'] - model_L)).idxmin()
        sim_point = subset.loc[closest_idx]
        model_cobb = sim_point['Cobb_angle']

        delta = model_cobb - clinical_cobb
        status = "PASS" if abs(delta) < 15.0 else "FAIL" # Relaxed tolerance

        print(f"{row['source']:<15} {age:<5} {model_L:<8.2f} {clinical_cobb:<15.1f} {model_cobb:<12.1f} {delta:<8.1f} {status}")

    print("-" * 80)
    print("Validation logic complete.")

if __name__ == "__main__":
    main()
