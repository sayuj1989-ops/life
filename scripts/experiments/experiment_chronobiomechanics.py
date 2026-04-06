import os
import sys
import time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

try:
    import elastica as ea
    from spinalmodes.countercurvature.coupling import CounterCurvatureParams
    from spinalmodes.countercurvature.info_fields import InfoField1D
    from spinalmodes.countercurvature.pyelastica_bridge import (
        PYELASTICA_AVAILABLE,
        CounterCurvatureRodSystem,
        SimulationResult,
    )
except ImportError as e:
    print(f"Error importing simulation module: {e}")
    sys.exit(1)

class LocomotorGravity(ea.NoForces):
    """Oscillating gravity force."""
    def __init__(self, base_gravity=9.81, amplitude=0.5, frequency=2.0):
        super().__init__()
        self.base_gravity = base_gravity
        self.amplitude = amplitude
        self.frequency = frequency

    def apply_forces(self, system, time=0.0):
        g_t = self.base_gravity * (1.0 + self.amplitude * np.sin(2.0 * np.pi * self.frequency * time))
        system.external_forces[2, :] -= system.mass * g_t

def run_point(circadian_phase_hours, locomotor_freq, duration=1.0, dt=1e-4):
    """
    Simulates a 1-second burst of physical activity at a specific time of day.
    """
    # 1. Map Time of Day (0-24h) to Circadian phase phi in [0, 2pi)
    # Peak activity/stiffness assumed at 12:00 (midday). Trough at 00:00 (midnight).
    # chi_kappa(t) = chi_base * (1 + A * cos(phi))

    chi_base = 8.0
    A = 0.5
    # Phase shift so that phase_hours=12 gives cos(0)=1
    phi = (circadian_phase_hours - 12.0) * (2.0 * np.pi / 24.0)
    chi_kappa = chi_base * (1.0 + A * np.cos(phi))

    length = 0.4
    n_elements = 20

    s = np.linspace(0, length, n_elements + 1)
    info_center = 0.5 * length
    info_width = 0.1 * length
    I = 0.5 + 0.5 * np.exp(-0.5 * ((s - info_center) / info_width)**2)
    dIds = np.gradient(I, s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    params = CounterCurvatureParams(
        chi_kappa=chi_kappa,
        chi_tau=0.0, chi_E=0.0, chi_M=0.0, scale_length=length
    )

    kappa_gen = np.zeros((3, n_elements + 1))
    kappa_gen[1, :] = 2.0  # Natural kyphosis
    kappa_gen[0, :] = 0.05 # Initial lateral defect

    rod_system = CounterCurvatureRodSystem.from_iec(
        info=info, params=params, length=length, n_elements=n_elements,
        kappa_gen=kappa_gen, stiffness_anisotropy=5.0, E0=1e6, radius=0.01, rho=1000.0
    )

    class ResonantSystem(ea.BaseSystemCollection, ea.Constraints, ea.Forcing, ea.Damping, ea.CallBacks):
        pass

    system = ResonantSystem()
    system.append(rod_system.rod)
    system.constrain(rod_system.rod).using(ea.OneEndFixedBC, constrained_position_idx=(0,), constrained_director_idx=(0,))

    system.add_forcing_to(rod_system.rod).using(
        LocomotorGravity, base_gravity=9.81, amplitude=0.5, frequency=locomotor_freq
    )
    system.dampen(rod_system.rod).using(ea.AnalyticalLinearDamper, damping_constant=0.5, time_step=dt)

    results = {"time": [], "centerline": [], "kappa": []}
    class SaveCallback(ea.CallBackBaseClass):
        def __init__(self, step_skip, results):
            super().__init__()
            self.every = step_skip
            self.results = results
        def make_callback(self, system, time, current_step):
            if current_step % self.every == 0:
                self.results["time"].append(time)
                self.results["centerline"].append(system.position_collection.copy().T)
                self.results["kappa"].append(system.kappa.copy().T)

    save_every = max(1, int(duration/dt/20))
    system.collect_diagnostics(rod_system.rod).using(SaveCallback, step_skip=save_every, results=results)
    system.finalize()

    try:
        ea.integrate(ea.PositionVerlet(), system, duration, int(duration/dt), progress_bar=False)
        centerlines = np.array(results["centerline"])
        max_dynamic_lat = np.max(np.abs(centerlines[:, :, 0]))
        return max_dynamic_lat
    except Exception as e:
        print(f"Failed at {circadian_phase_hours}h, {locomotor_freq}Hz: {e}")
        return np.nan

def run_experiment():
    print("Running Chronobiomechanical Vulnerability Map...")
    out_dir = Path("outputs/figures")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Grid search
    hours = np.linspace(0, 24, 7)    # Time of day (e.g. 0, 4, 8, 12, 16, 20, 24)
    freqs = np.linspace(0.5, 4.0, 8) # Locomotor frequency

    results = []
    Z = np.zeros((len(freqs), len(hours)))

    for i, f in enumerate(freqs):
        for j, h in enumerate(hours):
            print(f"Simulating H={h:.1f}, Freq={f:.1f}Hz...")
            val = run_point(h, f)
            Z[i, j] = val
            results.append({"time_of_day": h, "locomotor_freq": f, "max_lateral_dev": val})

    df = pd.DataFrame(results)
    df.to_csv("outputs/chronobiomechanics_map.csv", index=False)

    # Plot heatmap
    plt.figure(figsize=(10, 6))
    X, Y = np.meshgrid(hours, freqs)
    cp = plt.contourf(X, Y, Z, levels=20, cmap='inferno_r')
    plt.colorbar(cp, label="Max Lateral Deviation (m)")

    plt.title("Chronobiomechanical Vulnerability Map\nSpinal Instability vs. Time of Day and Locomotor Frequency")
    plt.xlabel("Time of Day (Hours, 12=Peak Circadian Coupling)")
    plt.ylabel("Locomotor Frequency (Hz, Walking ~ 2Hz)")

    # Highlight highest vulnerability zone
    plt.axvspan(0, 6, color='red', alpha=0.1, label='Night/Trough (High Vulnerability)')
    plt.axvspan(18, 24, color='red', alpha=0.1)

    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "chronobiomechanics_heatmap.png", dpi=300)
    print(f"Saved to {out_dir / 'chronobiomechanics_heatmap.png'}")

if __name__ == "__main__":
    run_experiment()
