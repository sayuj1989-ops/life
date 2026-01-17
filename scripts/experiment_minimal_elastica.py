"""
Minimal reproducible experiment for PyElastica rod simulation.

This script maps protein/ECM-inspired parameters (stiffness anisotropy)
to emergent curvature/torsion outputs using a vertical rod model (spine-like).

It runs a parameter sweep over stiffness anisotropy and prints a metrics table.
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
    print("Goal: Map stiffness anisotropy to emergent curvature/torsion.")

    # Experiment parameters
    anisotropies = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]

    # Rod parameters (approximate spine scale)
    length = 0.5  # meters
    radius = 0.01 # meters
    n_elements = 50
    E0 = 1e6      # Pa (soft tissue/cartilage range)
    rho = 1000.0  # kg/m^3
    gravity = 9.81

    # Time parameters
    final_time = 2.0
    dt = 1e-5 # Stable time step

    # Results storage
    results_table = []

    print("-" * 110)
    print(f"{'Anisotropy':<12} | {'Max Curv':<10} | {'Max Torsion':<12} | {'Y Tip (m)':<10} | {'S_lat':<8} | {'Cobb (deg)':<10} | {'Time (s)':<10} | {'Mem (MB)':<10}")
    print("-" * 110)

    for anisotropy in anisotropies:
        # Start tracking memory
        tracemalloc.start()
        t0 = time.time()

        # 1. Setup Information Field
        s = np.linspace(0, length, n_elements + 1)
        I = 0.5 + 0.1 * np.exp(-0.5 * ((s - 0.6*length)/(0.1*length))**2)
        dIds = np.gradient(I, s)
        info = InfoField1D(s=s, I=I, dIds=dIds)

        # 2. Setup Coupling Parameters
        params = CounterCurvatureParams(
            chi_kappa=5.0,
            chi_E=0.0,
            chi_M=0.0,
            scale_length=length
        )

        # 3. Setup Geometric Curvature (kappa_gen)
        # Constant curvature about d1 to induce bending in Y-Z plane.
        # Stiffness Anisotropy scales stiffness about d1.
        kappa_gen = np.zeros((3, n_elements + 1))
        kappa_gen[0, :] = 2.0 # 1/m

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
            save_every=5000,
            gravity=gravity,
            boundary_condition="fixed"
        )

        t1 = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        runtime = t1 - t0
        peak_mb = peak / (1024 * 1024)

        # 6. Compute Metrics
        metrics = result.compute_final_metrics()

        # 7. Store and Print
        res_row = {
            "anisotropy": anisotropy,
            "metrics": metrics,
            "runtime": runtime,
            "peak_memory_mb": peak_mb
        }
        results_table.append(res_row)

        y_tip = metrics.get('y_tip', 0.0)
        max_torsion = metrics.get('max_torsion', 0.0)
        max_curvature = metrics.get('max_curvature', 0.0)
        s_lat = metrics.get('S_lat', 0.0)
        cobb = metrics.get('cobb_angle', 0.0)

        print(f"{anisotropy:<12.2f} | {max_curvature:<10.4f} | {max_torsion:<12.4f} | {y_tip:<10.4f} | {s_lat:<8.4f} | {cobb:<10.4f} | {runtime:<10.4f} | {peak_mb:<10.2f}")

    print("-" * 110)
    print("Experiment complete.")

if __name__ == "__main__":
    run_experiment()
