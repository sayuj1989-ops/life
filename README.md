# Spine growth under gravity

Research code and manuscript for a proposed framework connecting spinal loading, geometric restoration, and growth-dependent remodeling in adolescent idiopathic scoliosis (AIS).

**Current status, 2026-09-08:** hypothesis and computational research; independent clinical validation remains outstanding. The original growth-delay correlation and human-specific gravitational threshold were withdrawn. A focused review found additional model and manuscript inconsistencies, including in the current compiled PDF. Earlier “publication-ready” status documents are historical.

## Start here

- [Current gap analysis and research priorities](reports/spine_growth_review_2026-09-08/REVIEW.md)
- [Reproducible equation checks](reports/spine_growth_review_2026-09-08/check_equations.py)
- [Existing audit ledger](AUDIT_LEDGER.md)
- [Authoritative manuscript entry point](manuscript/main.tex)
- [Core model code](src/spinalmodes/)
- [Legacy status archive and restore instructions](archive/status_cleanup_2026-09-08/README.md)

`manuscript/main.tex` includes `sections/theory_summary.tex` and `sections/methods_summary.tex`; the full `theory.tex` and `methods.tex` are not its active sections. Editing an unused draft does not fix the published PDF. The working copy at `~/jupyterlab/scoliosis` and publication-strategy directory can contain superseded claims; this repository is the manuscript source of truth.

## Evidence boundaries

- The recovery-ratchet scalar model illustrates a possible progression process. Its persistent asymmetric forcing and monotone accumulation are assumptions that require testing.
- Protein-structure comparisons are exploratory. Predicted shape does not measure metabolic cost or tissue mechanics.
- Synthetic clinical rate matching is calibration. Cross-sectional image geometry checks do not validate progression mechanisms.
- The Newton rod experiment has failed ordering checks and an invalid reported Cobb magnitude; it requires mechanical and measurement verification.
- The untracked `src/spine_growth_analysis.py` is not a trusted correction: the new audit records equation and integration defects.

## Repository layout

- `src/`: core model implementations.
- `scripts/`: simulations and analysis utilities.
- `manuscript/`: manuscript sources, tables and figures.
- `data/`, `research/`, `results/`, `outputs/`: inputs and research artifacts.
- `reports/`, `docs/`: reviews, methods and documentation.
- `archive/`: preserved historical material.

## Local checks

The existing project Makefile provides installation and test targets. The focused scientific audit can be reproduced from this directory with:

```bash
python3 reports/spine_growth_review_2026-09-08/check_equations.py
```

It writes only `equation_checks.json` beside the script, reads existing models, and does not run the large experiment suites. These checks verify selected equations, not biological validity.

For the manuscript, use its existing build tooling and inspect the resulting PDF text against the audit. Successful compilation is not scientific validation. The remaining legacy `final_verification.sh`, `DO_THIS_NOW.txt` and `SUBMISSION_READY_FINAL.md` refer to an earlier submission workflow.

## Citation and licensing

Use [CITATION.cff](CITATION.cff) with the exact version used, and check its metadata against that release. See [LICENSE](LICENSE) and [component licensing documentation](docs/LICENSING.md).
