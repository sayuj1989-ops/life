import time

import numpy as np

from research.alphafold_countercurvature.src.afcc.metrics import MetricsAnalyzer


def benchmark():
    N = 3000
    pae_matrix = np.random.randint(0, 32, size=(N, N), dtype=np.uint8)
    plddt = np.random.randint(50, 100, size=N)
    analyzer = MetricsAnalyzer()

    t0 = time.time()
    for _ in range(50):
        analyzer.calculate_pae_metrics(pae_matrix, plddt)
    t1 = time.time()
    print(f"Current method: {t1 - t0:.4f} seconds")

if __name__ == '__main__':
    benchmark()
