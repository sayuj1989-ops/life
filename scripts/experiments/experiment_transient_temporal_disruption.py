import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0, k_passive=5.0, c_passive=0.5):
    """Non-linear inverted pendulum dynamics with state bounding and passive stiffness."""
    # State bounding to prevent overflow
    theta = np.clip(x[0], -1.5, 1.5)
    omega = np.clip(x[1], -10.0, 10.0)

    dtheta = omega

    # Add passive cubic stiffness to prevent total runaway
    passive_torque = -k_passive * theta - k_passive * 0.1 * theta**3 - c_passive * omega

    domega = (g / L) * np.sin(theta) + (u + passive_torque) / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0, k_passive=5.0, c_passive=0.5):
    """Runge-Kutta 4 integration."""
    k1 = dynamics(x, u, L=L, m=m, k_passive=k_passive, c_passive=c_passive)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m, k_passive=k_passive, c_passive=c_passive)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m, k_passive=k_passive, c_passive=c_passive)
    k4 = dynamics(x + dt * k3, u, L=L, m=m, k_passive=k_passive, c_passive=c_passive)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_transient_disruption():
    """Simulates a transient temporal disruption where T_pred drops behind tau."""
    dt = 0.01
    T_total = 10.0
    steps = int(T_total / dt)
    time_array = np.linspace(0, T_total, steps, dtype=float)

    L = 1.0
    m = 1.0
    tau = 0.18 # 180 ms physical delay
    delay_steps = int(tau / dt)

    # Control gains
    Kp = 25.0
    Kd = 10.0

    x = np.zeros((steps, 2), dtype=float)
    u = np.zeros(steps, dtype=float)
    T_pred_array = np.zeros(steps, dtype=float)
    energetic_cost = np.zeros(steps, dtype=float)

    # Initial perturbation
    x[0] = np.array([0.05, 0.0])

    # Define T_pred trajectory: transient drop between 3s and 7s
    for i, t in enumerate(time_array):
        if 3.0 <= t <= 7.0:
            # Smooth transition using cosine
            drop_factor = 0.5 * (1 - np.cos(2 * np.pi * (t - 3.0) / 4.0))
            T_pred_array[i] = tau - 0.08 * drop_factor # Drops by up to 80ms
        else:
            T_pred_array[i] = tau

    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        pred_steps = int(T_pred_array[i] / dt)

        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                if idx_u < i:
                    u_hat = u[idx_u]
                else:
                    u_hat = 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        # Control action
        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]

        # Add a small continuous noise perturbation to represent biological reality
        u[i] += np.random.normal(0, 0.5)

        # Next state
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        # Energetic consequences (Free Energy Proxy: structural error + control effort)
        # Using instantaneous values
        energetic_cost[i] = 0.5 * (20.0 * x[i, 0]**2 + 0.1 * u[i]**2)

    df = pd.DataFrame({
        'Time_s': time_array,
        'T_pred_s': T_pred_array,
        'Physical_Delay_tau_s': [tau]*steps,
        'Theta_rad': x[:, 0],
        'Omega_rad_s': x[:, 1],
        'Control_Torque_Nm': u,
        'Energetic_Cost': energetic_cost
    })

    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    # Plotting
    fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    axs[0].plot(time_array, [tau]*steps, 'k--', label=r'Physical Delay $\tau$')
    axs[0].plot(time_array, T_pred_array, 'b-', linewidth=2, label=r'Cognitive Prediction $T_{pred}$')
    axs[0].set_ylabel('Time Horizon (s)', fontsize=12)
    axs[0].set_title('Transient Temporal Disruption (Derivative Gain Gap)', fontsize=14)
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)

    axs[1].plot(time_array, x[:, 0], 'r-', linewidth=1.5, label=r'Structural Perturbation $\theta$')
    axs[1].set_ylabel('Postural Angle (rad)', fontsize=12)
    axs[1].legend()
    axs[1].grid(True, alpha=0.3)

    axs[2].plot(time_array, energetic_cost, 'g-', linewidth=1.5, label='Energetic Cost (Free Energy Proxy)')
    axs[2].set_ylabel('Energetic Cost', fontsize=12)
    axs[2].set_xlabel('Time (s)', fontsize=12)
    axs[2].legend()
    axs[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

    print("Simulation complete. Saved to outputs/embodied_time/transient_temporal_disruption.csv and .png")

if __name__ == "__main__":
    setup_directories()
    simulate_transient_disruption()
