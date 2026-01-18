"""
Minimal reproducible experiment for PyElastica rod simulation.

This script maps protein/ECM-inspired parameters (stiffness anisotropy, boundary conditions)
to emergent curvature/torsion outputs using a vertical rod model (spine-like).

Biological Context:
- Stiffness Anisotropy: Maps to protein clusters.
    - Low Anisotropy (~1.0): "Signaling Blocks" (Cluster 1, e.g., YAP1) - Isotropic stiffness.
    - High Anisotropy (>5.0): "Tension Rods" (Cluster 0, e.g., POC5) - Highly directional stiffness.
- Boundary Conditions:
    - Fixed: Sacrum fully constrained (clamped).
    - Pinned: Sacrum allows rotation (moment-free), testing stability without base moment support.

It runs a parameter sweep and prints a metrics table.
"""

import sys
import numpy as np
import tracemalloc
import time

try:
    import elastica as ea
except ImportError:
    print("PyElastica is not installed.")
    print("To install, run:")
    print("  pip install pyelastica")
    print("Or refer to https://github.com/GazzolaLab/PyElastica")
    sys.exit(0)

from spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.coupling import CounterCurvatureParams

def run_experiment():
    print("Running minimal PyElastica experiment...")
    print("Goal: Map stiffness anisotropy & BCs to emergent curvature/torsion.")

    # Experiment parameters
    # High anisotropy = Cluster 0 (Tension Rods), Low = Cluster 1 (Signaling Blocks)
    anisotropies = [1.0, 10.0]
    boundary_conditions = ["fixed", "pinned"]

    # Rod parameters (approximate spine scale)
    length = 0.5  # meters
    radius = 0.01 # meters
    n_elements = 30 # Reduced for speed
    E0 = 1e6      # Pa (soft tissue/cartilage range)
    rho = 1000.0  # kg/m^3
    gravity = 9.81

    # Time parameters
    final_time = 1.0 # Reduced for speed
    dt = 4e-5 # Larger step, checked for stability with n=30

    print("-" * 130)
    print(f"{'Context':<25} | {'BC':<6} | {'Aniso':<6} | {'Max Curv':<10} | {'Max Tor':<10} | {'S_lat':<8} | {'Cobb':<6} | {'Time (s)':<8} | {'Mem (MB)':<8}")
    print("-" * 130)

    for bc in boundary_conditions:
        for anisotropy in anisotropies:
            # Determine biological label
            if anisotropy < 2.0:
                label = "Cluster 1 (Blocks)"
            else:
                label = "Cluster 0 (Rods)"

            # Start tracking memory
            tracemalloc.start()
            t0 = time.time()

            # 1. Setup Information Field
            s = np.linspace(0, length, n_elements + 1)
            # Gaussian bump info field representing localized signaling
            I = 0.5 + 0.1 * np.exp(-0.5 * ((s - 0.6*length)/(0.1*length))**2)
            dIds = np.gradient(I, s)
            info = InfoField1D(s=s, I=I, dIds=dIds)

            # 2. Setup Coupling Parameters
            params = CounterCurvatureParams(
                chi_kappa=5.0, # Growth gain
                chi_E=0.0,
                chi_M=0.0,
                scale_length=length
            )

            # 3. Setup Geometric Curvature (kappa_gen)
            # Constant curvature about d1 to induce bending in Y-Z plane.
            kappa_gen = np.zeros((3, n_elements + 1))
            kappa_gen[0, :] = 2.0 # 1/m initial rest curvature preference

            # 4. Create Rod System
            rod_system = CounterCurvatureRodSystem.from_iec(
                info=info,
                params=params,
                length=length,
                n_elements=n_elements,
                E0=E0,
                rho=rho,
                radius=radius,
                kappa_gen=kappa_gen,
                gravity=gravity,
                base_position=(0.0, 0.0, 0.0),
                base_direction=(0.0, 0.0, 1.0), # Vertical
                normal=(1.0, 0.0, 0.0),         # Normal in X
                stiffness_anisotropy=anisotropy
            )

            # 5. Run Simulation
            result = rod_system.run_simulation(
                final_time=final_time,
                dt=dt,
                save_every=2000,
                gravity=gravity,
                boundary_condition=bc
            )

            t1 = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            runtime = t1 - t0
            peak_mb = peak / (1024 * 1024)

            # 6. Compute Metrics
            metrics = result.compute_final_metrics()

            max_torsion = metrics.get('max_torsion', 0.0)
            max_curvature = metrics.get('max_curvature', 0.0)
            s_lat = metrics.get('S_lat', 0.0)
            cobb = metrics.get('cobb_angle', 0.0)

            print(f"{label:<25} | {bc:<6} | {anisotropy:<6.1f} | {max_curvature:<10.4f} | {max_torsion:<10.4f} | {s_lat:<8.4f} | {cobb:<6.2f} | {runtime:<8.2f} | {peak_mb:<8.2f}")

    print("-" * 130)
    print("Experiment complete.")

if __name__ == "__main__":
    run_experiment()
