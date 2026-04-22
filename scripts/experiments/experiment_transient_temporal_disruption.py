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

def simulate_transient_disruption(T_total=20.0, dt=0.01, L=1.0, m=1.0, Kp=20.0, Kd=8.0, k_adapt=2.0):
    """
    Simulates a period of rapid adolescent growth causing a transient mismatch
    between physical neural delay (tau) and cognitive predictive horizon (T_pred).
    """
    steps = int(T_total / dt)
    time = np.linspace(0, T_total, steps)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    # Baseline stable state
    tau_history = np.zeros(steps)
    T_pred_history = np.zeros(steps)
    free_energy = np.zeros(steps)

    tau_base = 0.15
    T_pred_base = 0.15

    # Growth spurt parameters
    growth_start = 5.0
    growth_end = 10.0
    tau_max = 0.22

    # Initial perturbation
    x[0] = np.array([0.05, 0.0])

    T_pred = T_pred_base

    for i in range(steps - 1):
        t = time[i]

        # 1. Physical Growth Dynamics (tau increases rapidly during growth spurt)
        if t < growth_start:
            tau = tau_base
        elif t < growth_end:
            progress = (t - growth_start) / (growth_end - growth_start)
            # Smooth step increase
            tau = tau_base + (tau_max - tau_base) * (1 - np.cos(progress * np.pi)) / 2
        else:
            tau = tau_max

        tau_history[i] = tau

        # 2. Cognitive Adaptation Dynamics (T_pred tries to catch up)
        dT_pred = k_adapt * (tau - T_pred) * dt
        T_pred += dT_pred
        T_pred_history[i] = T_pred

        # The Derivative Gain Gap
        delta_T = tau - T_pred

        # 3. Control loop with current tau and T_pred
        delay_steps = max(1, int(tau / dt))
        pred_steps = max(0, int(T_pred / dt))

        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        # Predict forward
        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                u_hat = u[idx_u] if idx_u < i else 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        # Calculate proxy for Free Energy (Prediction Error + Control Effort)
        pred_error = np.linalg.norm(x_hat - x[i])

        # Apply PD control
        # If delta_T is large, it's equivalent to degraded Kd
        effective_Kd = Kd * np.exp(-10.0 * max(0, delta_T))

        u[i] = -Kp * x_hat[0] - effective_Kd * x_hat[1]

        # Add a small continuous noise to keep the system active
        u[i] += np.random.normal(0, 0.5)

        # Advance physics
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        # Calculate instantaneous free energy cost
        free_energy[i] = pred_error + 0.1 * np.abs(u[i])

        # Cap instability for plotting purposes if it completely falls
        if abs(x[i+1, 0]) > np.pi/2:
            x[i+1, 0] = np.sign(x[i+1, 0]) * np.pi/2
            free_energy[i] = 10.0

    # Fill last elements
    tau_history[-1] = tau_history[-2]
    T_pred_history[-1] = T_pred_history[-2]
    free_energy[-1] = free_energy[-2]

    return time, x, u, tau_history, T_pred_history, free_energy

def run_experiment():
    print("Running Transient Temporal Disruption Experiment...")
    setup_directories()

    # Run simulation with standard adaptation rate
    time, x, u, tau, T_pred, F = simulate_transient_disruption(T_total=20.0, k_adapt=0.5)

    # Run a faster adaptation baseline to show contrast
    _, _, _, _, T_pred_fast, F_fast = simulate_transient_disruption(T_total=20.0, k_adapt=5.0)

    # Save CSV
    df = pd.DataFrame({
        'Time': time,
        'Theta': x[:, 0],
        'Omega': x[:, 1],
        'Control_U': u,
        'Delay_tau': tau,
        'Pred_Horizon_T_pred': T_pred,
        'Derivative_Gain_Gap': tau - T_pred,
        'Free_Energy': F,
        'Free_Energy_FastAdapt': F_fast
    })
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    # Plotting
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # Plot 1: Temporal Mismatch
    axes[0].plot(time, tau, 'k--', linewidth=2, label=r'Physical Delay $\tau$ (Growth)')
    axes[0].plot(time, T_pred, 'r-', linewidth=2, label=r'Cognitive Horizon $T_{pred}$ (Slow Adapt)')
    axes[0].plot(time, T_pred_fast, 'g:', linewidth=2, label=r'Cognitive Horizon $T_{pred}$ (Fast Adapt)')
    axes[0].fill_between(time, T_pred, tau, where=(tau > T_pred), color='red', alpha=0.2, label='Derivative Gain Gap')
    axes[0].set_ylabel('Time Horizon (s)')
    axes[0].set_title('Transient Temporal Disruption during Growth Spurt', fontsize=12)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: Structural Consequence (Postural Instability)
    axes[1].plot(time, np.degrees(x[:, 0]), 'b-', linewidth=1.5)
    axes[1].set_ylabel('Postural Angle (deg)')
    axes[1].set_title('Structural Consequence: Amplified Oscillatory Perturbations', fontsize=12)
    axes[1].grid(True, alpha=0.3)

    # Plot 3: Thermodynamic Consequence (Free Energy)
    # Smooth the free energy signal for cleaner visualization
    window = 50
    F_smooth = np.convolve(F, np.ones(window)/window, mode='same')
    F_fast_smooth = np.convolve(F_fast, np.ones(window)/window, mode='same')

    axes[2].plot(time, F_smooth, 'r-', linewidth=2, label='Thermodynamic Cost (Gap)')
    axes[2].plot(time, F_fast_smooth, 'g--', linewidth=2, label='Thermodynamic Cost (No Gap)')
    axes[2].set_ylabel('Free Energy Proxy\n(Error + Effort)')
    axes[2].set_xlabel('Simulation Time (s)')
    axes[2].set_title('Thermodynamic Consequence: Spike in Free Energy during Gap', fontsize=12)
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

    print("Experiment complete. Outputs saved to outputs/embodied_time/")

if __name__ == "__main__":
    run_experiment()
