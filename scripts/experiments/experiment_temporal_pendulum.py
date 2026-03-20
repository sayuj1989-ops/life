import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

def setup_directories():
    os.makedirs('outputs/temporal_pendulum', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    """Non-linear inverted pendulum dynamics."""
    theta, omega = x
    dtheta = omega
    # Equation of motion: ml^2 \ddot{\theta} = mgl \sin(\theta) + u
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt):
    """Runge-Kutta 4 integration."""
    k1 = dynamics(x, u)
    k2 = dynamics(x + 0.5 * dt * k1, u)
    k3 = dynamics(x + 0.5 * dt * k2, u)
    k4 = dynamics(x + dt * k3, u)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_agent(tau, T_pred, Kp=20.0, Kd=8.0, T=4.0, dt=0.01):
    """
    Simulates a predictive agent with a specific neural delay (tau) and predictive horizon (T_pred).
    Returns True if stable (did not fall past 90 degrees), False otherwise.
    Also returns the total control effort.
    """
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    # Initial condition: 5 degrees perturbation (0.087 rad)
    x[0] = np.array([0.087, 0.0])

    stable = True
    total_effort = 0.0

    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        # Predict state forward by T_pred
        x_hat = np.copy(x_obs)
        # Fast path if T_pred == 0
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                if idx_u < i:
                    u_hat = u[idx_u]
                else:
                    u_hat = 0.0 # No action assumed in the un-acted future
                x_hat = rk4(x_hat, u_hat, dt)

        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt)
        total_effort += abs(u[i]) * dt

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            total_effort = np.inf
            break

    return stable, total_effort

