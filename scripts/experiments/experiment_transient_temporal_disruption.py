import numpy as np
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

def run_transient_disruption_sim():
    print("Running Transient Temporal Disruption Simulation...")

    T = 15.0
    dt = 0.01
    steps = int(T / dt)
    t = np.linspace(0, T, steps)

    tau_base = 0.15
    T_pred_base = 0.15

    tau_t = np.full(steps, tau_base)
    disruption_idx = (t >= 3.0) & (t <= 8.0)
    tau_t[disruption_idx] = 0.25

    T_pred_t = np.zeros(steps)
    T_pred_t[0] = T_pred_base
    tau_adapt = 1.5

    for i in range(1, steps):
        dT_pred = (1.0 / tau_adapt) * (tau_t[i-1] - T_pred_t[i-1]) * dt
        T_pred_t[i] = T_pred_t[i-1] + dT_pred

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    Kp = 25.0
    Kd = 10.0
    L = 1.0
    m = 1.0

    x[0] = np.array([0.05, 0.0])

    alpha, beta, gamma = 1.0, 0.1, 0.01
    F = np.zeros(steps)

    stable = True

    for i in range(steps - 1):
        delay_steps = int(tau_t[i] / dt)
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        pred_steps = int(T_pred_t[i] / dt)

        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                u_hat = u[idx_u] if idx_u < i else 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        F[i] = 0.5 * (alpha * x[i, 0]**2 + beta * x[i, 1]**2 + gamma * u[i]**2)

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            F[i+1:] = np.nan
            x[i+2:] = np.nan
            print(f"System collapsed at t={t[i]:.2f}s due to transient temporal disruption!")
            break

    df = pd.DataFrame({
        'Time_s': t,
        'Physical_Delay_tau': tau_t,
        'Cognitive_T_pred': T_pred_t,
        'Temporal_Gap': tau_t - T_pred_t,
        'Theta_rad': x[:, 0],
        'Control_Torque_u': u,
        'Free_Energy_F': F
    })
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    axs[0].plot(t, tau_t * 1000, 'k-', label=r'Physical Delay $\tau(t)$')
    axs[0].plot(t, T_pred_t * 1000, 'b--', label=r'Cognitive Horizon $T_{pred}(t)$')
    axs[0].fill_between(t, T_pred_t * 1000, tau_t * 1000, color='red', alpha=0.3, label='Derivative Gain Gap')
    axs[0].set_ylabel('Time (ms)')
    axs[0].set_title('Transient Temporal Disruption (Derivative Gain Gap)')
    axs[0].legend(loc='upper right')
    axs[0].grid(True)

    axs[1].plot(t, np.degrees(x[:, 0]), 'g-', label=r'Postural Angle $\theta$')
    axs[1].axhline(90, color='r', linestyle=':', alpha=0.5)
    axs[1].axhline(-90, color='r', linestyle=':', alpha=0.5)
    axs[1].set_ylabel('Angle (degrees)')
    axs[1].set_title('Structural Consequence (Loss of Stability)')
    axs[1].legend(loc='upper left')
    axs[1].grid(True)

    axs[2].plot(t, F, 'r-', label=r'Thermodynamic Free Energy $\mathcal{F}$')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Energy')
    axs[2].set_title('Energetic Cost of Temporal Mismatch')
    axs[2].legend(loc='upper left')
    axs[2].grid(True)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    setup_directories()
    run_transient_disruption_sim()
