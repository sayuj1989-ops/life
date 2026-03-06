import os
import sys
import time
import tracemalloc
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    import elastica as ea

    from spinalmodes.countercurvature.coupling import CounterCurvatureParams
    from spinalmodes.countercurvature.info_fields import InfoField1D
    from spinalmodes.countercurvature.pyelastica_bridge import (
        PYELASTICA_AVAILABLE,
        CounterCurvatureRodSystem,
        PinnedBC,
        SimulationResult,
    )
except ImportError as e:
    print(f"Error importing simulation module: {e}")
    sys.exit(1)

if not PYELASTICA_AVAILABLE:
    print("PyElastica is not available. Exiting.")
    sys.exit(1)


class LateralBrace(ea.NoForces):
    """
    Custom Forcing class to simulate a clinical brace intervention.
    Applies a restorative force to the lateral plane (x-axis) pushing the spine
    back towards the midline (x=0) when it deviates.
    """
    def __init__(self, stiffness: float = 5000.0, target_node_range: tuple = (0.2, 0.8), length: float = 0.5, apply_force: bool = True):
        super().__init__()
        self.stiffness = stiffness
        self.target_node_range = target_node_range
        self.length = length
        self.apply_force = apply_force

    def apply_forces(self, system, time: float = 0.0):
        if not self.apply_force:
            return

        # Get positions
        positions = system.position_collection

        # Calculate arc length coordinates roughly
        n_nodes = positions.shape[1]
        s = np.linspace(0, self.length, n_nodes)

        # Determine which nodes are in the "brace zone" (e.g. thoracic apex)
        brace_mask = (s >= self.target_node_range[0] * self.length) & (s <= self.target_node_range[1] * self.length)

        # Apply Hookean restorative force towards midline (x=0)
        # F = -k * x
        x_positions = positions[0, :]
        restorative_force = -self.stiffness * x_positions

        # Apply force only to nodes in the brace zone
        system.external_forces[0, brace_mask] += restorative_force[brace_mask]


def run_brace_simulation(
    is_braced: bool,
    brace_stiffness: float = 10000.0,
    active_curvature: float = 5.0, # Increased to ensure buckling occurs
    anisotropy: float = 0.8, # Reduced anisotropy to further encourage buckling
    length: float = 0.5,
    n_elements: int = 40,
    duration: float = 3.0,
    dt: float = 1e-4,
    gravity: float = 9.81,
    initial_lateral_defect: float = 0.15, # Increased defect to ensure buckling
):
    """Runs a single simulation, with or without a brace."""
    tracemalloc.start()
    t0 = time.time()

    chi_kappa = active_curvature * 15.0 # Vastly increased to force S-shape curvature

    try:
        s = np.linspace(0, length, n_elements + 1)
        info_center = 0.5 * length
        info_width = 0.1 * length
        I = 0.5 + 0.5 * np.exp(-0.5 * ((s - info_center) / info_width)**2)
        dIds = np.gradient(I, s)
        info = InfoField1D(s=s, I=I, dIds=dIds)

        params = CounterCurvatureParams(
            chi_kappa=chi_kappa,
            chi_tau=0.0,
            chi_E=0.0,
            chi_M=0.0,
            scale_length=length
        )

        kappa_gen = np.zeros((3, n_elements + 1))
        kappa_gen[1, :] = 2.0 # Natural kyphosis
        kappa_gen[0, :] = 5.0 # High initial lateral defect to ensure huge scoliosis baseline

        rod_system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=length,
            n_elements=n_elements,
            kappa_gen=kappa_gen,
            stiffness_anisotropy=anisotropy,
            E0=1e6,
            radius=0.01,
            rho=1000.0,
        )

        class BracedSystem(ea.BaseSystemCollection, ea.Constraints, ea.Forcing, ea.Damping, ea.CallBacks):
            pass

        system = BracedSystem()
        system.append(rod_system.rod)

        # Fixed at bottom (sacrum)
        system.constrain(rod_system.rod).using(
            ea.OneEndFixedBC,
            constrained_position_idx=(0,),
            constrained_director_idx=(0,)
        )

        # Apply standard gravity
        system.add_forcing_to(rod_system.rod).using(
            ea.GravityForces, acc_gravity=np.array([0.0, 0.0, -gravity])
        )

        # Apply Brace
        system.add_forcing_to(rod_system.rod).using(
            LateralBrace,
            stiffness=brace_stiffness,
            target_node_range=(0.3, 0.7), # Brace covers middle 40% of spine
            length=length,
            apply_force=is_braced
        )

        # Apply damping
        system.dampen(rod_system.rod).using(ea.AnalyticalLinearDamper, damping_constant=2.0, time_step=dt)

        # Callback
        class SaveCallback(ea.CallBackBaseClass):
            def __init__(self, step_skip, results):
                super().__init__()
                self.every = step_skip
                self.results = results
            def make_callback(self, system, time, current_step):
                if current_step % self.every == 0:
                    self.results["time"].append(time)
                    # Track max lateral deviation (x-axis)
                    max_x = np.max(np.abs(system.position_collection[0, :]))
                    self.results["max_lat_dev"].append(max_x)
                    self.results["kappa"].append(system.kappa.copy().T)

        results = {"time": [], "max_lat_dev": [], "kappa": []}
        save_every = max(1, int(duration/dt/100)) # Save 100 points
        system.collect_diagnostics(rod_system.rod).using(SaveCallback, step_skip=save_every, results=results)

        system.finalize()
        timestepper = ea.PositionVerlet()
        ea.integrate(timestepper, system, duration, int(duration/dt), progress_bar=False)

        # Process results
        times = np.array(results["time"])
        lat_devs = np.array(results["max_lat_dev"])

        # Calculate final Cobb angle roughly from final curvature
        final_kappa = results["kappa"][-1]
        lat_kappa = final_kappa[:, 0]
        # Integrate lateral curvature to get angle (simplified Cobb)
        ds = length / n_elements
        max_angle = np.max(np.cumsum(np.abs(lat_kappa)) * ds) * (180/np.pi)

        success = True
        error_msg = ""

    except Exception as e:
        success = False
        error_msg = str(e)
        times = np.array([])
        lat_devs = np.array([])
        max_angle = 0.0

    finally:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    t1 = time.time()

    return {
        "is_braced": is_braced,
        "runtime_sec": t1 - t0,
        "success": success,
        "error": error_msg,
        "times": times,
        "lat_devs": lat_devs,
        "final_cobb": max_angle
    }

