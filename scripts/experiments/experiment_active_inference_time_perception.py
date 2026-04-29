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
    dtheta = omega
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    x_next = x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
    return np.clip(x_next, -10.0, 10.0)

def simulate_agent_full(tau, T_pred, pi_y1, L=1.0, m=1.0, Kp=20.0, base_Kd=8.0, T=4.0, dt=0.01):
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    Kd = base_Kd * pi_y1

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
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            u[i:] = 1000.0
            break

    total_effort = np.sum(np.abs(u)*dt)
    return stable, total_effort, x, u

def run_experiment():
    tau = 0.18
    T_preds = np.linspace(0.0, 0.25, 6)
    pi_y1_vals = np.linspace(0.1, 1.0, 6)

    results = []

    for T_pred in T_preds:
        for pi_y1 in pi_y1_vals:
            stable, effort, _, _ = simulate_agent_full(tau, T_pred, pi_y1)
            results.append({
                'T_pred': T_pred,
                'Pi_y1': pi_y1,
                'Stable': stable,
                'Control_Effort': effort if stable else np.nan
            })

    df = pd.DataFrame(results)
    df.to_csv('outputs/embodied_time/active_inference_time_perception.csv', index=False)

    plt.figure(figsize=(10, 6))
    for pi_y1 in [1.0, 0.46, 0.1]:
        # Using closest float representation to requested 1.0, 0.5, 0.1
        # pi_y1_vals is np.linspace(0.1, 1.0, 6) -> [0.1, 0.28, 0.46, 0.64, 0.82, 1.0]
        # So using 1.0, 0.46, 0.1
        closest_pi_y1 = min(pi_y1_vals, key=lambda x:abs(x-pi_y1))
        sub_df = df[df['Pi_y1'] == closest_pi_y1]
        plt.plot(sub_df['T_pred'], sub_df['Control_Effort'], marker='o', label=rf'$\Pi_{{y,1}}$ = {closest_pi_y1:.2f}')

    plt.axvline(tau, color='r', linestyle='--', label=rf'Actual Delay $\tau$={tau}s')
    plt.title('Active Inference: Precision Collapse & Time Perception', fontsize=14)
    plt.xlabel(r'Internal Predictive Horizon $T_{pred}$ (s)', fontsize=12)
    plt.ylabel('Control Effort', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('outputs/embodied_time/active_inference_time_perception.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    setup_directories()
    run_experiment()
