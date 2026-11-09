# Saved-campaign convergence diagnostic protocol

Documented 2026-10-01 after observing the existing failures. This is retrospective
implementation diagnosis, not a new preregistration of biological evidence.
The frozen campaign, its acceptance limits, source, ledger, assessment and saved
states remain unchanged. No new simulation or three-dimensional model is authorized
or launched by this protocol.

## Evidence inventory and precise count

The frozen report defines **10 comparisons**: four evaluated failures and six
unevaluated comparisons. The latter arise from **three missing jobs** (`iter600`,
`mesh96`, `combined`). A claim of three unevaluated comparisons confuses job count
with comparison count. The existing assessment remains NUMERICALLY_UNRESOLVED.

| Failed comparison | Bend worlds failing | Permanent-bend worlds failing | Crossing-age failures | Maximum bend error, degrees |
|---|---:|---:|---:|---:|
| baseline vs dt120 | 18/18 | 0/18 | 0/18 | 360.9904 |
| dt120 vs dt240 | 12/18 | 0/18 | 0/18 | 361.8073 |
| baseline vs iter300 | 14/18 | 0/18 | 0/18 | 359.8465 |
| baseline vs mesh48 | 18/18 | 6/18 | 0/18 | 359.9667 |

The mesh comparison's maximum permanent-bend error is 342.8021 degrees.
Mechanical flags additionally fail for baseline and mesh48.

| Completed corrected run | Recorded maximum axial strain | Recorded maximum shear strain | Frozen mechanical verdict |
|---|---:|---:|---|
| baseline | 1.077343% | 0.989533% | FAIL |
| dt120 | 0.290783% | 0.286094% | PASS |
| dt240 | 0.079254% | 0.076667% | PASS |
| iter300 | 0.459368% | 0.457875% | PASS |
| mesh48 | 5.946116% | 5.364621% | FAIL |

Recorded quaternion errors are approximately 1.19e-7 and recorded out-of-plane
tangents are zero. These values come from saved initial, shake and monthly states;
they are not maxima over every internal solver step. Initial/material/shake
diagnostics remain separate from these full-horizon results.

## A. CPU-only saved-evidence audit

1. Hash all consumed protocol, ledger, assessment, result and monthly NPZ files.
   Reject mismatched completed status, protocol identity, topology or nonfinite
   inputs. Keep all 18 worlds, including law-off controls and high-bend trajectories.
2. Independently replay both bend-field errors, the unchanged reference-peak
   tolerances, crossing ages and recorded mechanical gates. Report first breach,
   maximum and location for each mechanical metric. Match the existing assessment
   at absolute numeric tolerance 1e-10; a mismatch is a diagnostic failure.
3. Independently reconstruct local signed planar turns using
   `atan2((t_i cross t_j)_y, t_i dot t_j)` from saved body quaternions. Compare
   each joint and summed absolute turns with stored readouts. Record proximity to
   antiparallel adjacent tangents. This checks the planar angle extraction without
   depending on global `unwrap`; it does not recompute anchors or frame twist.
4. Preserve near-360-degree discrepancies. **Do not take aggregate total absolute
   bend modulo 360, subtract full turns, relabel it Cobb, discard worlds, increase
   the acceptance tolerance, or replace a frozen result.** Total absolute bend is
   a geometric total variation, not a periodic scalar. A branch hypothesis requires
   local state evidence; a looped or folded centerline may instead be a real
   divergence of simulated trajectories. Saved frames cannot establish what
   happened between monthly observations.
5. Read-only output is `saved_campaign_diagnostics.json` in this review directory.
   Its input manifest allows all consumed evidence to be rechecked. Numerical
   disagreement and mechanical failures retain their existing verdicts even if
   angle extraction proves internally consistent.

Run from `/home/sayuj/life`:

```sh
.venv/bin/python reports/helical_growth_research_2026-10-01/diagnose_saved_campaign.py
```

Re-execution changes this output's timestamp and therefore its seal. Verify the
current snapshot first; preserve it before generating another diagnostic snapshot.

## B. Future planar implementation benchmarks, conditional on authorization

This section specifies the next decision, not permission to execute it. GPU health
must be established first. Use a separate directory and protocol with its own
source/dependency seals, runtime budget and stopping rules. The existing 48-hour
campaign is not silently continued or amended.

- Verify actual stretch/shear/bend/twist gains and damping after replication and
  solver initialization at each mesh. Distinguish intended continuum EA/EI from
  the solver's effective constraint stiffness; static calibration must check the
  assumed mapping. Hold free length, root length, line density, EA, EI and loading
  fixed during mesh refinement and explicitly inspect inertia discretization.
- Use a straight clamped column with zero seed/load and growth off; then small
  static gravity loading and horizontal cantilever loading. For a uniform
  small-deflection cantilever with free length L and distributed force q,
  tip displacement is q L^4/(8 EI) and tip slope q L^3/(6 EI). For a straight
  axial column, uniform self-weight gives shortening mu g L^2/(2 EA).
  These are analytic implementation benchmarks within their assumptions, not
  patient predictions. Reduce benchmark loading if necessary to keep deflection
  small while holding the material arrays fixed.
- In this implementation `set_material` calculates EI from Bg times mass times
  g times length squared. Setting g to zero while recomputing gains also sets EI
  to zero. A no-gravity control must hold EA/EI fixed independently of g; otherwise
  it simultaneously removes loading and changes material mechanics. Verify that
  control in a separate diagnostic implementation, not by editing the frozen one.
- Sample before and after solver steps and the growth update, including shake
  endpoint, settling and clamped-root restoration. Record root position/rotation,
  velocities, constraint residuals, signed local angles and the state used for
  remodeling. Check whether forcing discontinuities, residual velocities or a
  poorly converged shake state contaminate the monthly reference-shape update.
- Freeze a small, bounded matrix that isolates timestep, iteration and mesh
  changes using matched law-off and law-on conditions. Record the same metrics
  at common physical times. No equation parameter is fitted to recover ordering.
  Define analytic accuracy and convergence criteria before running the matrix.
- If readout disagrees with independently reconstructed geometry, fix that
  demonstrated measurement defect under a new version and replay old snapshots
  separately. If mechanics fail, repair the identified solver/model mapping or
  discretization issue and establish benchmark convergence before any long horizon.
  If neither explains disagreement, retain the failure and refine the diagnostic;
  do not infer a biological instability from an unresolved solver.

## Decision boundary

Passing static benchmarks is necessary but insufficient for the growth experiment.
The planar growth trajectory still requires independent timestep, solver, mesh
and update-sampling checks. New checks do not retroactively certify the original
campaign. Three-dimensional biological modeling remains a later, separately
authorized stage. No treatment claim follows from any implementation benchmark.

## Artifact preservation

`SHA256SUMS` seals every ordinary file in this report directory except the checksum
file itself. The session reports the manifest's own SHA-256 as a separate reference.
Checksums detect drift relative to a trusted manifest; they are not authentication
against an actor who replaces both files and manifest. The directory can remain
untracked with this explicit snapshot, as allowed by the requested seal-file option.

Verify from `/home/sayuj/life`:

```sh
sha256sum --check reports/helical_growth_research_2026-10-01/SHA256SUMS
sha256sum --check reports/helical_growth_research_2026-10-01/INPUT_SHA256SUMS
```

`INPUT_SHA256SUMS` combines all external references in the gravity JSON and all
files consumed by the retrospective diagnosis. Verification checks those live
inputs as well as the local artifact snapshot. Original files remain unchanged.
