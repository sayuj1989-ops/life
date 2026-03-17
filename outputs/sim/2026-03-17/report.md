# Weekly Simulation Report: Stiffness Anisotropy Sweep

**Date**: 2026-03-17
**Parameter Swept**: Stiffness Anisotropy (1.0 to 10.0)

## What changed
Fixed active_curvature=15.0 and torsion_drive=0.5 while sweeping anisotropy.

## Emergent Shapes
The Cobb angle was sensitive to varying levels of anisotropy under a fixed combination of growth and torsion drive. High and low extremes show differing stabilization.

## Relevance to Scoliosis
This relates directly to how the structural anisotropy of ECM components (like collagen) buffers biological growth drives.

## Next Sweep Suggestion
Sweep `torsion_drive` at critical thresholds of anisotropy (e.g. 3.0) to find the buckling point.
