# Retrospective diagnostic results

Executed 2026-10-01 IST using the existing life NumPy environment, CPU only.
Protocol: `DIAGNOSTIC_PROTOCOL.md`. Full evidence and all input hashes:
`saved_campaign_diagnostics.json`.

## Reproduction

All eight completed runs and **944 initial/monthly NPZ states** were inspected.
All ten saved comparison entries were accounted for: **four failures and six
unevaluated comparisons**, the latter caused by three missing jobs. Evaluated
comparison values, tolerances, crossing flags and field/overall verdicts reproduce
to the replay's 1e-10 numeric tolerance. Mechanical flags reproduce from recorded
initial, shake and monthly metrics. The original verdict remains
**NUMERICALLY_UNRESOLVED**.

The independent local-turn calculation uses float64 adjacent-tangent cross products
and dot products, rather than unwrapping absolute segment angles. Its maximum
difference from stored total absolute bend is **4.5475e-13 degrees** over all saved
states; maximum signed local-angle difference is **1.5821e-15 radians**.
An initial diagnostic calculation retained the float32 snapshot dtype and differed
by up to 1.80e-4 degrees due to intermediate arithmetic precision. Converting
snapshots to float64 before recomputation removed that roundoff. Neither calculation
changed any campaign readout or explained its approximately 360-degree discrepancies.

## What this resolves

At the saved initial/monthly states, disagreement is **not explained by the global
unwrap calculation of planar total absolute bend**. Independent local geometry
reproduces those values. Taking the aggregate modulo 360 would remove recorded
geometric variation and would not be a measurement repair.

Several trajectories contain sharply opposed adjacent tangents: mesh48's minimum
adjacent tangent dot product is -0.8598, and its maximum total absolute bend is
901.3121 degrees. This is evidence of substantial recorded bending; it does not
establish self-contact, the physical validity of the trajectory, or a clinical
angle. Neither global angle interpretation nor a clinical analogy can rescue the
mechanical gate failures.

Timestep and iteration comparisons fail on total bend but not permanent bend.
Mesh refinement fails on both: 18/18 total-bend worlds and 6/18 permanent-bend
worlds. All sampled crossing-age comparisons pass. Baseline violates the 1% axial
strain limit; mesh48 violates both axial and shear limits, reaching **5.9461%** and
**5.3646%**. Quaternion norm and planarity pass at recorded observations.

## What remains unresolved

This audit does not reconstruct joint anchors from NPZ, replay the solver, inspect
unsaved shake states, identify between-observation transients, establish energy or
contact validity, or identify the cause of trajectory divergence. It does not
change the six missing comparison outcomes or establish solver convergence.

The next conditional work is the separately documented planar benchmark sequence:
material/constraint mapping, clamp and load history, transient constraint residuals,
and isolated timestep/iteration/mesh tests. That sequence has not been executed or
authorized by this report. New 3D biological modeling remains a later stage.

## GPU and artifact status

`GPU_STATUS.md` records failure to enumerate a GPU outside the execution sandbox,
a loaded NVIDIA 580.178.04 module, and unknown device identity/UUID. GPU health
remains unverified; no driver repair or GPU simulation was attempted.

The seal-file option requested by the user is used. `SHA256SUMS` covers this report
directory and `INPUT_SHA256SUMS` records its consumed local/external references.
Their checks must pass against the live files before this snapshot is reused.
The four original report artifacts, manuscript, frozen campaign and unrelated
working-tree changes are preserved. No git commit, push or task-board mutation is
performed.
