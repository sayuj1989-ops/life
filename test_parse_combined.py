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


def analytical_hopf_boundary_old(Kp, Kd, b=1.0, I=0.8, mgL=73.575):
    omega = np.linspace(0.5, 60, 6000)
    lhs = Kp**2 + (Kd * omega)**2
    rhs = (b * omega)**2 + (I * omega**2 + mgL)**2
    max_val = np.maximum(lhs, rhs)
    max_val = np.maximum(max_val, 1e-12)

    mask = np.abs(lhs - rhs) / max_val < 0.002
    valid_omegas = omega[mask]

    best_tau = None
    best_residual = np.inf

    for w in valid_omegas:
        A = I * w**2 + mgL
        B = b * w
        denom = Kp**2 + (Kd * w)**2
        cos_wt = (A * Kp - B * Kd * w) / denom
        sin_wt = (A * Kd * w + B * Kp) / denom
        if abs(cos_wt) <= 1.01 and abs(sin_wt) <= 1.01:
            cos_wt = np.clip(cos_wt, -1, 1)
            sin_wt = np.clip(sin_wt, -1, 1)
            wt = np.arctan2(sin_wt, cos_wt)
            if wt < 0:
                wt += 2 * np.pi
            tau_c = wt / w
            if 0.001 < tau_c < 0.5:
                r_real = -I*w**2 - mgL + Kp*np.cos(w*tau_c) + Kd*w*np.sin(w*tau_c)
                r_imag = b*w - Kp*np.sin(w*tau_c) + Kd*w*np.cos(w*tau_c)
                residual = r_real**2 + r_imag**2
                if residual < best_residual:
                    best_residual = residual
                    best_tau = tau_c
    return best_tau if best_tau else 0.0

def analytical_hopf_boundary_new(Kp, Kd, b=1.0, I=0.8, mgL=73.575):
    omega = np.linspace(0.5, 60, 6000)
    lhs = Kp**2 + (Kd * omega)**2
    rhs = (b * omega)**2 + (I * omega**2 + mgL)**2
    max_val = np.maximum(lhs, rhs)
    max_val = np.maximum(max_val, 1e-12)

    mask = np.abs(lhs - rhs) / max_val < 0.002
    valid_omegas = omega[mask]

    if len(valid_omegas) == 0:
        return 0.0

    w = valid_omegas
    A = I * w**2 + mgL
    B = b * w
    denom = Kp**2 + (Kd * w)**2

    cos_wt = (A * Kp - B * Kd * w) / denom
    sin_wt = (A * Kd * w + B * Kp) / denom

    valid_mask = (np.abs(cos_wt) <= 1.01) & (np.abs(sin_wt) <= 1.01)

    if not np.any(valid_mask):
        return 0.0

    w = w[valid_mask]
    cos_wt = np.clip(cos_wt[valid_mask], -1, 1)
    sin_wt = np.clip(sin_wt[valid_mask], -1, 1)

    wt = np.arctan2(sin_wt, cos_wt)
    wt[wt < 0] += 2 * np.pi

    tau_c = wt / w

    tau_mask = (tau_c > 0.001) & (tau_c < 0.5)
    if not np.any(tau_mask):
        return 0.0

    w = w[tau_mask]
    tau_c = tau_c[tau_mask]

    r_real = -I*w**2 - mgL + Kp*np.cos(w*tau_c) + Kd*w*np.sin(w*tau_c)
    r_imag = b*w - Kp*np.sin(w*tau_c) + Kd*w*np.cos(w*tau_c)
    residuals = r_real**2 + r_imag**2

    best_idx = np.argmin(residuals)
    return float(tau_c[best_idx])

# Run all with old vs all with new to see cumulative time savings
t0 = time.time()
for _ in range(50):
    for i in range(10):
        analytical_hopf_boundary_old(120, 10 + i)
        simulate_dde_old(120, 10 + i, 0.070, duration=1.0)
print(f"Old Combined: {time.time() - t0:.3f}s")

t0 = time.time()
for _ in range(50):
    for i in range(10):
        analytical_hopf_boundary_new(120, 10 + i)
        simulate_dde_opt2(120, 10 + i, 0.070, duration=1.0)
print(f"Opt Combined: {time.time() - t0:.3f}s")
