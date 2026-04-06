import numpy as np
import time

def analytical_hopf_boundary_old(Kp, Kd, b=1.0, I=0.8, mgL=73.575):
    omega = np.linspace(0.5, 60, 6000)

    # Vectorized computation of lhs and rhs
    lhs = Kp**2 + (Kd * omega)**2
    rhs = (b * omega)**2 + (I * omega**2 + mgL)**2
    max_val = np.maximum(lhs, rhs)
    max_val = np.maximum(max_val, 1e-12)

    # Check modulus condition vectorized, avoiding a slow 6000-iteration python loop
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
                # Verify residual
                r_real = -I*w**2 - mgL + Kp*np.cos(w*tau_c) + Kd*w*np.sin(w*tau_c)
                r_imag = b*w - Kp*np.sin(w*tau_c) + Kd*w*np.cos(w*tau_c)
                residual = r_real**2 + r_imag**2
                if residual < best_residual:
                    best_residual = residual
                    best_tau = tau_c
    return best_tau if best_tau else 0.0


def analytical_hopf_boundary_new(Kp, Kd, b=1.0, I=0.8, mgL=73.575):
    omega = np.linspace(0.5, 60, 6000)

    # Vectorized computation of lhs and rhs
    lhs = Kp**2 + (Kd * omega)**2
    rhs = (b * omega)**2 + (I * omega**2 + mgL)**2
    max_val = np.maximum(lhs, rhs)
    max_val = np.maximum(max_val, 1e-12)

    # Check modulus condition vectorized
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

# Test correctness
print("Old:", analytical_hopf_boundary_old(120, 10))
print("New:", analytical_hopf_boundary_new(120, 10))

# Test performance
t0 = time.time()
for _ in range(500):
    analytical_hopf_boundary_old(120, 10)
print(f"Old: {time.time() - t0:.3f}s")

t0 = time.time()
for _ in range(500):
    analytical_hopf_boundary_new(120, 10)
print(f"New: {time.time() - t0:.3f}s")
