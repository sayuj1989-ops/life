# AlphaFold DB fetcher review — 2026-09-12

Card t_b2ca945a. Independent review of the 2026-09-09 AFCC fetcher hardening
(`research/alphafold_countercurvature/src/afcc/afdb.py`, `scripts/02_fetch_afdb.py`) and its
downstream parser compatibility. Baseline before any change: the 33-test command passed.
Interpreter: `.venv` (Python 3.12.3, numpy 2.4.4, pandas 2.3.3, biopython 1.87, requests 2.33.1).
The publication dataset (`data/`, `outputs/`, `manuscript/`, `results/`) was read, never written.

Live check (one call, 20 s timeout, 1.1 s): `GET /api/prediction/P02452` → 200, one entry,
`modelEntityId` = `entryId` = `AF-P02452-F1`, `sequenceStart/End` = `uniprotStart/End` = 1–1464,
`latestVersion` 6, `pdbUrl`/`cifUrl`/`paeDocUrl` all present (`…-model_v6.pdb`, `…_v6.json`).
Both legacy and current field names are still served.

## Findings

Severity: high = wrong data could enter the publication tables; medium = crash or silent skip; low = cosmetic.
Reproducers marked `test:` are in `tests/test_afdb_reliability.py` and failed before the fix
(pre-fix run: 7 failed / 18 passed; post-fix: 25 passed). `repro:` items are sections of
`reproducers.py` (output in `reproducers_output.txt`).

| # | Finding | Area | Reproducer | Sev | Disposition | Changed |
|---|---|---|---|---|---|---|
| 1 | PAE whose dimension ≠ structure residue count was recorded `downloaded`; `calculate_pae_metrics` then averaged the wrong matrix with no error (3×3 PAE on a 5-residue model → `PAE_mean` 0.89) | PAE dims vs coverage | test: `test_pae_not_matching_structure_size_is_a_failed_download` | high | DEFECT, fixed: dimension compared with the CA count on download (`download_failed`, note `pae_dimension_mismatch: pae=N residues=M`) and on cache reuse; `residues` recorded in notes | afdb.py |
| 2 | CIF-only entry (no `pdbUrl`) was downloaded to `pdb_path`; every downstream reader is PDB-only (`fast_parse_pdb_arrays` → None, `PDBParser` → 0 atoms) and `analyze_structure` emitted a row `n_residues 0, plddt_mean 0, morphology "Unstructured/Disordered"` | CIF fallback | test: `test_cif_only_entry_is_not_recorded_as_a_pdb_download`; repro E | high | DEFECT, fixed fail-closed: manifest status `no_pdb_model`, nothing downloaded. Converting CIF→PDB is the alternative if a CIF-only entry ever appears (none observed; AFDB serves PDB for every entry checked) | afdb.py |
| 3 | All 260 legacy `downloaded` rows have empty `notes`, so the 09-09 "PAE requires its own checksum" rule made every publication row cache-invalid; the next `02_fetch_afdb.py` run would re-download and overwrite the whole dataset, contradicting the README's "cache reuse preserves a downloaded release" | Cache/manifest | test: `test_legacy_row_without_pae_checksum_is_reused_not_refetched` | high | DEFECT, fixed: a row without a recorded `sha256_pae` is reused when the PDB SHA-256 matches and the PAE parses square/finite/nonnegative with the structure's dimension; rows with a checksum stay strict | afdb.py |
| 4 | Manifest written in place (`to_csv` on the target); a crash mid-write leaves a truncated publication manifest, unlike the structure files which are temp+rename | Cache/manifest | test: `test_manifest_write_failure_preserves_previous_manifest` | low | DEFECT, fixed: write `manifest.csv.tmp` then `os.replace` | afdb.py |
| 5 | `entry.get("modelEntityId", entry.get("entryId"))` does not fall back when the new field is present as JSON `null` (same for `sequenceStart/uniprotStart`, `uniprotAccession`) → `MetadataError … found 0` | Canonical selection | test: `test_null_identifier_fields_fall_back_to_legacy_fields` | low | DEFECT, fixed via `_first_present()` (loud failure before, so no data risk) | afdb.py |
| 6 | An isoform (`P02452-2`) or whitespace accession in `uniprot_mapping.csv` raises `ValueError` inside the batch and aborts the remaining proteins (also under `--dry-run full`) | Malformed input | test: `test_cli_skips_non_canonical_accessions_instead_of_aborting` | medium | DEFECT, fixed in the CLI: non-`[A-Z0-9]+` accessions are listed and skipped; the module still raises. No isoform is present in the 276-row manifest; the mapping CSV is absent on this checkout | 02_fetch_afdb.py |
| 7 | Downstream PAE cache stores `uint8` (`structure.py:224`) and `calculate_pae_metrics` sums with `dtype=np.uint64` (`metrics.py:229`): fractional values are floored (`[[0,1.5],[2.9,0.75]]` → `[[0,1],[2,0]]`; mean 1.2875 → 0.75); values >255 or negative make `parse_pae` return None (PAE metrics silently 0.0). The fetcher accepts fractional and >255 files the parser cannot represent | PAE precision | repro F | high if it ever occurs; not occurring | LIMITATION, not fixed (files outside this card's write scope). Verified harmless today: the served v6 PAE is integer-valued (SOX9 509×509: 0 of 259,081 entries fractional, max 32, `max_predicted_aligned_error` 31.75; P02452's PAE file was not fetched). Fix belongs in `structure.py` (`np.rint` + range assert, or float16) and `metrics.py` (float-safe mean) | — |
| 8 | `03_parse_structures.py`/`04_analyze_metrics.py` use `Path(row['pdb_path'])` without joining `repo_root`; manifest paths are repo-relative (259 rows) so the scripts work only with cwd = repo root, else `04` `continue`s silently. One row (`Q9UKP6`/UTS2R) stores a docker-era absolute `/app/...` path and is unusable on any host | Parser compatibility | repro G | medium | LIMITATION, not fixed (scripts outside write scope; the `/app` row is a data edit). One-line fix: `repo_root / row['pdb_path']` in both scripts | — |
| 9 | Malformed/non-https structure URLs (`ftp://`, `file://`, non-string) → `download_failed`; HTML error pages and empty bodies rejected by content validation; 404 vs 5xx vs bad JSON distinguished | Malformed URLs | repro B; existing tests | — | OK (verified by reproducer + existing tests). No host allowlist: an `https://` URL on any host returned by the API would be fetched — trust is transitive from the TLS'd API response | — |
| 10 | Manifest with missing columns loads (filled `None`); a still-valid PDB whose stored SHA-256 differs is cache-invalid; corrupt file is cache-invalid (existing test) | Cache/manifest | repro C2; existing test | — | OK (verified) | — |
| 11 | Canonical F1 selected independent of order; ambiguous/duplicate F1 → `MetadataError`; entries for another accession excluded | Canonical selection | existing tests | — | OK (verified by existing tests, re-run) | — |
| 12 | Cosmetic: downloaded files are mode 0600 (`NamedTemporaryFile`); `retrieved_at` changed from `YYYY-MM-DD HH:MM:SS` to ISO-8601 with offset; `scripts/data_management/bolt_biofold_analysis.py:618` tests for a status `already_cached` the fetcher never returns (treats cache hits as failures) | Cache/manifest | by inspection | low | LIMITATION, documented | — |
| 13 | urllib3 `Retry` on 429/5xx is configured but not exercised by any test (tests mock `session.get`) | Malformed metadata | — | low | LIMITATION: verified by reading, not by test | — |

