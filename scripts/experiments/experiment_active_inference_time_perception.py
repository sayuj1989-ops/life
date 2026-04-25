import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def simulate_active_inference_agent(tau_phys, T_pred, L=1.0, m=1.0, T=15.0, dt=0.01):
    """
    Simulates a postural controller mapping Active Inference to PID control.
    - tau_phys: The actual physical delay in the sensory pathway.
    - T_pred: The internal predictive temporal horizon of the generative model.
    - Pi_y0: Precision on position prediction errors (~ Kp)
    - Pi_y1: Precision on velocity prediction errors (~ Kd)
    """
    steps = int(T / dt)

    # Active Inference baseline precisions
    # Optimal priors assuming perfect knowledge (T_pred == tau)
    Pi_y0_base = 20.0 * L  # Position precision maps to Kp
    Pi_y1_base = 10.0 * L  # Velocity precision maps to Kd

    # Precision Update Mechanism (Bayesian Learning):
    # If the internal model's time horizon (T_pred) mismatches the physical delay (tau_phys),
    # the generative model systematically mispredicts velocity (since velocity = d/dt).
    # This persistent velocity prediction error drives the variance estimate up,
    # causing optimal velocity precision (Pi_y1) to collapse.
    temporal_gap = max(0.0, tau_phys - T_pred)

    # Exponential decay of precision due to rising error variance
    Pi_y1_eff = Pi_y1_base * np.exp(-15.0 * temporal_gap)
    Pi_y0_eff = Pi_y0_base  # Position is easier to predict accurately, precision remains stable

    # Generalised coordinate system states
    # x = [theta, omega]
    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    # Initial perturbation
    x[0] = np.array([0.01, 0.0])

    g = 9.81
    K_pass = 5.0
    K_nonlin = 20.0

    delay_steps = int(tau_phys / dt)
    pred_steps = int(T_pred / dt)

    total_F = 0.0
    alpha, beta, gamma = 1.0, 0.1, 0.01

    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        # Forward Model Prediction
        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = max(0, obs_idx + j - delay_steps)
                u_hat = u[idx_u] if idx_u < i else 0.0

                # Internal physics model (rk4 equivalent)
                k1_th, k1_om = x_hat[1], (m*g*L*np.sin(x_hat[0]) + u_hat - K_pass*np.clip(x_hat[0], -10.0, 10.0) - K_nonlin*(np.clip(x_hat[0], -10.0, 10.0)**3)) / (m*L**2)
                x_hat = x_hat + dt * np.array([k1_th, k1_om])

        # Active Inference descending motor command (Suppressing prediction errors)
        # u ~ -Pi_y0 * e0 - Pi_y1 * e1
        u[i] = -Pi_y0_eff * x_hat[0] - Pi_y1_eff * x_hat[1]

        # True Plant Dynamics
        tau_pass = -K_pass * np.clip(x[i, 0], -10.0, 10.0) - K_nonlin * (np.clip(x[i, 0], -10.0, 10.0)**3)
        tau_grav = m * g * L * np.sin(x[i, 0])
        domega = (tau_grav + u[i] + tau_pass) / (m * L**2)
        dtheta = x[i, 1]

        x[i+1] = x[i] + dt * np.array([dtheta, domega])

        # Instantaneous Free Energy
        inst_F = 0.5 * (alpha * x[i, 0]**2 + beta * x[i, 1]**2 + gamma * u[i]**2)
        total_F += inst_F * dt

    steady_state_theta = np.mean(np.abs(x[-int(3/dt):, 0]))
    return total_F, steady_state_theta, Pi_y1_eff

def run_experiment():
    print("Simulating Embodied Time Perception as Active Inference...")
    years = np.linspace(8, 16, 50)
    dt_years = years[1] - years[0]

    # Adolescent Growth
    L_max, L_min = 1.7, 1.0
    k, t_mid = 1.5, 12.0
    L_t = L_min + (L_max - L_min) / (1 + np.exp(-k * (years - t_mid)))

    # Neural delay scales with length
    tau_0, v = 0.05, 15.0
    tau_t = tau_0 + L_t / v

    # Internal Time Horizon (Cognitive adaptation)
    tau_adapt = 0.8 # Adaptation time constant
    T_pred_t = np.zeros_like(years)
    T_pred_t[0] = tau_t[0]

    for i in range(1, len(years)):
        dT_pred = (1.0 / tau_adapt) * (tau_t[i-1] - T_pred_t[i-1]) * dt_years
        T_pred_t[i] = T_pred_t[i-1] + dT_pred

    gap_t = tau_t - T_pred_t

    F_cost = np.zeros_like(years)
    structural_theta = np.zeros_like(years)
    Pi_y1_list = np.zeros_like(years)

    for i in range(len(years)):
        f, theta_ss, pi_y1 = simulate_active_inference_agent(tau_phys=tau_t[i], T_pred=T_pred_t[i], L=L_t[i])
        F_cost[i] = f
        structural_theta[i] = theta_ss
        Pi_y1_list[i] = pi_y1

    df = pd.DataFrame({
        'Age': years,
        'Length': L_t,
        'Physical_Delay_tau': tau_t,
        'Cognitive_Horizon_Tpred': T_pred_t,
        'Temporal_Gap': gap_t,
        'Velocity_Precision_Pi_y1': Pi_y1_list,
        'Free_Energy_Cost': F_cost,
        'Cobb_Angle_rad': structural_theta
    })
    df.to_csv('outputs/embodied_time/active_inference_time_perception.csv', index=False)

    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # Top: Time mismatch
    axs[0].plot(years, tau_t * 1000, 'k-', linewidth=2, label=r'Physical Delay $\tau$')
    axs[0].plot(years, T_pred_t * 1000, 'b--', linewidth=2, label=r'Cognitive Horizon $T_{pred}$')
    axs[0].fill_between(years, T_pred_t * 1000, tau_t * 1000, color='red', alpha=0.3, label='Temporal Prediction Error')
    axs[0].set_ylabel('Time (ms)', fontsize=12)
    axs[0].set_title('Internal Time Perception lags Embodied Reality', fontsize=14)
    axs[0].legend(loc='upper left')
    axs[0].grid(True, alpha=0.3)

    # Middle: Precision Collapse
    axs[1].plot(years, Pi_y1_list, 'm-', linewidth=2.5, label=r'Velocity Precision $\Pi_{y,1}$ (Equivalent to $K_d$)')
    axs[1].set_ylabel(r'Precision $\Pi_{y,1}$', fontsize=12)
    axs[1].set_title(r'Bayesian Response: Velocity Precision Collapse', fontsize=14)
    axs[1].legend(loc='upper left')
    axs[1].grid(True, alpha=0.3)

    # Bottom: Pathology Emergence (Dark Room Attractor)
    axs[2].plot(years, np.degrees(structural_theta), 'g-', linewidth=2.5, label='Scoliosis (Dark Room Attractor)')
    axs[2].set_xlabel('Age (Years)', fontsize=12)
    axs[2].set_ylabel('Curve Magnitude (deg)', fontsize=12)
    axs[2].set_title('Phase Transition to Pathology driven by Time Misperception', fontsize=14)
    axs[2].legend(loc='upper left')
    axs[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/active_inference_time_perception.png', dpi=300)
    plt.close()

    print("Experiment complete.")

if __name__ == "__main__":
    setup_directories()
    run_experiment()
