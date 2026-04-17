import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from pathlib import Path

def setup_directories():
    os.makedirs('outputs/sleep_spindles', exist_ok=True)

class ActiveInferenceSpine:
    def __init__(self, L=1.0, tau=0.1, mass=1.0):
        self.L = L
        self.tau = tau
        self.mass = mass

        # True physics parameters
        self.true_g = 9.81
        self.dt = 0.01

        # Generative model parameters (internal brain model)
        self.mu_x = 0.0  # prior for position
        self.mu_v = 0.0  # prior for velocity

        # Precisions (inverse variances)
        self.Pi_y0 = 20.0 * L # Position precision ~ Kp
        self.Pi_y1 = 8.0 * L  # Velocity precision ~ Kd
        self.Pi_v = 1.0       # Prior precision

        # State
        self.x = 0.05 # Initial slight perturbation
        self.v = 0.0

        self.history = {'t': [], 'x': [], 'v': [], 'Pi_y1': [], 'g_load': []}
        self.time = 0.0

    def step(self, is_sleep=False, sleep_quality=1.0):
        """One integration step. Sleep disables physical gravity but enables latent learning."""
        g_load = 0.0 if is_sleep else self.true_g

        # 1. Physical Environment Dynamics (Delayed Delayed-Proportional-Derivative approximation)
        # Using a simple inverted pendulum
        # We assume control signal u is generated based on delayed sensory feedback

        # True state derivatives
        dx = self.v

        # Simulated "delay" error - internal model thinks it's at x, v
        # but rapid growth makes the internal model misspecified.
        # In this toy model, if awake, precision Pi_y1 degrades due to mismatch unless maintained

        # Active Inference Control: Action minimizes Free Energy
        # u = -Pi_y0 * x_sense - Pi_y1 * v_sense
        u = -self.Pi_y0 * self.x - self.Pi_y1 * self.v

        dv = (g_load / self.L) * np.sin(self.x) + u / (self.mass * self.L**2)

        self.x += dx * self.dt
        self.v += dv * self.dt

        # 2. Precision Updating (Learning)
        if not is_sleep:
            # Awake: Fast dynamics outpace learning, velocity prediction errors accumulate.
            # Precision drops (Sensory Attenuation / Derivative Gain Trap)
            pred_error_v = np.abs(self.v) # Simple proxy for prediction error
            degradation_rate = 0.5 * pred_error_v
            self.Pi_y1 = max(1.0, self.Pi_y1 - degradation_rate * self.dt)
        else:
            # Sleep (Latent Imagination): Replay restores precision safely.
            # Offline gradient descent restores the precision to optimal levels.
            restoration_rate = 2.0 * sleep_quality
            target_Pi_y1 = 8.0 * self.L
            self.Pi_y1 = min(target_Pi_y1, self.Pi_y1 + restoration_rate * self.dt)

        # Log
        self.history['t'].append(self.time)
        self.history['x'].append(self.x)
        self.history['v'].append(self.v)
        self.history['Pi_y1'].append(self.Pi_y1)
        self.history['g_load'].append(g_load)

        self.time += self.dt

def run_simulation(days=5, hours_per_day=24.0, sleep_hours=8.0, sleep_quality=1.0):
    spine = ActiveInferenceSpine(L=1.6) # Adolescent rapid growth length

    dt = spine.dt
    steps_per_hour = int(1.0 / dt) * 60 # Scale: 1 sim second = 1 hour? Let's keep it simple.
    # Let's say 1 unit of time = 1 hour

    spine.dt = 0.05 # larger step for multi-day sim
    time_total = days * 24.0

    for t in np.arange(0, time_total, spine.dt):
        hour_of_day = t % 24.0
        is_sleep = hour_of_day >= (24.0 - sleep_hours)
        spine.step(is_sleep=is_sleep, sleep_quality=sleep_quality)

    return pd.DataFrame(spine.history)

if __name__ == "__main__":
    setup_directories()

    print("Simulating Normal Sleep (8 hours/day)...")
    df_normal = run_simulation(days=10, sleep_hours=8.0, sleep_quality=1.0)

    print("Simulating Sleep Deprivation / Desynchronization (4 hours/day)...")
    df_deprived = run_simulation(days=10, sleep_hours=4.0, sleep_quality=0.5)

    # Plotting
    fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    axs[0].plot(df_normal['t']/24, df_normal['Pi_y1'], label='Normal Sleep', color='g')
    axs[0].plot(df_deprived['t']/24, df_deprived['Pi_y1'], label='Poor Sleep', color='r', linestyle='--')
    axs[0].set_ylabel('Velocity Precision ($\Pi_{y,1}$) ~ $K_d$')
    axs[0].set_title('Circadian Precision Updating (Latent Imagination)')
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(df_normal['t']/24, np.degrees(df_normal['x']), color='g')
    axs[1].plot(df_deprived['t']/24, np.degrees(df_deprived['x']), color='r', linestyle='--')
    axs[1].set_ylabel('Postural Deviation (deg)')
    axs[1].grid(True)

    axs[2].fill_between(df_normal['t']/24, 0, df_normal['g_load'] > 0, color='gray', alpha=0.3, label='Awake (Gravity Load)')
    axs[2].set_ylabel('Gravity Active')
    axs[2].set_xlabel('Days')
    axs[2].set_yticks([])

    plt.tight_layout()
    plt.savefig('outputs/sleep_spindles/spinal_sleep_spindles.png', dpi=300)
    print("Saved plot to outputs/sleep_spindles/spinal_sleep_spindles.png")
