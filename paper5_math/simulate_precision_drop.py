import numpy as np
import matplotlib.pyplot as plt
import os

# Create output directory if it doesn't exist
os.makedirs('paper5_figures', exist_ok=True)

def simulate_active_inference_pendulum(L, Pi_0, Pi_1, delay_steps, total_time, dt):
    """
    Simulates a 1D inverted pendulum with a delayed Active Inference controller.
    Action: a = -Pi_0 * e_0 - Pi_1 * e_1
    """
    n_steps = int(total_time / dt)
    theta = np.zeros(n_steps)
    theta_dot = np.zeros(n_steps)

    # Constants
    g = 9.81
    m = 1.0 # arbitrary mass

    # Initial condition (small perturbation)
    theta[0] = 0.05
    theta_dot[0] = 0.0

    for t in range(1, n_steps):
        # Delayed sensor readings
        idx_delay = max(0, t - delay_steps)
        e_0 = theta[idx_delay]     # Position error
        e_1 = theta_dot[idx_delay] # Velocity error

        # Action (Active Inference gradient descent step mapped to force)
        action = -Pi_0 * e_0 - Pi_1 * e_1

        # Physics: tau = I * alpha => a_angular = tau / I
        # Gravity torque + Action torque
        I = m * L**2
        torque_g = m * g * L * np.sin(theta[t-1])

        # Simplify action as a torque directly applied
        alpha = (torque_g + action) / I

        # Euler integration
        theta_dot[t] = theta_dot[t-1] + alpha * dt
        theta[t] = theta[t-1] + theta_dot[t] * dt

    return theta

# Simulation parameters
dt = 0.01
total_time = 5.0
time = np.arange(0, total_time, dt)
delay = 0.05 # 50ms delay
delay_steps = int(delay / dt)

# Baseline: Pre-growth, stable
L_base = 0.5
Pi_0_base = 20.0
Pi_1_base = 5.0

# Growth phase: Length increases, Velocity Precision (Pi_1) drops
L_growth = 1.0
Pi_0_growth = 20.0
Pi_1_growth = 0.5 # Severe precision drop

# Simulate
theta_base = simulate_active_inference_pendulum(L_base, Pi_0_base, Pi_1_base, delay_steps, total_time, dt)
theta_growth = simulate_active_inference_pendulum(L_growth, Pi_0_growth, Pi_1_growth, delay_steps, total_time, dt)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time, theta_base, label=f'Baseline (L={L_base}m, Pi_1={Pi_1_base})', color='blue')
plt.plot(time, theta_growth, label=f'Growth Phase (L={L_growth}m, Pi_1={Pi_1_growth})', color='red', linestyle='--')
plt.axhline(0, color='black', linewidth=0.5)
plt.title('Active Inference Postural Control: Precision Drop vs Growth')
plt.xlabel('Time (s)')
plt.ylabel('Postural Angle (rad)')
plt.legend()
plt.grid(True)

plt.savefig('paper5_figures/active_inference_wobble.png')
print("Simulation complete. Plot saved to paper5_figures/active_inference_wobble.png")
