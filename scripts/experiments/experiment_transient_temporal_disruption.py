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

def simulate_transient_disruption(tau, L=1.0, Kp=20.0, Kd=8.0, T=8.0, dt=0.01):
    steps = int(T / dt)
    delay_steps = int(tau / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    T_pred_history = np.zeros(steps)
    structural_stress = np.zeros(steps)

    x[0] = np.array([0.087, 0.0])

    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        time = i * dt
        if 2.0 <= time <= 4.0:
            T_pred = 0.05
        else:
            T_pred = tau

        T_pred_history[i] = T_pred
        pred_steps = int(T_pred / dt)

        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                u_hat = u[idx_u] if idx_u < i else 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L)

        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L)

        structural_stress[i] = abs(u[i]) * x[i, 0]**2

        if abs(x[i+1, 0]) > np.pi/2:
            x[i+1:, 0] = np.nan
            break

    return np.linspace(0, T, steps), x[:, 0], T_pred_history, structural_stress, u

def run_experiment():
    print("Running Transient Temporal Disruption...")
    t, theta, T_pred, stress, u = simulate_transient_disruption(0.18)

    df = pd.DataFrame({
        'time': t,
        'theta': theta,
        'T_pred': T_pred,
        'structural_stress': stress
    })
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    fig, axs = plt.subplots(3, 1, figsize=(10, 10))
    axs[0].plot(t, np.degrees(theta), 'b-')
    axs[0].axvspan(2.0, 4.0, color='red', alpha=0.2, label='Temporal Disruption')
    axs[0].set_ylabel(r'Angle $\theta$ (deg)')
    axs[0].legend()

    axs[1].plot(t, T_pred, 'g-')
    axs[1].set_ylabel(r'$T_{pred}$ (s)')

    axs[2].plot(t, stress, 'r-')
    axs[2].set_ylabel('Structural Stress\n(Energy Deficit)')
    axs[2].set_xlabel('Time (s)')

    plt.suptitle('Transient Temporal Disruption & Derivative Gain Gap')
    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png')
    plt.close()

if __name__ == '__main__':
    setup_directories()
    run_experiment()
