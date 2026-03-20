import numpy as np
import time

def calculate_fractions_sum(plddt_scores):
    mask_low = plddt_scores < 70
    mask_high = plddt_scores >= 90

    n_scores = len(plddt_scores)
    count_low = np.sum(mask_low)
    count_high = np.sum(mask_high)

    disorder_count = np.sum(plddt_scores[mask_low] < 50)
    return count_low, count_high, disorder_count

def calculate_fractions_count_nonzero(plddt_scores):
    mask_low = plddt_scores < 70
    mask_high = plddt_scores >= 90

    n_scores = len(plddt_scores)
    count_low = np.count_nonzero(mask_low)
    count_high = np.count_nonzero(mask_high)

    disorder_count = np.count_nonzero(plddt_scores[mask_low] < 50)
    return count_low, count_high, disorder_count

plddt = np.random.uniform(0, 100, 5000)

start = time.time()
for _ in range(10000):
    calculate_fractions_sum(plddt)
end_sum = time.time() - start

start = time.time()
for _ in range(10000):
    calculate_fractions_count_nonzero(plddt)
end_cnz = time.time() - start

print(f"np.sum: {end_sum:.4f}s")
print(f"np.count_nonzero: {end_cnz:.4f}s")
