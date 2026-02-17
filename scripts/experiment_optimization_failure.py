#!/usr/bin/env python3
"""
Phase 1, Week 3: Exploding Gradient and Sensory Noise.

Maps the "Exploding Gradient" region where high chi_kappa combined with sensory noise
leads to spinal instability (scoliosis).
"""

import sys
import os
import time
import argparse
import numpy as np
import pandas as pd
from datetime import date
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from spinalmodes.countercurvature.pyelastica_bridge import (
    CounterCurvatureRodSystem,
    CounterCurvatureParams,
    InfoField1D,
    compute_U_CC,
    SimulationResult,
    PYELASTICA_AVAILABLE
)
from spinalmodes.countercurvature.scoliosis_metrics import compute_scoliosis_metrics

if not PYELASTICA_AVAILABLE:
    print("Error: PyElastica not installed.")
    sys.exit(1)

def inject_noise(info: InfoField1D, sigma: float, seed: Optional[int] = None) -> InfoField1D:
    """Inject Gaussian noise into the information gradient."""
    if seed is not None:
        np.random.seed(seed)

    noise = np.random.normal(0.0, sigma, size=info.dIds.shape)
    dIds_noisy = info.dIds + noise

    # We do not update I(s) for consistency, assuming the sensor (gradient reader) is noisy,
    # not the underlying morphogen field itself.
    return InfoField1D(s=info.s, I=info.I, dIds=dIds_noisy)

