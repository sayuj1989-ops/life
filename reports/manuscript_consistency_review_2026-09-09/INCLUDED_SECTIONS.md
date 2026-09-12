# What `manuscript/main.tex` actually compiles (checked 2026-09-12, HEAD d9f532bb)

`grep -n '\\input' manuscript/main.tex` — twelve active sections, in order:

| main.tex line | section file | role |
|---|---|---|
| 102 | `sections/abstract.tex` | abstract |
| 119 | `sections/introduction.tex` | introduction |
| 121 | `sections/theory_summary.tex` | **theory (short form)** — not `theory.tex` |
| 123 | `sections/methods_summary.tex` | **methods (short form)** — not `methods.tex` |
| 125 | `sections/results.tex` | results |
| 127 | `sections/figures.tex` | figure environments |
| 129 | `sections/discussion.tex` | discussion |
| 131 | `sections/conclusion.tex` | conclusion |
| 133 | `sections/availability.tex` | data/code availability |
| 135 | `sections/statements.tex` | Springer declarations |
| 137 | `sections/tables.tex` | main-text tables (Table 1/3 spliced from `tables_generated/`) |
| 144 | `sections/supplementary.tex` | supplementary (same PDF) |

**Orphaned — present in `sections/`, compiled by nothing:** `theory.tex`, `methods.tex`,
`biophysical_origins.tex`, `availability_blinded.tex`, `statements_blinded.tex`, and the
`sections/submission_package/` subtree. Edits to these never reach the PDF
(`AUDIT_LEDGER.md`, standing gotcha 1). `biophysical_origins.tex` carries the two
additional errors listed in `reports/spine_growth_review_2026-09-08/REVIEW.md` §7 and
the desk-reject branding named in `WAY_FORWARD.md`; it is also where the nightly
`verify_bib` still finds undefined keys. It should not be edited as if it were current.

Compiled artifact checked: `manuscript/main.pdf`, mtime 2026-09-04 08:49, 5136 lines of
`pdftotext` output — **older than commits `3bbd55e2` (Table S2 q) and `0254a656`
(bibliography hygiene)**. PDF line numbers in `REVIEW.md` refer to
`pdftotext main.pdf -` of that file.
