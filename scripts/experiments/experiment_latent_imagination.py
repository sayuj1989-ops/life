import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "outputs/control_theory"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class LatentImaginationController:
    """
    Simulates a 'Dreamer-like' latent imagination controller for spinal posture.
    Instead of pure reactive PD control (subject to the Derivative Gain Trap),
    the system uses a learned internal forward model to predict the state t+tau
    and acts proactively.
    """
    def __init__(self, m=2.0, b=0.5, K_p=15.0, K_d=2.0, v_nerve=60.0, world_model_error=0.0):
        self.m = m
        self.b = b
        self.K_p = K_p
        self.K_d = K_d
        self.v_nerve = v_nerve
        self.g = 9.81
        self.world_model_error = world_model_error # Represents how poorly the internal model scales with L

    def run_simulation(self, L, T_max=10.0, dt=0.001):
        I = (1/3) * self.m * L**2
        tau = (2 * L) / self.v_nerve # Round trip delay
        delay_steps = int(tau / dt)

        num_steps = int(T_max / dt)
        t = np.linspace(0, T_max, num_steps)

        theta = np.zeros(num_steps)
        theta_dot = np.zeros(num_steps)
        theta[0] = 0.05 # Initial tilt

        for i in range(num_steps - 1):
            th = theta[i]
            w = theta_dot[i]

            idx_delayed = i - delay_steps
            if idx_delayed < 0:
                th_delayed = 0.0
                w_delayed = 0.0
            else:
                th_delayed = theta[idx_delayed]
                w_delayed = theta_dot[idx_delayed]

            # The 'World Model' predicts the current state based on delayed information
            # In a perfect world model, th_pred = th.
            # If the model hasn't adapted to rapid growth (L), it underestimates gravity/inertia.
            # We simulate this by blending the perfect prediction with the delayed state based on world_model_error.

            # Simple linear prediction (Taylor expansion) for the true state:
            th_linear_pred = th_delayed + w_delayed * tau
            w_linear_pred = w_delayed # Assuming constant velocity for simplicity

            # The error in the world model scales with how fast L is changing (which we model statically here as a parameter)
            th_pred = (1 - self.world_model_error) * th + self.world_model_error * th_linear_pred
            w_pred = (1 - self.world_model_error) * w + self.world_model_error * w_linear_pred

            # Control Torque uses the *imagined* (predicted) current state, not just the raw delayed state
            T_control = -self.K_p * th_pred - self.K_d * w_pred

            T_grav = self.m * self.g * L * th

            alpha = (T_grav - self.b * w + T_control) / I

            theta_dot[i+1] = w + alpha * dt
            theta[i+1] = th + w * dt

        return t, theta

def compare_controllers():
    lengths = np.linspace(0.2, 1.2, 50)

    # 1. Pure Reactive (World model error = 1.0, meaning it just uses delayed linear pred or fails)
    # Actually, the experiment_delayed_control.py showed instability.
    # We will vary the world_model_error.

    max_amps_perfect = []
    max_amps_degraded = []
    max_amps_reactive = []

    for L in lengths:
        # Perfect Latent Imagination (Dreamer adapted perfectly to L)
        ctrl_perf = LatentImaginationController(world_model_error=0.0)
        t, th = ctrl_perf.run_simulation(L)
        max_amps_perfect.append(np.max(np.abs(th[-2000:])))

        # Degraded Latent Imagination (Growth spurt outpaced learning, 40% error)
        ctrl_deg = LatentImaginationController(world_model_error=0.4)
        t, th = ctrl_deg.run_simulation(L)
        max_amps_degraded.append(np.max(np.abs(th[-2000:])))

        # Reactive (100% error, acts like classic delayed PD with poor linear projection)
        ctrl_react = LatentImaginationController(world_model_error=1.0)
        t, th = ctrl_react.run_simulation(L)
        max_amps_reactive.append(np.max(np.abs(th[-2000:])))

    plt.figure(figsize=(10, 6))
    plt.plot(lengths, max_amps_perfect, 'g-', label='Perfect Latent Imagination (Error=0)')
    plt.plot(lengths, max_amps_degraded, 'y-', label='Degraded World Model (Error=0.4)')
    plt.plot(lengths, max_amps_reactive, 'r-', label='Pure Reactive / Outdated Model (Error=1.0)')

    plt.axhline(y=0.05, color='k', linestyle='--', alpha=0.5, label='Initial Perturbation')
    plt.ylim(0, 0.5)
    plt.title('Hopf Bifurcation Rescue via Latent Imagination (Dream to Control)')
    plt.xlabel('Spine Length L (m)')
    plt.ylabel('Max Oscillation Amplitude (rad)')
    plt.grid(True)
    plt.legend()
    plt.savefig(f"{OUTPUT_DIR}/latent_imagination_rescue.png")
    print("Latent imagination comparison saved.")

if __name__ == "__main__":
    compare_controllers()
