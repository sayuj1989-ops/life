#!/usr/bin/env python3
"""
Phase 2, Weeks 5-7: Spinal Jetlag and Circadian Desynchronization.

Models time-varying information-curvature coupling modulated by a circadian clock
and simulates desynchronization ("jetlag") effects on spinal alignment.
"""

import sys
import os
import time
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from dataclasses import dataclass
from typing import Optional, List, Dict

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from spinalmodes.countercurvature.pyelastica_bridge import (
    CounterCurvatureRodSystem,
    CircadianParams,
    CounterCurvatureParams,
    InfoField1D,
    compute_U_CC,
    SimulationResult,
    ea, # Access to PyElastica classes
    PYELASTICA_AVAILABLE
)
from spinalmodes.countercurvature.scoliosis_metrics import compute_scoliosis_metrics

if not PYELASTICA_AVAILABLE:
    print("Error: PyElastica not installed.")
    sys.exit(1)

# --- Time Dependent Gravity ---
class TimeDependentGravity(ea.NoForces):
    """Applies a time-varying gravitational force to simulate daily activity cycles.

    g(t) = g_base * (0.5 + 0.5 * cos(omega * t))

    This approximates the cycle of upright posture (loading) and recumbent sleep (unloading).
    """
    def __init__(self, acc_gravity: np.ndarray, period: float = 24*3600, phase: float = 0.0):
        super().__init__()
        self.acc_gravity = np.array(acc_gravity) # Vector (0, 0, -g)
        self.period = period
        self.phase = phase
        self.omega = 2 * np.pi / period

    def apply_forces(self, system, time: float = 0.0):
        # Modulation: 0 to 1.
        # In phase: Max gravity at t=0 (noon?), Min gravity at t=period/2 (midnight?)
        # Adjust phase as needed.
        # Cosine: max at 0. (0.5 + 0.5*1) = 1.
        factor = 0.5 + 0.5 * np.cos(self.omega * time + self.phase)

        # Total force = mass * acc * factor
        # system.mass is (n_nodes,)
        # force is (3, n_nodes)

        # We need to add to system.external_forces
        # Expand dimensions for broadcasting
        force_vector = self.acc_gravity[:, None] * system.mass[None, :] * factor
        system.external_forces += force_vector

# --- Experiment Setup ---

