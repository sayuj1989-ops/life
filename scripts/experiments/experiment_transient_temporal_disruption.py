import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib

# Use Agg backend for headless environments
matplotlib.use('Agg')

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    theta, omega = x
    dtheta = omega
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_transient_disruption(T=10.0, dt=0.01):
    steps = int(T / dt)
    t = np.linspace(0, T, steps)

    L = 1.5
    m = 1.0
    Kp = 30.0
    Kd = 10.0

    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    F = np.zeros(steps)

    x[0] = np.array([0.05, 0.0])

    disruption_start = 3.0
    disruption_end = 6.0
    max_tau = 0.25
    base_tau = 0.10

    tau_t = np.ones(steps) * base_tau

    for i in range(steps):
        if disruption_start <= t[i] <= disruption_end:
            mid = (disruption_start + disruption_end) / 2
            width = (disruption_end - disruption_start) / 2
            spike = 1.0 - ((t[i] - mid) / width)**2
            tau_t[i] = base_tau + (max_tau - base_tau) * spike

    T_pred = base_tau

    alpha, beta, gamma = 1.0, 0.1, 0.01

    for i in range(steps - 1):
        delay_steps = int(tau_t[i] / dt)
        pred_steps = int(T_pred / dt)

        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                if idx_u < i:
                    u_hat = u[idx_u]
                else:
                    u_hat = 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        F[i] = 0.5 * (alpha * x[i, 0]**2 + beta * x[i, 1]**2 + gamma * u[i]**2)

        if abs(x[i+1, 0]) > np.pi/2:
            F[i+1:] = np.nan
            x[i+1:, :] = np.nan
            break

    if not np.isnan(F[-1]):
        F[-1] = 0.5 * (alpha * x[-1, 0]**2 + beta * x[-1, 1]**2 + gamma * u[-1]**2)

    return t, x, u, F, tau_t, T_pred

def run_experiment():
    print("Running transient temporal disruption simulation...")
    t, x, u, F, tau_t, T_pred = simulate_transient_disruption()

    df = pd.DataFrame({
        'Time_s': t,
        'Theta_rad': x[:, 0],
        'Omega_rad_s': x[:, 1],
        'Control_Torque_u': u,
        'Free_Energy_F': F,
        'Physical_Delay_tau': tau_t,
        'Cognitive_Horizon_Tpred': [T_pred]*len(t)
    })
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    axs[0].plot(t, tau_t * 1000, 'r-', linewidth=2, label=r'Physical Delay $\tau(t)$')
    axs[0].axhline(T_pred * 1000, color='b', linestyle='--', linewidth=2, label=r'Cognitive Horizon $T_{pred}$')
    axs[0].fill_between(t, T_pred * 1000, tau_t * 1000, where=(tau_t > T_pred), color='red', alpha=0.3, label='Derivative Gain Gap')
    axs[0].set_ylabel('Time (ms)', fontsize=12)
    axs[0].set_title('Transient Temporal Disruption (Derivative Gain Gap)', fontsize=14)
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)

    axs[1].plot(t, np.degrees(x[:, 0]), 'k-', linewidth=2, label='Postural Angle $\\theta$')
    axs[1].axhline(0, color='gray', linestyle='--')
    axs[1].set_ylabel('Angle (degrees)', fontsize=12)
    axs[1].set_title('Structural Consequences: Loss of Stability', fontsize=14)
    axs[1].legend()
    axs[1].grid(True, alpha=0.3)

    axs[2].plot(t, F, 'g-', linewidth=2, label=r'Free Energy $\mathcal{F}(t)$')
    axs[2].set_ylabel('Free Energy', fontsize=12)
    axs[2].set_xlabel('Time (s)', fontsize=12)
    axs[2].set_title('Energetic Consequences: Thermodynamic Cost Spike', fontsize=14)
    axs[2].set_yscale('log')
    axs[2].legend()
    axs[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

    print("Saved to outputs/embodied_time/transient_temporal_disruption.csv and .png")

if __name__ == "__main__":
    setup_directories()
    run_experiment()
