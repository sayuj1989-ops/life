import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import pandas as pd

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    """Non-linear inverted pendulum dynamics."""
    # Applying state bounding constraints to prevent scalar power overflow
    theta = np.clip(x[0], -10.0, 10.0)
    omega = np.clip(x[1], -10.0, 10.0)

    dtheta = omega
    # Equation of motion: ml^2 \ddot{\theta} = mgl \sin(\theta) + u
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    """Runge-Kutta 4 integration."""
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_agent_active_inference(tau, T_pred, precision_collapse=False, L=1.0, m=1.0, Kp_base=20.0, Kd_base=8.0, T=4.0, dt=0.01):
    """
    Simulates a predictive agent mapping Active Inference precision collapse to PID control degradation.
    """
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    pred_error = np.zeros(steps)
    precision_pi = np.ones(steps)
    kd_effective = np.ones(steps) * Kd_base

    # Initial condition: 5 degrees perturbation (0.087 rad)
    x[0] = np.array([0.087, 0.0])

    stable = True

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
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        pred_error[i] = np.linalg.norm(x_hat - x[i])

        # Active Inference mapping:
        # Precision (Pi_y) collapses if prediction error is high over time (e.g., mismatch between T_pred and tau)
        # We simulate this dynamically by reducing Precision when error is high
        if precision_collapse and i > delay_steps:
            # Simple moving average of past error
            recent_error = np.mean(pred_error[max(0, i-50):i])
            # Precision drops exponentially with sustained error
            precision_pi[i] = np.exp(-10.0 * recent_error)

        # Kd degrades linearly with precision collapse
        kd_effective[i] = Kd_base * precision_pi[i]

        # Control based on predicted state
        u[i] = -Kp_base * x_hat[0] - kd_effective[i] * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            pred_error[i:] = np.nan
            precision_pi[i:] = np.nan
            kd_effective[i:] = np.nan
            u[i:] = np.nan
            break

    # Calculate Total Energy Cost as proxy for Free Energy
    total_effort = np.sum(np.abs(np.nan_to_num(u))*dt)
    mean_error = np.nanmean(pred_error)

    return stable, total_effort, mean_error, x, u, pred_error, precision_pi, kd_effective

def exp_active_inference_collapse():
    print("Running Active Inference Time Perception Experiment...")

    # We simulate an adolescent with physical delay tau=0.22s.
    tau = 0.22
    L = 1.6

    # Case 1: Adaptive (T_pred = tau, precision maintained)
    stable_A, effort_A, err_A, x_A, u_A, pe_A, pi_A, kd_A = simulate_agent_active_inference(tau, tau, precision_collapse=True, L=L)

    # Case 2: Temporal Lag (T_pred < tau, precision collapses)
    lagging_T_pred = tau - 0.05
    stable_B, effort_B, err_B, x_B, u_B, pe_B, pi_B, kd_B = simulate_agent_active_inference(tau, lagging_T_pred, precision_collapse=True, L=L)

    # Save Results
    T = 4.0
    dt = 0.01
    time_axis = np.arange(0, T, dt)

    df = pd.DataFrame({
        'Time': time_axis,
        'Theta_Adaptive': x_A[:,0],
        'Theta_Lagging': x_B[:,0],
        'Precision_Adaptive': pi_A,
        'Precision_Lagging': pi_B,
        'Kd_Adaptive': kd_A,
        'Kd_Lagging': kd_B,
        'PredError_Adaptive': pe_A,
        'PredError_Lagging': pe_B
    })

    df.to_csv('outputs/embodied_time/active_inference_time_perception.csv', index=False)

    # Plotting
    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # Plot 1: Angle
    axs[0].plot(time_axis, x_A[:,0], 'g-', label=r'Adaptive ($T_{pred} = \tau$)')
    axs[0].plot(time_axis, x_B[:,0], 'r--', label=r'Lagging ($T_{pred} < \tau$)')
    axs[0].set_ylabel('Sway Angle (rad)')
    axs[0].set_title('Inverted Pendulum Stability')
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)

    # Plot 2: Prediction Error & Precision
    axs[1].plot(time_axis, pe_A, 'g-', alpha=0.5, label='Pred Error (Adaptive)')
    axs[1].plot(time_axis, pe_B, 'r--', alpha=0.5, label='Pred Error (Lagging)')
    ax1_twin = axs[1].twinx()
    ax1_twin.plot(time_axis, pi_A, 'g-', linewidth=2, label=r'Precision $\Pi_y$ (Adaptive)')
    ax1_twin.plot(time_axis, pi_B, 'r-', linewidth=2, label=r'Precision $\Pi_y$ (Lagging)')
    axs[1].set_ylabel('Prediction Error')
    ax1_twin.set_ylabel(r'Precision $\Pi_y$', color='b')
    axs[1].set_title('Active Inference: Prediction Error drives Precision Collapse')
    lines, labels = axs[1].get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1_twin.legend(lines + lines2, labels + labels2, loc='upper left')
    axs[1].grid(True, alpha=0.3)

    # Plot 3: Effective Damping (Kd)
    axs[2].plot(time_axis, kd_A, 'g-', label='Effective Kd (Adaptive)')
    axs[2].plot(time_axis, kd_B, 'r--', label='Effective Kd (Lagging)')
    axs[2].set_ylabel('Damping Gain $K_d$')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_title('Precision Collapse causes Derivative Gain Degradation')
    axs[2].legend()
    axs[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/active_inference_time_perception.png', dpi=300)
    plt.close()

    print("Experiment complete. Outputs saved.")

if __name__ == "__main__":
    setup_directories()
    exp_active_inference_collapse()
