import time
import sys

t0 = time.time()
import alphafold_pipeline_v2
t1 = time.time()
print(f"Total time: {t1 - t0:.2f}s")
