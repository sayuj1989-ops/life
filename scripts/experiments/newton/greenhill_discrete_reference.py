"""Analytic reference for the Allometric-Trap threshold.

The manuscript asserts a passive-stability boundary at B_g = EI/(M g L^2) ~ 0.1.
Greenhill's self-buckling criterion for a clamped-free column under its own weight
fixes that constant exactly: (qL)_crit = 7.8373 EI/L^2  =>  B_g_crit = 1/7.8373.

This computes the discrete equivalent for an N-link chain of rigid segments joined
by torsional springs -- the exact model Newton's `add_rod` builds -- so a simulator
result can be scored against its own discretisation rather than the continuum limit.

Linearised about the vertical:
    U = k/2 [ th_0^2 + sum_j (th_j - th_{j-1})^2 ]      (clamped base)
    V = const - (m g l / 2) sum_j (N - j - 1/2) th_j^2
Instability when the Hessian K - G loses positive definiteness, giving
    B_g_crit = lambda_max(A^-1 D) / N^3.
"""
import numpy as np

def bg_crit(N: int) -> float:
    A = np.zeros((N, N))          # elastic Hessian / k
    A[0, 0] = 1.0
    for j in range(1, N):
        A[j, j] += 1.0
        A[j - 1, j - 1] += 1.0
        A[j, j - 1] -= 1.0
        A[j - 1, j] -= 1.0
    D = np.diag([N - j - 0.5 for j in range(N)])   # gravitational softening / (m g l)
    lam = np.linalg.eigvals(np.linalg.solve(A, D)).real.max()
    return lam / N**3

print("Greenhill continuum:  B_g_crit = 1/7.837347 =", 1 / 7.837347)
print()
print(f"{'N links':>8} {'B_g_crit':>12} {'vs continuum':>14}")
for N in (4, 8, 12, 16, 24, 32, 64, 128, 256, 512):
    b = bg_crit(N)
    print(f"{N:8d} {b:12.6f} {b/(1/7.837347):13.4f}x")
print()
print("N=24 (the chain used in probe_greenhill_bg.py):", f"{bg_crit(24):.6f}")
