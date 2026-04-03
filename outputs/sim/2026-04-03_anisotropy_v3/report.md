# Weekly Simulation Report: Stiffness Anisotropy Sweep v3

**Date:** 2026-04-03
**Parameter Swept:** Stiffness Anisotropy Ratio (1.0 to 10.0)
**Fixed Parameters:**
- Active Curvature: 15.0
- Torsion Drive: 0.1
- Duration: 2.0s

## What Changed
We systematically varied the lateral-to-sagittal stiffness anisotropy ratio from 1.0 (isotropic) to 10.0 (highly anisotropic). Previous sweeps had indicated that while anisotropy generally stabilizes planar S-curves, its interaction with growth and torsion is complex. This sweep specifically tested a high active curvature (growth) regime coupled with a small symmetry-breaking torsional drive.

## Emergent Shapes
The sweep revealed a non-monotonic, highly complex stability landscape:
1.  **Low Anisotropy (1.0 - 2.0):** The spine exhibits moderate 3D scoliosis with Cobb angles between 34° and 46° and lateral deviation (S_lat) around 0.3 - 0.5.
2.  **Rescue Window (2.5 - 3.0):** A narrow "rescue window" appears around an anisotropy of 3.0, where the Cobb angle plummets to just 2.75°. Here, the specific tuning of lateral stiffness perfectly counteracts the destabilizing moments, maintaining a nearly straight (or purely planar S-shaped) spine.
3.  **Resonant Instability (3.5+):** Strikingly, as anisotropy increases further, the spine suffers catastrophic buckling. At an anisotropy of 3.5, the Cobb angle spikes to >100° with massive lateral deviation. This catastrophic instability persists and fluctuates at higher anisotropies (up to 10.0), indicating severe, chaotic 3D buckling modes.

## How this informs scoliosis vs normal S-curve
The biological countercurvature hypothesis suggests that an S-shape (sagittal plane) is the healthy, active mechanism to support the spine against gravity, while scoliosis is an uncontrolled 3D escape mode. This sweep profoundly reinforces that view by demonstrating that simple mechanical stiffening (increasing anisotropy) is *not* a universal protection mechanism.

Instead, there exists a delicate "Goldilocks zone" (around Anisotropy=3.0 for this growth regime). If the spine is too isotropic, it slowly deforms laterally. If it is too anisotropic in the lateral plane, the accumulated sagittal growth energy has nowhere to go but to violently snap into a high-torsion 3D scoliotic configuration. This supports the idea that pathological scoliosis might arise not just from 'weakness', but from a mismatch between aggressive axial growth drives and an over-constrained (or improperly tuned) lateral stiffness profile.

## Next Sweep Suggestion
Given the dramatic resonant instability seen here when combining high growth, torsion, and high anisotropy, the next sweep should investigate the **Torsion Drive (`chi_tau`)** across a wider range (e.g., 0.0 to 0.5) while holding Anisotropy fixed at one of these high, unstable values (e.g., Anisotropy=6.0). We need to determine if there's a threshold of torsion required to trigger these catastrophic buckling modes.
