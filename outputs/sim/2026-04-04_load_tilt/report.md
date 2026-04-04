# Simulation Report: Load Vector Tilt Sweep

## Objective
To test whether an S-shaped spinal profile emerges and changes under load vector tilt, effectively emulating asymmetric gravitational loading combined with growth and anisotropic stiffness.

## What Changed
- Ran a parameter sweep of load vector tilt (0.0 to 30.0 degrees).
- Used `initial_lateral_defect` as a proxy for tilt by mapping `defect = sin(tilt) * 0.5`.
- Active curvature was held at a moderate value (12.0) with intermediate stiffness anisotropy (2.5) and minor torsional drive (0.2).

## What Emergent Shapes Occurred
- At low tilt (0-6 degrees), the spine exhibits a consistent moderate 3D curve (Cobb ~42 deg, Lateral Deviation ~0.3m).
- At intermediate tilt (~8 degrees), a sharp structural transition occurs where the Cobb angle jumps to ~53 deg and Lateral Deviation more than doubles (>0.7m), indicating significant buckling.
- Further increasing tilt causes chaotic structural responses: temporary stabilization (Cobb dropping to ~2.6 deg at 12 deg tilt) before another massive buckling event at 20 degrees tilt (Cobb peaking at ~73 deg, Lateral Deviation ~0.74m).
- Beyond 20 degrees, the curve stabilizes back to milder deformations, suggesting a resonance window where tilt matches the critical buckling modes of the rod.

## How This Informs Scoliosis vs Normal S-curve
The extreme sensitivity of the Cobb angle to specific tilt angles (especially the resonance peaks at 8° and 20°) indicates that slight alterations in loading vectors (such as those from postural imbalances or asymmetric growth) can trigger massive 3D decompensation. The normal S-curve can maintain stability under straight loads, but slight tilt interacts nonlinearly with torsional and active growth drives, pushing the spine out of the "valley of stability" into severe scoliosis.

## Next Sweep Suggestion
A 2D parameter sweep combining Load Vector Tilt with Stiffness Anisotropy to map the full phase space and determine if higher anisotropy can "rescue" the spine from tilt-induced resonance.
