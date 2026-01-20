"""
Experiment: Parameter Map for Countercurvature Rod
==================================================

This script performs a parameter sweep over biological/mechanical parameters to map
emergent spinal shapes (curvature, torsion, tip deflection).

Parameters Mapped:
1. Stiffness Anisotropy (Stiffness_Lat / Stiffness_Sag):
   - Proxy for: Filament alignment / bundling (e.g., Vimentin/Actin organization).
   - High Anisotropy (~5-10) -> "Tension Rod" (Cluster 0).
   - Low Anisotropy (~1) -> "Blocky Scaffold" (Cluster 2).

2. Preferred Curvature Strength (chi_kappa):
   - Proxy for: Intrinsic growth gradients or wedging.
   - High chi_kappa -> Strong tendency to curve (e.g., rapid anterior growth).

3. Boundary Condition:
   - Proxy for: Pelvic/Sacral fixation.
   - "fixed" -> Rigid sacrum (clamped).
   - "pinned" -> Looser sacrum (hinged), allowing rotation.

Output:
- CSV file in `outputs/parameter_map_results.csv` containing metrics for each run.
"""

import sys
import os
import csv
import time
import tracemalloc
import numpy as np

# Ensure project root is in path
sys.path.append(os.getcwd())

try:
    import elastica as ea
    from spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
    from spinalmodes.countercurvature.info_fields import InfoField1D
    from spinalmodes.countercurvature.coupling import CounterCurvatureParams
except ImportError:
    print("PyElastica or spinalmodes not found.")
    print("Please install pyelastica: pip install pyelastica")
    sys.exit(1)

def run_parameter_map():
    print("Starting Parameter Map Experiment...")

    # ---------------------------------------------------------
    # Experiment Configuration
    # ---------------------------------------------------------

    # Sweep Parameters
    anisotropies = [0.5, 1.0, 5.0, 10.0]
    chi_kappas = [0.0, 2.0, 5.0]
    boundary_conditions = ["fixed", "pinned"]

    # Fixed Constants (Spine Scale)
    length = 0.5          # m
    radius = 0.01         # m
    n_elements = 30       # Optimized for stability/speed
    E0 = 1e6              # Pa
    rho = 1000.0          # kg/m3
    gravity = 9.81        # m/s2

    # Simulation Settings
    final_time = 1.0      # s (Sufficient for initial relaxation/buckling)
    dt = 4e-5             # s (Stable time step)
    save_every = 2000     # Save less frequently to save memory

    # Output Setup
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "parameter_map_results.csv")

    fieldnames = [
        "bc", "anisotropy", "chi_kappa",
        "max_curvature", "max_torsion", "z_tip", "y_tip", "s_lat", "cobb_angle",
        "runtime_sec", "memory_mb"
    ]

    # ---------------------------------------------------------
    # Execution Loop
    # ---------------------------------------------------------

    print(f"Writing results to: {csv_path}")
    print("-" * 80)
    print(f"{'BC':<8} | {'Aniso':<6} | {'Chi_K':<6} | {'MaxCurv':<8} | {'MaxTor':<8} | {'Z_Tip':<8} | {'Time':<6}")
    print("-" * 80)

    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for bc in boundary_conditions:
            for anisotropy in anisotropies:
                for chi_kappa in chi_kappas:

                    # 1. Setup Environment
                    tracemalloc.start()
                    t0 = time.time()

                    # Information Field (Simple Gradient)
                    # Using a dummy field that allows chi_kappa to act if it depends on gradients,
                    # or just setup kappa_gen if chi_kappa is just a multiplier.
                    # Assuming chi_kappa in CounterCurvatureParams couples Info Gradient to Curvature.
                    # Let's create a field with a gradient.
                    s = np.linspace(0, length, n_elements + 1)
                    # Gaussian bump info field
                    I = 0.5 + 0.5 * np.exp(-0.5 * ((s - 0.5 * length) / (0.2 * length))**2)
                    dIds = np.gradient(I, s)
                    info = InfoField1D(s=s, I=I, dIds=dIds)

                    # Params
                    # We treat chi_kappa as the magnitude of the curvature-inducing effect
                    params = CounterCurvatureParams(
                        chi_kappa=chi_kappa, # Induces curvature proportional to gradient
                        chi_E=0.0,
                        chi_M=0.0,
                        scale_length=length
                    )

                    # 2. Build System
                    # We start with a straight rod (kappa_gen=0).
                    # Curvature will emerge from chi_kappa * gradient(I)
                    # OR we can add intrinsic curvature directly via kappa_gen.
                    # For this map, let's assume 'Preferred Curvature' means 'Growth Curvature' driven by chi_kappa.

                    try:
                        system = CounterCurvatureRodSystem.from_iec(
                            info=info,
                            params=params,
                            length=length,
                            n_elements=n_elements,
                            E0=E0,
                            rho=rho,
                            radius=radius,
                            gravity=gravity,
                            stiffness_anisotropy=anisotropy,
                            base_direction=(0.0, 0.0, 1.0) # Vertical
                        )

                        # 3. Run
                        result = system.run_simulation(
                            final_time=final_time,
                            dt=dt,
                            save_every=save_every,
                            gravity=gravity,
                            boundary_condition=bc
                        )

                        # 4. Metrics
                        metrics = result.compute_final_metrics()

                        t1 = time.time()
                        current, peak = tracemalloc.get_traced_memory()
                        tracemalloc.stop()

                        runtime = t1 - t0
                        mem_mb = peak / (1024 * 1024)

                        # 5. Record
                        row = {
                            "bc": bc,
                            "anisotropy": anisotropy,
                            "chi_kappa": chi_kappa,
                            "max_curvature": metrics.get("max_curvature", 0.0),
                            "max_torsion": metrics.get("max_torsion", 0.0),
                            "z_tip": metrics.get("z_tip", 0.0),
                            "y_tip": metrics.get("y_tip", 0.0),
                            "s_lat": metrics.get("S_lat", 0.0),
                            "cobb_angle": metrics.get("cobb_angle", 0.0),
                            "runtime_sec": runtime,
                            "memory_mb": mem_mb
                        }

                        writer.writerow(row)
                        csvfile.flush() # Ensure data is written

                        print(f"{bc:<8} | {anisotropy:<6.1f} | {chi_kappa:<6.1f} | "
                              f"{row['max_curvature']:<8.4f} | {row['max_torsion']:<8.4f} | "
                              f"{row['z_tip']:<8.4f} | {runtime:<6.2f}")

                    except Exception as e:
                        print(f"Error in run ({bc}, {anisotropy}, {chi_kappa}): {e}")
                        tracemalloc.stop()

    print("-" * 80)
    print("Parameter Map Experiment Complete.")

if __name__ == "__main__":
    run_parameter_map()
