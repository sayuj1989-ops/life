import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import pandas as pd

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    theta, omega = x
    omega = np.clip(omega, -50.0, 50.0)
    dtheta = omega
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_active_inference(tau, T_pred, precision_collapse, L=1.0, Kp_base=20.0, Kd_base=8.0, T=4.0, dt=0.01):
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)
    Kd_eff = Kd_base * (1.0 - precision_collapse)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    x[0] = np.array([0.087, 0.0])
    stable = True

    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                u_hat = u[idx_u] if idx_u < i else 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L)

        u[i] = -Kp_base * x_hat[0] - Kd_eff * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L)

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            x[i+1:, 0] = np.nan
            break

    free_energy = np.sum(u**2) * dt if stable else np.nan
    return stable, x[:, 0], free_energy

def run_experiment():
    print("Running Active Inference Time Perception Experiment...")
    tau = 0.18
    stable_base, theta_base, F_base = simulate_active_inference(tau, tau, 0.0)
    stable_lag, theta_lag, F_lag = simulate_active_inference(tau, 0.05, 0.5)

    t = np.linspace(0, 4.0, len(theta_base))
    df = pd.DataFrame({
        'time': t,
        'theta_baseline': theta_base,
        'theta_collapse': theta_lag
    })
    df.to_csv('outputs/embodied_time/active_inference_time_perception.csv', index=False)

    plt.figure(figsize=(10, 6))
    plt.plot(t, np.degrees(theta_base), 'g-', label=r'Healthy Active Inference ($T_{pred} = \tau, \Pi_{y} = 1$)')
    plt.plot(t, np.degrees(theta_lag), 'r--', label=r'Precision Collapse ($T_{pred} < \tau, \Pi_{y} = 0.5$)')
    plt.axhline(90, color='k', linestyle=':')
    plt.axhline(-90, color='k', linestyle=':')
    plt.title('Active Inference Time Perception & Postural Collapse', fontsize=14)
    plt.xlabel('Time (s)')
    plt.ylabel(r'Angle $\theta$ (degrees)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('outputs/embodied_time/active_inference_time_perception.png')
    plt.close()

if __name__ == '__main__':
    setup_directories()
    run_experiment()
