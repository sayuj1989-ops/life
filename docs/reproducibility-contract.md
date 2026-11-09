# Numerical run contract

`solve_beam_static` consumes a one-dimensional arclength grid in metres and
equally shaped curvature (1/m), modulus (Pa) and active-moment (N m) fields.
The second moment is m^4, the tip force N and distributed force N/m. The model
is a cantilever with zero base angle; outputs are angle in radians and curvature
in 1/m. Invalid shapes, nonfinite values, nonpositive modulus and nonpositive
second moment fail before solving. The former stiffness clipping was removed:
it could silently substitute another material for the requested one.

The `iec demo` numerical stage writes a provenance sidecar containing all IEC
parameters, explicit solver defaults, boundary/coordinate descriptions, seed
(the stage is deterministic), package versions, repository commit, current
Python-source fingerprint and input hash. `tracked_run` keeps unique success
and failure receipts under `provenance_runs/<id>/`, plus an atomic latest copy.
It stores exception types, not exception text. A misspelled sweep parameter or
fewer than two sweep points is rejected before output creation.

The fingerprint includes uncommitted Python sources. It identifies a changed
checkout but is not a source-code backup; reproduce from the matching reviewed
checkout and dependency versions. Existing analysis scripts still using
`write_provenance` gain fingerprints and atomic writes; immutable run history
is enabled specifically where `tracked_run` is used. Other solver backends and
experiments have not been converted to a common adapter in this change.

Validation includes the analytical cantilever tip angle, invalid-input refusal,
failure receipt preservation, a small CPU-only demo and configuration refusal
tests. This verifies software and a numerical identity, not spinal biology,
clinical validity, or the withdrawn Newton results. Historical research outputs
and manuscripts are preserved.
