import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

def setup_directories():
    os.makedirs('outputs/pediatric_milestones', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    theta, omega = x
    dtheta = omega
    if L == 0:
        domega = u / m
    else:
        domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def compute_free_energy(theta, omega, u, alpha=1.0, beta=0.1, gamma=0.01):
    return 0.5 * (alpha * theta**2 + beta * omega**2 + gamma * u**2)

def rk4(x, u, dt, g, L, m):
    k1 = dynamics(x, u, g, L, m)
    k2 = dynamics(x + 0.5 * dt * k1, u, g, L, m)
    k3 = dynamics(x + 0.5 * dt * k2, u, g, L, m)
    k4 = dynamics(x + dt * k3, u, g, L, m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_milestone(tau, T_pred, L, m, g_eff=9.81, Kp=20.0, Kd=8.0, T=4.0, dt=0.01):
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    x[0] = np.array([0.087, 0.0]) # 5 degrees perturbation

    stable = True
    total_free_energy = 0.0
    alpha, beta, gamma = 1.0, 0.1, 0.01

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
                x_hat = rk4(x_hat, u_hat, dt, g_eff, L, m)

        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, g_eff, L, m)

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            total_free_energy = np.inf
            break

        total_free_energy += compute_free_energy(x[i, 0], x[i, 1], u[i], alpha, beta, gamma) * dt

    return stable, total_free_energy

def run_pediatric_sweep():
    milestones = [
        {"name": "Supine", "L": 0.0, "m": 5.0, "g_eff": 0.0, "Kp": 50.0, "Kd": 20.0},
        {"name": "Head Control", "L": 0.1, "m": 1.5, "g_eff": 9.81, "Kp": 3.0, "Kd": 1.0},
        {"name": "Sitting", "L": 0.3, "m": 5.0, "g_eff": 9.81, "Kp": 8.0, "Kd": 2.5},
        {"name": "Standing", "L": 0.6, "m": 10.0, "g_eff": 9.81, "Kp": 20.0, "Kd": 6.0}
    ]

    tau = 0.18 # fixed neural delay 180ms
    T_preds = np.linspace(0.0, 0.4, 41)

    results = []

    for ms in milestones:
        min_T_pred = np.inf
        for T_pred in T_preds:
            stable, F = simulate_milestone(tau, T_pred, ms['L'], ms['m'], ms['g_eff'], ms['Kp'], ms['Kd'])
            results.append({
                'Milestone': ms['name'],
                'L': ms['L'],
                'm': ms['m'],
                'T_pred': T_pred,
                'Stable': stable,
                'Free_Energy': F
            })
            # A threshold to define stability without massive oscillations
            if stable and F < 5e3 and T_pred < min_T_pred:
                min_T_pred = T_pred
        print(f"Milestone: {ms['name']} - Min T_pred for stability: {min_T_pred:.3f} s")

    df = pd.DataFrame(results)
    df.to_csv('outputs/pediatric_milestones/milestone_sweep.csv', index=False)

    # Plotting
    plt.figure(figsize=(10, 6))
    colors = ['gray', 'blue', 'orange', 'red']

    for idx, ms in enumerate(milestones):
        df_ms = df[df['Milestone'] == ms['name']]
        # filter out inf
        stable_F = df_ms[df_ms['Stable'] == True]
        plt.plot(stable_F['T_pred'], stable_F['Free_Energy'], marker='o', label=ms['name'], color=colors[idx], markersize=4)

    plt.axvline(x=0.18, color='k', linestyle='--', label=r'Neural Delay $\tau$ (180ms)')
    plt.xlabel('Predictive Horizon $T_{pred}$ (s)', fontsize=12)
    plt.ylabel(r'Total Free Energy (Action $\mathcal{S}$)', fontsize=12)
    plt.yscale('log')
    plt.title('Ontogeny of Time Perception:\nMinimum Predictive Horizon Required Across Milestones', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('outputs/pediatric_milestones/pediatric_time_milestones.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    setup_directories()
    run_pediatric_sweep()
