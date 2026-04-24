import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    theta, omega = x
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([omega, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def compute_free_energy(pred_error_hist, effort_hist, alpha=1.0, beta=0.1):
    total_pred_error = np.sum(np.nan_to_num(pred_error_hist))
    total_effort = np.sum(np.nan_to_num(effort_hist))
    return alpha * total_pred_error + beta * total_effort

def simulate_agent_full(tau, T_pred, L=1.0, m=1.0, Kp=20.0, Kd=8.0, T=4.0, dt=0.01):
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    pred_error = np.zeros(steps)

    x[0] = np.array([0.087, 0.0]) # 5 deg initial perturbation
    stable = True

    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                u_hat = u[idx_u] if idx_u < i else 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        pred_error[i] = np.linalg.norm(x_hat - x[i])
        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            pred_error[i:] = 1000.0
            u[i:] = 1000.0
            break

    F = compute_free_energy(pred_error, np.abs(u)*dt)
    max_angle = np.max(np.abs(x[:, 0])) if stable else np.pi/2
    return stable, F, max_angle, x, u, pred_error

def run_transient_temporal_disruption():
    print("Running Transient Temporal Disruption Simulation...")

    # 10 years to 20 years
    ages = np.linspace(10, 20, 100)

    # Physical Growth (Sigmoid L)
    L_base = 1.0
    L_max = 1.6
    k_growth = 1.5
    age_spurt = 13.0
    L_phys = L_base + (L_max - L_base) / (1 + np.exp(-k_growth * (ages - age_spurt)))

    # Physical Neural Delay (tracks length linearly roughly)
    tau_phys = 0.15 + (L_phys - 1.0) * 0.12

    # Cognitive Predictive Horizon T_pred (learns tau_phys with a delay)
    # Using a simple 1st order lag model for continuous updating
    alpha_learning = 0.8 # Learning rate
    dt_age = ages[1] - ages[0]

    T_pred_cog = np.zeros_like(ages)
    T_pred_cog[0] = tau_phys[0] # Starts perfectly adapted

    for i in range(1, len(ages)):
        # Euler integration of dT_pred/dt = alpha * (tau - T_pred)
        dT_pred = alpha_learning * (tau_phys[i-1] - T_pred_cog[i-1]) * dt_age
        T_pred_cog[i] = T_pred_cog[i-1] + dT_pred

    results = []

    for i, age in enumerate(ages):
        L = L_phys[i]
        tau = tau_phys[i]
        T_pred = T_pred_cog[i]

        Kp = 20.0 * (L/1.0)
        Kd = 8.0 * (L/1.0)

        stable, F, max_angle, _, _, _ = simulate_agent_full(tau, T_pred, L=L, Kp=Kp, Kd=Kd)

        results.append({
            'Age': age,
            'L_phys': L,
            'Tau_phys': tau,
            'T_pred_cog': T_pred,
            'Temporal_Lag': tau - T_pred,
            'Stable': stable,
            'Free_Energy': F if stable else np.nan,
            'Max_Angle_rad': max_angle
        })

    df = pd.DataFrame(results)
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    # Plotting
    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # Top: Physical vs Cognitive Time
    axs[0].plot(ages, df['Tau_phys']*1000, 'b-', label=r'Physical Neural Delay ($\tau$)')
    axs[0].plot(ages, df['T_pred_cog']*1000, 'g--', label=r'Cognitive Prediction Horizon ($T_{pred}$)')
    axs[0].fill_between(ages, df['T_pred_cog']*1000, df['Tau_phys']*1000, color='red', alpha=0.2, label='Derivative Gain Gap')
    axs[0].set_ylabel('Time (ms)')
    axs[0].set_title('Transient Temporal Disruption during Growth Spurt')
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)

    # Middle: Energetic Consequence
    axs[1].plot(ages, df['Free_Energy'], 'r-', linewidth=2)
    axs[1].set_ylabel('Free Energy Proxy')
    axs[1].set_title('Thermodynamic Consequence (Energy Cost of Mismatch)')
    axs[1].grid(True, alpha=0.3)

    # Bottom: Structural Consequence
    axs[2].plot(ages, np.degrees(df['Max_Angle_rad']), 'k-', linewidth=2)
    axs[2].axhline(90, color='r', linestyle=':', label='Collapse')
    axs[2].set_ylabel('Max Postural Angle (deg)')
    axs[2].set_xlabel('Age (years)')
    axs[2].set_title('Structural Consequence (Instability / Buckling)')
    axs[2].legend()
    axs[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

    print("Experiment completed.")

if __name__ == "__main__":
    setup_directories()
    run_transient_temporal_disruption()
