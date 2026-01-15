# Bolt's Journal

## 2026-01-15 - [SASA Optimization with Bounding Box Pruning]
**Learning:**
Calculating the "Exposed Surface Proxy" (SASA) involves pairwise distances between all residues ($O(N^2)$). For large proteins (e.g., PIEZO1, N=4554), this dominated the metric calculation time (~90%).
While the previous implementation used blocked matrix multiplication to handle memory, it still computed all pairwise distances.

**Action:**
Implemented "Bounding Box Pruning" within the blocked loop.
For each pair of blocks $(I, J)$, we calculate their bounding boxes ($min, max$).
If the boxes are further apart than the threshold (10 Angstroms), we skip the expensive pairwise distance calculation entirely.
This reduces the complexity for elongated or multi-domain proteins significantly.

**Results:**
- PIEZO1 (4554 res): ~2.5x speedup in SASA calc (290ms -> 110ms)
- VANGL2 (2972 res): ~2.5x speedup
- Exact numerical results preserved.
