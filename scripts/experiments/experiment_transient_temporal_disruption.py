import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    """Non-linear inverted pendulum dynamics."""
    theta, omega = x
    dtheta = omega
    # ml^2 \ddot{\theta} = mgl \sin(\theta) + u
    if L == 0:
        domega = 0.0
    else:
        domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_agent_snapshot(tau, T_pred, L=1.0, m=1.0, T=4.0, dt=0.01):
    """
    Simulates a predictive agent for a short snapshot to calculate the Free Energy cost.
    """
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)

    x = np.zeros((steps, 2))
    u = np.zeros(steps)

    # Base control gains scaling loosely with length
    Kp_base = m * 9.81 * L * 1.5
    Kd_base = Kp_base * 0.4

    # The Derivative Gain Gap effect
    gap = max(0, tau - T_pred)
    # Derivative gain degrades if prediction horizon is shorter than physical delay
    Kd_eff = Kd_base * np.exp(-15.0 * gap)

    # Weighting for Free Energy: F = 0.5*alpha*theta^2 + 0.5*beta*omega^2 + 0.5*gamma*u^2
    alpha = 1.0
    beta = 0.1
    gamma = 0.01

    F_total = 0.0

    # Initial condition: small persistent perturbation
    x[0] = np.array([0.05, 0.0])
    stable = True

    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        # Simplified prediction: linear forward projection using current delayed observation
        if pred_steps > 0:
            x_pred_theta = x_obs[0] + x_obs[1] * (T_pred)
            x_pred_omega = x_obs[1]
        else:
            x_pred_theta = x_obs[0]
            x_pred_omega = x_obs[1]

        # PD Control using predicted state
        u[i] = -Kp_base * x_pred_theta - Kd_eff * x_pred_omega

        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        # Calculate instantaneous Free Energy
        F_inst = 0.5 * alpha * x[i+1, 0]**2 + 0.5 * beta * x[i+1, 1]**2 + 0.5 * gamma * u[i]**2
        F_total += F_inst * dt

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            F_total += 1000.0 * (steps - i) * dt # Heavy penalty for collapse
            break

    return F_total, stable

def exp_transient_temporal_disruption():
    """Simulates the derivative gain gap over adolescent growth."""
    print("Running Transient Temporal Disruption (Derivative Gain Gap)...")

    years = np.linspace(8, 18, 50)

    # Sigmoidal growth curve
    L_t = 1.0 + 0.6 / (1.0 + np.exp(-1.5 * (years - 12.5)))
    dL_dt = np.gradient(L_t, years)

    # Delay tau scales linearly with L
    tau_base = 0.05
    tau_t = tau_base + 0.06 * (L_t - 1.0)

    # T_pred tries to track tau but learns slowly
    T_pred_t = np.zeros_like(years)
    T_pred_t[0] = tau_t[0]

    learning_rate = 0.3
    for i in range(1, len(years)):
        dt_year = years[i] - years[i-1]
        dT = learning_rate * (tau_t[i-1] - T_pred_t[i-1]) * dt_year
        T_pred_t[i] = T_pred_t[i-1] + dT

    gap_t = np.maximum(0, tau_t - T_pred_t)

    F_t = np.zeros_like(years)
    F_perfect = np.zeros_like(years)

    for i in range(len(years)):
        F, _ = simulate_agent_snapshot(tau_t[i], T_pred_t[i], L=L_t[i], m=40.0, T=3.0, dt=0.01)
        F_t[i] = F

        # Perfect adaptation control case
        F_p, _ = simulate_agent_snapshot(tau_t[i], tau_t[i], L=L_t[i], m=40.0, T=3.0, dt=0.01)
        F_perfect[i] = F_p

    df = pd.DataFrame({
        'Age': years,
        'Height_L': L_t,
        'Growth_Vel': dL_dt,
        'Tau_delay': tau_t,
        'T_pred': T_pred_t,
        'Gap': gap_t,
        'FreeEnergy': F_t,
        'FreeEnergy_Ideal': F_perfect
    })
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    # Plotting
    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # Top Panel: Growth
    color = 'tab:blue'
    axs[0].set_ylabel('Height L(t) [m]', color=color, fontsize=12)
    axs[0].plot(years, L_t, color=color, linewidth=2, label='Height L(t)')
    axs[0].tick_params(axis='y', labelcolor=color)

    ax0_2 = axs[0].twinx()
    color2 = 'tab:gray'
    ax0_2.set_ylabel(r'Growth Velocity $\dot{L}$', color=color2, fontsize=12)
    ax0_2.plot(years, dL_dt, color=color2, linestyle='--', linewidth=2, label=r'Velocity $\dot{L}$')
    ax0_2.tick_params(axis='y', labelcolor=color2)
    axs[0].set_title('Adolescent Allometry', fontsize=14)

    # Middle Panel: Temporal Mismatch
    axs[1].plot(years, tau_t * 1000, 'k-', linewidth=2, label=r'Physical Delay $\tau(t)$')
    axs[1].plot(years, T_pred_t * 1000, 'b--', linewidth=2, label=r'Cognitive Horizon $T_{pred}(t)$')
    axs[1].fill_between(years, T_pred_t * 1000, tau_t * 1000, color='red', alpha=0.3, label='Derivative Gain Gap')
    axs[1].set_ylabel('Time (ms)', fontsize=12)
    axs[1].set_title('The Derivative Gain Gap', fontsize=14)
    axs[1].legend(loc='upper left')
    axs[1].grid(True, alpha=0.3)

    # Bottom Panel: Free Energy
    axs[2].plot(years, F_perfect, 'g--', linewidth=2, label=r'Ideal Adaptation ($\tau = T_{pred}$)')
    axs[2].plot(years, F_t, 'r-', linewidth=2.5, label=r'Lagging Adaptation ($T_{pred} < \tau$)')

    peak_idx = np.argmax(gap_t)
    axs[2].axvline(years[peak_idx], color='k', linestyle=':', label=f'Peak Vulnerability (Age {years[peak_idx]:.1f})')

    axs[2].set_xlabel('Age (Years)', fontsize=12)
    axs[2].set_ylabel(r'Thermodynamic Free Energy $\mathcal{F}$', fontsize=12)
    axs[2].set_title('Transient Instability (Scoliotic Drive)', fontsize=14)
    axs[2].legend(loc='upper left')
    axs[2].grid(True, alpha=0.3)

    # Cap y limit to handle explosive instability cleanly
    axs[2].set_ylim(0, np.max(F_perfect) * 6)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()
    print("Experiment complete. Saved outputs/embodied_time/transient_temporal_disruption.csv and .png")

if __name__ == "__main__":
    setup_directories()
    exp_transient_temporal_disruption()
