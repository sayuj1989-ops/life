# Simulation Report: Stiffness Anisotropy Sweep
Date: 2026-04-02

## What changed
We swept the `stiffness_anisotropy` parameter from 1.0 to 5.0 (17 steps) while maintaining a constant high active growth (`active_curvature = 12.0`) and non-zero torsion (`torsion_drive = 0.5`).

## What emergent shapes occurred
The results showed highly non-monotonic behavior, characteristic of complex buckling instabilities and resonance phenomena:
- At very low anisotropy (1.0 - 1.25), moderate lateral deviation (Cobb ~40-44 deg) was observed.
- A profound "rescue window" appeared exactly at Anisotropy=1.50, where the rod remained completely stable (Cobb=0.76 deg, S_lat=0.12).
- Anisotropy=2.0 triggered extreme, catastrophic buckling (Cobb > 120 deg).
- Intermittent localized regions of relative stability (e.g. Cobb=4.65 at Anisotropy=2.75) were followed immediately by severe instability regions (Cobb=69.7 deg at Anisotropy=3.0).

## How this informs scoliosis vs normal S-curve
The extreme non-linearity and sudden jumps from near-perfect stability (Cobb < 1 deg) to catastrophic 3D structural failure (Cobb > 120 deg) across very small increments of stiffness anisotropy strongly support the biological countercurvature hypothesis. Rather than a linear "weak spine = scoliosis" model, this reveals that structural stability is a resonant parameter mapping. A spine with high active growth requires precisely tuned anisotropic stiffness. If biological aging or growth perturbations slightly shift the stiffness tensor, the spine rapidly "falls off a cliff" into extreme scoliosis due to unconstrained torsional buckling.

## Next sweep suggestion
Run a 2D parameter sweep combining `torsion_drive` and `active_curvature` near the identified critical rescue point (`stiffness_anisotropy = 1.50`) to map the full phase boundary of this stability window.
