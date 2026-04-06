import numpy as np
import time
from numba import njit

def simulate_dde_old(Kp, Kd, tau, duration=10.0, dt=0.002, b=1.0, I=0.8,
                 mgL=73.575, theta0=0.05, noise_std=0.0):
    delay_steps = max(1, int(tau / dt))
    N = int(duration / dt)
    theta = np.zeros(N)
    omega = np.zeros(N)
    theta[0] = theta0

    AMP_CAP = 50.0

    for i in range(1, N):
        j = max(0, i - delay_steps)
        accel = (-b * omega[i-1] + mgL * theta[i-1]
                 - Kp * theta[j] - Kd * omega[j]) / I
        if noise_std > 0:
            accel += np.random.normal(0, noise_std)
        omega[i] = omega[i-1] + accel * dt
        theta[i] = theta[i-1] + omega[i] * dt
        if abs(theta[i]) > AMP_CAP:
            theta[i:] = AMP_CAP * np.sign(theta[i])
            omega[i:] = 0
            break

    return np.linspace(0, duration, N), np.degrees(theta)

@njit
def simulate_dde_jit_core(Kp, Kd, delay_steps, N, dt, b, I_inv, mgL, theta0, noise_std):
    theta = np.zeros(N)
    omega = np.zeros(N)
    theta[0] = theta0
    AMP_CAP = 50.0

    limit_1 = min(N, delay_steps)
    delayed_term = Kp * theta0

    if noise_std > 0:
        for i in range(1, limit_1):
            accel = (-b * omega[i-1] + mgL * theta[i-1] - delayed_term) * I_inv
            accel += np.random.normal(0, noise_std)
            omega[i] = omega[i-1] + accel * dt
            theta[i] = theta[i-1] + omega[i] * dt
            if theta[i] > AMP_CAP or theta[i] < -AMP_CAP:
                for k in range(i, N):
                    theta[k] = AMP_CAP if theta[i] > 0 else -AMP_CAP
                return theta

        for i in range(limit_1, N):
            j = i - delay_steps
            accel = (-b * omega[i-1] + mgL * theta[i-1] - Kp * theta[j] - Kd * omega[j]) * I_inv
            accel += np.random.normal(0, noise_std)
            omega[i] = omega[i-1] + accel * dt
            theta[i] = theta[i-1] + omega[i] * dt
            if theta[i] > AMP_CAP or theta[i] < -AMP_CAP:
                for k in range(i, N):
                    theta[k] = AMP_CAP if theta[i] > 0 else -AMP_CAP
                return theta
    else:
        for i in range(1, limit_1):
            accel = (-b * omega[i-1] + mgL * theta[i-1] - delayed_term) * I_inv
            omega[i] = omega[i-1] + accel * dt
            theta[i] = theta[i-1] + omega[i] * dt
            if theta[i] > AMP_CAP or theta[i] < -AMP_CAP:
                for k in range(i, N):
                    theta[k] = AMP_CAP if theta[i] > 0 else -AMP_CAP
                return theta

        for i in range(limit_1, N):
            j = i - delay_steps
            accel = (-b * omega[i-1] + mgL * theta[i-1] - Kp * theta[j] - Kd * omega[j]) * I_inv
            omega[i] = omega[i-1] + accel * dt
            theta[i] = theta[i-1] + omega[i] * dt
            if theta[i] > AMP_CAP or theta[i] < -AMP_CAP:
                for k in range(i, N):
                    theta[k] = AMP_CAP if theta[i] > 0 else -AMP_CAP
                return theta

    return theta

def simulate_dde_new(Kp, Kd, tau, duration=10.0, dt=0.002, b=1.0, I=0.8,
                 mgL=73.575, theta0=0.05, noise_std=0.0):
    delay_steps = max(1, int(tau / dt))
    N = int(duration / dt)
    I_inv = 1.0 / I
    theta = simulate_dde_jit_core(Kp, Kd, delay_steps, N, dt, b, I_inv, mgL, theta0, noise_std)
    return np.linspace(0, duration, N), np.degrees(theta)

# Test correctness
t1, th1 = simulate_dde_old(120, 10, 0.070)
t2, th2 = simulate_dde_new(120, 10, 0.070)
print("Max diff:", np.max(np.abs(th1 - th2)))

# Test performance
t0 = time.time()
for _ in range(250):
    simulate_dde_old(120, 10, 0.070)
print(f"Old time: {time.time() - t0:.3f}s")

t0 = time.time()
for _ in range(250):
    simulate_dde_new(120, 10, 0.070)
print(f"New time: {time.time() - t0:.3f}s")
