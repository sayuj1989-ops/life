import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

def setup_directories():
    os.makedirs('outputs/pediatric_milestones', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    """Non-linear inverted pendulum dynamics."""
    theta, omega = x
    dtheta = omega
    # Equation of motion: ml^2 \ddot{\theta} = mgl \sin(\theta) + u
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, g=9.81, L=1.0, m=1.0):
    """Runge-Kutta 4 integration."""
    k1 = dynamics(x, u, g=g, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, g=g, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, g=g, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, g=g, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_agent_full(tau, T_pred, g=9.81, L=1.0, m=1.0, Kp=20.0, Kd=8.0, T=4.0, dt=0.01, is_supine=False):
    """
    Simulates a predictive agent and returns detailed history for Free Energy computation.
    """
    if is_supine:
        # Supine infants aren't acting as inverted pendulums, gravity vector is perpendicular
        g = 0.0

    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    # Initial condition: 5 degrees perturbation (0.087 rad)
    x[0] = np.array([0.087, 0.0])

    stable = True
    total_effort = 0.0

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
                x_hat = rk4(x_hat, u_hat, dt, g=g, L=L, m=m)

        # Control based on predicted state
        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, g=g, L=L, m=m)
        total_effort += abs(u[i]) * dt

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            total_effort = np.inf
            x[i+2:] = np.nan
            break

    # Calculate Free Energy S = int F(t) dt
    alpha, beta, gamma = 1.0, 0.1, 0.01
    F = np.zeros(steps)
    valid_len = steps if stable else i+2
    for k in range(valid_len):
        if not np.isnan(x[k, 0]):
            F[k] = 0.5 * (alpha * x[k, 0]**2 + beta * x[k, 1]**2 + gamma * u[k]**2)

    if not stable:
        total_free_energy = np.inf
    else:
        total_free_energy = np.sum(F) * dt

    return stable, total_effort, total_free_energy

def run_pediatric_milestones_sweep():
    print("Running Pediatric Milestones Sweep (Ontogeny of Time Perception)...")

    # Defined pediatric developmental milestones
    # L represents the effective inverted pendulum length (distance to CoM)
    # tau represents typical neural processing delays at that age
    milestones = [
        {'name': 'Supine', 'age_mo': 0, 'L': 0.15, 'm': 3.5, 'tau': 0.05, 'is_supine': True, 'Kp_base': 5.0, 'Kd_base': 2.0},
        {'name': 'Head Control', 'age_mo': 3, 'L': 0.20, 'm': 6.0, 'tau': 0.08, 'is_supine': False, 'Kp_base': 10.0, 'Kd_base': 4.0},
        {'name': 'Sitting', 'age_mo': 6, 'L': 0.35, 'm': 7.5, 'tau': 0.12, 'is_supine': False, 'Kp_base': 15.0, 'Kd_base': 6.0},
        {'name': 'Standing', 'age_mo': 12, 'L': 0.50, 'm': 10.0, 'tau': 0.15, 'is_supine': False, 'Kp_base': 25.0, 'Kd_base': 10.0}
    ]

    # Evaluate over a range of predictive horizons
    T_preds = np.linspace(0.0, 0.3, 30)

    all_results = []

    for ms in milestones:
        for T_pred in T_preds:
            # Scale gains roughly with mass and length
            Kp = ms['Kp_base'] * ms['m'] * ms['L']
            Kd = ms['Kd_base'] * ms['m'] * ms['L']

            stable, effort, free_energy = simulate_agent_full(
                tau=ms['tau'],
                T_pred=T_pred,
                L=ms['L'],
                m=ms['m'],
                Kp=Kp,
                Kd=Kd,
                is_supine=ms['is_supine']
            )

            all_results.append({
                'Milestone': ms['name'],
                'Age_Months': ms['age_mo'],
                'Length_L': ms['L'],
                'Mass_m': ms['m'],
                'Delay_tau': ms['tau'],
                'Predictive_Horizon_Tpred': T_pred,
                'Stable': int(stable),
                'Total_Free_Energy': free_energy,
                'Control_Effort': effort
            })

    df = pd.DataFrame(all_results)
    df.to_csv('outputs/pediatric_milestones/milestone_sweep.csv', index=False)

    print("Generating visualization...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, ms_name in enumerate(df['Milestone'].unique()):
        ax = axes[idx]
        subset = df[df['Milestone'] == ms_name]

        # Plot Free Energy vs Predictive Horizon
        # Cap Free Energy for visualization
        fe_vals = subset['Total_Free_Energy'].values
        max_finite = np.nanmax(fe_vals[fe_vals != np.inf]) if np.any((fe_vals != np.inf) & ~np.isnan(fe_vals)) else 10.0
        capped_fe = np.where(fe_vals == np.inf, max_finite * 2, fe_vals)

        ax.plot(subset['Predictive_Horizon_Tpred'], capped_fe, 'b-', linewidth=2)

        # Mark actual delay tau
        tau = subset['Delay_tau'].iloc[0]
        ax.axvline(tau, color='r', linestyle='--', label=f'Neural Delay ($\\tau$ = {tau}s)')

        # Highlight minimum Free Energy
        valid_subset = subset[subset['Total_Free_Energy'] != np.inf]
        if not valid_subset.empty:
            min_idx = valid_subset['Total_Free_Energy'].idxmin()
            min_Tpred = valid_subset.loc[min_idx, 'Predictive_Horizon_Tpred']
            min_FE = valid_subset.loc[min_idx, 'Total_Free_Energy']
            ax.plot(min_Tpred, min_FE, 'g*', markersize=15, label=f'Optimal $T_{{pred}}$ = {min_Tpred:.2f}s')

            # Shaded region indicating "Zone of Life" (where Free Energy is reasonably bounded)
            threshold = min_FE * 2.0
            life_zone = subset[subset['Total_Free_Energy'] <= threshold]
            if not life_zone.empty:
                ax.axvspan(life_zone['Predictive_Horizon_Tpred'].min(), life_zone['Predictive_Horizon_Tpred'].max(), alpha=0.2, color='green', label='Stable "Life" Zone')

        ax.set_title(f'Milestone: {ms_name} ({subset["Age_Months"].iloc[0]} mo)', fontsize=14)
        ax.set_xlabel('Predictive Horizon $T_{pred}$ (s)', fontsize=12)
        ax.set_ylabel(r'Thermodynamic Free Energy $\mathcal{F}$', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')

        # Set y limits based on capped values
        ax.set_ylim([0, max_finite * 2.2])

    plt.suptitle(r'Ontogeny of Time Perception: The Emergence of Predictive Control' + '\n' + r'As infants develop into unstable inverted pendulums, temporal prediction ($T_{pred} \geq \tau$) becomes a thermodynamic necessity for life.', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('outputs/pediatric_milestones/pediatric_time_milestones.png', dpi=300)
    plt.close()

    print("Experiment complete. Outputs saved in 'outputs/pediatric_milestones/'.")

if __name__ == "__main__":
    setup_directories()
    run_pediatric_milestones_sweep()
