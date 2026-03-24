import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

def setup_directories():
    os.makedirs('outputs/pediatric_milestones', exist_ok=True)

def dynamics(x, u, m, L, g_eff):
    """
    Computes derivatives for inverted pendulum.
    If L=0 (Supine), system is not an inverted pendulum, just mass with friction.
    """
    theta, omega = x
    dtheta = omega
    if L == 0:
        domega = u / m - 0.5 * omega # Simple damped system, no gravity destabilization
    else:
        # Equation of motion: ml^2 \ddot{\theta} = mgl \sin(\theta) + u
        domega = (g_eff / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, m, L, g_eff):
    """Runge-Kutta 4 integration."""
    k1 = dynamics(x, u, m, L, g_eff)
    k2 = dynamics(x + 0.5 * dt * k1, u, m, L, g_eff)
    k3 = dynamics(x + 0.5 * dt * k2, u, m, L, g_eff)
    k4 = dynamics(x + dt * k3, u, m, L, g_eff)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_milestone(L, m, g_eff, tau, T_pred, Kp, Kd, T=4.0, dt=0.01):
    """
    Simulates a predictive agent for a specific developmental milestone.
    Returns True if stable (did not fall past 90 degrees), False otherwise.
    Also returns the total integrated Free Energy.
    """
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    # Initial condition: 5 degrees perturbation (0.087 rad)
    x[0] = np.array([0.087, 0.0])

    stable = True
    F_total = 0.0
    alpha, beta, gamma = 1.0, 0.1, 0.01

    for i in range(steps - 1):
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
                    u_hat = 0.0 # No action assumed in the un-acted future
                x_hat = rk4(x_hat, u_hat, dt, m, L, g_eff)

        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, m, L, g_eff)

        F_total += 0.5 * (alpha * x[i, 0]**2 + beta * x[i, 1]**2 + gamma * u[i]**2) * dt

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            F_total = np.inf
            break

    return stable, F_total

def run_milestones():
    print("Running Pediatric Milestones Simulation...")

    milestones = [
        {"name": "Supine (0m)", "L": 0.0, "m": 5.0, "g_eff": 0.0, "Kp": 50.0, "Kd": 20.0, "desc": "Fully supported, no gravity penalty."},
        {"name": "Head Control (3m)", "L": 0.1, "m": 1.5, "g_eff": 9.81, "Kp": 5.0, "Kd": 2.0, "desc": "Short pendulum (head only)."},
        {"name": "Sitting (6m)", "L": 0.25, "m": 4.0, "g_eff": 9.81, "Kp": 15.0, "Kd": 5.0, "desc": "Medium pendulum (torso)."},
        {"name": "Standing (12m)", "L": 0.45, "m": 10.0, "g_eff": 9.81, "Kp": 50.0, "Kd": 15.0, "desc": "Full inverted pendulum."}
    ]

    tau = 0.18 # Constant 180ms neural delay
    T_preds = np.linspace(0.0, 0.4, 40)

    results = []

    for mstone in milestones:
        print(f"  Simulating {mstone['name']}...")
        for T_pred in T_preds:
            stable, F_total = simulate_milestone(mstone["L"], mstone["m"], mstone["g_eff"], tau, T_pred, mstone["Kp"], mstone["Kd"])
            results.append({
                'Milestone': mstone["name"],
                'T_pred': T_pred,
                'Stable': stable,
                'Free_Energy': F_total
            })

    df = pd.DataFrame(results)
    df.to_csv('outputs/pediatric_milestones/milestone_sweep.csv', index=False)

    # Plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='T_pred', y='Free_Energy', hue='Milestone', marker='o')
    plt.axvline(tau, color='k', linestyle='--', label=r'Neural Delay ($\tau = 180$ms)')

    plt.title('Ontogeny of Time Perception:\nMinimum Predictive Horizon ($T_{pred}$) across Pediatric Milestones', fontsize=14)
    plt.xlabel('Predictive Horizon $T_{pred}$ (s)', fontsize=12)
    plt.ylabel(r'Thermodynamic Free Energy $\mathcal{F}$', fontsize=12)

    # Cap y-axis for readability since unstable F_total goes to infinity
    max_finite = df.loc[df['Free_Energy'] != np.inf, 'Free_Energy'].max()
    plt.ylim(0, max_finite * 2)
    plt.xlim(0, 0.4)

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('outputs/pediatric_milestones/pediatric_time_milestones.png', dpi=300)
    plt.close()

    print("Simulation complete. Data saved to outputs/pediatric_milestones/")

if __name__ == "__main__":
    setup_directories()
    run_milestones()
