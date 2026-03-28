"""
Baseline Predictive Processing Simulation (Active Inference)
Maps the PID controller from Paper 2 to Friston's active inference formalism:
- K_p <-> sensory precision on position
- K_d <-> sensory precision on velocity (generalised motion)
- K_i <-> prior precision on persistent causes
- tau <-> sensory delay

Building upon Baltieri & Buckley (2019) 'PID Control as a Process of Active Inference with Linear Generative Models'.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def plant_dynamics(y, t, u, tau, history):
    # Simple damped harmonic oscillator for the plant (spine)
    x, v = y
    omega_0 = 1.0  # Natural frequency
    zeta = 0.5     # Damping ratio

    # Use delayed state if available
    idx = int(t / dt)
    delay_idx = int(tau / dt)
    if idx >= delay_idx and len(history) > idx - delay_idx:
        x_delayed, v_delayed = history[idx - delay_idx]
    else:
        x_delayed, v_delayed = x, v

    dxdt = v
    dvdt = -omega_0**2 * x - 2 * zeta * omega_0 * v + u
    return [dxdt, dvdt]

def simulate_active_inference_pid():
    global dt
    dt = 0.01
    t = np.arange(0, 20, dt)

    # Active Inference parameters mapping to PID
    Kp = 5.0  # sensory precision on position
    Kd = 2.0  # sensory precision on velocity
    Ki = 0.5  # prior precision on persistent causes
    tau = 0.1 # sensory delay

    # Target state
    x_target = 1.0

    # Initialize history
    history = []
    u_history = []

    # Initial state
    y0 = [0.0, 0.0]

    # Integral term accumulator
    integral = 0.0

    x_hist = [y0[0]]
    v_hist = [y0[1]]

    for i in range(1, len(t)):
        # Active Inference step (calculating control u)
        # Assuming linear generative model where precision acts as gain

        # Get delayed observation
        delay_idx = int(tau / dt)
        if i >= delay_idx:
            x_obs = x_hist[i - delay_idx]
            v_obs = v_hist[i - delay_idx]
        else:
            x_obs = x_hist[-1]
            v_obs = v_hist[-1]

        # Error signals (Prediction Errors)
        ex = x_target - x_obs
        ev = 0.0 - v_obs # Target velocity is 0

        # Update integral (prior on persistent causes)
        integral += ex * dt

        # Action selection (Minimizing free energy -> gradient descent on prediction errors)
        # Control signal is sum of precision-weighted prediction errors
        u = Kp * ex + Kd * ev + Ki * integral
        u_history.append(u)

        # Plant step
        history.append([x_hist[-1], v_hist[-1]])
        y_next = odeint(plant_dynamics, [x_hist[-1], v_hist[-1]], [t[i-1], t[i]], args=(u, tau, history))

        x_hist.append(y_next[1, 0])
        v_hist.append(y_next[1, 1])

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(t, x_hist, label='Position (x)', color='blue')
    plt.plot(t, v_hist, label='Velocity (v)', color='orange')
    plt.axhline(y=x_target, color='r', linestyle='--', label='Target Position')
    plt.title('Baseline Predictive Processing Simulation (Active Inference)')
    plt.xlabel('Time')
    plt.ylabel('State')
    plt.legend()
    plt.grid(True)

    # Ensure directory exists
    import os
    os.makedirs('paper5_figures', exist_ok=True)

    plt.savefig('paper5_figures/baseline_active_inference.png')
    print("Simulation complete. Plot saved to paper5_figures/baseline_active_inference.png")

if __name__ == '__main__':
    simulate_active_inference_pid()
