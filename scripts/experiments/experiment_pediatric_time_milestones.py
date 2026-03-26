import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

def setup_directories():
    os.makedirs('outputs/pediatric_milestones', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    """Non-linear inverted pendulum dynamics."""
    theta, omega = x
    dtheta = omega
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L, m):
    """Runge-Kutta 4 integration."""
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_agent(tau, T_pred, L, m, Kp=20.0, Kd=8.0, T=4.0, dt=0.01):
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    x[0] = np.array([0.087, 0.0])

    stable = True
    total_effort = 0.0

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
                x_hat = rk4(x_hat, u_hat, dt, L, m)

        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L, m)
        total_effort += abs(u[i]) * dt

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            total_effort = np.inf
            x[i+2:] = np.nan
            break

    alpha, beta, gamma = 1.0, 0.1, 0.01
    F = np.zeros(steps)
    valid_len = steps if stable else i+2
    for k in range(valid_len):
        if not np.isnan(x[k, 0]):
            F[k] = 0.5 * (alpha * x[k, 0]**2 + beta * x[k, 1]**2 + gamma * u[k]**2)

    if not stable:
        total_free_energy = np.inf
    else:
        total_free_energy = np.sum(F) * dt

    return stable, total_effort, total_free_energy

def run_milestone_sweep():
    print("Running Pediatric Milestone Sweep...")

    milestones = [
        {"name": "Supine", "L": 0.01, "m": 3.5, "tau": 0.1},
        {"name": "Head Control", "L": 0.1, "m": 6.0, "tau": 0.12},
        {"name": "Sitting", "L": 0.3, "m": 8.0, "tau": 0.15},
        {"name": "Standing", "L": 0.5, "m": 10.0, "tau": 0.18}
    ]

    T_preds = np.linspace(0.0, 0.4, 40)
    results = []

    for milestone in milestones:
        min_stable_T_pred = None
        for T_pred in T_preds:
            # Scale Kp and Kd based on mass and L to provide sufficient but not excessive control
            Kp = 50.0 * milestone['m'] * milestone['L']**2 + 5.0
            Kd = 20.0 * milestone['m'] * milestone['L']**2 + 2.0
            stable, effort, free_energy = simulate_agent(
                tau=milestone['tau'],
                T_pred=T_pred,
                L=milestone['L'],
                m=milestone['m'],
                Kp=Kp,
                Kd=Kd
            )

            results.append({
                'Milestone': milestone['name'],
                'L': milestone['L'],
                'mass': milestone['m'],
                'Neural_Delay_tau': milestone['tau'],
                'Predictive_Horizon_Tpred': T_pred,
                'Stable': int(stable),
                'Total_Free_Energy': free_energy
            })

            if stable and min_stable_T_pred is None:
                min_stable_T_pred = T_pred

    df_sweep = pd.DataFrame(results)
    df_sweep.to_csv('outputs/pediatric_milestones/milestone_sweep.csv', index=False)

    # Plot min T_pred for stability across milestones
    min_T_pred_data = df_sweep[df_sweep['Stable'] == 1].groupby('Milestone')['Predictive_Horizon_Tpred'].min().reset_index()
    # Sort by developmental order
    milestone_order = ["Supine", "Head Control", "Sitting", "Standing"]
    min_T_pred_data['Milestone'] = pd.Categorical(min_T_pred_data['Milestone'], categories=milestone_order, ordered=True)
    min_T_pred_data = min_T_pred_data.sort_values('Milestone')

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Milestone', y='Predictive_Horizon_Tpred', data=min_T_pred_data, palette='viridis')
    plt.title('Ontogeny of Time Perception: Minimum Predictive Horizon by Milestone')
    plt.ylabel('Minimum Predictive Horizon $T_{pred}$ (s)')
    plt.xlabel('Pediatric Developmental Milestone')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('outputs/pediatric_milestones/pediatric_time_milestones.png', dpi=300)
    plt.close()

    print("Pediatric Milestone Sweep complete.")

if __name__ == "__main__":
    setup_directories()
    run_milestone_sweep()
