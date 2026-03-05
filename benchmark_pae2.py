import time

import numpy as np


def current_reduce(pae_hc, indices, valid_lengths):
    row_sums = np.add.reduceat(pae_hc, indices, axis=0)
    block_sums = np.add.reduceat(row_sums, indices, axis=1)
    return block_sums

def new_reduce(pae_hc, indices, valid_lengths):
    # reduceat along axis 1 (cols) first because array is C-contiguous (default)
    # This improves memory access patterns
    col_sums = np.add.reduceat(pae_hc, indices, axis=1)
    block_sums = np.add.reduceat(col_sums, indices, axis=0)
    return block_sums

N = 2500
pae_hc = np.random.randint(0, 32, size=(N, N), dtype=np.uint8)
valid_lengths = np.random.randint(10, 50, size=50)
indices = np.cumsum([0] + list(valid_lengths))[:-1]

pae_hc = np.ascontiguousarray(pae_hc)

t0 = time.time()
for _ in range(5000):
    res1 = current_reduce(pae_hc, indices, valid_lengths)
t1 = time.time()
print(f"Current method (axis 0 then 1): {t1 - t0:.4f} seconds")

t0 = time.time()
for _ in range(5000):
    res2 = new_reduce(pae_hc, indices, valid_lengths)
t1 = time.time()
print(f"New method (axis 1 then 0): {t1 - t0:.4f} seconds")

print(f"Equal? {np.array_equal(res1, res2)}")