def run_experiment(
    condition: str,
    circadian_params: CircadianParams,
    duration_hours: float = 72.0,
    quick_test: bool = False,
    dt: float = 2e-4,
    gravity_strength: float = 9.81,
    scale_length: float = 1.0
):
    """Run a single experimental condition."""

    print(f"Running Condition: {condition}")

    # 1. Physics Parameters
    n_elements = 50
    L = 0.4 # m
    radius = 0.01 # m
    E0 = 1e7 # Pa (Softer than bone to allow visible deformation in short time)
    rho = 1000.0

    # Duration
    duration = duration_hours * 3600.0
    if quick_test:
        duration = 10.0 # 10 seconds per condition for code verification

    # 2. Information Field
    # Localized signal at center
    s = np.linspace(0, L, n_elements + 1)
    info_center = 0.5 * L
    info_width = 0.15 * L
    I = 0.8 * np.exp(-0.5 * ((s - info_center) / info_width)**2)
    dIds = np.gradient(I, s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    # 3. Coupling Parameters
    # chi_kappa needs to be strong enough to counter gravity
    # With E0=1e7, L=0.4, we need substantial curvature drive.
    chi_kappa_base = 15.0
    params = CounterCurvatureParams(
        chi_kappa=chi_kappa_base,
        chi_E=0.0,
        chi_M=0.0,
        chi_tau=0.0,
        scale_length=scale_length
    )

    # 4. Geometry and Initial State
    # Lateral defect to ensure measurable scoliosis if stabilization fails
    kappa_gen = np.zeros((3, n_elements + 1))
    kappa_gen[0, :] = 0.2 # Lateral defect
    kappa_gen[1, :] = 2.0 # Natural kyphosis

    # 5. Create System
    # Note: We pass gravity=0 to the factory because we will add TimeDependentGravity manually
    # Wait, run_simulation adds GravityForces if gravity > 0.
    # We should modify how we call run_simulation or hack it.
    # run_simulation adds GravityForces. We can pass gravity=0.0 to disable standard gravity,
    # and add our custom forcing via a callback or by manually modifying the system?
    # CounterCurvatureRodSystem.run_simulation builds the system internally.
    # To inject TimeDependentGravity, we'd need to modify run_simulation or subclass.

    # HACK: Since we cannot easily inject TimeDependentGravity into CounterCurvatureRodSystem.run_simulation
    # without modifying the library again, we will use a workaround.
    # We will let run_simulation handle a constant gravity if condition is "Microgravity".
    # For others, we need oscillating gravity.
    #
    # Actually, the user prompt implies "Simulates ... through phase offset (phi) between gravity loading and circadian rhythm".
    # If I can't oscillate gravity, I can't change the phase offset effect properly unless I oscillate the clock relative to constant gravity.
    # Constant gravity is always "ON".
    # If the clock oscillates, the "active counter-curvature" oscillates.
    # If they are "in phase", it means Peak Curvature Drive coincides with Peak Load.
    # If gravity is constant (Peak Load always), then phase doesn't mean much except shifting the peak of drive.
    #
    # However, biologically, "Entrained" means the internal clock matches the external cycle.
    # If the external cycle (Gravity) is constant, there is no phase to lock to.
    # So Gravity MUST vary.
    #
    # Since I cannot modify run_simulation (I marked it complete), I have to find a way.
    # I can copy-paste the logic of run_simulation here and modify it, OR
    # I can assume "Gravity Loading" is implicitly handled or that I can subclass CounterCurvatureRodSystem to override run_simulation.
    #
    # Subclassing is cleaner.

    class TimeVaryingGravityRodSystem(CounterCurvatureRodSystem):
        def run_simulation(self, final_time, dt, gravity_params=None, **kwargs):
            # We copy the structure of parent run_simulation but add custom forcing

            # ... (Copying generic setup from parent is hard without copy-paste)
            # Alternative: Use the parent run_simulation but pass gravity=0,
            # and use a "Callback" that is actually a Forcing?
            # PyElastica Callbacks are for diagnostics. Forcing is for physics.
            # run_simulation defines the system class:
            # class CCSystem(ea.BaseSystemCollection, ea.Constraints, ea.Forcing, ea.Damping, ea.CallBacks): pass
            # And it allows `system.add_forcing_to(self.rod)...`
            # But I can't inject code into the parent method.

            # OK, I will duplicate `run_simulation` logic in this script.
            # It allows full control.
            return run_simulation_custom(self, final_time, dt, gravity_params=gravity_params, **kwargs)

    # Instantiate
    system_wrapper = TimeVaryingGravityRodSystem.from_iec(
        info=info,
        params=params,
        length=L,
        n_elements=n_elements,
        E0=E0,
        radius=radius,
        kappa_gen=kappa_gen,
        gravity=0.0, # We will handle gravity manually
        stiffness_anisotropy=2.0
    )

    # Gravity Params
    g_params = {
        "strength": gravity_strength,
        "period": circadian_params.gravity_period if circadian_params.gravity_period else circadian_params.period,
        "phase": 0.0 # External time reference usually 0
    }

    if condition == "Microgravity":
        g_params["strength"] = 0.0 # Or very low

    # Run
    results = system_wrapper.run_simulation(
        final_time=duration,
        dt=dt,
        save_every=max(1, int(duration/dt/50)), # 50 frames
        gravity=0.0, # Disable internal gravity
        circadian_params=circadian_params,
        gravity_params=g_params, # Custom arg passed to our custom runner
        progress_bar=True
    )

    # Compute Metrics
    # Average over last 24 hours (or last period)
    mask = results.time > (duration - 24*3600)
    if not np.any(mask):
        mask = np.full(results.time.shape, True)

    avg_curvature = np.mean(results.curvature[mask])
    avg_s_lat = np.mean([compute_scoliosis_metrics(results.centerline[i][:,2], results.centerline[i][:,0]).S_lat for i in np.where(mask)[0]])

    # Energy
    u_cc = compute_U_CC(results, info, params, gravity=gravity_strength, E0=E0)

    return {
        "Condition": condition,
        "Avg_Curvature": avg_curvature,
        "Avg_S_Lat": avg_s_lat,
        "U_CC": u_cc["U_CC"],
        "Info_Gain": u_cc["info_gain_ratio"],
        "Final_Cobb": results.compute_final_metrics().get("cobb_angle", 0.0)
    }

def run_simulation_custom(wrapper, final_time, dt, gravity_params=None, circadian_params=None, save_every=100, progress_bar=True, gravity=0.0, **kwargs):
    # Re-implementation of run_simulation to support custom forcing
    class CCSystem(ea.BaseSystemCollection, ea.Constraints, ea.Forcing, ea.Damping, ea.CallBacks):
        pass

    system = CCSystem()
    system.append(wrapper.rod)

    # Constraints (Fixed)
    system.constrain(wrapper.rod).using(
        ea.OneEndFixedBC,
        constrained_position_idx=(0,),
        constrained_director_idx=(0,)
    )

    # Custom Gravity
    if gravity_params and gravity_params["strength"] > 1e-6:
        system.add_forcing_to(wrapper.rod).using(
            TimeDependentGravity,
            acc_gravity=np.array([0.0, 0.0, -gravity_params["strength"]]),
            period=gravity_params["period"],
            phase=gravity_params["phase"]
        )

    # Damping
    system.dampen(wrapper.rod).using(ea.AnalyticalLinearDamper, damping_constant=0.5, time_step=dt)

    # Diagnostics
    class CCCallback(ea.CallBackBaseClass):
        def __init__(self, step_skip, results):
            super().__init__()
            self.every = step_skip
            self.results = results
        def make_callback(self, system, time, current_step):
            if current_step % self.every == 0:
                self.results["time"].append(time)
                self.results["centerline"].append(system.position_collection.copy().T)
                self.results["kappa"].append(system.kappa.copy().T)

    results = {"time": [], "centerline": [], "kappa": []}
    system.collect_diagnostics(wrapper.rod).using(CCCallback, step_skip=save_every, results=results)

    # Circadian Callback (Copied logic)
    if circadian_params:
        class CircadianModulationCallback(ea.CallBackBaseClass):
            def __init__(self, system_wrapper, c_params, step_skip=1):
                super().__init__()
                self.system_wrapper = system_wrapper
                self.c_params = c_params
                self.every = step_skip
                self.chi_0 = system_wrapper.params.chi_kappa

            def make_callback(self, system, time, current_step):
                if current_step % self.every == 0:
                    omega = 2 * np.pi / self.c_params.period
                    modulation = 1.0 + self.c_params.amplitude * np.cos(omega * time + self.c_params.phase)
                    new_chi_kappa = self.chi_0 * modulation
                    new_params = self.system_wrapper.params._replace(chi_kappa=new_chi_kappa)
                    self.system_wrapper.update_rest_curvature(new_params)

        system.collect_diagnostics(wrapper.rod).using(
            CircadianModulationCallback,
            system_wrapper=wrapper,
            c_params=circadian_params,
            step_skip=1
        )

    system.finalize()
    timestepper = ea.PositionVerlet()
    ea.integrate(timestepper, system, final_time, int(final_time/dt), progress_bar=progress_bar)

    # Process results (padding kappa)
    kappa_raw = np.array(results["kappa"])
    n_elems = wrapper.n_elements
    if len(kappa_raw) > 0:
        n_time, n_internal, n_dim = kappa_raw.shape
        padded_kappa = np.zeros((n_time, n_internal + 2, n_dim))
        padded_kappa[:, 1:-1, :] = kappa_raw
        padded_kappa[:, 0, :] = kappa_raw[:, 0, :]
        padded_kappa[:, -1, :] = kappa_raw[:, -1, :]
    else:
        padded_kappa = np.empty((0, n_elems + 1, 3))

    # Compute final energies
    final_energies = {}
    if hasattr(wrapper.rod, "compute_bending_energy"):
        final_energies["bending_energy"] = float(wrapper.rod.compute_bending_energy())
    if hasattr(wrapper.rod, "compute_shear_energy"):
        final_energies["shear_energy"] = float(wrapper.rod.compute_shear_energy())
    if hasattr(wrapper.rod, "compute_translational_energy"):
        final_energies["translational_energy"] = float(wrapper.rod.compute_translational_energy())
    if hasattr(wrapper.rod, "compute_rotational_energy"):
        final_energies["rotational_energy"] = float(wrapper.rod.compute_rotational_energy())

    # Gravitational Potential Energy
    # Note: If using TimeDependentGravity, the potential energy is ill-defined or time-dependent.
    # We use standard m*g*z with the peak gravity strength for consistency,
    # or instantaneous gravity?
    # Usually U_gravity is defined with respect to a static field.
    # We will use the base gravity_strength passed in gravity_params or 9.81 default.
    g_ref = 9.81
    if gravity_params:
        g_ref = gravity_params.get("strength", 9.81)

    if hasattr(wrapper.rod, "mass") and hasattr(wrapper.rod, "position_collection"):
        z_pos = wrapper.rod.position_collection[2, :]
        final_energies["gravitational_energy"] = float(np.sum(wrapper.rod.mass * g_ref * z_pos))

    return SimulationResult(
        time=np.array(results["time"]),
        centerline=np.array(results["centerline"]),
        kappa=padded_kappa,
        info_field=wrapper.info_field,
        final_energies=final_energies
    )

def main():
    parser = argparse.ArgumentParser(description="Spinal Jetlag Simulation")
    parser.add_argument("--quick-test", action="store_true", help="Run short simulation for verification")
    args = parser.parse_args()

    print("Starting Spinal Jetlag Experiment...")

    # Define Conditions
    # Period = 24h = 86400s
    T_24 = 24 * 3600.0

    conditions = {
        "Entrained": CircadianParams(
            period=T_24,
            amplitude=0.5,
            phase=0.0,
            gravity_period=T_24
        ),
        "Free-running": CircadianParams(
            period=24.5 * 3600.0, # Slight mismatch
            amplitude=0.5,
            phase=0.0,
            gravity_period=T_24
        ),
        "Jetlagged": CircadianParams(
            period=T_24,
            amplitude=0.5,
            phase=np.pi, # Anti-phase
            gravity_period=T_24
        ),
        "Microgravity": CircadianParams(
            period=T_24,
            amplitude=0.1, # Amplitude decays
            phase=0.0,
            gravity_period=T_24 # Gravity period exists but strength will be 0
        )
    }

    all_results = []

    for name, params in conditions.items():
        res = run_experiment(name, params, quick_test=args.quick_test)
        all_results.append(res)

    df = pd.DataFrame(all_results)
    print("\nResults:")
    print(df)

    # Save Outputs
    today = date.today().isoformat()
    output_dir = f"outputs/sim/{today}"
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, "jetlag_experiment.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV to {csv_path}")

    # Generate Report
    report_path = os.path.join(output_dir, "jetlag_report.md")
    with open(report_path, "w") as f:
        f.write(f"# Spinal Jetlag Experiment Report\n")
        f.write(f"Date: {today}\n\n")
        f.write("## Hypothesis\n")
        f.write("Desynchronization between the internal circadian clock (regulating counter-curvature stiffness/growth) "
                "and the external gravity cycle leads to periods of high mechanical vulnerability, increasing the risk of scoliosis.\n\n")
        f.write("## Results Summary\n")
        f.write(df.to_markdown(index=False))
        f.write("\n\n## Analysis\n")
        f.write("The 'Jetlagged' condition (Anti-phase) is expected to show higher Cobb angles/lateral deformation due to "
                "destructive interference: peak load coincides with minimum structural reinforcement.\n")

    print(f"Saved Report to {report_path}")

if __name__ == "__main__":
    main()