def run_simulation():
    # Initial test baseline
    g = 9.81
    L = 1.0     # ~COM height of a human
    m = 1.0     # Normalized mass
    tau = 0.18  # 180ms neural delay
    dt = 0.01   # 10ms discrete time step
    T = 4.0     # Simulation duration

    steps = int(T / dt)
    delay_steps = int(tau / dt)

    Kp = 20.0
    Kd = 8.0

    t = np.linspace(0, T, steps)

    x_ideal = np.zeros((steps, 2))
    x_naive = np.zeros((steps, 2))
    x_pred  = np.zeros((steps, 2))

    u_ideal = np.zeros(steps)
    u_naive = np.zeros(steps)
    u_pred  = np.zeros(steps)

    pred_error = np.zeros(steps)

    x0 = np.array([0.087, 0.0])
    x_ideal[0] = x_naive[0] = x_pred[0] = x0

    for i in range(steps - 1):
        u_ideal[i] = -Kp * x_ideal[i, 0] - Kd * x_ideal[i, 1]
        x_ideal[i+1] = rk4(x_ideal[i], u_ideal[i], dt)

        obs_idx = max(0, i - delay_steps)
        x_obs_naive = x_naive[obs_idx]
        u_naive[i] = -Kp * x_obs_naive[0] - Kd * x_obs_naive[1]
        x_naive[i+1] = rk4(x_naive[i], u_naive[i], dt)

        if abs(x_naive[i+1, 0]) > np.pi/2:
            x_naive[i+1:] = np.nan

        if np.isnan(x_pred[i, 0]):
            continue

        x_obs_pred = x_pred[obs_idx]

        x_hat = np.copy(x_obs_pred)
        for j in range(obs_idx, i):
            x_hat = rk4(x_hat, u_pred[j], dt)

        pred_error[i] = np.linalg.norm(x_hat - x_pred[i])

        u_pred[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x_pred[i+1] = rk4(x_pred[i], u_pred[i], dt)

        if abs(x_pred[i+1, 0]) > np.pi/2:
            x_pred[i+1:] = np.nan

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.title(r'Inverted Pendulum Stability: The Computational Necessity of "Time Perception"', fontsize=14)
    plt.plot(t, np.degrees(x_ideal[:, 0]), 'g--', label=r'Ideal Baseline ($\tau=0$ms)')
    plt.plot(t, np.degrees(x_naive[:, 0]), 'r-', linewidth=2, label=r'Reactive Agent ($\tau=180$ms, No Prediction)')
    plt.plot(t, np.degrees(x_pred[:, 0]), 'b-', linewidth=2, label=r'Predictive Agent ($\tau=180$ms, Forward Model)')
    plt.axhline(90, color='k', linestyle=':', alpha=0.5)
    plt.axhline(-90, color='k', linestyle=':', alpha=0.5)
    plt.ylabel('Postural Angle $\\theta$ (degrees)', fontsize=12)
    plt.xlim([0, T])
    plt.ylim([-100, 100])
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper right')

    plt.subplot(2, 1, 2)
    plt.title('Control Effort / Free Energy (Action History)', fontsize=14)
    plt.plot(t, u_ideal, 'g--', label='Ideal Effort')
    plt.plot(t, u_naive, 'r-', alpha=0.7, label='Reactive Effort (Oscillatory divergence)')
    plt.plot(t, u_pred, 'b-', label='Predictive Effort')
    plt.ylabel('Torque $u(t)$ (Nm)', fontsize=12)
    plt.xlabel('Time (s)', fontsize=12)
    plt.xlim([0, T])
    plt.ylim([-50, 50])
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig('outputs/temporal_pendulum/time_perception_necessity.png', dpi=300)
    plt.close()

    df = pd.DataFrame({
        'time': t,
        'theta_ideal': x_ideal[:, 0],
        'theta_naive': x_naive[:, 0],
        'theta_pred': x_pred[:, 0],
        'u_naive': u_naive,
        'u_pred': u_pred
    })
    df.to_csv('outputs/temporal_pendulum/temporal_simulation.csv', index=False)

    print("Baseline simulation complete.")

def run_temporal_sweep():
    print("Running Temporal Sweep (Neural Delay vs Predictive Horizon)...")

    # Reduced grid size for faster simulation
    taus = np.linspace(0.0, 0.4, 20) # 0 to 400ms delay
    T_preds = np.linspace(0.0, 0.4, 20) # 0 to 400ms prediction horizon

    results = []

    for tau in taus:
        for T_pred in T_preds:
            stable, effort = simulate_agent(tau, T_pred)
            results.append({
                'Neural_Delay_tau': tau,
                'Predictive_Horizon_Tpred': T_pred,
                'Stable': int(stable),
                'Control_Effort': effort
            })

    df_sweep = pd.DataFrame(results)
    df_sweep.to_csv('outputs/temporal_pendulum/temporal_sweep.csv', index=False)

    # Plot Phase Diagram Heatmap
    plt.figure(figsize=(10, 8))

    # Create pivot table for heatmap
    heatmap_data = df_sweep.pivot(index='Neural_Delay_tau', columns='Predictive_Horizon_Tpred', values='Stable')
    # Reverse index to have 0 delay at the bottom
    heatmap_data = heatmap_data.iloc[::-1]

    ax = sns.heatmap(heatmap_data, cmap='RdYlGn', cbar=False,
                xticklabels=np.round(heatmap_data.columns, 2),
                yticklabels=np.round(heatmap_data.index, 2))

    plt.title('Phase Diagram: The "Zone of Life"\n(Green = Stable, Red = Unstable)', fontsize=16)
    plt.xlabel('Predictive Horizon ($T_{pred}$) [s]', fontsize=14)
    plt.ylabel('Neural Delay ($\\tau$) [s]', fontsize=14)

    # Add a diagonal line for T_pred = tau
    x_lims = ax.get_xlim()
    y_lims = ax.get_ylim()
    # the heatmap coordinates go from 0 to 20.
    # The line T_pred = tau corresponds to drawing a line from bottom left to top right
    ax.plot([x_lims[0], x_lims[1]], [y_lims[0], y_lims[1]], 'k--', linewidth=2, label='Perfect Prediction ($T_{pred} = \\tau$)')

    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig('outputs/temporal_pendulum/temporal_phase_diagram.png', dpi=300)
    plt.close()

    print("Temporal Sweep complete. Data saved to outputs/temporal_pendulum/temporal_sweep.csv and heatmap generated.")

if __name__ == "__main__":
    setup_directories()
    run_simulation()
    run_temporal_sweep()
