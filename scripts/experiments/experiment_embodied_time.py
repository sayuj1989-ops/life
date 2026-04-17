import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

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

        # Assuming x[i] is the true state at time i (only known by a perfect observer)
        # Prediction error is the difference between predicted state and true state
        # In actual biology, true state isn't known, but we compute it to quantify the Free Energy of the system
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

def exp1_free_energy_landscape():
    print("Running Experiment 1: Free Energy Landscape...")
    tau = 0.18  # 180ms delay
    T_preds = np.linspace(0.0, 0.4, 40)

    results = []

    for T_pred in T_preds:
        stable, F, effort, _, _, _ = simulate_agent_full(tau, T_pred)
        results.append({
            'T_pred': T_pred,
            'Free_Energy': F if stable else np.nan,
            'Stable': stable,
            'Control_Effort': effort if stable else np.nan
        })

    df = pd.DataFrame(results)
    df.to_csv('outputs/embodied_time/free_energy_landscape.csv', index=False)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['T_pred'], df['Free_Energy'], 'b-', linewidth=2, marker='o')
    plt.axvline(tau, color='r', linestyle='--', label=f'Actual Delay $\\tau$={tau}s')

    # Mark min Free Energy
    if not df['Free_Energy'].isna().all():
        min_idx = df['Free_Energy'].idxmin()
        min_T_pred = df.loc[min_idx, 'T_pred']
        min_F = df.loc[min_idx, 'Free_Energy']
        plt.plot(min_T_pred, min_F, 'g*', markersize=15, label=f'Min Free Energy ($T_{{pred}}$={min_T_pred:.2f}s)')

    plt.title('Time Perception as a Thermodynamic Attractor\nFree Energy is minimized when Internal Time ($T_{pred}$) matches Physics ($\\tau$)', fontsize=14)
    plt.xlabel('Internal Predictive Horizon $T_{pred}$ (s)', fontsize=12)
    plt.ylabel('Free Energy Proxy $F$ (Error + Effort)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('outputs/embodied_time/free_energy_landscape.png', dpi=300)
    plt.close()
    print("Experiment 1 complete.")

def exp2_developmental_scaling():
    print("Running Experiment 2: Generative Model Bifurcation (Free Energy Landscape)...")
    # We create a more advanced conceptual visualization: The Energy Deficit Window
    # induces a pitchfork bifurcation in the Free Energy Landscape

    # Simulating the Free Energy F(x) = U(x) - T S
    # For a delayed system with degrading velocity precision (Kd collapse)
    x_range = np.linspace(-40, 40, 400)

    fig, ax = plt.subplots(figsize=(10, 6))

    # 1. Normal State (High precision Kd, Adaptive model)
    # Deep single minimum at x=0
    F_normal = 0.5 * (x_range)**2
    ax.plot(x_range, F_normal, 'g-', linewidth=2, label='Normal (High $\Pi_{y,1}$ Velocity Precision)')

    # 2. Onset of Rapid Growth (Precision starts dropping)
    F_transition = 0.1 * (x_range)**2 - 0.005 * (x_range)**4

    # 3. Pathological State (Derivative Gain Trap, Low precision Kd)
    # Pitchfork bifurcation: x=0 becomes a local maximum, creating two "Dark Room" minima (Lenke 1 types)
    F_scoliosis = -0.1 * (x_range)**2 + 0.0002 * (x_range)**4
    F_scoliosis -= np.min(F_scoliosis) # Normalize bottom to zero for visualization
    ax.plot(x_range, F_scoliosis, 'r-', linewidth=2, label='Scoliosis (Collapsed $\Pi_{y,1}$ precision)')

    ax.set_ylim(-5, 40)
    ax.set_xlabel('Spinal Postural Deflection (Degrees)')
    ax.set_ylabel('Free Energy F(x)')
    ax.set_title('Bifurcation of the Free Energy Landscape\nVelocity Precision Collapse creates "Dark Room" Attractors (Scoliosis)')
    ax.axvline(0, color='k', linestyle='--', alpha=0.3, label='Straight Spine (x=0)')

    # Annotate local minima
    minima_x = np.sqrt(0.1 / (2 * 0.0002))
    ax.plot([-minima_x, minima_x], [0, 0], 'r*', markersize=12)
    ax.annotate('Left Curve Attractor', xy=(-minima_x, 0), xytext=(-minima_x-15, 5), arrowprops=dict(facecolor='black', arrowstyle='->'))
    ax.annotate('Right Curve Attractor', xy=(minima_x, 0), xytext=(minima_x+5, 5), arrowprops=dict(facecolor='black', arrowstyle='->'))

    ax.legend(loc='upper center')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/fep_bifurcation_landscape.png', dpi=300)
    plt.close()

    print("Experiment 2 complete.")

if __name__ == "__main__":
    setup_directories()
    exp1_free_energy_landscape()
    exp2_developmental_scaling()
