## 2024-03-24 - [Optimize Metric Calculation Loop]

**Learning:** BioPython `Structure` traversal is slow when repeated multiple times. Iterating over residues to extract coordinates for Rg, then again for Anisotropy, then again for pLDDT is inefficient.
**Action:** Implemented `extract_coords_and_plddt` in `StructureParser` to do a single pass extraction into NumPy arrays. Refactored `MetricsAnalyzer` to operate on these arrays, achieving ~1.8x speedup on metric calculation.

**Learning:** When refactoring methods that take complex objects (like `Structure`) to take simple arrays, backward compatibility can be tricky if the `analyze` method is the public entry point.
**Action:** Updated `analyze_structure` to handle both the extraction (if needed) and the calculation, but optimized the main pipeline script `04_analyze_metrics.py` to perform extraction once and pass arrays.
