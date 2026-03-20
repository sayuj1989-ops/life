import numpy as np
import time

def benchmark_sum(n_iter=1000):
    cn = np.random.randint(0, 30, 5000)
    start = time.time()
    for _ in range(n_iter):
        n_exposed = np.sum(cn < 15)
    return time.time() - start

def benchmark_cnz(n_iter=1000):
    cn = np.random.randint(0, 30, 5000)
    start = time.time()
    for _ in range(n_iter):
        n_exposed = np.count_nonzero(cn < 15)
    return time.time() - start

print(f"np.sum(cn < 15): {benchmark_sum():.4f}s")
print(f"np.count_nonzero(cn < 15): {benchmark_cnz():.4f}s")

def benchmark_sum_hinge(n_iter=1000):
    hinges = np.random.choice([True, False], 5000)
    start = time.time()
    for _ in range(n_iter):
        n = np.sum(hinges)
    return time.time() - start

def benchmark_cnz_hinge(n_iter=1000):
    hinges = np.random.choice([True, False], 5000)
    start = time.time()
    for _ in range(n_iter):
        n = np.count_nonzero(hinges)
    return time.time() - start

print(f"np.sum(hinges): {benchmark_sum_hinge():.4f}s")
print(f"np.count_nonzero(hinges): {benchmark_cnz_hinge():.4f}s")
