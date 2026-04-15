import numpy as np
import matplotlib.pyplot as plt

def simulate_active_inference_posture():
    dt = 0.01
    T = 60.0
    t_span = np.arange(0, T, dt)
    n_steps = len(t_span)

    # Delay steps
    delay_time = 0.1
    delay_steps = int(delay_time / dt)

    # State arrays
    x = np.zeros(n_steps)
    v = np.zeros(n_steps)
    a = np.zeros(n_steps)

    # Trackers for plotting
    I_phys_arr = np.zeros(n_steps)
    I_hat_arr = np.zeros(n_steps)

    # Observations
    y0 = np.zeros(n_steps)
    y1 = np.zeros(n_steps)

    # Internal model params
    m_phys = 10.0
    l_phys = 0.5
    I_phys = m_phys * l_phys**2
    k_phys = 20.0
    b_phys = 2.0
    g = 9.8

    m_hat = m_phys
    l_hat = l_phys
    I_hat = I_phys

    # Active inference variables
    Sigma_y1 = np.ones(n_steps) * 0.01
    Pi_y1 = np.ones(n_steps) * (1.0 / 0.01)
    eps_y1 = np.zeros(n_steps)

    # Baseline gains
    Kp_base = 150.0
    Kd_base = 30.0
    Pi_y1_base = 100.0

    # Growth phase
    growth_start = 10.0
    growth_end = 30.0

    # Learning rate for internal model
    eta = 0.05

    # Precision updating rate
    kappa = 0.5

    for i in range(1, n_steps):
        t = t_span[i]

        # Physical plant growth
        if growth_start <= t <= growth_end:
            m_phys += 5.0 / ((growth_end - growth_start) / dt)
            l_phys += 0.2 / ((growth_end - growth_start) / dt)
            I_phys = m_phys * l_phys**2

        # Internal model update (slow tracking)
        m_hat += eta * (m_phys - m_hat) * dt
        l_hat += eta * (l_phys - l_hat) * dt
        I_hat = m_hat * l_hat**2

        I_phys_arr[i] = I_phys
        I_hat_arr[i] = I_hat

        # Delayed observations
        obs_idx = max(0, i - delay_steps)
        y0[i] = x[obs_idx]
        y1[i] = v[obs_idx]

        # Generative model's forward prediction for velocity (from previous step's observation)
        prev_obs_idx = max(0, i - delay_steps - 1)
        prev_y0 = x[prev_obs_idx]
        prev_y1 = v[prev_obs_idx]
        prev_a = a[prev_obs_idx]

        # Nonlinear stiffness (soft limit for scoliosis)
        k_nl = k_phys * (1.0 + 5.0 * prev_y0**2)

        # Predicted velocity derivative
        v_dot_hat = (m_hat * g * l_hat * np.sin(prev_y0) - k_nl * prev_y0 - b_phys * prev_y1 + prev_a) / I_hat
        y1_hat = prev_y1 + v_dot_hat * dt

        # Prediction error
        eps_y1[i] = y1[i] - y1_hat

        # Precision update
        Sigma_y1[i] = Sigma_y1[i-1] + kappa * (eps_y1[i]**2 - Sigma_y1[i-1]) * dt
        Sigma_y1[i] = max(Sigma_y1[i], 1e-5) # Lower bound
        Pi_y1[i] = 1.0 / Sigma_y1[i]

        # Effective gains
        Kp = Kp_base
        # Kd tracks precision of velocity
        Kd = Kd_base * (Pi_y1[i] / Pi_y1_base)

        # Control action
        a[i] = - Kp * y0[i] - Kd * y1[i]

        # Plant dynamics (true)
        k_nl_phys = k_phys * (1.0 + 5.0 * x[i-1]**2)
        v_dot_phys = (m_phys * g * l_phys * np.sin(x[i-1]) - k_nl_phys * x[i-1] - b_phys * v[i-1] + a[i]) / I_phys

        v[i] = v[i-1] + v_dot_phys * dt
        x[i] = x[i-1] + v[i] * dt

        # Inject small persistent disturbance to break symmetry
        if t > 5.0:
            v[i] += 0.01 * dt

    I_phys_arr[0] = I_phys_arr[1]
    I_hat_arr[0] = I_hat_arr[1]

    # Plotting
    fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    axs[0].plot(t_span, x * 180/np.pi, 'b')
    axs[0].set_ylabel('Posture Angle (deg)')
    axs[0].set_title('Plant Posture over Time')
    axs[0].axvspan(growth_start, growth_end, color='r', alpha=0.1, label='Growth Spurt')
    axs[0].legend()

    axs[1].plot(t_span, I_phys_arr, 'k', label='True Inertia')
    axs[1].plot(t_span, I_hat_arr, 'r--', label='Internal Model Inertia')
    axs[1].set_ylabel('Inertia')
    axs[1].legend()

    axs[2].plot(t_span, Pi_y1, 'g')
    axs[2].set_ylabel(r'Velocity Precision $\Pi_{y,1}$')

    Kd_eff = Kd_base * (Pi_y1 / Pi_y1_base)
    axs[3].plot(t_span, Kd_eff, 'm')
    axs[3].set_ylabel('Effective Derivative Gain ($K_d$)')
    axs[3].set_xlabel('Time (s)')

    plt.tight_layout()
    plt.savefig('paper5_figures/precision_collapse.png')
    plt.close()

if __name__ == "__main__":
    simulate_active_inference_posture()
