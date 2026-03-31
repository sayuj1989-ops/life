import numpy as np
import matplotlib.pyplot as plt

def run_fep_sim(growth_velocity, tau, steps=1000):
    dt = 0.01

    # Plant parameters (simplified inverted pendulum)
    m = 10.0  # Mass
    g = 9.81  # Gravity
    L_initial = 0.5 # Initial length

    # Generative model priors
    theta_prior = 0.0
    vel_prior = 0.0

    # Precisions
    pi_pos = 100.0  # Proportional

    # State tracking
    theta_true = np.zeros(steps)
    theta_vel_true = np.zeros(steps)

    # The generative model estimate of the delayed state
    mu_theta = np.zeros(steps)
    mu_vel = np.zeros(steps)

    # Precision tracking
    pi_vel_history = np.zeros(steps)

    # Delay buffer
    delay_steps = int(tau / dt)
    if delay_steps == 0: delay_steps = 1

    for t in range(1, steps):
        # 1. Update plant parameters (growth)
        L = L_initial + growth_velocity * (t * dt)

        # 2. Plant Dynamics (True state)
        # T_grav = m * g * L * np.sin(theta_true[t-1])
        # Simple linearised pendulum with noise
        noise_x = np.random.normal(0, 0.05)

        # 3. Model updates & Precision Collapse (The Core FEP Mechanism)
        # Variance of velocity prediction error scales with growth velocity and delay
        sigma_sq_v = 0.1 + (growth_velocity * tau) * 5.0

        # Precision is inverse variance
        pi_vel = 1.0 / sigma_sq_v
        pi_vel_history[t] = pi_vel

        # 4. Delayed Observation
        idx = max(0, t - delay_steps)
        obs_theta = theta_true[idx] + np.random.normal(0, 0.01)
        obs_vel = theta_vel_true[idx] + np.random.normal(0, 0.01)

        # 5. Active Inference (Action to minimise prediction error)
        # Action is proportional to precision-weighted prediction errors
        # a = - dF/da
        err_pos = obs_theta - theta_prior
        err_vel = obs_vel - vel_prior

        # The control signal
        action = -(pi_pos * err_pos + pi_vel * err_vel * 100.0)

        # Update true state (Euler integration)
        theta_vel_true[t] = theta_vel_true[t-1] + (action + m*g*L*theta_true[t-1] + noise_x) * dt
        theta_true[t] = theta_true[t-1] + theta_vel_true[t] * dt

    return theta_true, pi_vel_history

if __name__ == "__main__":
    t_slow = run_fep_sim(growth_velocity=0.01, tau=0.1)
    t_fast = run_fep_sim(growth_velocity=0.2, tau=0.2)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(t_slow[0], label="Slow Growth (Stable)")
    plt.plot(t_fast[0], label="Fast Growth (Unstable)")
    plt.title("Postural Angle (FEP Model)")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(t_slow[1], label="Pi_vel (Slow)")
    plt.plot(t_fast[1], label="Pi_vel (Fast)")
    plt.title("Precision on Velocity Error")
    plt.legend()

    plt.tight_layout()
    plt.savefig("paper5_figures/precision_collapse.png")
    print("Simulation complete. Figure saved.")
