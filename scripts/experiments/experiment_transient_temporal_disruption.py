import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    theta, omega = x
    dtheta = omega
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_transient_disruption(T=10.0, dt=0.01):
    steps = int(T / dt)
    time = np.linspace(0, T, steps)

    L_base = 1.0
    L_max = 1.6

    tau_0 = 0.05
    v_nerve = 15.0 # m/s for proprioception approximation to get decent delay

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    L_hist = np.zeros(steps)
    tau_hist = np.zeros(steps)
    T_pred_hist = np.zeros(steps)
    delta_T_hist = np.zeros(steps)
    free_energy = np.zeros(steps)

    x[0] = np.array([0.05, 0.0]) # 5 degrees intial perturbation
    T_pred = tau_0 + L_base/v_nerve

    tau_adapt = 1.5 # Adaptation time constant

    buckled = False

    for i in range(steps - 1):
        t = time[i]

        # Logistic growth spurt around t=5.0
        L = L_base + (L_max - L_base) / (1.0 + np.exp(-4.0 * (t - 5.0)))

        tau = tau_0 + L / v_nerve
        dT_pred = (tau - T_pred) / tau_adapt * dt
        T_pred += dT_pred

        L_hist[i] = L
        tau_hist[i] = tau
        T_pred_hist[i] = T_pred
        delta_T = tau - T_pred
        delta_T_hist[i] = delta_T

        delay_steps = int(tau / dt)
        pred_steps = int(T_pred / dt)

        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                u_hat = u[idx_u] if idx_u < i else 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L)

        Kp = 25.0 * L
        Kd = 10.0 * L

        pred_error = np.linalg.norm(x_hat - x[i])

        if buckled:
            u[i] = 0.0
            x[i+1, 0] = np.pi / 6 # 30 deg scoliosis
            x[i+1, 1] = 0.0
            current_cost = pred_error * 10.0 + 0.1 * abs(u[i])
            free_energy[i] = current_cost
        else:
            # Calculate provisional control u to compute cost
            u_provisional = -Kp * x_hat[0] - Kd * x_hat[1]
            current_cost = pred_error * 10.0 + 0.1 * abs(u_provisional)
            free_energy[i] = current_cost

            if current_cost > 12.0: # Buckling threshold
                buckled = True
                u[i] = 0.0
                x[i+1, 0] = np.pi / 6
                x[i+1, 1] = 0.0
            else:
                u[i] = u_provisional
                x[i+1] = rk4(x[i], u[i], dt, L=L)

                # Small random perturbation to keep it challenging
                if i % 10 == 0:
                     x[i+1, 1] += np.random.normal(0, 0.05)

    # Fill last elements
    L_hist[-1] = L_hist[-2]
    tau_hist[-1] = tau_hist[-2]
    T_pred_hist[-1] = T_pred_hist[-2]
    delta_T_hist[-1] = delta_T_hist[-2]
    free_energy[-1] = free_energy[-2]
    x[-1] = x[-2]
    u[-1] = u[-2]

    return time, x, u, L_hist, tau_hist, T_pred_hist, delta_T_hist, free_energy

def run_experiment():
    print("Running Transient Temporal Disruption Simulation...")
    time, x, u, L_hist, tau_hist, T_pred_hist, delta_T_hist, free_energy = simulate_transient_disruption()

    df = pd.DataFrame({
        'Time': time,
        'Postural_Angle': x[:, 0],
        'Control_Torque': u,
        'Length': L_hist,
        'Physical_Delay_tau': tau_hist,
        'Perceived_Time_T_pred': T_pred_hist,
        'Derivative_Gain_Gap': delta_T_hist,
        'Thermodynamic_Free_Energy': free_energy
    })

    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    axs[0].plot(time, L_hist, 'k-', linewidth=2)
    axs[0].set_ylabel('Body Length L (m)')
    axs[0].set_title('Adolescent Growth Spurt')
    axs[0].grid(True)

    axs[1].plot(time, tau_hist, 'r-', label='Physical Delay ($\\tau$)')
    axs[1].plot(time, T_pred_hist, 'b--', label='Internal Model ($T_{pred}$)')
    axs[1].fill_between(time, T_pred_hist, tau_hist, color='red', alpha=0.3, label='Derivative Gain Gap ($\\Delta T$)')
    axs[1].set_ylabel('Time (s)')
    axs[1].legend()
    axs[1].grid(True)

    axs[2].plot(time, free_energy, 'g-', linewidth=2)
    axs[2].axhline(12.0, color='r', linestyle='--', label='Buckling Threshold')
    axs[2].set_ylabel('Free Energy')
    axs[2].set_title('Thermodynamic Cost')
    axs[2].legend()
    axs[2].grid(True)

    axs[3].plot(time, np.degrees(x[:, 0]), 'purple', linewidth=2)
    axs[3].set_ylabel('Spinal Angle (deg)')
    axs[3].set_xlabel('Simulation Time (s)')
    axs[3].set_title('Structural Posture (Buckling to Scoliosis)')
    axs[3].grid(True)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()
    print("Simulation complete. Outputs saved.")

if __name__ == "__main__":
    setup_directories()
    run_experiment()
