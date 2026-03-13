import os
import sys
import time
import tracemalloc
from datetime import datetime
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import from spinalmodes
try:
    from spinalmodes.countercurvature.pyelastica_bridge import (
        PYELASTICA_AVAILABLE,
        CounterCurvatureRodSystem,
        CounterCurvatureParams,
        InfoField1D,
        compute_U_CC
    )
except ImportError as e:
    print(f"Error importing simulation module: {e}")
    sys.exit(1)

def run_tilt_sweep():
    if not PYELASTICA_AVAILABLE:
        print("PyElastica not available. Exiting.")
        sys.exit(1)

    # Reproducibility
    seed = 42
    np.random.seed(seed)

    # Setup parameters
    tilt_values = np.linspace(0.0, 30.0, 20)  # Sweep tilt from 0 to 30 degrees
    anisotropy = 3.0 # Moderate anisotropy
    active_curvature = 10.0 # High growth drive
    natural_kyphosis = 2.0
    duration = 2.0
    dt = 1e-4
    n_elements = 50
    length = 1.0
    radius = 0.01
    E0 = 1e6
    rho = 1000.0

    scale_factor_kappa = 5.0
    chi_kappa = active_curvature * scale_factor_kappa

    results = []

    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(f"outputs/sim/{date_str}_tilt_sweep")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting Load Vector Tilt Sweep (N={len(tilt_values)})...")
    print(f"Tilt Range: [{tilt_values[0]:.1f}, {tilt_values[-1]:.1f}] degrees")
    print(f"Anisotropy: {anisotropy}, Active Curvature: {active_curvature}")

    for i, tilt_deg in enumerate(tilt_values):
        print(f"[{i+1}/{len(tilt_values)}] Simulating Tilt = {tilt_deg:.1f} degrees...")

        tracemalloc.start()
        t0 = time.time()

        tilt_rad = np.deg2rad(tilt_deg)
        # Apply tilt to gravity vector in lateral (x) direction
        # gravity normal: [0, 0, -9.81]
        # tilted gravity: [sin(tilt), 0, -cos(tilt)] * 9.81
        gx = np.sin(tilt_rad) * 9.81
        gz = -np.cos(tilt_rad) * 9.81

        try:
            # Setup Information Field
            s = np.linspace(0, length, n_elements + 1)
            info_center = 0.5 * length
            info_width = 0.1 * length
            I = 0.5 + 0.5 * np.exp(-0.5 * ((s - info_center) / info_width)**2)
            dIds = np.gradient(I, s)
            info = InfoField1D(s=s, I=I, dIds=dIds)

            # Setup Parameters
            params = CounterCurvatureParams(
                chi_kappa=chi_kappa,
                chi_tau=0.0,
                chi_E=0.0,
                chi_M=0.0,
                scale_length=length
            )

            # Create System with constant intrinsic curvature base
            kappa_gen = np.zeros((3, n_elements + 1))
            kappa_gen[1, :] = natural_kyphosis  # Sagittal Kyphosis

            rod_system = CounterCurvatureRodSystem.from_iec(
                info=info,
                params=params,
                length=length,
                n_elements=n_elements,
                E0=E0,
                rho=rho,
                radius=radius,
                kappa_gen=kappa_gen,
                gravity=9.81, # We'll override gravity using PyElastica forces later, but need placeholder here
                stiffness_anisotropy=anisotropy
            )

            # Manually run simulation to inject custom gravity forcing
            import elastica as ea
            class CCSystem(ea.BaseSystemCollection, ea.Constraints, ea.Forcing, ea.Damping, ea.CallBacks):
                pass

            system = CCSystem()
            system.append(rod_system.rod)

            # Constraints
            system.constrain(rod_system.rod).using(
                ea.OneEndFixedBC,
                constrained_position_idx=(0,),
                constrained_director_idx=(0,)
            )

            # Gravity - Custom Load Vector
            system.add_forcing_to(rod_system.rod).using(ea.GravityForces, acc_gravity=np.array([gx, 0.0, gz]))

            # Damping
            system.dampen(rod_system.rod).using(ea.AnalyticalLinearDamper, damping_constant=0.5, time_step=dt)

            # Callback for diagnostics
            class CCCallback(ea.CallBackBaseClass):
                def __init__(self, step_skip, cb_results):
                    super().__init__()
                    self.every = step_skip
                    self.results = cb_results
                def make_callback(self, system, time, current_step):
                    if current_step % self.every == 0:
                        self.results["time"].append(time)
                        self.results["centerline"].append(system.position_collection.copy().T)
                        self.results["kappa"].append(system.kappa.copy().T)

            sim_results_dict = {"time": [], "centerline": [], "kappa": []}
            save_every = max(1, int(duration/dt/10))
            system.collect_diagnostics(rod_system.rod).using(CCCallback, step_skip=save_every, cb_results=sim_results_dict)

            system.finalize()
            timestepper = ea.PositionVerlet()
            ea.integrate(timestepper, system, duration, int(duration/dt), progress_bar=False)

            # Format final results
            from spinalmodes.countercurvature.pyelastica_bridge import SimulationResult

            # Pad kappa to match n_nodes (n_elems + 1)
            kappa_raw = np.array(sim_results_dict["kappa"])
            if len(kappa_raw) > 0:
                n_time, n_internal, n_dim = kappa_raw.shape
                padded_kappa = np.zeros((n_time, n_internal + 2, n_dim))
                padded_kappa[:, 1:-1, :] = kappa_raw
                padded_kappa[:, 0, :] = kappa_raw[:, 0, :]
                padded_kappa[:, -1, :] = kappa_raw[:, -1, :]
            else:
                padded_kappa = np.empty((0, n_elements + 1, 3))

            final_energies = {}
            if hasattr(rod_system.rod, "compute_bending_energy"):
                final_energies["bending_energy"] = float(rod_system.rod.compute_bending_energy())
            if hasattr(rod_system.rod, "compute_shear_energy"):
                final_energies["shear_energy"] = float(rod_system.rod.compute_shear_energy())
            if hasattr(rod_system.rod, "compute_translational_energy"):
                final_energies["translational_energy"] = float(rod_system.rod.compute_translational_energy())
            if hasattr(rod_system.rod, "compute_rotational_energy"):
                final_energies["rotational_energy"] = float(rod_system.rod.compute_rotational_energy())
            if hasattr(rod_system.rod, "mass") and hasattr(rod_system.rod, "position_collection"):
                z_pos = rod_system.rod.position_collection[2, :]
                final_energies["gravitational_energy"] = float(np.sum(rod_system.rod.mass * 9.81 * z_pos))

            sim_result = SimulationResult(
                time=np.array(sim_results_dict["time"]),
                centerline=np.array(sim_results_dict["centerline"]),
                kappa=padded_kappa,
                info_field=info,
                final_energies=final_energies
            )

            metrics = sim_result.compute_final_metrics()

            energy_metrics = compute_U_CC(
                sim_result, info, params, gravity=9.81, rho=rho, E0=E0,
                radius=radius, anisotropy=anisotropy
            )
            metrics.update(energy_metrics)

            success = True
            error_msg = ""
        except Exception as e:
            success = False
            error_msg = str(e)
            metrics = {}
            print(f"  FAILED: {error_msg}")

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        t1 = time.time()

        if success:
            cobb_angle = metrics.get("cobb_angle", 0.0)
            max_curvature = metrics.get("max_curvature", 0.0)
            s_lat = metrics.get("S_lat", 0.0)
            u_cc = metrics.get("U_CC", 0.0)

            print(f"  -> Cobb: {cobb_angle:.2f} deg, MaxCurv: {max_curvature:.2f}, S_lat: {s_lat:.4f}")

            results.append({
                "tilt_deg": tilt_deg,
                "anisotropy": anisotropy,
                "active_curvature": active_curvature,
                "cobb_angle": cobb_angle,
                "max_curvature": max_curvature,
                "s_lat": s_lat,
                "u_cc": u_cc,
                "runtime_sec": t1 - t0,
                "peak_memory_mb": peak / (1024 * 1024),
                "success": success,
                "error": error_msg
            })
        else:
             results.append({
                "tilt_deg": tilt_deg,
                "anisotropy": anisotropy,
                "active_curvature": active_curvature,
                "cobb_angle": np.nan,
                "max_curvature": np.nan,
                "s_lat": np.nan,
                "u_cc": np.nan,
                "runtime_sec": t1 - t0,
                "peak_memory_mb": peak / (1024 * 1024),
                "success": success,
                "error": error_msg
            })

    # Save Results
    df = pd.DataFrame(results)
    csv_path = out_dir / "results.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved results to {csv_path}")

    # Save Params (for reproducibility)
    params_path = out_dir / "params.csv"
    params_df = pd.DataFrame([{
        "tilt_min": tilt_values[0],
        "tilt_max": tilt_values[-1],
        "steps": len(tilt_values),
        "anisotropy": anisotropy,
        "active_curvature": active_curvature,
        "natural_kyphosis": natural_kyphosis,
        "duration": duration,
        "dt": dt,
        "n_elements": n_elements,
        "seed": seed
    }])
    params_df.to_csv(params_path, index=False)
    print(f"Saved params to {params_path}")

    # Generate Plots
    generate_plots(df, out_dir)

