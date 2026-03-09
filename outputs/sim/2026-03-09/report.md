# Simulation Report: Active Curvature Sweep

**Date:** 2026-03-09
**Sweep Parameter:** `active_curvature` (5.0 to 25.0)
**Fixed Parameters:** `anisotropy` = 2.0, `torsion_drive` = 0.5, `duration` = 2.0s

## What Changed
A parameter sweep was conducted varying the scalar `active_curvature` signal (mapping to sagittal growth drive, e.g., via chi_kappa) from 5.0 to 25.0. Structural stabilization (`anisotropy` = 2.0) and a destabilizing rotational force (`torsion_drive` = 0.5) were held constant to model the competitive mechanics in the Biological Counter-Curvature framework.

## Emergent Shapes
The simulation reveals a profound transition in the rod's equilibrium geometry as the active curvature driving force increases:

1.  **Low Growth (Active Curvature 5.0 - 9.3):** The spine exhibits moderate instability. Cobb angles initially decrease from ~36° (at AC=6.4) down to ~28° (at AC=9.3). The lateral deviation ($S_{lat}$) remains relatively low, showing the system can partially absorb the sagittal growth into a stable planar S-curve despite the torsional drive.
2.  **Critical Transition (Active Curvature 10.7 - 12.1):** As growth passes ~10.7, there is a massive spike in lateral instability, with the Cobb angle surging to ~78°. Curiously, at AC=12.1, the system briefly finds a "rescue" state, dropping back to a Cobb angle of ~7.3°. This suggests complex re-entrant stability regions where the interactions between growth, anisotropy, and torsion hit specific resonant nodes.
3.  **High Growth Collapse (Active Curvature 13.5 - 25.0):** Beyond the brief rescue window, the system completely loses stability. As the active curvature increases towards 25.0, the Cobb angle steadily climbs back up, reaching ~55°. The maximum 3D curvature and torsion metrics become extreme (>130 $m^{-1}$), indicating a highly buckled, tightly coiled conformation. The thermodynamic cost ($U_{CC}$) becomes highly negative, showing the information coupling ($U_{info}$) is completely overwhelming the geometric resistance ($U_{elastic}$).

## Implications for Scoliosis vs Normal S-Curve
This parameter sweep firmly supports the core "Energy Deficit / Metabolic Buckling" hypothesis. Moderate growth drives the formation of the normal sagittal S-curve, stabilized by anisotropic stiffness (the "Information-Cosserat" vector chain). However, when the scalar growth drive ($\chi_\kappa$) exceeds the critical capacity of the anisotropic constraints to channel it sagittally, the system breaks symmetry. The presence of `torsion_drive` converts what would be a planar buckling event into a full 3D scoliotic deformity. The existence of a "rescue" window (at AC=12.1) suggests that there may be specific developmental growth rates that naturally tune out resonant instability.

## Next Sweep Suggestion
The complex, non-monotonic behavior observed around `active_curvature` ~ 10-12 under `torsion_drive=0.5` warrants closer inspection.
**Next step:** Run a high-resolution 2D phase space sweep mapping `active_curvature` (8.0 to 14.0) against `torsion_drive` (0.0 to 1.0) with fixed `anisotropy=2.0`. This will clearly delineate the "rescue" window and map the exact boundary where torsional coupling shatters the planar S-curve into a 3D scoliotic helix.