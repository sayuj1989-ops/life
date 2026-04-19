import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('outputs/figures', exist_ok=True)

def sensor_response(strain, noise_std, threshold=0.01):
    noise = np.random.normal(0, noise_std, size=strain.shape)
    return np.where(np.abs(strain + noise) > threshold, 1.0, 0.0)

def simulate_dither_therapy(L=0.45, dt=0.01, steps=3000):
    mass = L**3 * 1000
    g = 9.81
    EI_passive = 0.01 * L**4
    theta = 0.005
    omega = 0.0
    gain = 5.0 * L**2
    tau_delay = int(0.1 / dt)

    theta_history = np.zeros(steps)
    theta_history[:tau_delay] = theta

    # Noise profile over time
    # Phase 1 (0-1000): Normal physiological noise
    # Phase 2 (1000-2000): Growth spurt (low noise -> sensor lock up)
    # Phase 3 (2000-3000): Dither Therapy (high external noise)
    noise_std = np.zeros(steps)
    noise_std[:1000] = 0.008
    noise_std[1000:2000] = 0.001
    noise_std[2000:] = 0.015

    for i in range(tau_delay, steps):
        current_theta = theta_history[i-1]
        M_grav = mass * g * (L/2) * np.sin(current_theta)
        M_pass = -EI_passive * current_theta

        delayed_theta = theta_history[i - tau_delay]
        strain_signal = delayed_theta

        n_samples = 10
        current_noise = noise_std[i]
        sensor_fires = np.mean([sensor_response(np.array([strain_signal]), current_noise)[0] for _ in range(n_samples)])

        M_act = -gain * np.sign(delayed_theta) * sensor_fires
        M_tot = M_grav + M_pass + M_act

        I = (1/3) * mass * L**2
        alpha = M_tot / I

        omega += alpha * dt
        omega *= 0.95

        new_theta = current_theta + omega * dt

        # Limit the deflection so we can see the rescue
        if new_theta > 1.2:
            new_theta = 1.2
            omega = 0
        elif new_theta < -1.2:
            new_theta = -1.2
            omega = 0

        theta_history[i] = new_theta

    return theta_history

def main():
    time_steps = 3000
    dt = 0.01
    time = np.arange(time_steps) * dt

    theta_history = simulate_dither_therapy(steps=time_steps)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot phases
    ax.axvspan(0, 10, color='green', alpha=0.1, label='Phase 1: Normal Physiology')
    ax.axvspan(10, 20, color='red', alpha=0.1, label='Phase 2: Growth Spurt (Lock-up)')
    ax.axvspan(20, 30, color='blue', alpha=0.1, label='Phase 3: Vibratory Dither Therapy')

    ax.plot(time, np.rad2deg(theta_history), 'k-', linewidth=2)

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Spinal Deflection (degrees)')
    ax.set_title('Vibratory Dither Therapy Rescue (Stochastic Resonance Model)')
    ax.axhline(0, color='k', linestyle='--', alpha=0.3)
    ax.axhline(10, color='r', linestyle=':', alpha=0.5)
    ax.text(1, 11, r'Clinical Scoliosis Threshold ($10^\circ$)', color='r')

    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = 'outputs/figures/dither_therapy_rescue.png'
    plt.savefig(output_path, dpi=300)
    print(f"Figure saved to {output_path}")

if __name__ == "__main__":
    main()
