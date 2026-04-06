import time
import os
import numpy as np

def simulate_dde_old(Kp, Kd, tau, duration=8.0, dt=0.002, b=1.0, I=0.8,
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

def simulate_dde_opt2(Kp, Kd, tau, duration=8.0, dt=0.002, b=1.0, I=0.8,
                 mgL=73.575, theta0=0.05, noise_std=0.0):
    delay_steps = max(1, int(tau / dt))
    N = int(duration / dt)
    theta = np.zeros(N)
    omega = np.zeros(N)
    theta[0] = theta0

    AMP_CAP = 50.0  # Radians cap to prevent overflow
    inv_I = 1.0 / I

    # Optimize the loop by avoiding repeated max() calls and using simple array indexing.
    # Phase 1: t < tau
    limit_1 = min(N, delay_steps)
    delayed_theta = Kp * theta0
    for i in range(1, limit_1):
        accel = (-b * omega[i-1] + mgL * theta[i-1] - delayed_theta) * inv_I
        omega[i] = omega[i-1] + accel * dt
        theta[i] = theta[i-1] + omega[i] * dt
        if theta[i] > AMP_CAP or theta[i] < -AMP_CAP:
            theta[i:] = AMP_CAP if theta[i] > 0 else -AMP_CAP
            omega[i:] = 0
            return np.linspace(0, duration, N), np.degrees(theta)

    # Phase 2: t >= tau
    for i in range(limit_1, N):
        j = i - delay_steps
        accel = (-b * omega[i-1] + mgL * theta[i-1] - Kp * theta[j] - Kd * omega[j]) * inv_I
        omega[i] = omega[i-1] + accel * dt
        theta[i] = theta[i-1] + omega[i] * dt
        if theta[i] > AMP_CAP or theta[i] < -AMP_CAP:
            theta[i:] = AMP_CAP if theta[i] > 0 else -AMP_CAP
            omega[i:] = 0
            break

    return np.linspace(0, duration, N), np.degrees(theta)


t0 = time.time()
for _ in range(50):
    for i in range(10):
        simulate_dde_old(120, 10 + i, 0.070, duration=10.0)
print(f"Old Combined: {time.time() - t0:.3f}s")

t0 = time.time()
for _ in range(50):
    for i in range(10):
        simulate_dde_opt2(120, 10 + i, 0.070, duration=10.0)
print(f"Opt Combined: {time.time() - t0:.3f}s")
