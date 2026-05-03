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
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_active_inference_agent(tau, T_pred, precision_Pi_y1, L=1.0, m=1.0, Kp_base=20.0, Kd_base=8.0, T=4.0, dt=0.01):
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    # Active Inference precision mapping to Kd degradation
    Kd = Kd_base * precision_Pi_y1
    Kp = Kp_base

    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    pred_error = np.zeros(steps)

    x[0] = np.array([0.087, 0.0])
    stable = True

    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                if idx_u < i:
                    u_hat = u[idx_u]
                else:
                    u_hat = 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        pred_error[i] = np.linalg.norm(x_hat - x[i])

        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            pred_error[i:] = 1000.0
            u[i:] = 1000.0
            break

    F = np.sum(pred_error) + 0.1 * np.sum(np.abs(u)*dt)
    return stable, F, np.sum(np.abs(u)*dt), x, u, pred_error

def run_experiment():
    setup_directories()

    precisions = np.linspace(1.0, 0.1, 20)
    tau = 0.18
    T_preds = [0.18, 0.13]

    results = []

    for T_pred in T_preds:
        for p in precisions:
            stable, F, effort, _, _, _ = simulate_active_inference_agent(tau, T_pred, p)
            results.append({
                'T_pred': T_pred,
                'Precision_Pi_y1': p,
                'Kd_effective': 8.0 * p,
                'Free_Energy': F if stable else np.nan,
                'Stable': stable
            })

    df = pd.DataFrame(results)
    df.to_csv('outputs/embodied_time/active_inference_time_perception.csv', index=False)

    plt.figure(figsize=(10, 6))

    df_perf = df[df['T_pred'] == 0.18]
    df_lag = df[df['T_pred'] == 0.13]

    plt.plot(df_perf['Precision_Pi_y1'], df_perf['Free_Energy'], 'b-o', label=r'$T_{pred} = \tau = 0.18$ (Adaptive)')
    plt.plot(df_lag['Precision_Pi_y1'], df_lag['Free_Energy'], 'r-s', label=r'$T_{pred} = 0.13 < \tau$ (Lagging)')

    plt.gca().invert_xaxis()
    plt.title('Active Inference Precision Collapse and Temporal Lag', fontsize=14)
    plt.xlabel(r'Precision $\Pi_{y,1}$ (decreasing $\rightarrow$)', fontsize=12)
    plt.ylabel('Free Energy Proxy $F$', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/active_inference_time_perception.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    run_experiment()
