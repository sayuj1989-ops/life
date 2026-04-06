import time
import os
import numpy as np

def flexibility_index(plddts, domain_start=None, domain_end=None):
    residues = sorted(plddts.keys())
    if domain_start and domain_end:
        residues = [r for r in residues if domain_start <= r <= domain_end]
    if not residues:
        return 0.5
    scores = [plddts[r] for r in residues]
    return 1.0 - np.mean(scores) / 100.0

def flexibility_index_opt(plddts, domain_start=None, domain_end=None):
    if domain_start and domain_end:
        scores = [v for k, v in plddts.items() if domain_start <= k <= domain_end]
    else:
        scores = list(plddts.values())
    if not scores:
        return 0.5
    return 1.0 - np.mean(scores) / 100.0


def disorder_fraction(plddts, threshold=50.0, domain_start=None, domain_end=None):
    residues = sorted(plddts.keys())
    if domain_start and domain_end:
        residues = [r for r in residues if domain_start <= r <= domain_end]
    if not residues:
        return 0.0
    return sum(1 for r in residues if plddts[r] < threshold) / len(residues)

def disorder_fraction_opt(plddts, threshold=50.0, domain_start=None, domain_end=None):
    if domain_start and domain_end:
        scores = [v for k, v in plddts.items() if domain_start <= k <= domain_end]
    else:
        scores = list(plddts.values())
    if not scores:
        return 0.0
    return sum(1 for s in scores if s < threshold) / len(scores)

plddts = {i: np.random.uniform(20, 100) for i in range(1500)}

t0 = time.time()
for _ in range(5000):
    flexibility_index(plddts, 200, 1200)
    disorder_fraction(plddts, 50, 200, 1200)
print(f"Old Combined: {time.time() - t0:.3f}s")

t0 = time.time()
for _ in range(5000):
    flexibility_index_opt(plddts, 200, 1200)
    disorder_fraction_opt(plddts, 50, 200, 1200)
print(f"Opt Combined: {time.time() - t0:.3f}s")
