import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    """Non-linear inverted pendulum dynamics."""
    theta, omega = x
    dtheta = omega
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    """Runge-Kutta 4 integration."""
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_transient_disruption(T=10.0, dt=0.01):
    """
    Simulates three branches of the temporal perception model during rapid growth.
    Phase 1: Life (Stable, T_pred >= tau)
    Phase 2: Disruption (T_pred < tau) - The Derivative Gain Gap
    Phase 3: Resolution (Death vs Exaptation/Buckling)
    """
    steps = int(T / dt)
    t = np.linspace(0, T, steps)

    # Base params
    m = 1.0
    L_base = 1.0
    tau = 0.18  # 180ms neural delay
    delay_steps = int(tau / dt)

    # The agent's cognitive predictive horizon (T_pred) profile over time
    T_pred = np.full(steps, tau)  # Phase 1: Perfect prediction

    # Phase 2: Disruption occurs from t=3 to t=7 (Growth spurt, cognitive lag)
    disrupt_start_idx = int(3.0 / dt)
    disrupt_end_idx = int(7.0 / dt)
    # T_pred lags behind tau during this period
    T_pred[disrupt_start_idx:disrupt_end_idx] = np.linspace(tau, 0.05, disrupt_end_idx - disrupt_start_idx)
    T_pred[disrupt_end_idx:] = 0.05 # Stays disrupted for branching

    Kp = 20.0
    Kd = 8.0

    alpha, beta, gamma = 1.0, 0.1, 0.01 # Free energy weights

    def run_branch(exaptation=False):
        x = np.zeros((steps, 2))
        u = np.zeros(steps)
        F = np.zeros(steps)

        # Small initial perturbation
        x[0] = np.array([0.05, 0.0])
        stable = True

        for i in range(steps - 1):
            # Exaptation (Buckling): Drop effective length at t=5.5
            current_L = L_base
            if exaptation and t[i] >= 5.5:
                current_L = L_base * 0.5 # Symmetry breaking reduces effective height
                # Also effectively lowers required Kp/Kd because mechanical advantage changes
                current_Kp = Kp * 0.5
                current_Kd = Kd * 0.5
            else:
                current_Kp = Kp
                current_Kd = Kd

            obs_idx = max(0, i - delay_steps)
            x_obs = x[obs_idx]

            # Predict state forward by T_pred[i]
            pred_steps = int(T_pred[i] / dt)
            x_hat = np.copy(x_obs)
            if pred_steps > 0:
                for j in range(pred_steps):
                    idx_u = obs_idx + j
                    u_hat = u[idx_u] if idx_u < i else 0.0
                    x_hat = rk4(x_hat, u_hat, dt, L=current_L, m=m)

            # Control
            u[i] = -current_Kp * x_hat[0] - current_Kd * x_hat[1]
            x[i+1] = rk4(x[i], u[i], dt, L=current_L, m=m)

            # Instantaneous Free Energy
            F[i] = 0.5 * (alpha * x[i, 0]**2 + beta * x[i, 1]**2 + gamma * u[i]**2)

            # Structural failure threshold
            if abs(x[i+1, 0]) > np.pi/2:
                stable = False
                F[i+1:] = np.nan
                x[i+1:] = np.nan
                break

        # Last F
        if stable:
            F[steps-1] = 0.5 * (alpha * x[steps-1, 0]**2 + beta * x[steps-1, 1]**2 + gamma * u[steps-1]**2)

        return F, x, stable

    # Run branches
    F_death, x_death, _ = run_branch(exaptation=False)
    F_scoliosis, x_scoliosis, _ = run_branch(exaptation=True)

    # Run ideal for baseline comparison
    T_pred_ideal = np.full(steps, tau)
    F_ideal = np.zeros(steps)
    x_ideal = np.zeros((steps, 2))
    u_ideal = np.zeros(steps)
    x_ideal[0] = np.array([0.05, 0.0])
    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x_ideal[obs_idx]
        pred_steps = int(T_pred_ideal[i] / dt)
        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                u_hat = u_ideal[idx_u] if idx_u < i else 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L_base, m=m)
        u_ideal[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x_ideal[i+1] = rk4(x_ideal[i], u_ideal[i], dt, L=L_base, m=m)
        F_ideal[i] = 0.5 * (alpha * x_ideal[i, 0]**2 + beta * x_ideal[i, 1]**2 + gamma * u_ideal[i]**2)
    F_ideal[steps-1] = 0.5 * (alpha * x_ideal[steps-1, 0]**2 + beta * x_ideal[steps-1, 1]**2 + gamma * u_ideal[steps-1]**2)

    return t, T_pred, F_death, F_scoliosis, F_ideal

def main():
    setup_directories()
    t, T_pred, F_death, F_scoliosis, F_ideal = simulate_transient_disruption()

    # Save CSV
    df = pd.DataFrame({
        'time': t,
        'T_pred': T_pred,
        'F_ideal': F_ideal,
        'F_death': F_death,
        'F_scoliosis': F_scoliosis
    })
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # Panel 1: The temporal disruption
    ax1.plot(t, np.full_like(t, 0.18), 'k--', label=r'Physical Delay $\tau$')
    ax1.plot(t, T_pred, 'b-', linewidth=2, label=r'Cognitive Horizon $T_{pred}$')
    ax1.axvspan(3.0, 7.0, color='red', alpha=0.1, label='The Derivative Gain Gap (Growth Spurt)')
    ax1.set_ylabel('Time (s)', fontsize=12)
    ax1.set_title('Transient Disruption of Temporal Cognition During Growth', fontsize=14)
    ax1.legend(loc='lower left')
    ax1.grid(True, alpha=0.3)

    # Panel 2: Thermodynamic Resolution
    ax2.plot(t, F_ideal, 'g--', linewidth=2, label='Stable Life (Perfect Time Perception)')

    # Plot death line up to nan
    valid_death = ~np.isnan(F_death)
    ax2.plot(t[valid_death], F_death[valid_death], 'r-', linewidth=2.5, label='Thermodynamic Collapse (Death)')
    if not valid_death.all():
        idx_fail = np.where(valid_death == False)[0][0] - 1
        ax2.plot(t[idx_fail], F_death[idx_fail], 'rX', markersize=10, label='Structural Failure')

    # Plot exaptation/scoliosis
    ax2.plot(t, F_scoliosis, 'purple', linewidth=2.5, label='Symmetry Breaking Exaptation (Scoliosis)')
    ax2.axvline(5.5, color='purple', linestyle=':', label='Buckling Event ($L$ reduced)')

    ax2.set_ylabel(r'Thermodynamic Free Energy $\mathcal{F}(t)$', fontsize=12)
    ax2.set_xlabel('Time (s)', fontsize=12)
    ax2.set_title('Scoliosis as Thermodynamic Exaptation (Bounding Free Energy)', fontsize=14)
    ax2.set_yscale('log')
    ax2.set_ylim([1e-4, 1e2])
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()

    print("Simulation complete. Outputs saved.")

if __name__ == '__main__':
    main()
