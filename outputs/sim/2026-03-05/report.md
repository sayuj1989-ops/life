# Simulation Report: Active Growth Bifurcation Sweep

**Date:** 2026-03-05

## What Changed
Swept `active_curvature` (proxy for sagittal active growth drive) from 0.0 to 10.0 over 20 increments. Maintained a constant moderate `anisotropy=1.5`, a slight `torsion_drive=0.05`, and a small `initial_lateral_defect=0.5`.

## What Emergent Shapes Occurred
As the active growth curvature increased beyond a certain threshold, the rod underwent a structural bifurcation. The mechanical metric decoupled from the stable sagittal kyphosis, leading to a sudden increase in lateral deviation (`S_lat`) and significant lateral bending (Cobb Angle) characteristic of an S-shaped/C-shaped curve.

## How This Informs Scoliosis vs Normal S-Curve
This validates that even in the presence of modest stiffness anisotropy (ECM alignment), an excessive or disproportionate active sagittal growth drive (`active_curvature`) can precipitate a mechanical instability, causing the normal sagittal profile to buckle laterally. This represents the 'Energy Deficit Bifurcation' where active control fails to contain the growing potential energy, yielding adolescent idiopathic scoliosis (AIS).

## Next Sweep Suggestion
Sweep the interaction between `anisotropy` (vector signal) and `active_curvature` (scalar signal) dynamically over time, perhaps introducing an abrupt drop in `anisotropy` midway through the growth phase to simulate sudden ECM degradation or delayed active control.
