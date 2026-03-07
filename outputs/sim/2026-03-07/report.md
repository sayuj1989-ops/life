# Weekly Simulation: Asymmetric Dynamic Loading (2026-03-07)

## Overview
This experiment tests the hypothesis that asymmetric dynamic loading (e.g., unilateral sports, heavy one-sided backpacks) exacerbates curvature during the Energy Deficit Window (EDW).
We sweep over `torsion_drive` as a proxy for the intensity of the asymmetric twisting load.

## Method & Changes
- **Fixed Parameters**: `anisotropy = 1.2` (Low, representing the EDW vulnerability), `active_curvature = 6.0`.
- **Sweep Parameter**: `torsion_drive` from 0.0 to 5.0 (15 steps).

## Emergent Shapes & Results
- Maximum observed Cobb angle: **113.7°**.
- **Conclusion**: The simulated spine transitions from a normal S-curve into clinical scoliosis (>10°) as the asymmetric torsional load increases, demonstrating high vulnerability during the EDW.

## Next Sweep Suggestions
- Sweep both `torsion_drive` and `anisotropy` simultaneously to map the exact phase boundary where structural stiffening (e.g., night bracing) can successfully rescue the spine from this dynamic load.