## Remaining fragment/isoform coverage limitations

- Only `AF-<acc>-F1` is fetched. AFDB splits proteins longer than ~2700 aa into overlapping
  1400-residue fragments, so for such proteins `n_residues` in `protein_metrics.csv` is the F1
  window, not the protein. Rows written from now on carry `sequence_start`, `sequence_end` and
  `residues` in `notes`; the 260 publication rows carry none of these, and `data/raw/` is absent
  on this checkout, so their coverage and model version cannot be audited from the manifest.
  A provenance backfill (re-parse, no downloads) is the prerequisite for any cache-aware re-run.
- Isoform accessions are rejected by the module and skipped by the CLI. AFDB models canonical
  sequences only, so this is coverage the source cannot provide.
- A cached row is never version-checked against `latestVersion`; a corrupt cache is refreshed to
  the current release, which the new `version` note makes visible but does not prevent.
- `AFCC_BASE_DIR` outside the repo makes `repo_root` derivation wrong and stores absolute paths
  (the mechanism behind the `/app/...` row).

## Is another review needed?

Yes, but not of `afdb.py`. Three items sit outside this card's write scope and each is a
one-to-three-line change with its reproducer already written here: (a) the parser-side PAE
contract (#7: integrality/range check or float storage in `structure.py`, float-safe mean in
`metrics.py`); (b) repo-root path joining in `03`/`04` plus the single `/app` manifest row (#8);
(c) a no-download provenance backfill of the 260 legacy rows before `02_fetch_afdb.py` is ever
run against the publication manifest (#3 keeps them cacheable, but their version stays unknown).
`afdb.py` itself needs a further look only if a CIF-only or non-AlphaFold provider entry appears
(#2: decide convert-vs-refuse).

## Commands

```
cd /home/sayuj/life
PYTHONPATH=src:. .venv/bin/python -m pytest tests/test_afdb_reliability.py tests/test_recovery_two_state.py tests/test_alphafold_integration.py research/alphafold_countercurvature/tests/test_afcc_pipeline.py -q   # 39 passed
PYTHONPATH=src:. .venv/bin/python -m pytest tests/test_afcc_pipeline.py research/alphafold_countercurvature/tests/ -q   # 13 passed
PYTHONPATH=src:. .venv/bin/python reports/alphafold_api_review_2026-09-09/reproducers.py
```

Changed: `research/alphafold_countercurvature/src/afcc/afdb.py`,
`research/alphafold_countercurvature/scripts/02_fetch_afdb.py`, `tests/test_afdb_reliability.py`
(6 new tests, 1 extended). Created: this directory (`REVIEW.md`, `reproducers.py`,
`reproducers_output.txt`). Not committed.
