import numpy as np
import time

def calculate_rg_curr(coords: np.ndarray) -> float:
    if len(coords) == 0:
        return 0.0

    center_of_mass = np.mean(coords, axis=0)
    sq_dists = np.sum((coords - center_of_mass)**2, axis=1)
    rg = np.sqrt(np.mean(sq_dists))
    return float(rg)

def fast_rg(coords: np.ndarray) -> float:
    if len(coords) == 0:
        return 0.0

    # Bolt Optimization: Vectorized variance
    # Var(X) = E[(X - E[X])^2]. Summing variance across x, y, z axes
    # gives the mean squared distance from the center of mass.
    # This avoids allocating the large intermediate (N, 3) array.
    rg_sq = np.sum(np.var(coords, axis=0))
    return float(np.sqrt(rg_sq))

N = 1000000
coords = np.random.rand(N, 3) * 100

for _ in range(5):
    start = time.time()
    r1 = calculate_rg_curr(coords)
    t1 = time.time() - start

    start = time.time()
    r2 = fast_rg(coords)
    t2 = time.time() - start

    print(f"Curr: {t1:.4f}s, Var: {t2:.4f}s, Match: {np.isclose(r1, r2)}")
