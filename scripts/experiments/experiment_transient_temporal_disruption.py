import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0, k_stiff=0.0):
    """
    Non-linear inverted pendulum dynamics with optional non-linear passive stiffness
    representing biological countercurvature.
    """
    theta, omega = x
    dtheta = omega

    # Clip theta to avoid scalar power overflow RuntimeWarning during extreme collapse
    theta_clipped = np.clip(theta, -np.pi, np.pi)

    # Equation of motion: ml^2 \ddot{\theta} = mgl \sin(\theta) + u - k_stiff * theta^3
    # The cubic stiffness term kicks in strongly at large deflections to prevent total collapse
    restoring_torque = -k_stiff * (theta_clipped**3)

    domega = (g / L) * np.sin(theta_clipped) + (u + restoring_torque) / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0, k_stiff=0.0):
    """Runge-Kutta 4 integration."""
    k1 = dynamics(x, u, L=L, m=m, k_stiff=k_stiff)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m, k_stiff=k_stiff)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m, k_stiff=k_stiff)
    k4 = dynamics(x + dt * k3, u, L=L, m=m, k_stiff=k_stiff)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_developmental_snapshot(tau, T_pred, base_Kp=20.0, base_Kd=8.0, L=1.0, m=1.0, k_stiff=0.0, T=4.0, dt=0.01):
    """
    Simulates a snapshot in development to assess structural and energetic consequences.
    """
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    # Precision-modulated gains (from previous experiment logic)
    gap = max(0, tau - T_pred)
    precision_factor = np.exp(-15.0 * gap)
    effective_Kp = base_Kp * (0.8 + 0.2 * precision_factor)
    effective_Kd = base_Kd * precision_factor

    x[0] = np.array([0.087, 0.0])  # Initial perturbation (5 degrees)

    stable = True
    total_effort = 0.0
    structural_stress = 0.0

    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        # Predict state forward by T_pred
        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                if idx_u < i:
                    u_hat = u[idx_u]
                else:
                    u_hat = 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        # Control action based on degraded precision gains
        u[i] = -effective_Kp * x_hat[0] - effective_Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m, k_stiff=k_stiff)

        total_effort += abs(u[i]) * dt

        # Accumulate structural stress proxy (integral of large deflections)
        structural_stress += abs(x[i+1, 0]) * dt

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            total_effort = 1000.0
            structural_stress = 1000.0
            break

    return stable, total_effort, structural_stress

def run_experiment():
    print("Running Transient Temporal Disruption Experiment...")

    # Simulate a developmental trajectory (e.g., ages 8 to 18)
    ages = np.linspace(8, 18, 50)

    # Model a transient spurt in growth/delay around age 12
    L_t = 1.0 + 0.6 / (1 + np.exp(-1.5 * (ages - 12)))
    tau_t = 0.10 + L_t / 15.0  # Physical delay increases with nerve length

    # Cognitive predictive model T_pred lags behind tau during the spurt
    # T_pred(t) is a smoothed, delayed version of tau(t)
    T_pred_t = np.zeros_like(ages)
    T_pred_t[0] = tau_t[0]
    dt_age = ages[1] - ages[0]
    tau_adapt = 1.5  # Adaptation time constant (years)

    for i in range(1, len(ages)):
        dT_pred = (1.0 / tau_adapt) * (tau_t[i-1] - T_pred_t[i-1]) * dt_age
        T_pred_t[i] = T_pred_t[i-1] + dT_pred

    results = []

    # Base parameters
    m = 50.0  # Proxy mass
    k_stiff_healthy = 0.0   # Healthy system (no countercurvature needed)
    k_stiff_scoliosis = 500.0 # Pathological system (relies on structural stiffness)

    for i in range(len(ages)):
        age = ages[i]
        tau = tau_t[i]
        T_pred = T_pred_t[i]
        L = L_t[i]

        # Scale gains with L roughly
        Kp = 200.0 * L
        Kd = 80.0 * L

        # Scenario 1: Healthy (no structural stiffness compensation)
        stable_H, effort_H, stress_H = simulate_developmental_snapshot(
            tau, T_pred, base_Kp=Kp, base_Kd=Kd, L=L, m=m, k_stiff=k_stiff_healthy
        )

        # Scenario 2: Countercurvature Compensation (relies on passive stiffness)
        stable_C, effort_C, stress_C = simulate_developmental_snapshot(
            tau, T_pred, base_Kp=Kp, base_Kd=Kd, L=L, m=m, k_stiff=k_stiff_scoliosis
        )

        results.append({
            'Age': age,
            'Physical_Delay_tau': tau,
            'Cognitive_T_pred': T_pred,
            'Temporal_Gap': tau - T_pred,
            'Effort_Healthy': effort_H,
            'Stress_Healthy': stress_H,
            'Stable_Healthy': stable_H,
            'Effort_Compensated': effort_C,
            'Stress_Compensated': stress_C,
            'Stable_Compensated': stable_C
        })

    df = pd.DataFrame(results)
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    # Plotting
    fig, axs = plt.subplots(3, 1, figsize=(8, 12), sharex=True)

    axs[0].plot(df['Age'], df['Physical_Delay_tau'] * 1000, 'k-', linewidth=2, label=r'Physical Delay $\tau(t)$')
    axs[0].plot(df['Age'], df['Cognitive_T_pred'] * 1000, 'b--', linewidth=2, label=r'Cognitive Model $T_{pred}(t)$')
    axs[0].fill_between(df['Age'], df['Cognitive_T_pred'] * 1000, df['Physical_Delay_tau'] * 1000, color='red', alpha=0.3, label='Derivative Gain Gap')
    axs[0].set_ylabel('Time (ms)', fontsize=12)
    axs[0].set_title('Transient Temporal Disruption During Growth Spurt', fontsize=14)
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)

    # Clean up stress and effort for plotting (cap at penalty values)
    max_plot_stress = df[df['Stable_Compensated']]['Stress_Compensated'].max() * 2
    if np.isnan(max_plot_stress): max_plot_stress = 100.0

    axs[1].plot(df['Age'], df['Stress_Healthy'], 'r-', linewidth=2, label='Healthy (Active Control Only)')
    axs[1].plot(df['Age'], df['Stress_Compensated'], 'g-', linewidth=2, label='Compensated (Biological Countercurvature)')
    axs[1].set_ylabel('Structural Deflection Stress', fontsize=12)
    axs[1].set_title('Structural Consequences', fontsize=14)
    axs[1].set_ylim([0, max_plot_stress])
    axs[1].legend()
    axs[1].grid(True, alpha=0.3)

    max_plot_effort = df[df['Stable_Compensated']]['Effort_Compensated'].max() * 2
    if np.isnan(max_plot_effort): max_plot_effort = 100.0

    axs[2].plot(df['Age'], df['Effort_Healthy'], 'r-', linewidth=2, label='Healthy (Active Control Only)')
    axs[2].plot(df['Age'], df['Effort_Compensated'], 'g-', linewidth=2, label='Compensated (Biological Countercurvature)')
    axs[2].set_xlabel('Age (Years)', fontsize=12)
    axs[2].set_ylabel('Energetic Cost (Effort)', fontsize=12)
    axs[2].set_title('Energetic Consequences', fontsize=14)
    axs[2].set_ylim([0, max_plot_effort])
    axs[2].legend()
    axs[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

    print("Experiment complete.")

if __name__ == "__main__":
    setup_directories()
    run_experiment()
