import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    theta, omega = x
    dtheta = omega
    if L == 0:
        domega = 0.0
    else:
        domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_agent_snapshot(tau, T_pred, L=1.0, m=1.0, T=4.0, dt=0.01):
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    Kp = 20.0 * max(0.1, (L/1.0))
    Kd = 8.0 * max(0.1, (L/1.0))

    x[0] = np.array([0.087, 0.0])

    stable = True
    alpha, beta, gamma = 1.0, 0.1, 0.01
    total_F = 0.0
    max_theta = abs(x[0, 0])

    for i in range(steps - 1):
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

        current_theta = abs(x[i+1, 0])
        if current_theta > max_theta:
            max_theta = current_theta

        inst_F = 0.5 * (alpha * x[i, 0]**2 + beta * x[i, 1]**2 + gamma * u[i]**2)
        total_F += inst_F * dt

        if current_theta > np.pi/2:
            stable = False
            total_F = 1000.0
            break

    return stable, total_F, max_theta

def exp_transient_temporal_disruption():
    print("Running Transient Temporal Disruption (Derivative Gain Gap) Simulation...")

    years = np.linspace(5, 20, 100)
    dt_years = years[1] - years[0]

    L_max = 1.7
    L_min = 0.6
    k = 1.2
    t_mid = 12.0

    L_t = L_min + (L_max - L_min) / (1 + np.exp(-k * (years - t_mid)))

    tau_0 = 0.05
    v = 15.0
    tau_t = tau_0 + L_t / v

    tau_adapt = 1.5

    T_pred_t = np.zeros_like(years)
    T_pred_t[0] = tau_t[0]

    for i in range(1, len(years)):
        dT_pred = (1.0 / tau_adapt) * (tau_t[i-1] - T_pred_t[i-1]) * dt_years
        T_pred_t[i] = T_pred_t[i-1] + dT_pred

    gap_t = tau_t - T_pred_t

    F_t = np.zeros_like(years)
    F_perfect = np.zeros_like(years)
    max_theta_t = np.zeros_like(years)
    max_theta_perfect = np.zeros_like(years)
    stable_t = np.zeros_like(years, dtype=bool)

    for i in range(len(years)):
        stable, f_cost, m_theta = simulate_agent_snapshot(tau=tau_t[i], T_pred=T_pred_t[i], L=L_t[i])
        F_t[i] = f_cost
        max_theta_t[i] = m_theta
        stable_t[i] = stable

        _, f_perf, m_theta_perf = simulate_agent_snapshot(tau=tau_t[i], T_pred=tau_t[i], L=L_t[i])
        F_perfect[i] = f_perf
        max_theta_perfect[i] = m_theta_perf

    df = pd.DataFrame({
        'Age_Years': years,
        'Length_L': L_t,
        'Physical_Delay_tau': tau_t,
        'Cognitive_T_pred': T_pred_t,
        'Temporal_Gap': gap_t,
        'Free_Energy_Cost': F_t,
        'Free_Energy_Perfect': F_perfect,
        'Max_Sway_Angle': max_theta_t,
        'Max_Sway_Angle_Perfect': max_theta_perfect,
        'Stable': stable_t
    })
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    axs[0].plot(years, tau_t * 1000, 'k-', linewidth=2, label=r'Neural Delay $\tau(t)$ (msec)')
    axs[0].plot(years, T_pred_t * 1000, 'b--', linewidth=2, label=r'Internal Predictive Horizon $T_{pred}(t)$')
    axs[0].fill_between(years, T_pred_t * 1000, tau_t * 1000, color='red', alpha=0.3, label='Derivative Gain Gap')
    axs[0].set_ylabel('Time (ms)', fontsize=12)
    axs[0].set_title('Transient Temporal Disruption (The Gap)', fontsize=14)
    axs[0].legend(loc='upper left')
    axs[0].grid(True, alpha=0.3)

    axs[1].plot(years, np.degrees(max_theta_perfect), 'g--', linewidth=2, label=r'Ideal Postural Sway ($T_{pred} = \tau$)')
    axs[1].plot(years, np.degrees(max_theta_t), 'r-', linewidth=2.5, label=r'Perturbed Sway ($T_{pred} < \tau$)')
    axs[1].set_ylabel('Max Sway Angle (deg)', fontsize=12)
    axs[1].set_title('Structural Consequences: Increased Sway Amplitude', fontsize=14)
    axs[1].legend(loc='upper left')
    axs[1].grid(True, alpha=0.3)
    max_perf_sway = np.max(np.degrees(max_theta_perfect))
    if np.any(np.degrees(max_theta_t) > 90):
        axs[1].set_ylim([0, 95])
    else:
        axs[1].set_ylim([0, np.max(np.degrees(max_theta_t)) * 1.2])

    axs[2].plot(years, F_perfect, 'g--', linewidth=2, label=r'Ideal Energy Cost')
    axs[2].plot(years, F_t, 'r-', linewidth=2.5, label=r'Disrupted Energy Cost')
    peak_gap_idx = np.argmax(gap_t)
    peak_age = years[peak_gap_idx]
    axs[2].axvline(peak_age, color='k', linestyle=':', label=f'Peak Gap (Age {peak_age:.1f})')
    axs[2].set_xlabel('Age (Years)', fontsize=12)
    axs[2].set_ylabel('Thermodynamic Cost', fontsize=12)
    axs[2].set_title('Energetic Consequences: Free Energy Spike', fontsize=14)
    axs[2].legend(loc='upper left')
    axs[2].grid(True, alpha=0.3)
    max_perf = np.max(F_perfect)
    axs[2].set_ylim([0, max_perf * 5])

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

    print("Experiment complete. Saved to outputs/embodied_time/transient_temporal_disruption.csv and .png")

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('Agg')
    setup_directories()
    exp_transient_temporal_disruption()
