
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time
import tracemalloc

from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.scoliosis_metrics import compute_scoliosis_metrics

def run_experiment():
    print("Starting minimal PyElastica rod experiment...")

    # 1. Define Information Field (e.g., sinusoidal modulation)
    L = 1.0
    n_points = 200
    s = np.linspace(0, L, n_points)
    # A simple sinusoidal info field: high information -> stiffer or more curved
    I = np.sin(2 * np.pi * s / L)**2
    dIds = np.gradient(I, s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    # 2. Define Parameters (Protein/ECM-inspired)
    # chi_E: stiffness modulation (e.g., calcification or ECM stiffening)
    # chi_kappa: countercurvature gain (e.g., intrinsic shape programming)
    params = CounterCurvatureParams(
        chi_E=0.5,       # 50% max stiffness increase
        chi_kappa=2.0,   # Significant rest curvature modulation
        chi_M=0.0,
        scale_length=L
    )

    # 3. Setup Simulation
    n_elements = 50
    # Horizontal rod to see gravity sag vs countercurvature
    # gravity acts in -z (vertical). Rod along x.
    # Sagittal plane bending around y.

    # Measure resource usage
    tracemalloc.start()
    start_time = time.time()

    system = CounterCurvatureRodSystem.from_iec(
        info=info,
        params=params,
        length=L,
        n_elements=n_elements,
        E0=1e6,           # Baseline Young's modulus (Pa)
        radius=0.02,      # 2cm radius
        rho=1000,         # Density
        gravity=9.81,
        base_direction=(1.0, 0.0, 0.0), # Horizontal
        normal=(0.0, 1.0, 0.0)
    )

    # 4. Run Simulation
    # Relax to equilibrium
    final_time = 2.0
    dt = 1e-4 # Conservative time step

    print(f"Running simulation for {final_time}s...")
    result = system.run_simulation(final_time=final_time, dt=dt, save_every=100)

    end_time = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Simulation completed in {end_time - start_time:.2f}s")
    print(f"Peak memory usage: {peak_mem / 1024 / 1024:.2f} MB")

    # 5. Analyze Results
    final_curvature = result.curvature[-1]
    final_centerline = result.centerline[-1]

    # Calculate average curvature
    avg_curvature = np.mean(final_curvature)
    print(f"Final average curvature: {avg_curvature:.4f} m^-1")

    # Output simple validation
    # If chi_kappa is positive and dIds has structure, we expect curvature variance
    curvature_std = np.std(final_curvature)
    print(f"Curvature standard deviation: {curvature_std:.4f} m^-1")

    # 6. Compute Scoliosis Metrics
    # The simulation aligns the rod initially along x, with gravity in -z.
    # Sagittal plane bending is in (x, z).
    # Coronal plane deviation is in y.

    # Coordinates from PyElastica: (3, n_nodes)
    # final_centerline[0, :] -> x (longitudinal approx)
    # final_centerline[1, :] -> y (lateral/coronal deviation)
    # final_centerline[2, :] -> z (vertical/sagittal deviation)

    # Debug info
    print(f"Final centerline shape: {final_centerline.shape}")

    x_coords = final_centerline[:, 0]
    y_coords = final_centerline[:, 1]
    z_coords = final_centerline[:, 2]

    print(f"X range: {np.min(x_coords):.4f} to {np.max(x_coords):.4f}")
    print(f"Y range: {np.min(y_coords):.4f} to {np.max(y_coords):.4f}")
    print(f"Z range: {np.min(z_coords):.4f} to {np.max(z_coords):.4f}")

    # Sagittal indices (using x as longitudinal, z as "lateral" in the sagittal plane)
    sagittal_metrics = compute_scoliosis_metrics(z=x_coords, y=z_coords)
    print(f"Sagittal Metrics (S_lat): {sagittal_metrics.S_lat:.4f}")

    # Coronal indices (using x as longitudinal, y as lateral)
    # Should be near zero for this symmetric setup
    coronal_metrics = compute_scoliosis_metrics(z=x_coords, y=y_coords)
    print(f"Coronal Metrics (S_lat): {coronal_metrics.S_lat:.6f}")
    print(f"Coronal Cobb Angle: {coronal_metrics.cobb_like_deg:.6f} deg")

    # Create output directory
    output_dir = Path("outputs/experiments/minimal_rod")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save minimal report
    with open(output_dir / "report.txt", "w") as f:
        f.write("Minimal Rod Experiment Report\n")
        f.write("=============================\n")
        f.write(f"Runtime: {end_time - start_time:.2f}s\n")
        f.write(f"Peak Memory: {peak_mem / 1024 / 1024:.2f} MB\n")
        f.write(f"Avg Curvature: {avg_curvature:.4f}\n")
        f.write(f"Curvature Std: {curvature_std:.4f}\n")
        f.write(f"Sagittal S_lat: {sagittal_metrics.S_lat:.4f}\n")
        f.write(f"Coronal S_lat: {coronal_metrics.S_lat:.6f}\n")
        f.write(f"Coronal Cobb Angle: {coronal_metrics.cobb_like_deg:.6f} deg\n")
        f.write(f"Parameters: {params}\n")

    print(f"Report saved to {output_dir / 'report.txt'}")

if __name__ == "__main__":
    run_experiment()
