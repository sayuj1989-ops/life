# Simulations Status

| Date       | Sweep Name             | Parameter | Outcome                                                                 | Report Link                                |
|------------|------------------------|-----------|-------------------------------------------------------------------------|--------------------------------------------|
| 2026-01-06 | weekly-sim-01          | chi_kappa | S-shapes emerged at high gain                                           | [Report](../outputs/sim/2026-01-06/report.md) |
| 2026-01-08 | weekly-sim-active-torque | chi_M     | Active moments counteract gravity, inducing complex curvature (e.g., at chi_M=2.0) | [Report](../outputs/sim/2026-01-08/report.md) |
| 2026-01-09 | weekly-sim-active-sweep | chi_M     | Strong S-shapes (multiple zero crossings) emerge at high active torque gains | [Report](../outputs/sim/2026-01-09/report.md) |
| 2026-01-13 | weekly-sim-posture     | theta     | S-shape complexity (zero crossings) depends on load vector tilt; vertical posture simplifies curve | [Report](../outputs/sim/2026-01-13/report.md) |
| 2026-01-14 | weekly-sim-anisotropy  | Anisotropy Ratio | Peak lateral deviation at ~0.75; high lateral stiffness suppresses deviation | [Report](../outputs/sim/2026-01-14/report.md) |
| 2026-01-15 | weekly-sim-growth      | chi_kappa | Growth induces lateral instability (max dev 0.17m) under weak anisotropy | [Report](../outputs/sim/2026-01-15/report.md) |
| 2026-02-18 | weekly-sim-stiffness   | chi_E     | Stiffness modulation reduces sag but suppresses S-shape at high gains; optimal window ~6-8 | [Report](../outputs/sim/2026-02-18/report.md) |
| 2026-02-19 | weekly-sim-torsion     | chi_tau   | Torsional coupling transforms planar S-curve into 3D scoliosis (Lateral Deviation > 0.2m) | [Report](../outputs/sim/2026-02-19/report.md) |
| 2026-01-16 | weekly-sim-growth-posture | theta    | Growth-induced S-shapes buckle laterally (Dev > 0.15m) across all postures, peaking at 70 deg. | [Report](../outputs/sim/2026-01-16/report.md) |
| 2026-01-17 | weekly-sim-growth-shape | chi_kappa | Optimal gravity compensation at chi=12; Anisotropy decoupled from planar S-shape. | [Report](../outputs/sim/2026-01-17_growth_shape/report.md) |
| 2026-01-18 | weekly-sim-torsion-anisotropy | chi_tau, anisotropy | High anisotropy (R=10) reduces torsion-induced scoliosis by ~15%, providing partial stabilization. | [Report](../outputs/sim/2026-01-18_torsion_anisotropy/report.md) |
| 2026-01-21 | weekly-sim-tilt        | tilt_deg  | Lateral tilt combined with anisotropy triggers significant lateral instability (S_lat > 0.3) | [Report](../outputs/sim/2026-01-21/report.md) |
| 2026-07-15 | weekly-sim-anisotropy-growth | Anisotropy Ratio | High anisotropy (R=6) destabilizes spine via torsion (Cobb > 70 deg), contradicting simple Vector Chain protection. | [Report](../outputs/sim/2026-07-15/report.md) |
| 2026-01-24 | weekly-sim-tilted-anisotropy | stiffness_anisotropy | Intermediate anisotropy (R=2.0) triggers maximal lateral S-shape (S_lat > 0.3); high anisotropy stabilizes. | [Report](../outputs/sim/2026-01-24/report.md) |
| 2026-01-25 | weekly-sim-torsion-drive | chi_tau | Critical coupling at chi_tau=1.0 maximizes Cobb Angle (80 deg) despite lower S_lat. | [Report](../outputs/sim/2026-01-25/report.md) |
| 2026-01-26 | weekly-sim-anisotropy-torsion | Anisotropy Ratio | Torsional coupling (chi=1.0) flips anisotropy role: R>=1.0 triggers high Cobb (~80 deg) vs low R. | [Report](../outputs/sim/2026-01-26/report.md) |
| 2026-01-27 | weekly-sim-tilt-torsion | tilt_deg, chi_tau | Torsion (chi_tau=1.0) reduces lateral deviation (S_lat) by 20% under high tilt (20 deg), despite similar Cobb angles. | [Report](../outputs/sim/2026-01-27/report.md) |
| 2026-07-22 | weekly-sim-growth-location | Info Center | Growth location determines curve shape (C vs S); Interacts with anisotropy. | [Report](../outputs/sim/2026-07-22/report.md) |
| 2026-01-31 | weekly-sim-growth-width | info_width | Localized growth (Width=0.1) triggers massive lateral S-shape (S_lat > 0.9), acting as a 'hinge' instability. | [Report](../outputs/sim/2026-01-31/report.md) |
| 2026-02-01 | weekly-sim-critical-anisotropy | stiffness_anisotropy | High growth (chi=10) with weak torsion (chi=0.2) remained stable (Dev < 8mm) across all anisotropy levels. | [Report](../outputs/sim/2026-02-01/report.md) |
| 2026-07-28 | weekly-sim-tilt-growth | tilt_deg, chi_kappa | High growth (chi=15) amplifies Cobb angle (75 deg) under tilt (30 deg) but reduces lateral deviation, suggesting tighter curling. | [Report](../outputs/sim/2026-07-28/report.md) |
| 2026-08-01 | weekly-sim-gravity-anisotropy | Gravity, Anisotropy | High gravity (2g) combined with high anisotropy (R=10) and sagittal growth (chi=10) maintained perfect stability (Cobb=0) in a vertical setup. | [Report](../outputs/sim/2026-08-01/report.md) |
| 2026-08-08 | weekly-sim-anisotropy-s-curve | Anisotropy Ratio | Optimal stability at R~3.6 (Cobb ~10 deg); High Anisotropy (R=10) destabilizes (Cobb ~68 deg) while Low R causes collapse. | [Report](../outputs/sim/2026-08-08/report.md) |
| 2026-02-11 | weekly-sim-torsion-high-anisotropy | chi_tau (0.0-2.0) | High anisotropy (R=10) remains unstable (Cobb ~68 deg) with minimal effect from torsion (chi_tau up to 2.0). | [Report](../outputs/sim/2026-02-11/report.md) |
| 2026-02-12 | weekly-sim-tilted-growth-anisotropy | tilt_deg, Anisotropy | Intermediate anisotropy (R=1.0) maximizes lateral deviation (S_lat > 0.5) under tilt; Low R maximizes Cobb. | [Report](../outputs/sim/2026-02-12/report.md) |
| 2026-08-19 | weekly-sim-growth-location-high-res | Info Center (0.1-0.9) | Cobb peaks at lower spine (0.3); Lateral Deviation peaks at apex (0.9). Apical defects maximize lateral shift. | [Report](../outputs/sim/2026-08-19/report.md) |
