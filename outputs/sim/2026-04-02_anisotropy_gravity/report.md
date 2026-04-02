# Anisotropy under Gravity Loading Parameter Sweep

**Date**: 2026-04-02
**Sweep Name**: weekly-sim-anisotropy-gravity
**Parameter Swept**: `anisotropy` (1.0 to 5.0)

## What Changed
Conducted a parameter sweep over stiffness anisotropy (ratio of lateral to sagittal stiffness) under constant high growth (`active_curvature = 14.0`) and standard earth gravity (`gravity = 9.81 m/s^2`). This investigates the hypothesis that a specific "window of stability" exists where structural anisotropy can effectively resist the lateral buckling forces induced by asymmetric growth under gravity.

## Emergent Shapes
The sweep reveals highly non-monotonic, complex behavior:
- **Low Anisotropy (R=1.0):** Immediate catastrophic lateral buckling (Cobb ~69 deg).
- **Lower-Mid Anisotropy (R~1.6 - 2.0):** Severe S-shapes still emerge (Cobb ~48-51 deg) interspersed with false stability peaks. S_lat deviation jumps massively up to 1.0m.
- **Optimal Stability Window (R~2.6 - 3.3):** A distinct "valley of stability" emerges. The Cobb angle drops dramatically to near zero (Cobb < 3 deg, min at ~0.35 deg at R=3.11). S_lat hits maximum values (~0.98m), indicating the spine is translating laterally as a whole or forming a massive gentle C-curve rather than buckling into tight scoliotic S-curves.
- **High Anisotropy (R>4.0):** Re-entrant instability. Excessive lateral stiffness paradoxically triggers severe secondary buckling (Cobb spiking >90 deg at R=4.79).

## How this informs scoliosis vs normal S-curve
This is a critical finding for the "Countercurvature Hypothesis". A "normal" spine does not simply maximize stiffness to prevent scoliosis. Instead, it must tune its structural anisotropy into a precise "Goldilocks zone" (here around R=3.0) to safely channel high adolescent growth forces into sagittal expansion without triggering lateral collapse.

Scoliosis can thus be seen as a failure to maintain this precise mechanical tuning during the adolescent growth spurt—either falling short (isotropic buckling) or over-compensating (high-stiffness re-entrant buckling).

## Next Sweep Suggestion
The presence of a sharp "valley of stability" warrants further investigation. The next sweep should add **torsional coupling** to this exact setup to see if torsion narrows, shifts, or completely destroys this stable window, as rotational forces are heavily implicated in true 3D scoliosis.
