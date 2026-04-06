# Weekly Simulation: Torsional Coupling Sweep

## Experiment Overview
Sweeping `torsion_drive` to observe how torsional coupling transforms a planar S-curve into 3D scoliosis.

## Changes
- Parameter family swept: `torsion_drive`
- 15 runs from 0.0 to 3.0

## Emergent Shapes
Higher torsion drives the spine from a primarily 2D sagittal deviation into severe 3D scoliotic bucking, peaking at a Cobb angle of 114.4 degrees.

## Relevance to Scoliosis
Normal S-curves exist primarily in the sagittal plane. This simulation shows that torsional defects (e.g. from asymmetric muscle tone or PCP pathway defects) are a critical symmetry-breaking mechanism required to generate the true 3D lateral-rotatory deformity seen in AIS.

## Next Sweep Suggestion
Investigate the interaction between `natural_kyphosis` and `torsion_drive` to see if a hyperkyphotic initial state resists torsional buckling better than a hypokyphotic one.
