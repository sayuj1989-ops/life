import numpy as np
import time

def pae_sum(pae_matrix):
    pae_mean = np.sum(pae_matrix, dtype=np.uint64) / pae_matrix.size
    return pae_mean

def pae_mean(pae_matrix):
    pae_mean = np.mean(pae_matrix)
    return pae_mean

pae = np.random.randint(0, 32, (1000, 1000), dtype=np.uint8)

start = time.time()
for _ in range(1000):
    pae_sum(pae)
end_sum = time.time() - start

start = time.time()
for _ in range(1000):
    pae_mean(pae)
end_mean = time.time() - start

print(f"np.sum: {end_sum:.4f}s")
print(f"np.mean: {end_mean:.4f}s")
