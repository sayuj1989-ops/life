import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
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

        inst_F = 0.5 * (alpha * x[i, 0]**2 + beta * x[i, 1]**2 + gamma * u[i]**2)
        total_F += inst_F * dt

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            total_F = 1000.0
            break

    return stable, total_F

def exp_transient_temporal_disruption():
    years = np.linspace(5, 20, 100)
    dt_years = years[1] - years[0]

    L_max = 1.7
    L_min = 0.6
    k = 1.2
    t_mid = 12.0
    L_t = L_min + (L_max - L_min) / (1 + np.exp(-k * (years - t_mid)))
    dL_dt = np.gradient(L_t, years)

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
    stable_t = np.zeros_like(years, dtype=bool)

    for i in range(len(years)):
        stable, f_cost = simulate_agent_snapshot(tau=tau_t[i], T_pred=T_pred_t[i], L=L_t[i])
        F_t[i] = f_cost
        stable_t[i] = stable
        _, f_perf = simulate_agent_snapshot(tau=tau_t[i], T_pred=tau_t[i], L=L_t[i])
        F_perfect[i] = f_perf

    df = pd.DataFrame({
        'Age_Years': years,
        'Length_L': L_t,
        'Growth_Velocity': dL_dt,
        'Physical_Delay_tau': tau_t,
        'Cognitive_T_pred': T_pred_t,
        'Temporal_Gap': gap_t,
        'Free_Energy_Cost': F_t,
        'Free_Energy_Perfect': F_perfect,
        'Stable': stable_t
    })
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    color = 'tab:blue'
    axs[0].set_ylabel('COM Height $L$ (m)', color=color, fontsize=12)
    axs[0].plot(years, L_t, color=color, linewidth=2, label='Height $L(t)$')
    axs[0].tick_params(axis='y', labelcolor=color)
    ax2 = axs[0].twinx()
    color2 = 'tab:gray'
    ax2.set_ylabel('Growth Velocity $\dot{L}$ (m/yr)', color=color2, fontsize=12)
    ax2.plot(years, dL_dt, color=color2, linestyle='--', linewidth=2, label='Velocity $\dot{L}(t)$')
    ax2.tick_params(axis='y', labelcolor=color2)
    axs[0].set_title('Adolescent Growth Spurt', fontsize=14)

    axs[1].plot(years, tau_t * 1000, 'k-', linewidth=2, label=r'Physical Delay $\tau(t)$')
    axs[1].plot(years, T_pred_t * 1000, 'b--', linewidth=2, label=r'Cognitive Horizon $T_{pred}(t)$')
    axs[1].fill_between(years, T_pred_t * 1000, tau_t * 1000, color='red', alpha=0.3, label='Derivative Gain Gap')
    axs[1].set_ylabel('Time (ms)', fontsize=12)
    axs[1].set_title('Spinal Jetlag: Transient Temporal Disruption', fontsize=14)
    axs[1].legend(loc='upper left')
    axs[1].grid(True, alpha=0.3)

    axs[2].plot(years, F_perfect, 'g--', linewidth=2, label=r'Ideal Adaptation ($T_{pred} = \tau$)')
    axs[2].plot(years, F_t, 'r-', linewidth=2.5, label=r'Lagging Adaptation ($T_{pred} < \tau$)')
    peak_gap_idx = np.argmax(gap_t)
    peak_age = years[peak_gap_idx]
    axs[2].axvline(peak_age, color='k', linestyle=':', label=f'Peak Vulnerability (Age {peak_age:.1f})')
    axs[2].set_xlabel('Age (Years)', fontsize=12)
    axs[2].set_ylabel(r'Thermodynamic Cost $\mathcal{F}$', fontsize=12)
    axs[2].set_title('The Metabolic Trap: Transient Temporal Disruption', fontsize=14)
    axs[2].legend(loc='upper left')
    axs[2].grid(True, alpha=0.3)
    max_perf = np.max(F_perfect)
    axs[2].set_ylim([0, max_perf * 5])

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    setup_directories()
    exp_transient_temporal_disruption()
