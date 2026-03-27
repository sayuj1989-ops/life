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

def simulate_agent_full(tau, T_pred, L=1.0, m=1.0, Kp=20.0, Kd=8.0, T=4.0, dt=0.01, is_supine=False):
    """
    Simulates a predictive agent. For 'Supine', we assume gravity holds it stable.
    Returns whether it was stable, and the maximum free energy equivalent (prediction error proxy)
    """
    if is_supine:
        # Supine is infinitely stable against falling over in this context
        return True, 0.0, 0.0

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

    total_pred_error = np.sum(np.nan_to_num(pred_error))
    total_effort = np.sum(np.abs(u)*dt)

    # Simple proxy for Free Energy: α * Error + β * Effort
    F = 1.0 * total_pred_error + 0.1 * total_effort

    if not stable:
        F = np.inf

    return stable, F, total_effort

def run_pediatric_milestones_sweep():
    print("Running Pediatric Milestones Simulation...")

    # Milestones (L is center of mass height, tau is roughly sensory-motor delay)
    # T_pred_range to sweep
    milestones = [
        {'name': 'Supine', 'L': 0.1, 'tau': 0.05, 'is_supine': True},
        {'name': 'Head Control', 'L': 0.2, 'tau': 0.08, 'is_supine': False},
        {'name': 'Sitting', 'L': 0.4, 'tau': 0.12, 'is_supine': False},
        {'name': 'Standing', 'L': 0.6, 'tau': 0.15, 'is_supine': False}
    ]

    T_preds = np.linspace(0.0, 0.3, 30)

    results = []

    for stage in milestones:
        for T_pred in T_preds:
            # Scale control gains loosely with mass/height to maintain baseline controllability
            Kp = 20.0 * (stage['L']/1.0)
            Kd = 8.0 * (stage['L']/1.0)

            stable, F, _ = simulate_agent_full(
                tau=stage['tau'],
                T_pred=T_pred,
                L=stage['L'],
                Kp=Kp,
                Kd=Kd,
                is_supine=stage.get('is_supine', False)
            )

            results.append({
                'Milestone': stage['name'],
                'Length_L': stage['L'],
                'Neural_Delay_tau': stage['tau'],
                'Predictive_Horizon_Tpred': T_pred,
                'Stable': stable,
                'Free_Energy': F
            })

    df = pd.DataFrame(results)
    df.to_csv('outputs/pediatric_milestones/milestone_sweep.csv', index=False)

    # Calculate min required T_pred for each stage
    # For supine, it's 0. For others, it's the first T_pred where Free Energy is finite (stable)
    min_T_preds = []
    for stage in milestones:
        stage_df = df[df['Milestone'] == stage['name']]
        stable_df = stage_df[stage_df['Stable'] == True]
        if len(stable_df) > 0:
            min_t = stable_df['Predictive_Horizon_Tpred'].min()
        else:
            min_t = np.nan
        min_T_preds.append((stage['name'], min_t, stage['tau']))

    # Plot
    plt.figure(figsize=(12, 6))

    colors = ['gray', 'blue', 'orange', 'red']
    markers = ['o', 's', '^', 'D']

    for i, stage in enumerate(milestones):
        stage_df = df[df['Milestone'] == stage['name']]

        # Replace inf with a high value for plotting
        max_finite = df.loc[df['Free_Energy'] != np.inf, 'Free_Energy'].max()
        fe = stage_df['Free_Energy'].replace(np.inf, max_finite * 1.5)

        plt.plot(stage_df['Predictive_Horizon_Tpred'], fe,
                 label=f"{stage['name']} ($\\tau$={stage['tau']}s)",
                 color=colors[i], marker=markers[i], markevery=2)

        # Mark tau
        plt.axvline(stage['tau'], color=colors[i], linestyle=':', alpha=0.5)

    plt.title('Ontogeny of Time Perception: Pediatric Milestones\nFree Energy vs Predictive Horizon', fontsize=16)
    plt.xlabel('Predictive Horizon ($T_{pred}$) [s]', fontsize=14)
    plt.ylabel('Thermodynamic Free Energy (Action)', fontsize=14)
    plt.yscale('log')
    plt.grid(True, alpha=0.3)
    plt.legend(title='Developmental Stage')
    plt.tight_layout()
    plt.savefig('outputs/pediatric_milestones/pediatric_time_milestones.png', dpi=300)
    plt.close()

    print("Pediatric milestones simulation complete.")
    for name, min_t, tau in min_T_preds:
        print(f"Stage: {name}, Delay tau: {tau:.3f}s, Min Required T_pred: {min_t:.3f}s")


if __name__ == "__main__":
    setup_directories()
    run_pediatric_milestones_sweep()
