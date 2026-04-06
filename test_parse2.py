import time
import os
import numpy as np

def parse_pdb_plddt_newer(pdb_path):
    plddts = {}
    with open(pdb_path, 'r') as f:
        for line in f:
            if line[0:4] == 'ATOM':
                if line[13:15] == 'CA':
                    plddts[int(line[22:26])] = float(line[60:66])
    return plddts

def parse_pdb_plddt_dict(pdb_path):
    # This is equivalent, just slightly different syntax
    plddts = {}
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM') and line[13:15] == 'CA':
                plddts[int(line[22:26])] = float(line[60:66])
    return plddts


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


def simulate_dde_opt(Kp, Kd, tau, duration=8.0, dt=0.002, b=1.0, I=0.8,
                 mgL=73.575, theta0=0.05, noise_std=0.0):
    delay_steps = max(1, int(tau / dt))
    N = int(duration / dt)
    theta = np.zeros(N)
    omega = np.zeros(N)
    theta[0] = theta0

    AMP_CAP = 50.0
    inv_I = 1.0 / I

    # Avoid max(0, i - delay_steps) inside the loop
    # Phase 1: j = 0
    delayed_theta = Kp * theta0
    limit_1 = min(N, delay_steps)
    for i in range(1, limit_1):
        accel = (-b * omega[i-1] + mgL * theta[i-1] - delayed_theta) * inv_I
        if noise_std > 0:
            accel += np.random.normal(0, noise_std)
        omega[i] = omega[i-1] + accel * dt
        theta[i] = theta[i-1] + omega[i] * dt
        if theta[i] > AMP_CAP or theta[i] < -AMP_CAP:
            theta[i:] = AMP_CAP if theta[i] > 0 else -AMP_CAP
            omega[i:] = 0
            return np.linspace(0, duration, N), np.degrees(theta)

    # Phase 2: j = i - delay_steps
    for i in range(limit_1, N):
        j = i - delay_steps
        accel = (-b * omega[i-1] + mgL * theta[i-1] - Kp * theta[j] - Kd * omega[j]) * inv_I
        if noise_std > 0:
            accel += np.random.normal(0, noise_std)
        omega[i] = omega[i-1] + accel * dt
        theta[i] = theta[i-1] + omega[i] * dt
        if theta[i] > AMP_CAP or theta[i] < -AMP_CAP:
            theta[i:] = AMP_CAP if theta[i] > 0 else -AMP_CAP
            omega[i:] = 0
            break

    return np.linspace(0, duration, N), np.degrees(theta)


t0 = time.time()
for _ in range(300):
    simulate_dde_old(120, 10, 0.070, duration=10.0)
print(f"Old DDE: {time.time() - t0:.3f}s")

t0 = time.time()
for _ in range(300):
    simulate_dde_opt(120, 10, 0.070, duration=10.0)
print(f"Opt DDE: {time.time() - t0:.3f}s")
