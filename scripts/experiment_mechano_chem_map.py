import os
import sys
import time
import datetime
import tracemalloc
import numpy as np
import pandas as pd
from pathlib import Path
import logging

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem, SimulationResult
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.coupling import CounterCurvatureParams

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_simulation_step(
    chi_kappa: float,
    anisotropy: float,
    boundary_condition: str,
    base_length: float = 1.0,
    n_elements: int = 40,
    final_time: float = 5.0, # Reduced for speed in sweep
    dt: float = 1e-4,
) -> dict:
    """
    Run a single simulation with performance tracking.

    Parameters:
    - chi_kappa: Strength of preferred curvature (Growth/Protein proxy).
    - anisotropy: Stiffness anisotropy ratio (ECM proxy).
    - boundary_condition: 'fixed' or 'pinned'.

    Returns:
    - Dictionary of metrics including runtime and memory.
    """

    # Start tracking
    start_time = time.time()
    tracemalloc.start()

    metrics = {}

    try:
        # Create info field (linear growth gradient)
        # I(s) = s / L (linear increase from 0 to 1)
        s = np.linspace(0, base_length, n_elements + 1)
        I = s / base_length
        info = InfoField1D.from_array(s, I)

        # Params
        params = CounterCurvatureParams(
            chi_kappa=chi_kappa,
            chi_E=0.0,
            chi_M=0.0,
            chi_tau=0.0,
            scale_length=1.0
        )

        # Create System
        # Standard gravity alignment (vertical Z-axis)
        base_direction = (0.0, 0.0, 1.0)
        normal = (0.0, 1.0, 0.0)

        # Create the rod system using the factory bridge
        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=base_length,
            n_elements=n_elements,
            radius=0.02,
            E0=1e6,
            rho=1000.0,
            base_direction=base_direction,
            normal=normal,
            stiffness_anisotropy=anisotropy,
        )

        # Run Simulation
        res = system.run_simulation(
            final_time=final_time,
            dt=dt,
            save_every=int(final_time/dt/50),
            boundary_condition=boundary_condition
        )

        metrics = res.compute_final_metrics()

    except Exception as e:
        logger.error(f"Simulation failed for parameters (ck={chi_kappa}, aniso={anisotropy}, bc={boundary_condition}): {e}")
        metrics = {"error": str(e)}
        # Ensure we have minimal fields to prevent DataFrame collapse
        metrics.update({"S_lat": 0.0, "max_torsion": 0.0, "max_curvature": 0.0})

    finally:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time.time()

    # Add Performance Metrics
    metrics['runtime_sec'] = end_time - start_time
    metrics['peak_memory_mb'] = peak / 1024 / 1024

    # Add Inputs
    metrics['chi_kappa'] = chi_kappa
    metrics['anisotropy'] = anisotropy
    metrics['boundary_condition'] = boundary_condition

    return metrics

def main():
    seed = 2026
    np.random.seed(seed)

    today = datetime.date.today().isoformat()
    output_dir = Path(f"outputs/sim/{today}/mechano_chem_map")
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Starting Mechano-Chemical Parameter Map -> {output_dir}")
    logger.info("Mapping: Stiffness (ECM) x Preferred Curvature (Growth) -> Emergent Shape")

    # Sweep Parameters
    # Anisotropy: 0.1 (Highly Anisotropic, soft lateral) to 1.0 (Isotropic)
    # Reduced set for quick demonstration/verification
    anisotropies = [0.1, 0.5, 1.0]

    # Chi Kappa: 0 (Passive) to 15 (Active Growth)
    chi_kappas = [0.0, 5.0, 10.0, 15.0]

    boundary_conditions = ["fixed", "pinned"]

    results = []

    total_runs = len(anisotropies) * len(chi_kappas) * len(boundary_conditions)
    current_run = 0

    logger.info(f"Total runs scheduled: {total_runs}")

    for bc in boundary_conditions:
        for aniso in anisotropies:
            for ck in chi_kappas:
                current_run += 1
                logger.info(f"Run {current_run}/{total_runs}: BC={bc}, Aniso={aniso}, Chi_K={ck}")

                metrics = run_simulation_step(
                    chi_kappa=ck,
                    anisotropy=aniso,
                    boundary_condition=bc
                )
                results.append(metrics)

    # Save Results
    df = pd.DataFrame(results)
    csv_path = output_dir / "results.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"Saved results to {csv_path}")

    # Generate Summary Report
    report_path = output_dir / "report.md"
    with open(report_path, "w") as f:
        f.write(f"# Mechano-Chemical Map Report - {today}\n\n")
        f.write("## Objective\n")
        f.write("Map protein/ECM-inspired parameters to emergent spinal curvature metrics, measuring computational cost.\n\n")
        f.write("## Parameters\n")
        f.write(f"- Stiffness Anisotropy (ECM): {anisotropies}\n")
        f.write(f"- Preferred Curvature (Growth): {chi_kappas}\n")
        f.write(f"- Boundary Conditions: {boundary_conditions}\n\n")

        f.write("## Performance Summary\n")
        if not df.empty and 'runtime_sec' in df.columns:
            avg_runtime = df['runtime_sec'].mean()
            max_mem = df['peak_memory_mb'].max()
            f.write(f"- Avg Runtime: {avg_runtime:.2f} sec/run\n")
            f.write(f"- Max Peak Memory: {max_mem:.2f} MB\n\n")
        else:
            f.write("No performance data available.\n\n")

        f.write("## Scientific Insights\n")
        if not df.empty and 'S_lat' in df.columns:
            # High Scoliosis Cases
            # S_lat is dimensionless lateral deviation. > 0.05 is significant.
            high_scol = df[df['S_lat'] > 0.05]
            if not high_scol.empty:
                f.write("### Emergent Scoliosis (S_lat > 0.05)\n")
                f.write("Significant lateral deviation observed in the following cases:\n\n")
                f.write(high_scol[['boundary_condition', 'anisotropy', 'chi_kappa', 'S_lat', 'max_torsion']].to_markdown(index=False))
                f.write("\n\n")
            else:
                f.write("No significant scoliosis (S_lat > 0.05) observed in this regime.\n")

            # Torsion analysis
            if 'max_torsion' in df.columns:
                 max_t = df['max_torsion'].max()
                 f.write(f"\n### Max Torsion Observed: {max_t:.4f} rad/m\n")
        else:
            f.write("No metric data available.\n")

    logger.info(f"Report written to {report_path}")

if __name__ == "__main__":
    main()
