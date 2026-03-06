# Simulation Report: Initial Lateral Defect Sweep

**Date**: 2026-03-06
**Sweep Name**: weekly-sim-defect-sweep
**Parameter Swept**: `initial_lateral_defect` (0.00 to 0.15)
**Fixed Parameters**:
- Anisotropy Ratio = 3.0
- Active Curvature (Growth) = 10.0
- Natural Kyphosis = 2.0

## What Changed
We systematically varied the magnitude of the `initial_lateral_defect` (an initial structural perturbation) to test the robustness of the spine's S-curve. This explores the "basin of attraction" for the counter-curvature stability model under a realistic (moderate) level of active growth and tissue anisotropy.

## Emergent Shapes
The spine demonstrated a roughly linear, monotonic response to the initial lateral defect size. As the `initial_lateral_defect` scaled from 0.0 to 0.15:
- The emergent Cobb angle scaled proportionately from ~0 degrees (stable) to ~13.9 degrees.
- The lateral deviation (`S_lat`) similarly grew from 0.0m to ~0.38m.
- We did *not* observe a sharp "catastrophic collapse" bifurcation at this specific moderate anisotropy (3.0) and growth (10.0) level, indicating that the system's active control provides robust proportional resistance to structural imperfections within this parameter window.

## How this informs Scoliosis vs Normal S-curve
This result shows that under healthy biomechanical settings (sufficient anisotropy and controlled active growth), the spinal geometry can tolerate small, naturally occurring structural asymmetries (like slight vertebral wedging) without triggering a runaway buckling feedback loop. The linear relationship suggests an intact vector chain acting as a proportional dampener, rather than failing catastrophically. Scoliosis progression is therefore likely characterized not just by an initial defect, but by a systemic failure in the damping parameters (e.g., lower anisotropy or pathologically high active growth) that shrink this stable basin.

## Next Sweep Suggestion
**Parameter**: `active_curvature` AND `anisotropy` (2D Phase Space Sweep)
**Rationale**: Now that we see linear scaling in this specific healthy parameter regime, we need to map the full phase boundary. Sweeping active growth vs anisotropy simultaneously, while holding a fixed initial defect (e.g., 0.05), will allow us to define the precise "Energy Deficit Bifurcation" boundary where the dampening fails and Cobb angles jump non-linearly.