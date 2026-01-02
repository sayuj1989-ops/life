import numpy as np
import time
import tracemalloc
import sys
from spinalmodes.countercurvature.pyelastica_bridge import (
    CounterCurvatureRodSystem,
    CounterCurvatureParams,
    PYELASTICA_AVAILABLE
)
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.scoliosis_metrics import compute_scoliosis_metrics, ScoliosisMetrics

def run_experiment(output_file=None):
    """
    Run a minimal countercurvature experiment mapping protein-inspired parameters
    to emergent rod geometry using PyElastica.

    This experiment demonstrates:
    1. Mapping 'InfoField' (surrogate for developmental morphogen gradient) to
       mechanical parameters (stiffness, rest curvature).
    2. Simulating the rod under gravity and internal active moments.
    3. Extracting geometry metrics (curvature, torsion, lateral deviation).
    4. Measuring computational cost (runtime, memory).
    """
    if not PYELASTICA_AVAILABLE:
        print("PyElastica not available, skipping.")
        return

    # 1. Setup Parameters representing Protein/ECM Properties
    # -----------------------------------------------------
    # Protein/ECM properties are often spatially graded.
    # Here we map a sinusoidal 'information field' (e.g. HOX gene expression)
    # to stiffness and preferred curvature.
    n_elements = 50
    length = 1.0 # meters

    # Grid for the rod (nodes)
    s = np.linspace(0, length, n_elements + 1)

    # Information Field I(s): Surrogate for a morphogen gradient.
    # A simple sine wave mimics periodic somite-like patterning.
    info_vals = 0.5 + 0.5 * np.sin(2 * np.pi * s / length)
    dIds = np.gradient(info_vals, s) # Gradient drives curvature changes
    info = InfoField1D(s=s, I=info_vals, dIds=dIds)

    # Coupling parameters (connecting biology to mechanics)
    params = CounterCurvatureParams(
        chi_E=0.5,       # Stiffness modulation strength (alpha_s)
        chi_kappa=0.2,   # Curvature modulation strength (beta_c)
        chi_M=0.0        # Active moment strength (gamma_m)
    )

    print("=== Minimal Countercurvature Rod Experiment ===")
    print(f"Rod Length: {length} m, Elements: {n_elements}")
    print(f"Info Field: Sinusoidal pattern (freq=1/L)")
    print(f"Coupling: chi_E={params.chi_E}, chi_kappa={params.chi_kappa}")

    # 2. Initialize System & Measure Memory
    # -------------------------------------
    tracemalloc.start()

    print("\nInitializing system...")
    start_time = time.time()

    # Horizontal initialization to observe gravity sag vs countercurvature
    system = CounterCurvatureRodSystem.from_iec(
        info=info,
        params=params,
        length=length,
        n_elements=n_elements,
        E0=1e6,  # Young's Modulus (Pa)
        rho=1000.0, # Density (kg/m^3)
        radius=0.01, # Radius (m)
        base_direction=(1.0, 0.0, 0.0), # Horizontal alignment
        gravity=9.81
    )
    init_time = time.time() - start_time
    print(f"Initialization took {init_time:.4f}s")

    # 3. Run Simulation
    # -----------------
    print("Running simulation...")
    sim_start = time.time()

    # Timestep must satisfy Courant condition (dt < dl/c)
    # roughly dt ~ 1e-5 for these stiffness/density parameters
    final_time = 2.0
    dt = 1e-5
    res = system.run_simulation(final_time=final_time, dt=dt, save_every=200)

    sim_time = time.time() - sim_start
    print(f"Simulation took {sim_time:.4f}s")

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")

    # 4. Analyze Results
    # ------------------
    # Extract final state
    final_centerline = res.centerline[-1] # Shape (3, n_nodes)
    final_kappa = res.kappa[-1]           # Shape (3, n_nodes) [Padded]

    # Metrics
    # Curvature (magnitude of kappa vector)
    curvature = np.linalg.norm(final_kappa, axis=0)
    max_curvature = np.max(curvature)

    # Torsion (twist about the tangent vector, kappa[2] in material frame)
    # Note: PyElastica material frame d3 is tangent.
    torsion = final_kappa[2, :]
    max_torsion = np.max(np.abs(torsion))

    # Scoliosis-like metrics (using projections)
    # x is longitudinal (initial), z is vertical (gravity), y is lateral.
    # We map (z_coord, y_coord) -> (x_rod, y_rod) for the metrics function
    # The metrics assume z is longitudinal. So we pass x as longitudinal.
    x_coords = final_centerline[0, :]
    y_coords = final_centerline[1, :]
    z_coords = final_centerline[2, :] # Vertical sag

    scoliosis = compute_scoliosis_metrics(z=x_coords, y=y_coords)

    output = []
    output.append("\n=== Results ===")
    output.append(f"Final Tip Position (x, y, z): ({x_coords[-1]:.4f}, {y_coords[-1]:.4f}, {z_coords[-1]:.4f})")
    output.append(f"Max Curvature: {max_curvature:.4f} m^-1")
    output.append(f"Max Torsion: {max_torsion:.4f} m^-1")
    output.append(f"Vertical Sag (Tip Z): {z_coords[-1]:.4f} m")

    output.append("\n--- Scoliosis Metrics (Lateral Deviation) ---")
    output.append(f"S_lat (Dimensionless index): {scoliosis.S_lat:.4e}")
    output.append(f"Max Lateral Deviation: {scoliosis.lat_dev_max:.4e} m")
    output.append(f"Cobb-like Angle: {scoliosis.cobb_like_deg:.4f} degrees")

    # Biological Interpretation
    output.append("\n=== Biological Interpretation ===")
    if abs(z_coords[-1]) < 0.1: # Threshold depends on gravity/stiffness
        output.append("Result: Effective countercurvature. The rod resisted gravity sag significantly.")
    else:
        output.append("Result: Gravity dominated. The rod sagged significantly.")

    if scoliosis.S_lat > 0.05:
        output.append("Result: Significant lateral asymmetry detected (Scoliosis-like).")
    else:
        output.append("Result: No significant lateral asymmetry.")

    output_str = "\n".join(output)
    print(output_str)

    if output_file:
        with open(output_file, "w") as f:
            f.write(output_str)

if __name__ == "__main__":
    run_experiment()