def generate_plots(df, out_dir):
    df_valid = df.dropna(subset=['cobb_angle'])

    if df_valid.empty:
        print("No valid results to plot.")
        return

    # Plot 1: Tilt vs Cobb Angle
    plt.figure(figsize=(10, 6))
    plt.plot(df_valid['tilt_deg'], df_valid['cobb_angle'], 'o-', linewidth=2, color='blue')
    plt.xlabel('Load Vector Tilt (degrees)')
    plt.ylabel('Cobb Angle (degrees)')
    plt.title('Effect of Load Vector Tilt on Cobb Angle\n(Anisotropy=3.0, Active Growth=10.0)')
    plt.grid(True, alpha=0.3)

    plot_path = out_dir / "plot_tilt_cobb.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path}")

    # Plot 2: Tilt vs Lateral Deviation (S_lat)
    plt.figure(figsize=(10, 6))
    plt.plot(df_valid['tilt_deg'], df_valid['s_lat'], 's--', linewidth=2, color='red')
    plt.xlabel('Load Vector Tilt (degrees)')
    plt.ylabel('Lateral Deviation S_lat (m)')
    plt.title('Effect of Load Vector Tilt on Lateral Deviation\n(Anisotropy=3.0, Active Growth=10.0)')
    plt.grid(True, alpha=0.3)

    plot_path2 = out_dir / "plot_tilt_slat.png"
    plt.savefig(plot_path2, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path2}")

if __name__ == "__main__":
    run_tilt_sweep()
