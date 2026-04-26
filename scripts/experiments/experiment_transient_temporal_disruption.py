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

def compute_free_energy(pred_error, effort, alpha=1.0, beta=0.1):
    return alpha * pred_error + beta * effort

def simulate_transient_disruption(T=15.0, dt=0.01):
    steps = int(T / dt)
    t = np.linspace(0, T, steps)
    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    F = np.zeros(steps)
    x[0] = np.array([0.05, 0.0])
    L = 1.0; m = 1.0; Kp = 20.0; Kd_base = 8.0
    tau_actual = 0.15; tau_pred = 0.15
    stable = True
    for i in range(steps - 1):
        if 5.0 <= t[i] <= 10.0:
            tau_actual = 0.22; tau_pred = 0.15
        else:
            tau_actual = 0.22; tau_pred = 0.22
        delay_steps = int(tau_actual / dt)
        pred_steps = int(tau_pred / dt)
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]
        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                x_hat = rk4(x_hat, 0.0, dt, L=L)
        mismatch = abs(tau_actual - tau_pred)
        Kd_eff = Kd_base * np.exp(-50.0 * mismatch**2)
        u[i] = -Kp * x_hat[0] - Kd_eff * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L)
        pred_error = np.linalg.norm(x_hat - x[i])
        effort = abs(u[i]) * dt
        F[i] = compute_free_energy(pred_error, effort)
        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            F[i+1:] = np.nan
            break
    F[-1] = F[-2] if steps > 1 else 0
    return t, x, u, F, stable

def run_experiment():
    print("Running Transient Temporal Disruption Experiment...")
    setup_directories()
    t, x, u, F, stable = simulate_transient_disruption()
    df = pd.DataFrame({'time': t, 'theta': x[:, 0], 'energy': F})
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, x[:, 0], 'b-')
    plt.axvspan(5.0, 10.0, color='red', alpha=0.2, label='Transient Disruption\n(Growth Spurt)')
    plt.ylabel('Angle (rad)')
    plt.title('Structural Consequence (Angle)')
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(t, F, 'g-')
    plt.axvspan(5.0, 10.0, color='red', alpha=0.2)
    plt.ylabel('Thermodynamic Cost')
    plt.title('Energetic Consequence (Free Energy Proxy)')
    plt.xlabel('Time (s)')
    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    run_experiment()
