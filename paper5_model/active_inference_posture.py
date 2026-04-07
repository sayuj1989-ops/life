import numpy as np
import matplotlib.pyplot as plt
import os

def run_simulation(pi_v_list):
    """
    Simulates a simple inverted pendulum (posture) controlled by active inference.
    Pi_v is the precision of velocity errors (effectively K_d).
    """
    dt = 0.01
    t_max = 5.0
    time = np.arange(0, t_max, dt)

    # Physics parameters
    m = 1.0
    g = 9.81
    l = 1.0

    # Active Inference Parameters
    pi_p = 50.0  # Precision of position (K_p)

    plt.figure(figsize=(10, 6))

    for pi_v in pi_v_list:
        theta = np.zeros_like(time)
        theta_dot = np.zeros_like(time)

        # Initial perturbation
        theta[0] = 0.1
        theta_dot[0] = 0.0

        for i in range(1, len(time)):
            # Sensory prediction error (desired theta = 0)
            err_p = theta[i-1] - 0.0
            err_v = theta_dot[i-1] - 0.0

            # Action minimizes prediction error weighted by precision
            # action a ~ torque
            torque = - (pi_p * err_p + pi_v * err_v)

            # Physics update: tau = I * alpha
            # I = m * l^2
            # alpha = (m*g*l*sin(theta) + torque) / I
            I = m * l**2
            alpha = (m * g * l * np.sin(theta[i-1]) + torque) / I

            theta_dot[i] = theta_dot[i-1] + alpha * dt
            theta[i] = theta[i-1] + theta_dot[i] * dt

        plt.plot(time, theta, label=f'Pi_v (K_d) = {pi_v}')

    plt.title('Active Inference Postural Control: Effect of Velocity Precision (Pi_v)')
    plt.xlabel('Time (s)')
    plt.ylabel('Sway Angle (rad)')
    plt.axhline(0, color='black', linestyle='--')
    plt.legend()
    plt.grid(True)

    os.makedirs('paper5_figures', exist_ok=True)
    plt.savefig('paper5_figures/active_inference_posture.png')
    print("Saved figure to paper5_figures/active_inference_posture.png")

if __name__ == '__main__':
    run_simulation([20.0, 10.0, 2.0, 0.0])
