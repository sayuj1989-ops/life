import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    """Non-linear inverted pendulum dynamics."""
    theta, omega = x
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

def simulate_transient_disruption(tau=0.18, T=6.0, dt=0.01, disruption_start=2.0, disruption_end=3.5, disruption_T_pred=0.12):
    """
    Simulates a predictive agent experiencing a transient 'Derivative Gain Gap'
    where the cognitive predictive horizon T_pred temporarily drops below physical delay tau.
    """
    steps = int(T / dt)
    delay_steps = int(tau / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    F = np.zeros(steps)
    T_pred_history = np.zeros(steps)

    # Agent parameters
    L = 1.0
    m = 1.0
    Kp = 20.0
    Kd = 8.0

    # Free Energy weights
    alpha = 1.0
    beta = 0.1
    gamma = 0.01

    # Initial condition: small persistent perturbation to keep the agent working
    x[0] = np.array([0.05, 0.0]) # ~2.8 degrees

    stable = True

    for i in range(steps - 1):
        t_current = i * dt

        # Determine current T_pred
        if disruption_start <= t_current <= disruption_end:
            T_pred_current = disruption_T_pred # Disrupted cognitive horizon (T_pred < tau)
        else:
            T_pred_current = tau # Ideal cognitive horizon (T_pred == tau)

        T_pred_history[i] = T_pred_current
        pred_steps = int(T_pred_current / dt)

        # Observation is delayed
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        # Forward internal model prediction
        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                if idx_u < i:
                    u_hat = u[idx_u]
                else:
                    u_hat = 0.0 # Un-acted future
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        # Apply control effort based on predicted state
        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]

        # Add a constant tiny perturbance mimicking gravity/respiration micro-movements
        # to ensure the system is continuously active
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m) + np.array([0.0005, 0.0])

        # Compute Instantaneous Free Energy cost proxy
        F[i] = 0.5 * (alpha * x[i, 0]**2 + beta * x[i, 1]**2 + gamma * u[i]**2)

        # Check for structural failure
        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            F[i+1:] = np.nan
            x[i+1:, 0] = np.nan
            break

    # Calculate last state if stable
    if stable:
        T_pred_history[steps-1] = tau
        F[steps-1] = 0.5 * (alpha * x[steps-1, 0]**2 + beta * x[steps-1, 1]**2 + gamma * u[steps-1]**2)

    return stable, x, u, F, T_pred_history

def exp_transient_temporal_disruption():
    print("Running Transient Temporal Disruption Simulation...")

    T = 6.0
    dt = 0.01
    t = np.linspace(0, T, int(T/dt))

    # Scenario 1: Unperturbed (Ideal adaptation, always T_pred == tau)
    # We set disruption parameters to never trigger
    _, x_ideal, u_ideal, F_ideal, _ = simulate_transient_disruption(T=T, dt=dt, disruption_start=10.0, disruption_end=11.0)

    # Scenario 2: Transient Disruption (Derivative Gain Gap)
    # T_pred drops to 120ms (below tau=180ms) from t=2.0 to 3.5s
    stable, x_disrupted, u_disrupted, F_disrupted, T_pred_hist = simulate_transient_disruption(T=T, dt=dt, disruption_start=2.0, disruption_end=3.5, disruption_T_pred=0.12)

    # Save to CSV
    df = pd.DataFrame({
        'Time_s': t,
        'T_pred_disrupted': T_pred_hist,
        'Theta_Ideal': x_ideal[:, 0],
        'Theta_Disrupted': x_disrupted[:, 0],
        'Effort_Ideal': u_ideal,
        'Effort_Disrupted': u_disrupted,
        'F_Ideal': F_ideal,
        'F_Disrupted': F_disrupted
    })
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    # Plotting
    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # Disruption highlighting function
    def highlight_disruption(ax):
        ax.axvspan(2.0, 3.5, color='red', alpha=0.1, label='Temporal Disruption\n(Derivative Gain Gap)')
        ax.axvline(2.0, color='r', linestyle=':', alpha=0.5)
        ax.axvline(3.5, color='r', linestyle=':', alpha=0.5)

    # Top Panel: Postural Angle (Structural Consequence)
    axs[0].plot(t, np.degrees(x_ideal[:, 0]), 'g--', linewidth=2, label='Ideal Stability ($T_{pred} = \\tau$)')
    axs[0].plot(t, np.degrees(x_disrupted[:, 0]), 'r-', linewidth=2.5, label='Disrupted Agent')
    highlight_disruption(axs[0])
    axs[0].set_ylabel('Postural Angle $\\theta$ (degrees)', fontsize=12)
    axs[0].set_title('Structural Consequence of Transient Temporal Mismatch', fontsize=14)
    axs[0].legend(loc='upper right')
    axs[0].grid(True, alpha=0.3)

    # Middle Panel: Control Effort
    axs[1].plot(t, u_ideal, 'g--', linewidth=2, label='Ideal Control Torque')
    axs[1].plot(t, u_disrupted, 'b-', linewidth=2.5, label='Disrupted Control Torque')
    highlight_disruption(axs[1])
    axs[1].set_ylabel('Active Torque $u(t)$ (Nm)', fontsize=12)
    axs[1].set_title('Metabolic Overcompensation During Delay Mismatch', fontsize=14)
    axs[1].legend(loc='upper right')
    axs[1].grid(True, alpha=0.3)

    # Bottom Panel: Thermodynamic Free Energy
    # Use log scale to show the massive spike during the gap
    axs[2].plot(t, F_ideal, 'g--', linewidth=2, label='Bounded Free Energy Attractor')
    axs[2].plot(t, F_disrupted, 'm-', linewidth=2.5, label='Thermodynamic Spike $\\mathcal{F}(t)$')
    highlight_disruption(axs[2])
    axs[2].set_xlabel('Time (s)', fontsize=12)
    axs[2].set_ylabel(r'Thermodynamic Free Energy $\mathcal{F}(t)$', fontsize=12)
    axs[2].set_title('The Energy Deficit Window: Diverging Free Energy', fontsize=14)
    axs[2].legend(loc='upper left')
    axs[2].grid(True, alpha=0.3)
    axs[2].set_yscale('log')

    # Add text annotation
    axs[2].text(2.1, np.nanmax(F_disrupted)*0.01,
                'Derivative Gain Gap ($T_{pred} < \\tau$):\nExponential divergence of required energy.\nSystem must break symmetry to survive.',
                fontsize=11, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

    print("Transient Disruption Simulation complete. Saved to outputs/embodied_time/transient_temporal_disruption.csv and .png")

if __name__ == "__main__":
    setup_directories()
    exp_transient_temporal_disruption()
