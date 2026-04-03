import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('outputs/figures', exist_ok=True)

def sensor_response(strain, noise_signal, threshold=0.01):
    return np.where(np.abs(strain + noise_signal) > threshold, 1.0, 0.0)

def simulate_feedback(noise_type, noise_std, L=0.45, dt=0.01, steps=2000):
    mass = L**3 * 1000
    g = 9.81
    EI_passive = 0.01 * L**4
    theta = 0.005
    omega = 0.0
    gain = 5.0 * L**2
    tau_delay = int(0.1 / dt)

    theta_history = np.zeros(steps)
    theta_history[:tau_delay] = theta

    time = np.arange(steps) * dt

    if noise_type == 'none':
        noise = np.zeros(steps)
    elif noise_type == 'white':
        noise = np.random.normal(0, noise_std, steps)
    elif noise_type == 'structured':
        # Simulate physiological pink noise / heartbeat / muscle tremor
        # Fundamental frequency ~1.5 Hz (heartbeat/gait) + ~10 Hz (muscle tremor)
        noise = noise_std * (0.6 * np.sin(2 * np.pi * 1.5 * time) +
                             0.3 * np.sin(2 * np.pi * 10 * time) +
                             0.1 * np.random.normal(0, 1, steps))

    for i in range(tau_delay, steps):
        current_theta = theta_history[i-1]
        M_grav = mass * g * (L/2) * np.sin(current_theta)
        M_pass = -EI_passive * current_theta

        delayed_theta = theta_history[i - tau_delay]

        n_samples = 10
        idx_start = max(0, i - tau_delay - n_samples)
        idx_end = i - tau_delay
        if idx_end <= idx_start: idx_start = 0

        local_noise = noise[idx_start:idx_end] if idx_end > idx_start else np.array([0])

        fires = np.mean(sensor_response(np.full_like(local_noise, delayed_theta), local_noise))

        M_act = -gain * np.sign(delayed_theta) * fires
        M_tot = M_grav + M_pass + M_act

        I = (1/3) * mass * L**2
        alpha = M_tot / I
        omega += alpha * dt
        omega *= 0.95

        new_theta = current_theta + omega * dt
        theta_history[i] = new_theta

        if abs(new_theta) > 1.0:
            theta_history[i:] = new_theta
            break

    return theta_history

def main():
    time_steps = 2000
    dt = 0.01
    time = np.arange(time_steps) * dt

    theta_none = simulate_feedback('none', 0.0)
    theta_white = simulate_feedback('white', 0.008)
    theta_structured = simulate_feedback('structured', 0.008)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(time, np.rad2deg(theta_none), 'r-', linewidth=2, label='No Noise (Buckling)')
    ax.plot(time, np.rad2deg(theta_white), 'b--', linewidth=2, alpha=0.7, label='White Noise')
    ax.plot(time, np.rad2deg(theta_structured), 'g-', linewidth=2, label='Structured Physiological Noise (Optimal Stabilization)')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Spinal Deflection (degrees)')
    ax.set_title('Bio-Acoustic Tensegrity Dithering in Postural Control')
    ax.set_ylim(-30, 30)
    ax.axhline(0, color='k', linestyle='--', alpha=0.3)
    ax.axhline(10, color='r', linestyle=':', alpha=0.5)
    ax.axhline(-10, color='r', linestyle=':', alpha=0.5)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/figures/toy_model_tensegrity_resonance.png', dpi=300)
    print("Figure saved to outputs/figures/toy_model_tensegrity_resonance.png")

if __name__ == "__main__":
    main()
