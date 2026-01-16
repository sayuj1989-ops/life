"""
Reproducible Protein Rod Comparison Experiment.

This script executes a minimal comparative simulation between two rod configurations
representing distinct protein/ECM states defined by the AlphaFold CounterCurvature (AFCC) analysis:

1. Wild Type (Cluster 0 - 'Anisotropic Cilio-Nuclear Tethers'):
   - High Stiffness Anisotropy (2.0)
   - Represents healthy, aligned cytoskeletal/ECM networks capable of resisting gravity.

2. Mutant (Cluster 2 - 'Isotropic'):
   - Low/Unity Stiffness Anisotropy (1.0)
   - Represents disordered networks (e.g. scoliosis candidates) prone to gravity-driven buckling.

Metrics:
- Runtime & Memory Usage (measured via tracemalloc/time)
- Emergent Curvature & Torsion
- Lateral Instability
"""

import sys
import time
import tracemalloc
import numpy as np
import csv
from pathlib import Path

# Ensure repo root is in path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.spinalmodes.countercurvature.pyelastica_bridge import (
    CounterCurvatureRodSystem,
    ProteinRodConfig,
    CounterCurvatureParams,
    InfoField1D,
    PYELASTICA_AVAILABLE,
)

def run_comparison():
    if not PYELASTICA_AVAILABLE:
        print("PyElastica is not installed. To install:")
        print("pip install pyelastica")
        print("Or see: https://github.com/GazzolaLab/PyElastica")
        sys.exit(0)

    # Setup Output
    output_dir = Path("outputs/sim/protein_rod_comparison")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting Protein Rod Comparison in {output_dir}...")

    # 1. Define Configurations
    configs = [
        ProteinRodConfig(
            name="Wild_Type_Cluster0",
            stiffness_anisotropy=2.0,
            cluster_id=0,
            description="High anisotropy, healthy tethering."
        ),
        ProteinRodConfig(
            name="Mutant_Cluster2",
            stiffness_anisotropy=1.0,
            cluster_id=2,
            description="Isotropic, potential failure mode."
        )
    ]

    # Shared Physical Parameters
    L = 1.0
    n_elements = 50
    E0 = 1e6
    radius = 0.02
    rho = 1000.0
    gravity = 9.81

    # Information Field (Constant growth gradient, simulating intrinsic curvature drive)
    s = np.linspace(0, L, n_elements + 1)
    # Simple linear gradient
    info = InfoField1D(
        s=s,
        I=s/L,
        dIds=np.ones_like(s)/L
    )

    # Coupling Parameters
    # Strong curvature drive, strong torsion coupling to induce lateral instability
    params = CounterCurvatureParams(
        chi_kappa=20.0,
        chi_tau=5.0,
        scale_length=L
    )

    results = []

    # 2. Run Simulations
    for config in configs:
        print(f"\nRunning Simulation: {config.name}")
        print(f"  > Anisotropy: {config.stiffness_anisotropy}")

        # Start Measurement
        tracemalloc.start()
        start_time = time.time()

        # Initialize System
        system = CounterCurvatureRodSystem.from_protein_config(
            config=config,
            info=info,
            params=params,
            length=L,
            n_elements=n_elements,
            E0=E0,
            radius=radius,
            rho=rho,
            gravity=gravity,
        )

        # Run
        sim_res = system.run_simulation(
            final_time=1.0,
            dt=1e-4,
            gravity=gravity
        )

        # End Measurement
        duration = time.time() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # 3. Compute Metrics
        # Centerline shape: (time, n_nodes, 3) due to transpose in bridge
        # Axis 2, Index 0: X (Sagittal/Primary Bending Plane due to kappa_y)
        # Axis 2, Index 1: Y (Lateral/Coupled Bending Plane due to torsion)
        # Axis 2, Index 2: Z (Axial/Vertical)

        max_curvature = np.max(sim_res.curvature)
        max_torsion = np.max(np.abs(sim_res.torsion))

        max_sagittal_dev = np.max(np.abs(sim_res.centerline[:, :, 0])) # X-axis
        max_lateral_dev = np.max(np.abs(sim_res.centerline[:, :, 1]))  # Y-axis
        max_vertical_disp = np.max(np.abs(sim_res.centerline[:, :, 2] - np.linspace(0, L, n_elements+1)))

        print(f"  > Duration: {duration:.4f}s")
        print(f"  > Peak Memory: {peak / 1024 / 1024:.2f} MB")
        print(f"  > Max Curvature: {max_curvature:.4f}")
        print(f"  > Max Sagittal Deviation (X): {max_sagittal_dev:.4f} m")
        print(f"  > Max Lateral Deviation (Y):  {max_lateral_dev:.4f} m")

        results.append({
            "name": config.name,
            "anisotropy": config.stiffness_anisotropy,
            "cluster": config.cluster_id,
            "runtime_sec": duration,
            "peak_memory_mb": peak / 1024 / 1024,
            "max_curvature": max_curvature,
            "max_torsion": max_torsion,
            "max_sagittal_dev": max_sagittal_dev,
            "max_lateral_dev": max_lateral_dev,
            "max_vertical_disp": max_vertical_disp
        })

    # 4. Save Results
    csv_path = output_dir / "results.csv"
    keys = results[0].keys()
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

    # Generate Summary Report
    report_path = output_dir / "summary_report.txt"
    with open(report_path, "w") as f:
        f.write("Protein Rod Comparison Experiment Report\n")
        f.write("========================================\n\n")
        for res in results:
            f.write(f"Configuration: {res['name']}\n")
            f.write(f"  - Anisotropy: {res['anisotropy']}\n")
            f.write(f"  - Max Sagittal Deviation (X): {res['max_sagittal_dev']:.4f} m\n")
            f.write(f"  - Max Lateral Instability (Y): {res['max_lateral_dev']:.4f} m\n")
            f.write(f"  - Runtime: {res['runtime_sec']:.4f} s\n")
            f.write(f"  - Memory: {res['peak_memory_mb']:.2f} MB\n")
            f.write("\n")

    print(f"\nExperiment Complete. Results saved to {output_dir}")

if __name__ == "__main__":
    run_comparison()
