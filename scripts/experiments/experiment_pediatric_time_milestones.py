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
    if L == 0:
        return np.array([0.0, 0.0])
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def compute_free_energy(x, u, alpha=1.0, beta=0.1, gamma=0.01):
    """Computes instantaneous Free Energy: F = 0.5 * (alpha * theta^2 + beta * dtheta^2 + gamma * u^2)"""
    theta = x[:, 0]
    dtheta = x[:, 1]

    # Mask nan values (where system collapsed)
    valid = ~np.isnan(theta)

    F = np.full_like(theta, np.nan)
    F[valid] = 0.5 * (alpha * theta[valid]**2 + beta * dtheta[valid]**2 + gamma * u[valid]**2)
    return F

def rk4(x, u, dt, L):
    """Runge-Kutta 4 integration."""
    if L == 0:
        return x
    k1 = dynamics(x, u, L=L)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L)
    k4 = dynamics(x + dt * k3, u, L=L)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_agent(tau, T_pred, L, Kp=20.0, Kd=8.0, T=4.0, dt=0.01):
    """
    Simulates a predictive agent with a specific neural delay (tau) and predictive horizon (T_pred).
    Returns True if stable (did not fall past 90 degrees), False otherwise.
    Also returns the total control effort and the total integrated Free Energy.
    """
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    # Initial condition: 5 degrees perturbation (0.087 rad)
    x[0] = np.array([0.087, 0.0])

    if L == 0:
        # Supine - unconditionally stable
        return True, 0.0, 0.0

    stable = True
    total_effort = 0.0

    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        # Predict state forward by T_pred
        x_hat = np.copy(x_obs)
        # Fast path if T_pred == 0
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                if idx_u < i:
                    u_hat = u[idx_u]
                else:
                    u_hat = 0.0 # No action assumed in the un-acted future
                x_hat = rk4(x_hat, u_hat, dt, L)

        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L)
        total_effort += abs(u[i]) * dt

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            total_effort = np.inf
            x[i+2:] = np.nan
            break

    # Calculate total Free Energy S = int F(t) dt
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

def run_milestone_sweep():
    print("Running Pediatric Milestone Sweep...")

    milestones = {
        'Supine': 0.0,          # L=0 (lying down, no inverted pendulum dynamics)
        'Head Control': 0.1,    # L=0.1 (balancing just the head)
        'Sitting': 0.3,         # L=0.3 (balancing the upper body)
        'Standing': 0.5         # L=0.5 (full body minus legs)
    }

    # Focus on realistic neural delay range and minimum required prediction
    taus = np.linspace(0.0, 0.4, 41) # 0 to 400ms delay

    results = []

    for name, L in milestones.items():
        print(f"Simulating {name} milestone (L={L}m)...")
        for tau in taus:
            min_T_pred = None
            min_free_energy = np.inf

            # Find the minimum T_pred required for stability
            # Search from 0 up to tau + 0.2
            for T_pred in np.linspace(0.0, tau + 0.2, 41):
                stable, effort, free_energy = simulate_agent(tau, T_pred, L)
                if stable:
                    if min_T_pred is None:
                        min_T_pred = T_pred
                        min_free_energy = free_energy
                    break # Found the minimum, move to next tau

            # If no stable T_pred found in range, mark as NaN
            if min_T_pred is None:
                min_T_pred = np.nan

            results.append({
                'Milestone': name,
                'Length_L': L,
                'Neural_Delay_tau': tau,
                'Min_T_pred': min_T_pred,
                'Total_Free_Energy': min_free_energy
            })

    df_sweep = pd.DataFrame(results)
    df_sweep.to_csv('outputs/pediatric_milestones/milestone_sweep.csv', index=False)

    # Plot
    plt.figure(figsize=(10, 6))

    for name in milestones.keys():
        subset = df_sweep[df_sweep['Milestone'] == name]
        plt.plot(subset['Neural_Delay_tau'], subset['Min_T_pred'], label=f'{name} (L={milestones[name]}m)', marker='o', markersize=4)

    # Add y=x reference line
    plt.plot(taus, taus, 'k--', alpha=0.5, label='Perfect Prediction ($T_{pred} = \\tau$)')

    plt.title('Ontogeny of Time Perception: Required Predictive Horizon\nAcross Pediatric Milestones', fontsize=14)
    plt.xlabel('Neural Delay $\\tau$ (s)', fontsize=12)
    plt.ylabel('Minimum Required Predictive Horizon $T_{pred}$ (s)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('outputs/pediatric_milestones/pediatric_time_milestones.png', dpi=300)
    # Also save to the current directory as requested by memory/plan instructions if ambiguous
    plt.savefig('pediatric_time_milestones.png', dpi=300)
    plt.close()

    print("Pediatric Milestone Sweep complete.")

if __name__ == "__main__":
    setup_directories()
    run_milestone_sweep()
