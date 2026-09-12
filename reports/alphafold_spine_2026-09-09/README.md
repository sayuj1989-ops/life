# AlphaFold API and spine research continuation — 2026-09-09

This continues the September 8 gap review in the authoritative `/home/sayuj/life` repository. “ATLAS” was provisionally interpreted as the existing DeepMind/EMBL-EBI AlphaFold Database integration; no distinct local ATLAS project was found.

## API changes

The AFCC fetcher now selects the canonical F1 model by identifier, accepting current `modelEntityId` and legacy `entryId`, rather than taking the first response entry. Missing canonical models or ambiguous matches are explicit failures. This policy does not claim to cover every fragment/isoform of large proteins.

HTTP 404/empty results are distinct from transport, service, JSON and schema failures. Requests use bounded retries for transient HTTP statuses. Structure and square nonnegative finite PAE contents are checked before atomic file replacement; HTTP error pages cannot be recorded as successful downloads. Cached structures are checked against their stored SHA-256 and parsed again; available PAE files require their own checksum. Cache paths resolve independently of the launch directory. Dry runs report metadata checks without claiming downloads or writing a manifest. The CLI counts this status separately, and the module requirements explicitly include requests.

Manifest notes record model identifier, release version, sequence start/end, source URLs and PAE checksum, retaining the existing CSV columns. Files come from URLs returned by the API; PAE URLs are no longer guessed. Cache reuse preserves a downloaded release rather than automatically updating publication data.

Live checks returned COL1A1 P02452 v6 metadata, and downloaded SOX9 P48436 v6 structure plus PAE (sequence interval 1–509), followed by a successful cache-only repeat. These are public database checks, not new structure predictions. The observed endpoint still supplied both identifier fields despite the documented legacy-field sunset.

Primary API references: [EMBL-EBI field migration](https://www.ebi.ac.uk/pdbe/news/breaking-changes-afdb-predictions-api), [release/version guidance](https://www.ebi.ac.uk/pdbe/news/alphafold-database-release-notes). Checked September 9, 2026. A separate older `jupyterlab/scoliosis/src/alphafold` client requires legacy `entryId`; this continuation changes the active AFCC pipeline and does not synchronize that older checkout.

## Signed two-state research comparator

The added `spinalmodes.recovery_two_state` implements the immediate comparator proposed in yesterday's review:

```
de/dt = u(t) - (kr(t) + kg(t)) e
dp/dt = kg(t) e - kh(t) p
```

Time is in years, signed curvature deviations e and p in 1/m, rates in 1/year and forcing u in 1/m/year. Rates must be nonnegative and all inputs finite. Callable rates and forcing permit independently supplied growth/load histories. Discontinuous protocols should be integrated as separate intervals at each jump. No fixed positive seed or monotonicity constraint is imposed. The original scalar model and manuscript are preserved for comparison.

With an initial impulse A, constant kr and kg, zero forcing and kh=0, the exact remodeled deviation is `A*kg/(kr+kg)*(1-exp(-(kr+kg)*t))`. The control run's maximum error was 1.85e-13. A second test compares constant forcing and reverse remodeling against a matrix exponential. Zero-load and no-growth controls remain zero; reversing the signed load reverses the response. Positive kh allows correction after growth ceases. A variable-growth oscillatory-load run also agrees with a smaller maximum integration step.

These checks verify equations and software. They do not establish a growth-triggered bifurcation, curve handedness, anatomical localization, a clinical recovery measurement, or patient-level predictive value. Rate values are assumed examples. The model still needs a measured load-to-curvature-rate relation and comparison with stress-modulated growth using independent longitudinal data. AlphaFold confidence/shape descriptors cannot determine kr, kg, kh or tissue stiffness without an independently validated link.

## Reproduction

From the active repository, using its existing virtual environment:

```bash
PYTHONPATH=src:. .venv/bin/python -m pytest tests/test_afdb_reliability.py tests/test_recovery_two_state.py -q
PYTHONPATH=src:. .venv/bin/python reports/alphafold_spine_2026-09-09/check_improvements.py
# Optional public download into this report's isolated live/ directory:
PYTHONPATH=src:. .venv/bin/python reports/alphafold_spine_2026-09-09/check_improvements.py --live
```

Numerical results and observed API provenance are in `checks.json`. The validation download uses its own manifest and does not alter publication inputs. An offline rerun regenerates numerical checks without the live fields; use `--live` to include API verification again.

Next research priority: prespecify the measurable meaning of slow recovery, then compare this model with conventional stress-modulated growth and the original scalar model. Existing September 8 manuscript and Newton geometry concerns remain unresolved by this focused continuation.
