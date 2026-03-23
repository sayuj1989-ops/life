import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

def setup_directories():
    os.makedirs('outputs/pediatric_milestones', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    """Non-linear inverted pendulum dynamics."""
    theta, omega = x
    dtheta = omega
    # Equation of motion: ml^2 \ddot{\theta} = mgl \sin(\theta) + u
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    """Runge-Kutta 4 integration."""
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def compute_free_energy(pred_error_hist, effort_hist, alpha=1.0, beta=0.1):
    """
    Computes a proxy for Free Energy: F = alpha * Prediction_Error + beta * Control_Effort
    """
    total_pred_error = np.sum(np.nan_to_num(pred_error_hist))
    total_effort = np.sum(np.nan_to_num(effort_hist))
    return alpha * total_pred_error + beta * total_effort

def simulate_agent_full(tau, T_pred, L=1.0, m=1.0, Kp=20.0, Kd=8.0, T=4.0, dt=0.01):
    """
    Simulates a predictive agent and returns detailed history for Free Energy computation.
    """
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    pred_error = np.zeros(steps)

    # Initial condition: 5 degrees perturbation (0.087 rad)
    x[0] = np.array([0.087, 0.0])

    stable = True

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
                    u_hat = 0.0 # No action assumed in the un-acted future
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        pred_error[i] = np.linalg.norm(x_hat - x[i])

        # Control based on predicted state
        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            # Penalize heavily if it falls
            pred_error[i:] = 1000.0
            u[i:] = 1000.0
            break

    # Calculate Free Energy proxy
    F = compute_free_energy(pred_error, np.abs(u)*dt)
    total_effort = np.sum(np.abs(u)*dt)

    return stable, F, total_effort, x, u, pred_error

def exp_pediatric_milestones():
    print("Running Pediatric Milestones Simulation...")

    # Define developmental milestones
    # L: approx length of inverted pendulum segment (m)
    # tau: neural delay approx (s)
    stages = [
        {'name': 'Supine Infant (Stable)', 'L': 0.1, 'tau': 0.05, 'g_eff': 0.0}, # g=0 to simulate supine
        {'name': 'Head Control (3mo)', 'L': 0.15, 'tau': 0.08, 'g_eff': 9.81},
        {'name': 'Sitting (6mo)', 'L': 0.35, 'tau': 0.12, 'g_eff': 9.81},
        {'name': 'Standing (12mo)', 'L': 0.55, 'tau': 0.15, 'g_eff': 9.81},
        {'name': 'Walking Toddler', 'L': 0.7, 'tau': 0.18, 'g_eff': 9.81}
    ]

    T_preds = np.linspace(0.0, 0.3, 31) # 0 to 300ms

    all_results = []

    plt.figure(figsize=(12, 8))

    colors = sns.color_palette("husl", len(stages))

    for idx, stage in enumerate(stages):
        L = stage['L']
        tau = stage['tau']
        name = stage['name']
        g = stage['g_eff']

        Kp = 20.0 * (L/1.0)
        Kd = 8.0 * (L/1.0)

        # Override dynamics g locally if needed, but rk4 uses dynamics default.
        # We'll just define a lambda to pass g.
        def custom_rk4(x, u, dt, L=1.0, m=1.0):
            k1 = dynamics(x, u, g=g, L=L, m=m)
            k2 = dynamics(x + 0.5 * dt * k1, u, g=g, L=L, m=m)
            k3 = dynamics(x + 0.5 * dt * k2, u, g=g, L=L, m=m)
            k4 = dynamics(x + dt * k3, u, g=g, L=L, m=m)
            return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

        # Need a modified simulate_agent_full to use custom_rk4
        def simulate_custom(tau, T_pred, L=1.0, m=1.0, Kp=20.0, Kd=8.0, T=4.0, dt=0.01):
            steps = int(T / dt)
            delay_steps = int(tau / dt)
            pred_steps = int(T_pred / dt)

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
                        x_hat = custom_rk4(x_hat, u_hat, dt, L=L, m=m)

                pred_error[i] = np.linalg.norm(x_hat - x[i])

                u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
                x[i+1] = custom_rk4(x[i], u[i], dt, L=L, m=m)

                if abs(x[i+1, 0]) > np.pi/2:
                    stable = False
                    pred_error[i:] = 1000.0
                    u[i:] = 1000.0
                    break

            F = compute_free_energy(pred_error, np.abs(u)*dt)
            return stable, F

        stage_F = []
        for T_pred in T_preds:
            stable, F = simulate_custom(tau, T_pred, L=L, Kp=Kp, Kd=Kd)
            stage_F.append(F if stable else np.nan)
            all_results.append({
                'Stage': name,
                'L': L,
                'tau': tau,
                'T_pred': T_pred,
                'Free_Energy': F if stable else np.nan,
                'Stable': stable
            })

        plt.plot(T_preds, stage_F, label=f"{name} ($\\tau$={tau}s)", color=colors[idx], linewidth=2, marker='o', markersize=4)
        if tau > 0:
            plt.axvline(tau, color=colors[idx], linestyle='--', alpha=0.5)

    plt.title('Ontogeny of Time Perception: Free Energy Landscapes across Pediatric Milestones\nTime Perception ($T_{pred}$) is a Control-Theoretic Necessity to bound Free Energy', fontsize=14)
    plt.xlabel('Internal Predictive Horizon $T_{pred}$ (s)', fontsize=12)
    plt.ylabel('Thermodynamic Free Energy (Action)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('outputs/pediatric_milestones/milestone_free_energy.png', dpi=300)
    plt.close()

    df = pd.DataFrame(all_results)
    df.to_csv('outputs/pediatric_milestones/pediatric_milestones_data.csv', index=False)

    # Calculate minimal T_pred for stability at each stage
    min_t_preds = []
    for stage in stages:
        stage_data = df[(df['Stage'] == stage['name']) & (df['Stable'] == True)]
        if len(stage_data) > 0:
            # We define minimal T_pred as the one that minimizes Free Energy
            best_row = stage_data.loc[stage_data['Free_Energy'].idxmin()]
            min_t_preds.append({
                'Stage': stage['name'],
                'L': stage['L'],
                'Optimal_T_pred': best_row['T_pred'],
                'Required_T_pred_for_stability': stage_data['T_pred'].min()
            })

    df_min = pd.DataFrame(min_t_preds)

    plt.figure(figsize=(10, 6))
    x = np.arange(len(df_min))
    plt.bar(x, df_min['Required_T_pred_for_stability'], color='royalblue')
    plt.xticks(x, df_min['Stage'], rotation=15)
    plt.ylabel('Minimal Predictive Horizon $T_{pred}$ Required (s)', fontsize=12)
    plt.title('The Developmental Emergence of Time Perception\nMinimal $T_{pred}$ strictly required to avoid structural collapse (Death)', fontsize=14)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('outputs/pediatric_milestones/critical_t_pred_bar.png', dpi=300)
    plt.close()

    print("Pediatric Milestones Simulation complete.")

if __name__ == "__main__":
    setup_directories()
    exp_pediatric_milestones()
