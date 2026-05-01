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

def simulate_active_inference_agent(tau, T_pred, base_Kp=20.0, base_Kd=8.0, L=1.0, m=1.0, T=4.0, dt=0.01):
    """
    Simulates Active Inference agent where temporal mismatch causes precision collapse,
    leading to degradation of derivative gain Kd.
    """
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    # Active Inference precision logic
    # Temporal mismatch gap
    gap = max(0, tau - T_pred)

    # Precision collapses as an exponential function of the temporal gap
    # Pi_y1 maps directly to our confidence in velocity (derivative) predictions
    precision_collapse_factor = np.exp(-15.0 * gap)  # Tunable decay rate

    # Kp and Kd modulated by precision
    # Proportional gain relies on current state (less affected)
    # Derivative gain relies entirely on predictive precision
    effective_Kp = base_Kp * (0.8 + 0.2 * precision_collapse_factor)
    effective_Kd = base_Kd * precision_collapse_factor

    x[0] = np.array([0.087, 0.0])  # Initial perturbation (5 degrees)

    stable = True
    total_effort = 0.0

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
                    u_hat = 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        # Control action based on degraded precision gains
        u[i] = -effective_Kp * x_hat[0] - effective_Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        total_effort += abs(u[i]) * dt

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            total_effort = 1000.0  # Penalty
            break

    return stable, effective_Kd, precision_collapse_factor, total_effort

def run_experiment():
    print("Running Active Inference Time Perception Experiment...")
    tau = 0.18  # 180ms typical physical delay

    T_preds = np.linspace(0.0, 0.2, 50)

    results = []

    for T_pred in T_preds:
        stable, eff_Kd, precision, effort = simulate_active_inference_agent(tau, T_pred)

        results.append({
            'T_pred': T_pred,
            'Physical_Delay_tau': tau,
            'Temporal_Gap': tau - T_pred,
            'Precision_Pi_y1': precision,
            'Effective_Kd': eff_Kd,
            'Control_Effort': effort,
            'Stable': stable
        })

    df = pd.DataFrame(results)
    df.to_csv('outputs/embodied_time/active_inference_time_perception.csv', index=False)

    # Plotting
    fig, axs = plt.subplots(2, 1, figsize=(8, 10), sharex=True)

    axs[0].plot(df['Temporal_Gap'] * 1000, df['Precision_Pi_y1'], 'b-', linewidth=2, label=r'Precision $\Pi_{y,1}$')
    axs[0].set_ylabel('Active Inference Precision', fontsize=12)
    axs[0].set_title('Precision Collapse due to Temporal Mismatch', fontsize=14)
    axs[0].grid(True, alpha=0.3)
    axs[0].legend()

    axs[1].plot(df['Temporal_Gap'] * 1000, df['Effective_Kd'], 'r-', linewidth=2, label=r'Effective Derivative Gain $K_d$')

    # Mark instability region
    unstable_gaps = df[~df['Stable']]['Temporal_Gap'] * 1000
    if len(unstable_gaps) > 0:
        axs[1].axvspan(unstable_gaps.min(), unstable_gaps.max(), color='red', alpha=0.2, label='Unstable Region')

    axs[1].set_xlabel('Temporal Mismatch Gap $\\tau - T_{pred}$ (ms)', fontsize=12)
    axs[1].set_ylabel('Derivative Gain $K_d$', fontsize=12)
    axs[1].set_title('PID Control Degradation', fontsize=14)
    axs[1].grid(True, alpha=0.3)
    axs[1].legend()

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/active_inference_time_perception.png', dpi=300)
    plt.close()
    print("Experiment complete.")

if __name__ == "__main__":
    setup_directories()
    run_experiment()