def run_trial(
    chi_kappa: float,
    sigma_noise: float,
    anisotropy: float = 1.5,
    duration: float = 5.0, # Enough to settle
    trial_id: int = 0,
    quick_test: bool = False
) -> Dict[str, float]:
    """Run a single stochastic trial."""

    # 1. Physics Parameters
    n_elements = 50
    L = 0.4 # m
    radius = 0.01 # m
    E0 = 1e7 # Pa
    rho = 1000.0

    if quick_test:
        duration = 1.0
        n_elements = 20 # Coarser for speed

    # 2. Information Field (Baseline)
    s = np.linspace(0, L, n_elements + 1)
    # Gradient drives counter-curvature.
    # Let's assume a simple linear gradient or a bump.
    # A bump ensures dIds has + and - regions.
    info_center = 0.5 * L
    info_width = 0.15 * L
    I = 0.8 * np.exp(-0.5 * ((s - info_center) / info_width)**2)
    dIds = np.gradient(I, s)
    info_base = InfoField1D(s=s, I=I, dIds=dIds)

    # 3. Inject Noise
    # This simulates "Imprecise Mechanosensing"
    info_noisy = inject_noise(info_base, sigma_noise, seed=trial_id)

    # 4. Coupling Parameters
    params = CounterCurvatureParams(
        chi_kappa=chi_kappa,
        chi_E=0.0,
        chi_M=0.0,
        chi_tau=0.0,
        scale_length=L
    )

    # 5. Geometry
    # Start straight but with small lateral imperfection to allow buckling
    kappa_gen = np.zeros((3, n_elements + 1))
    kappa_gen[1, :] = 2.0 # Natural kyphosis
    kappa_gen[0, :] = 0.1 # Small lateral defect (perturbation)

    # 6. Create System
    system = CounterCurvatureRodSystem.from_iec(
        info=info_noisy, # System sees noisy info
        params=params,
        length=L,
        n_elements=n_elements,
        E0=E0,
        radius=radius,
        kappa_gen=kappa_gen,
        gravity=9.81,
        stiffness_anisotropy=anisotropy
    )

    # 7. Run Simulation
    try:
        dt = 2e-4 if not quick_test else 1e-3
        n_steps = int(duration / dt)
        save_every = max(1, n_steps // 10) # Save 10 frames

        result = system.run_simulation(
            final_time=duration,
            dt=dt,
            save_every=save_every,
            progress_bar=False
        )

        # 8. Compute Metrics
        metrics = result.compute_final_metrics()

        # Compute U_CC
        # Use base info for energy calculation? Or noisy?
        # Biologically, the organism *thinks* it is minimizing energy based on noisy info.
        # But we want to know the "true" cost or the "perceived" cost?
        # Usually U_CC is the objective function.
        # Let's compute based on the actual field used (noisy).
        energies = compute_U_CC(result, info_noisy, params, gravity=9.81, E0=E0)

        s_lat = metrics.get("S_lat", 0.0)
        cobb = metrics.get("cobb_angle", 0.0)

        # Failure Definition: S_lat > 2.0 mm? Or Cobb > 10 deg?
        # Clinical scoliosis is Cobb > 10.
        is_unstable = cobb > 10.0

        return {
            "chi_kappa": chi_kappa,
            "sigma_noise": sigma_noise,
            "trial_id": trial_id,
            "S_lat": s_lat,
            "Cobb_angle": cobb,
            "Is_Unstable": float(is_unstable),
            "U_CC": energies["U_CC"],
            "Max_Curvature": metrics.get("max_curvature", 0.0)
        }

    except Exception as e:
        print(f"Simulation failed: {e}")
        return {
            "chi_kappa": chi_kappa,
            "sigma_noise": sigma_noise,
            "trial_id": trial_id,
            "S_lat": np.nan,
            "Cobb_angle": np.nan,
            "Is_Unstable": np.nan,
            "U_CC": np.nan,
            "Max_Curvature": np.nan
        }

def main():
    parser = argparse.ArgumentParser(description="Optimization Failure Experiment")
    parser.add_argument("--quick-test", action="store_true", help="Run short simulation for verification")
    args = parser.parse_args()

    print("Starting Optimization Failure (Exploding Gradient) Experiment...")

    # Parameters
    # Anisotropy fixed low
    ANISOTROPY = 1.5

    # Sweeps
    if args.quick_test:
        chi_values = [5.0, 10.0]
        sigma_values = [0.0, 1.0]
        n_trials = 1
    else:
        chi_values = np.linspace(0, 20, 11) # 0, 2, ..., 20
        sigma_values = np.linspace(0, 5.0, 11) # 0, 0.5, ..., 5.0
        n_trials = 5

    results = []

    total_runs = len(chi_values) * len(sigma_values) * n_trials
    count = 0
    start_time = time.time()

    for chi in chi_values:
        for sigma in sigma_values:
            for i in range(n_trials):
                count += 1
                if count % 10 == 0:
                    elapsed = time.time() - start_time
                    print(f"Progress: {count}/{total_runs} ({count/total_runs*100:.1f}%) - Elapsed: {elapsed:.1f}s")

                res = run_trial(
                    chi_kappa=chi,
                    sigma_noise=sigma,
                    anisotropy=ANISOTROPY,
                    trial_id=i,
                    quick_test=args.quick_test
                )
                results.append(res)

    df = pd.DataFrame(results)

    # Save Outputs
    today = date.today().isoformat()
    output_dir = f"outputs/sim/{today}"
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, "optimization_failure.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV to {csv_path}")

    # Aggregation
    agg = df.groupby(["chi_kappa", "sigma_noise"]).agg({
        "Cobb_angle": ["mean", "std"],
        "Is_Unstable": "mean" # Probability of failure
    }).reset_index()

    # Flatten columns
    agg.columns = ["chi_kappa", "sigma_noise", "Cobb_mean", "Cobb_std", "Failure_Prob"]

    # Generate Report
    report_path = os.path.join(output_dir, "optimization_failure_report.md")

    try:
        import tabulate
        table = agg.to_markdown(index=False)
    except ImportError:
        table = agg.to_string(index=False)

    with open(report_path, "w") as f:
        f.write(f"# Optimization Failure: Exploding Gradient Report\n")
        f.write(f"Date: {today}\n\n")
        f.write("## Hypothesis\n")
        f.write("In the 'Exploding Gradient' regime, high coupling strength (chi_kappa) amplifies sensory noise (sigma), "
                "leading to stochastic failure of spinal alignment (scoliosis).\n\n")
        f.write("## Phase Diagram Data (Aggregated)\n")
        f.write(table)
        f.write("\n\n## Analysis\n")
        f.write("The 'Failure_Prob' column indicates the likelihood of Cobb angle > 10 degrees. "
                "We expect a transition boundary where failure probability jumps from 0 to 1 as chi_kappa * sigma_noise increases.\n")

    print(f"Saved Report to {report_path}")

if __name__ == "__main__":
    main()
