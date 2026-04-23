import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

def simulate_transient_disruption(tau_base=0.15, tau_peak=0.25, T_pred_adapt_rate=0.5, T=10.0, dt=0.01, L=1.5, Kp=30.0, Kd=12.0):
    steps = int(T / dt)
    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    tau_hist = np.zeros(steps)
    T_pred_hist = np.zeros(steps)
    error_hist = np.zeros(steps)
    effort_hist = np.zeros(steps)

    x[0] = np.array([0.05, 0.0])

    T_pred = tau_base
    stable = True

    for i in range(steps - 1):
        t = i * dt

        if 2.0 < t < 6.0:
            bump = np.sin(np.pi * (t - 2.0) / 4.0)**2
            current_tau = tau_base + (tau_peak - tau_base) * bump
        else:
            current_tau = tau_base

        tau_hist[i] = current_tau
        T_pred_hist[i] = T_pred

        delay_steps = int(current_tau / dt)
        pred_steps = int(T_pred / dt)

        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                u_hat = u[idx_u] if idx_u < i else 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L)

        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]

        x[i+1] = rk4(x[i], u[i], dt, L=L)

        T_pred += T_pred_adapt_rate * (current_tau - T_pred) * dt

        effort_hist[i] = np.abs(u[i]) * dt
        error_hist[i] = np.linalg.norm(x_hat - x[i])

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            effort_hist[i:] = np.nan
            error_hist[i:] = np.nan
            break

    tau_hist[-1] = tau_hist[-2]
    T_pred_hist[-1] = T_pred_hist[-2]

    return t, x, u, tau_hist, T_pred_hist, effort_hist, error_hist, stable

def main():
    setup_directories()
    dt = 0.01
    T = 10.0

    t, x, u, tau_hist, T_pred_hist, effort_hist, error_hist, stable = simulate_transient_disruption(
        tau_base=0.15, tau_peak=0.25, T_pred_adapt_rate=0.5, T=T, dt=dt, L=1.5, Kp=30.0, Kd=12.0
    )

    time_arr = np.linspace(0, T, int(T/dt))

    df = pd.DataFrame({
        'Time': time_arr,
        'Theta': x[:, 0],
        'Omega': x[:, 1],
        'Control_U': u,
        'Physical_Delay_Tau': tau_hist,
        'Cognitive_Predict_T_pred': T_pred_hist,
        'Effort': effort_hist,
        'Error': error_hist
    })

    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    axs[0].plot(time_arr, tau_hist, 'r-', linewidth=2, label=r'Physical Neural Delay ($\tau$)')
    axs[0].plot(time_arr, T_pred_hist, 'b--', linewidth=2, label=r'Cognitive Prediction ($T_{pred}$)')
    axs[0].fill_between(time_arr, tau_hist, T_pred_hist, color='orange', alpha=0.3, label='Derivative Gain Gap')
    axs[0].set_ylabel('Time (s)')
    axs[0].set_title('Transient Temporal Disruption (Cognition Lagging Physics)')
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)

    axs[1].plot(time_arr, x[:, 0], 'g-', label=r'Postural Angle ($\theta$)')
    axs[1].set_ylabel('Angle (rad)')
    axs[1].legend()
    axs[1].grid(True, alpha=0.3)

    axs[2].plot(time_arr, effort_hist, 'm-', label='Thermodynamic Effort (Control Energy)')
    axs[2].plot(time_arr, error_hist, 'k:', label='Prediction Error')
    axs[2].set_ylabel('Energy / Error')
    axs[2].set_xlabel('Time (s)')
    axs[2].legend()
    axs[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

    print("Simulation completed. Outputs saved to outputs/embodied_time/")

if __name__ == "__main__":
    main()
