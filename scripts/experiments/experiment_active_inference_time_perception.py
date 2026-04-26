import numpy as np
import pandas as pd
import os
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
    return np.clip(x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4), -10.0, 10.0)

def simulate_active_inference(tau_actual, tau_pred, T=10.0, dt=0.01, L=1.0):
    steps = int(T / dt)
    delay_steps = int(tau_actual / dt)
    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    Pi_y0 = 20.0
    Pi_y1_base = 8.0
    x[0] = np.array([0.05, 0.0])
    Pi_y1_hist = np.zeros(steps)
    stable = True
    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]
        error_velocity = abs(tau_actual - tau_pred) * abs(x_obs[1])
        Pi_y1 = Pi_y1_base / (1.0 + 50.0 * error_velocity**2)
        Pi_y1_hist[i] = Pi_y1
        Kp_eff = Pi_y0
        Kd_eff = Pi_y1
        pred_steps = int(tau_pred / dt)
        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                x_hat = rk4(x_hat, 0.0, dt, L=L)
        u[i] = -Kp_eff * x_hat[0] - Kd_eff * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L)
        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            Pi_y1_hist[i+1:] = np.nan
            break
    Pi_y1_hist[-1] = Pi_y1_hist[-2] if steps > 1 else 0
    return stable, x, u, Pi_y1_hist

def run_experiment():
    print("Running Active Inference Time Perception Experiment...")
    setup_directories()
    T = 5.0
    dt = 0.01
    t = np.arange(0, T, dt)
    tau_actual = 0.2
    tau_pred_adaptive = 0.2
    s1, x1, u1, pi1 = simulate_active_inference(tau_actual, tau_pred_adaptive, T, dt)
    tau_pred_lagging = 0.1
    s2, x2, u2, pi2 = simulate_active_inference(tau_actual, tau_pred_lagging, T, dt)
    df = pd.DataFrame({'time': t, 'theta_adaptive': x1[:, 0], 'pi_y1_adaptive': pi1, 'theta_lagging': x2[:, 0], 'pi_y1_lagging': pi2})
    df.to_csv('outputs/embodied_time/active_inference_time_perception.csv', index=False)
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(t, x1[:, 0], label='Adaptive ($T_{pred} = \\tau$)')
    plt.plot(t, x2[:, 0], label='Lagging ($T_{pred} < \\tau$)')
    plt.title('Postural Stability (Inverted Pendulum)')
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (rad)')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(t, pi1, label=r'Adaptive $\Pi_{y,1}$')
    plt.plot(t, pi2, label=r'Lagging $\Pi_{y,1}$ (Precision Collapse)')
    plt.title(r'Velocity Precision $\Pi_{y,1}$ ($K_d$ degradation)')
    plt.xlabel('Time (s)')
    plt.ylabel('Precision')
    plt.legend()
    plt.tight_layout()
    plt.savefig('outputs/embodied_time/active_inference_time_perception.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    run_experiment()
