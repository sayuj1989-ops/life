import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    """Non-linear inverted pendulum dynamics."""
    theta, omega = x
    dtheta = omega
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    """Runge-Kutta 4 integration."""
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_disruption(T=10.0, dt=0.01, tau_base=0.18, T_pred_base=0.18):
    """Simulates a transient temporal disruption."""
    steps = int(T / dt)
    t_arr = np.linspace(0, T, steps)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    F = np.zeros(steps)

    # Dynamics parameters
    L = 1.0
    m = 1.0
    Kp = 20.0
    Kd = 8.0

    # Cost weights
    alpha = 1.0
    beta = 0.1
    gamma = 0.01

    x[0] = np.array([0.05, 0.0])  # Initial small perturbation

    # Growth spurt parameters for transient mismatch
    # Spurt from t=3s to t=6s
    spurt_start = 3.0
    spurt_end = 6.0

    # We will compute arrays for tau and T_pred
    tau_arr = np.ones(steps) * tau_base
    T_pred_arr = np.ones(steps) * T_pred_base

    for i, t in enumerate(t_arr):
        if spurt_start <= t <= spurt_end:
            # tau increases due to rapid physical growth
            tau_arr[i] = tau_base + 0.08 * np.sin(np.pi * (t - spurt_start) / (spurt_end - spurt_start))
            # T_pred lags behind tau
            T_pred_arr[i] = T_pred_base + 0.02 * np.sin(np.pi * (t - spurt_start) / (spurt_end - spurt_start))

    stable = True

    for i in range(steps - 1):
        tau = tau_arr[i]
        T_pred = T_pred_arr[i]

        delay_steps = int(tau / dt)
        pred_steps = int(T_pred / dt)

        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        # Predict state forward by T_pred
        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                if idx_u < i:
                    u_hat = u[idx_u]
                else:
                    u_hat = 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        # Control
        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        # Free energy
        F[i] = 0.5 * (alpha * x[i, 0]**2 + beta * x[i, 1]**2 + gamma * u[i]**2)

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            F[i+1:] = np.nan
            break

    if stable:
        F[steps-1] = 0.5 * (alpha * x[steps-1, 0]**2 + beta * x[steps-1, 1]**2 + gamma * u[steps-1]**2)

    return t_arr, x, u, F, tau_arr, T_pred_arr

def main():
    setup_directories()

    print("Simulating Transient Temporal Disruption (Derivative Gain Gap)...")
    t, x, u, F, tau, T_pred = simulate_disruption()

    df = pd.DataFrame({
        'time': t,
        'theta': x[:, 0],
        'omega': x[:, 1],
        'control_u': u,
        'free_energy': F,
        'tau': tau,
        'T_pred': T_pred,
        'derivative_gain_gap': tau - T_pred
    })

    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # Plot 1: Delay and Prediction Horizon
    axs[0].plot(t, tau, 'r-', linewidth=2, label=r'Physical Neural Delay ($\tau$)')
    axs[0].plot(t, T_pred, 'g--', linewidth=2, label=r'Cognitive Prediction Horizon ($T_{pred}$)')
    axs[0].fill_between(t, tau, T_pred, where=(tau > T_pred), color='red', alpha=0.2, label=r'Derivative Gain Gap ($\Delta T > 0$)')
    axs[0].set_ylabel('Time (s)', fontsize=12)
    axs[0].set_title('Transient Temporal Disruption during Simulated Growth Spurt', fontsize=14)
    axs[0].legend(loc='upper right')
    axs[0].grid(True, alpha=0.3)

    # Plot 2: Postural Angle (Stability)
    axs[1].plot(t, np.degrees(x[:, 0]), 'b-', linewidth=2, label='Postural Angle ($\\theta$)')
    axs[1].axhline(0, color='black', linewidth=1, linestyle='--')
    axs[1].set_ylabel('Angle (degrees)', fontsize=12)
    axs[1].legend(loc='upper right')
    axs[1].grid(True, alpha=0.3)

    # Plot 3: Free Energy
    # Filter NaNs for plotting
    mask = ~np.isnan(F)
    axs[2].plot(t[mask], F[mask], 'k-', linewidth=2, label=r'Instantaneous Free Energy ($\mathcal{F}$)')
    axs[2].set_ylabel('Free Energy Proxy', fontsize=12)
    axs[2].set_xlabel('Time (s)', fontsize=12)
    axs[2].set_yscale('log')
    axs[2].legend(loc='upper right')
    axs[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()
    print("Experiment complete. Outputs saved.")

if __name__ == "__main__":
    main()
