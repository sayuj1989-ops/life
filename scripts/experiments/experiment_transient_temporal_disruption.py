import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0, K_pass=5.0, K_nonlin=20.0):
    """
    Non-linear inverted pendulum with passive spinal stiffness.
    K_pass: Linear passive stiffness
    K_nonlin: Non-linear hardening (prevents complete collapse, creating a 'dark room' local minimum)
    """
    theta, omega = x
    dtheta = omega
    # Passive stiffness
    tau_pass = -K_pass * theta - K_nonlin * (theta**3)

    # Gravity torque
    tau_grav = m * g * L * np.sin(theta)

    # Acceleration
    domega = (tau_grav + u + tau_pass) / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_agent_with_disruption(tau, T_pred, L=1.0, m=1.0, T=15.0, dt=0.01):
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    # Active control gains
    Kp = 20.0 * L
    Kd_base = 10.0 * L

    # In FEP, if T_pred lags tau, velocity prediction error variance increases.
    # The system optimally down-weights velocity precision (Pi_y,1), which degrades effective Kd.
    # We model this degradation as proportional to the temporal gap.
    temporal_gap = max(0.0, tau - T_pred)

    # Effective Kd degrades with the gap
    Kd_eff = Kd_base * np.exp(-15.0 * temporal_gap)

    # Initial condition: tiny perturbation
    x[0] = np.array([0.01, 0.0])

    alpha, beta, gamma = 1.0, 0.1, 0.01
    total_F = 0.0

    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        # Predict state forward by T_pred
        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = max(0, obs_idx + j - delay_steps)
                u_hat = u[idx_u] if idx_u < i else 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        # Active control with degraded Kd
        u[i] = -Kp * x_hat[0] - Kd_eff * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        # Compute instantaneous Free Energy cost proxy
        inst_F = 0.5 * (alpha * x[i, 0]**2 + beta * x[i, 1]**2 + gamma * u[i]**2)
        total_F += inst_F * dt

    # Structural consequence: mean absolute posture angle in the last 3 seconds
    steady_state_theta = np.mean(np.abs(x[-int(3/dt):, 0]))

    return total_F, steady_state_theta, Kd_eff

def exp_transient_temporal_disruption():
    print("Simulating Transient Temporal Disruption (Derivative Gain Gap)...")

    years = np.linspace(8, 16, 50)
    dt_years = years[1] - years[0]

    # Adolescent Growth Spurt
    L_max, L_min = 1.7, 1.0
    k, t_mid = 1.5, 12.0
    L_t = L_min + (L_max - L_min) / (1 + np.exp(-k * (years - t_mid)))

    # Delay and Cognitive Horizon
    tau_0, v = 0.05, 15.0
    tau_t = tau_0 + L_t / v

    tau_adapt = 0.8 # Cognitive adaptation time constant
    T_pred_t = np.zeros_like(years)
    T_pred_t[0] = tau_t[0]

    for i in range(1, len(years)):
        dT_pred = (1.0 / tau_adapt) * (tau_t[i-1] - T_pred_t[i-1]) * dt_years
        T_pred_t[i] = T_pred_t[i-1] + dT_pred

    # Gap
    gap_t = tau_t - T_pred_t

    F_cost = np.zeros_like(years)
    structural_theta = np.zeros_like(years)
    Kd_eff_list = np.zeros_like(years)

    for i in range(len(years)):
        f, theta_ss, kd = simulate_agent_with_disruption(tau=tau_t[i], T_pred=T_pred_t[i], L=L_t[i])
        F_cost[i] = f
        structural_theta[i] = theta_ss
        Kd_eff_list[i] = kd

    df = pd.DataFrame({
        'Age': years,
        'Length': L_t,
        'Physical_Delay': tau_t,
        'Cognitive_Predictive_Horizon': T_pred_t,
        'Temporal_Gap': gap_t,
        'Effective_Kd': Kd_eff_list,
        'Free_Energy_Cost': F_cost,
        'Structural_Consequence_Angle_rad': structural_theta
    })
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # Top: The Temporal Disruption
    axs[0].plot(years, tau_t * 1000, 'k-', linewidth=2, label=r'Physical Delay $\tau$')
    axs[0].plot(years, T_pred_t * 1000, 'b--', linewidth=2, label=r'Cognitive Prediction $T_{pred}$')
    axs[0].fill_between(years, T_pred_t * 1000, tau_t * 1000, color='red', alpha=0.3, label='Transient Temporal Disruption')
    axs[0].set_ylabel('Time (ms)', fontsize=12)
    axs[0].set_title('Transient Temporal Disruption: Cognitive Model Lags Biology', fontsize=14)
    axs[0].legend(loc='upper left')
    axs[0].grid(True, alpha=0.3)

    # Middle: Energetic Consequence
    axs[1].plot(years, F_cost, 'r-', linewidth=2.5, label='Free Energy Proxy')
    axs[1].set_ylabel(r'Thermodynamic Cost $\mathcal{F}$', fontsize=12)
    axs[1].set_title(r'Energetic Consequence: Precision Collapse ($K_d$ degradation)', fontsize=14)
    axs[1].legend(loc='upper left')
    axs[1].grid(True, alpha=0.3)

    # Bottom: Structural Consequence
    axs[2].plot(years, np.degrees(structural_theta), 'g-', linewidth=2.5, label='Steady-State Posture Deviation')
    axs[2].set_xlabel('Age (Years)', fontsize=12)
    axs[2].set_ylabel('Cobb Angle equivalent (deg)', fontsize=12)
    axs[2].set_title('Structural Consequence: Phase Transition to Lateral Curvature Attractor', fontsize=14)
    axs[2].legend(loc='upper left')
    axs[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

    print("Experiment complete. Outputs saved.")

if __name__ == "__main__":
    setup_directories()
    exp_transient_temporal_disruption()
