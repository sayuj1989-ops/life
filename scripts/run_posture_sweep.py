
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time
import datetime
import tracemalloc
import csv
import sys
from typing import List, Dict, Any

# Ensure project root is in path
sys.path.append(".")

from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams

def generate_sine_field(s: np.ndarray, L: float) -> InfoField1D:
    # I(s) = sin(2*pi*s/L) -> Gradient creates alternating curvature
    # This creates a "Natural S-shape" rest state
    I = np.sin(2 * np.pi * s / L)
    dIds = np.gradient(I, s)
    return InfoField1D(s=s, I=I, dIds=dIds)

def run_experiment():
    print("Starting Posture Stability Sweep (Load Vector Tilt)...")

    # 1. Setup
    L = 1.0
    n_points = 200
    s = np.linspace(0, L, n_points)
    info = generate_sine_field(s, L)

    # Simulation Params
    n_elements = 50
    final_time = 3.0
    dt = 5e-5

    # Output Setup
    today = datetime.date.today()
    output_dir = Path(f"outputs/sim/{today}")
    output_dir.mkdir(parents=True, exist_ok=True)

    results_summary: List[Dict[str, Any]] = []

    tracemalloc.start()
    start_time_total = time.time()

    # --- Sweep: Tilt Angle (Posture) ---
    # 0 deg = Vertical (Upright). 90 deg = Horizontal (Prone).
    tilt_angles = [0, 15, 30, 45, 60, 75, 90]

    # Fixed parameters: purely growth-driven S-shape
    chi_kappa_fixed = 10.0
    chi_M_fixed = 0.0
    chi_E_fixed = 0.0

    print(f"Fixed chi_kappa: {chi_kappa_fixed}")
    print(f"Sweeping Tilt Angle: {tilt_angles} degrees")

    for angle_deg in tilt_angles:
        angle_rad = np.radians(angle_deg)
        # Rotate base direction in X-Z plane
        # Z is up. Rotate towards X.
        # dir = (sin(theta), 0, cos(theta))
        base_dir = (np.sin(angle_rad), 0.0, np.cos(angle_rad))

        params = CounterCurvatureParams(
            chi_E=chi_E_fixed,
            chi_kappa=chi_kappa_fixed,
            chi_M=chi_M_fixed,
            chi_tau=0.0,
            scale_length=L
        )

        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=L,
            n_elements=n_elements,
            E0=1e6,
            radius=0.02,
            rho=1000,
            gravity=9.81,
            base_direction=base_dir,
            normal=(0.0, 1.0, 0.0) # Y is out of plane
        )

        result = system.run_simulation(final_time=final_time, dt=dt, save_every=100)

        # Metrics
        final_centerline = result.centerline[-1] # (n_nodes, 3)

        # We need to project the shape into the "body frame" to see deformation relative to the spine axis
        # Base is at (0,0,0). Ideal spine axis is along base_dir.
        # Compute "Sag" as deviation from the straight line defined by base_dir.

        # Vector from base to each point
        P = final_centerline

        # Director (Unit vector)
        u = np.array(base_dir)

        # Projection of P onto u: (P . u) * u
        # Rejection (Deviation): P - (P . u) * u
        # We want the norm of the rejection vector for the tip, or max deviation.

        tip_pos = P[-1]
        tip_along_axis = np.dot(tip_pos, u)
        tip_deviation_vec = tip_pos - tip_along_axis * u
        tip_sag = np.linalg.norm(tip_deviation_vec)

        # Also measure geometric S-shape magnitude in the "bending plane" (Plane of curvature)
        # Since we use chi_kappa coupled to index 1 (Normal curvature), bending is in the plane normal to 'normal' (Y).
        # So bending is in X-Z plane (global).
        # But we rotated the spine in X-Z plane.

        # Let's just track Tip Sag (compliance to gravity) vs Angle.

        results_summary.append({
            "tilt_angle_deg": angle_deg,
            "tip_sag": tip_sag,
            "tip_axial_shortening": L - tip_along_axis
        })
        print(f"Angle={angle_deg:2d} deg: Tip Sag={tip_sag:.4f} m, Shortening={L - tip_along_axis:.4f} m")

    end_time_total = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nTotal Runtime: {end_time_total - start_time_total:.2f}s")

    # Save params
    with open(output_dir / "params.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["param", "value"])
        writer.writerow(["date", str(today)])
        writer.writerow(["n_elements", n_elements])
        writer.writerow(["final_time", final_time])
        writer.writerow(["dt", dt])
        writer.writerow(["chi_kappa_fixed", chi_kappa_fixed])
        writer.writerow(["swept_param", "tilt_angle"])
        writer.writerow(["values", str(tilt_angles)])

    # Save results
    results_path = output_dir / "results.csv"
    with open(results_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["tilt_angle_deg", "tip_sag", "tip_axial_shortening"])
        writer.writeheader()
        writer.writerows(results_summary)
    print(f"Results saved to {results_path}")

    # Plot
    plt.figure(figsize=(10, 6))

    angles = [r["tilt_angle_deg"] for r in results_summary]
    sags = [r["tip_sag"] for r in results_summary]
    shorts = [r["tip_axial_shortening"] for r in results_summary]

    plt.plot(angles, sags, 'o-', linewidth=2, label="Tip Sag (Deviation from Axis)")
    plt.plot(angles, shorts, 's--', linewidth=2, label="Axial Shortening")

    plt.xlabel("Posture Tilt Angle (deg) [0=Vertical, 90=Horizontal]")
    plt.ylabel("Deformation (m)")
    plt.title(f"Spinal Stability vs Posture (Growth-Driven S-shape, $\chi_\kappa={chi_kappa_fixed}$)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.savefig(output_dir / "plot_posture_sweep.png")
    print(f"Plot saved to {output_dir / 'plot_posture_sweep.png'}")

    # Write Report
    with open(output_dir / "report.md", "w") as f:
        f.write(f"# Simulation Report: Posture Stability Sweep ({today})\n\n")
        f.write("## Hypothesis\n")
        f.write("A purely growth-driven S-shape (fixed `chi_kappa`) without active muscle compensation (`chi_M=0`) "
                "will exhibit non-linear instability as the load vector rotates from axial (vertical) to transverse (horizontal).\n\n")

        f.write("## Setup\n")
        f.write(f"- Fixed `chi_kappa = {chi_kappa_fixed}` (Natural S-shape)\n")
        f.write(f"- Swept `Tilt Angle` from 0 to 90 degrees\n")
        f.write("- Information Field: Sine Wave (Periodic)\n")
        f.write("- Gravity: 9.81 m/s²\n\n")

        f.write("## Results\n")
        f.write("| Angle (deg) | Tip Sag (m) | Axial Shortening (m) |\n")
        f.write("|-------------|-------------|----------------------|\n")
        for r in results_summary:
            f.write(f"| {r['tilt_angle_deg']} | {r['tip_sag']:.4f} | {r['tip_axial_shortening']:.4f} |\n")

        f.write("\n## Observations\n")
        f.write(f"Measured deformation as the spine rotated from vertical to horizontal. Peak sag occurred at {angles[np.argmax(sags)]} degrees.\n")

if __name__ == "__main__":
    run_experiment()