def run_experiment():
    print("Running Clinical Brace Intervention Experiment...")
    out_dir = Path("outputs/clinical_brace")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Simulating Unbraced Spine (Natural Progression)...")
    res_unbraced = run_brace_simulation(is_braced=False)

    print("Simulating Braced Spine (Intervention)...")
    res_braced = run_brace_simulation(is_braced=True, brace_stiffness=500000.0)

    if not res_unbraced["success"] or not res_braced["success"]:
        print("Simulation failed.")
        if not res_unbraced["success"]: print(f"Unbraced Error: {res_unbraced['error']}")
        if not res_braced["success"]: print(f"Braced Error: {res_braced['error']}")
        sys.exit(1)

    print(f"Final Cobb Angle (Unbraced): {res_unbraced['final_cobb']:.2f}°")
    print(f"Final Cobb Angle (Braced): {res_braced['final_cobb']:.2f}°")

    # Save to CSV
    df_unbraced = pd.DataFrame({"time": res_unbraced["times"], "lat_dev": res_unbraced["lat_devs"], "scenario": "Unbraced"})
    df_braced = pd.DataFrame({"time": res_braced["times"], "lat_dev": res_braced["lat_devs"], "scenario": "Braced"})
    df_all = pd.concat([df_unbraced, df_braced])

    csv_path = out_dir / "brace_intervention.csv"
    df_all.to_csv(csv_path, index=False)
    print(f"Saved metrics to {csv_path}")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(res_unbraced["times"], res_unbraced["lat_devs"] * 100, 'r-', linewidth=2, label=f'Unbraced (Cobb: {res_unbraced["final_cobb"]:.1f}°)')
    plt.plot(res_braced["times"], res_braced["lat_devs"] * 100, 'b-', linewidth=2, label=f'Braced (Cobb: {res_braced["final_cobb"]:.1f}°)')

    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.title("Clinical Brace Intervention: Stabilizing the Energy Deficit Window", fontsize=14)
    plt.xlabel("Simulation Time (s)", fontsize=12)
    plt.ylabel("Maximum Lateral Deviation (cm)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)

    plot_path = out_dir / "brace_rescue_plot.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {plot_path}")

if __name__ == "__main__":
    run_experiment()
