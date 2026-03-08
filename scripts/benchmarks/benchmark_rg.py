import numpy as np
import timeit

def calc_rg_orig(coords):
    center_of_mass = np.mean(coords, axis=0)
    sq_dists = np.sum((coords - center_of_mass)**2, axis=1)
    return np.sqrt(np.mean(sq_dists))

def calc_rg_opt(coords):
    return np.sqrt(coords.var(axis=0).sum())

def run_benchmark():
    coords = np.random.rand(5000, 3)

    print("Benchmarking Radius of Gyration calculation (N=5000, 10000 iterations)...")

    # Correctness check
    orig_val = calc_rg_orig(coords)
    opt_val = calc_rg_opt(coords)
    assert np.isclose(orig_val, opt_val), f"Values differ! Orig: {orig_val}, Opt: {opt_val}"
    print(f"✅ Correctness verified: {orig_val:.6f}")

    time_orig = timeit.timeit(lambda: calc_rg_orig(coords), number=10000)
    time_opt = timeit.timeit(lambda: calc_rg_opt(coords), number=10000)

    speedup = time_orig / time_opt
    print(f"Original Time: {time_orig:.4f}s")
    print(f"Optimized Time: {time_opt:.4f}s")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    run_benchmark()