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

def simulate_agent_disruption(tau, T_pred, disruption_onset, disruption_duration, L=1.0, m=1.0, T=10.0, dt=0.01):
    steps = int(T / dt)
    delay_steps = int(tau / dt)

    # Normally T_pred matches tau.
    pred_steps_normal = int(T_pred / dt)

    # During disruption, the model lags (say drops to T_pred - 0.05)
    pred_steps_disrupted = max(0, int((T_pred - 0.05) / dt))

    disrupt_start_step = int(disruption_onset / dt)
    disrupt_end_step = int((disruption_onset + disruption_duration) / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    Kp = 20.0 * max(0.1, (L/1.0))
    Kd = 8.0 * max(0.1, (L/1.0))

    x[0] = np.array([0.087, 0.0]) # Perturbation

    alpha, beta, gamma = 1.0, 0.1, 0.01
    F = np.zeros(steps)

    stable = True

    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        # Check if in disruption window
        if disrupt_start_step <= i <= disrupt_end_step:
            current_pred_steps = pred_steps_disrupted
        else:
            current_pred_steps = pred_steps_normal

        # Predict state forward
        x_hat = np.copy(x_obs)
        if current_pred_steps > 0:
            for j in range(current_pred_steps):
                idx_u = obs_idx + j
                if idx_u < i:
                    u_hat = u[idx_u]
                else:
                    u_hat = 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        # Control based on predicted state
        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        # Compute Free Energy proxy
        F[i] = 0.5 * (alpha * x[i, 0]**2 + beta * x[i, 1]**2 + gamma * u[i]**2)

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            F[i:] = np.nan
            break

    if stable:
        F[steps-1] = 0.5 * (alpha * x[steps-1, 0]**2 + beta * x[steps-1, 1]**2 + gamma * u[steps-1]**2)

    return stable, x, F

def run_experiment():
    print("Running Experiment: Transient Temporal Disruption...")
    T = 10.0
    dt = 0.01
    t = np.linspace(0, T, int(T/dt))

    L = 1.6 # Adolescent length
    tau = 0.22 # Physical delay

    # 1. Baseline: T_pred matches tau (stable)
    _, x_base, f_base = simulate_agent_disruption(tau, tau, disruption_onset=0, disruption_duration=0, L=L, T=T, dt=dt)

    # 2. Transient disruption: A gap of 50ms for 2 seconds
    _, x_dis, f_dis = simulate_agent_disruption(tau, tau, disruption_onset=3.0, disruption_duration=2.0, L=L, T=T, dt=dt)

    df = pd.DataFrame({
        'time': t,
        'theta_baseline': x_base[:, 0],
        'F_baseline': f_base,
        'theta_disrupted': x_dis[:, 0],
        'F_disrupted': f_dis
    })

    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    axs[0].plot(t, np.degrees(x_base[:, 0]), 'g--', label='Baseline ($T_{pred} = \\tau$)')
    axs[0].plot(t, np.degrees(x_dis[:, 0]), 'r-', label='Transient Disruption')
    axs[0].axvspan(3.0, 5.0, color='yellow', alpha=0.3, label='Disruption Window')
    axs[0].set_ylabel('Postural Angle (degrees)')
    axs[0].set_title('Structural Consequences of Temporal Disruption (Derivative Gain Gap)')
    axs[0].legend()

    axs[1].plot(t, f_base, 'g--')
    axs[1].plot(t, f_dis, 'r-')
    axs[1].axvspan(3.0, 5.0, color='yellow', alpha=0.3)
    axs[1].set_ylabel('Thermodynamic Cost (F)')
    axs[1].set_title('Energetic Consequences of Temporal Disruption')
    axs[1].set_xlabel('Time (s)')

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)

    print("Saved to outputs/embodied_time/transient_temporal_disruption.csv and .png")

if __name__ == '__main__':
    setup_directories()
    run_experiment()
