# Manuscript consistency review — active sources vs the 2026-09-08 gap review

Card t_0bc99913 (spine-research). Performed 2026-09-12 on `~/life` HEAD `d9f532bb`
(branch `fix/audit-2026-08-06`). **Read-only**: no manuscript file was edited. Proposed
corrections are staged at
`~/jupyterlab/scoliosis_publication_strategy/patches/consistency_2026-09-12.md` and are
applied to `~/life/manuscript/` only on the author's instruction.

Method, per `AUDIT_LEDGER.md` rule 1: every claim below was located in the **source**
(`sections/*.tex` line) *and* in the **compiled text** (`pdftotext main.pdf -` line), not
inferred from a `latexmk` exit code. Active sections are listed in `INCLUDED_SECTIONS.md`.
Inputs: `reports/spine_growth_review_2026-09-08/REVIEW.md` (§4, §7),
`reports/alphafold_spine_2026-09-09/README.md`, `AUDIT_LEDGER.md` (R-1…R-5, O-1…O-3).

## Findings

Disposition key: **OPEN** = present in active source and PDF, contradicts another active
section or a ledger entry; **RESOLVED** = fixed in source and verified in PDF text;
**NOT-USED** = the concern refers to material no active section relies on.

| # | Issue | Source (file:line) | PDF line | Supporting artifact | Disposition | Proposed correction |
|---|---|---|---|---|---|---|
| 1 | Universal `B_g ≈ 0.1` threshold and "Humans occupy a unique position … deep within the Allometric Trap" | `theory_summary.tex:12` | 420–422 | Abstract Results paragraph (same PDF, line ~80) reports the **negative** result: human adult `B_g = 0.0101` indistinguishable from rabbit (0.0100), above cat/dog/horse/elephant; `AUDIT_LEDGER.md` R-1; `results.tex:5` (exponent −0.282, no threshold) | **OPEN** — the theory section asserts what the abstract and results retract | Replace the threshold/uniqueness sentences with the monotone-scaling statement and the posture/axial-load-path argument the abstract already uses (patch §1) |
| 2 | Conclusion: "a universal scaling constraint … AIS is a predictable consequence of crossing this boundary during growth" | `conclusion.tex:3` | 2534–2535 | Same as #1; 09-08 review §4 ("Gravity does not specify an S-curve", "universal threshold is unsupported by the project's own corrected table") | **OPEN** | Rewrite the first two sentences: no boundary is crossed; the model illustrates a rate competition (restoration vs growth remodeling) as a *possible* progression mechanism (patch §2) |
| 3 | Abstract Conclusions: "`B_g` serves as a robust biomechanical proxy for clinical progression and brace-treatment efficacy" | `abstract.tex` (Conclusions paragraph) | 100 | The abstract's own Results paragraph: `r = −0.483` is "a structural consistency check rather than independent validation", BrAIST rates "were themselves the grid-search targets"; 09-08 review §7 | **OPEN** — self-contradiction inside the abstract | "a candidate proxy whose association with the progression index is a structural consistency check, not an independent validation" (patch §3) |
| 3b | "predictable failure of an active … control system" (abstract, introduction ×2, discussion) | `abstract.tex` Conclusions; `introduction.tex`; `discussion.tex` | 99, 126, 175, 1904 | 09-08 review §7 (conclusion "claims a predictable boundary-crossing cause") | **OPEN (wording)** | "hypothesised failure" / "modelled as a failure" (patch §3b) |
| 4a | "reducing effective lateral stiffness by up to 80 %" | `theory_summary.tex:43`, `results.tex:53`, `results.tex:62`, `discussion.tex:15` | 601, 1406 | 09-08 review §7: no independently measured regional grounding; `results.tex:62` gives the *computed* reduction as **31.1 %** in the same paragraph as "∼80 %" | **OPEN** — internal inconsistency (80 vs 31.1 in one paragraph) | State "80 %" only as the model's ceiling (`E⊥/E∥` at `α → 0`) and "31.1 %" as the computed value at the profile peak; drop "up to 80 %" from theory/discussion (patch §4) |
| 4b | "the thoracolumbar junction (T8–T10)" | `theory_summary.tex:43`, `results.tex:60`, `results.tex:62` | 601, 1386, 1407 | Anatomy: the thoracolumbar junction is T12–L1; T8–T10 is mid/lower thoracic — the apex region of typical right-thoracic AIS. `introduction.tex` (PDF 204) correctly says "thoracic spine (T8–T10)" | **OPEN** — anatomical error, three places | Replace "thoracolumbar junction" with "mid-to-lower thoracic region (T8–T10), the usual apex of right-thoracic AIS"; keep the normalized position 0.596 as the model output (patch §4b) |
| 5 | Species count: "10 vertebrates (mouse to elephant)" vs "12 vertebrate species spanning mouse to dolphin" | `abstract.tex:4`, `results.tex:5` (n = 10) vs `methods_summary.tex:28`, `conclusion.tex:3` (12) | 72, 976 vs 741, 2536 | `outputs/thermodynamic_cost/cross_species_scaling.csv` has **12 rows** (11 species + human at two stages); `results.tex:5` pre-specifies giraffe and dolphin as exclusions, leaving **10 rows = 9 species + human child/adult**; `tables.tex:12–21` prints those 10 rows | **OPEN** — neither number is a species count, and the two disagree | Everywhere: "a 12-row panel (11 species; human at two developmental stages); after two pre-specified exclusions (giraffe, dolphin) all statistics use the remaining 10 rows (9 species)" (patch §5) |
| 6 | "we validated the model's clinical translation … against two gold-standard datasets" for the synthetic N = 1000 cohort | `methods_summary.tex:45`, `results.tex:88` | 832, 1481–1482 | Abstract: BrAIST success rates "were themselves the grid-search targets used to calibrate the three free parameters"; ledger H-1; 09-08 review §6 ("the synthetic BrAIST success-rate match remains calibration") | **OPEN (wording)** | "we calibrated the model against / compared its outputs with two reference datasets" (patch §6) |
| 7 | Is the Newton rod result used as support? | — | 2904 is the only "Newton" hit, a bibliography author | `grep -n Newton sections/*.tex` → no active section cites `results/newton_ratchet_rod/`; README (09-08) flags it as unverified | **NOT-USED** | None in the manuscript. Separately, the experiment has **two** defects, not one: (i) `joint_dtheta` takes `atan2(px, py)` of body *positions* (the 09-08 finding); (ii) the permanent set is written to `joint_rod_rest_kb_local[:, 0]` (bending about local x = the y–z plane) while the rod is loaded and shaken in the x–z plane (bending about local y, component 1). Both are being fixed and re-run today; see `AUDIT_LEDGER.md` entry to follow |
| 8 | Compiled PDF is stale | `manuscript/main.pdf` mtime 2026-09-04 08:49 | — | Commits `3bbd55e2` (Table S2 `q` 0.026→0.033) and `0254a656` (bibliography hygiene) post-date it | **OPEN (mechanical)** | `cd manuscript && make all`, then re-run this review's `pdftotext` checks before any upload |
| 9 | Withdrawn growth-delay / Hopf mechanism | `theory_summary.tex:39`; `supplementary.tex` rejected-Hopf section | 572, 790, 4071–4316 | Ledger R-4, R-5 (commits `2c394c24`, `add9718d`); theory now reads "approaches but does not cross the exact Hopf boundary" | **RESOLVED** | none |
| 10 | Ledger O-1 (protein table provenance), O-2 (cover letter), O-3 (availability statement) | `tables.tex` (generated), `cover_letter.txt`, `availability.tex` | — | Ledger marks all three RESOLVED 2026-09-04; tags named in `availability.tex` (`v1.0.0-submission`, `v1.4.7-editorial`, `v1.5-scaling-falsification`) exist in `git tag` | **RESOLVED** | none — but the submission tag will need adding once #1–#6 land |
| 11 | Orphaned drafts carry stale theory (`theory.tex`, `methods.tex`, `biophysical_origins.tex`) | `sections/` | — | `INCLUDED_SECTIONS.md`; 09-08 review §7 last bullet; nightly `verify_bib` undefined-key warnings all sit in `biophysical_origins.tex` | **NOT-USED** | Move to `manuscript/_archive/` or add a first-line `% ORPHANED — not input by main.tex` comment so the ledger's gotcha 1 stops recurring (patch §11, optional) |

**Counts:** 8 OPEN (1, 2, 3, 3b, 4a, 4b, 5, 6, 8 → 6 substantive + 2 wording + 1 mechanical),
2 RESOLVED (9, 10), 2 NOT-USED (7, 11).

## Resolved vs still open, in one paragraph

Everything the 2026-08-07 audit and the 09-04 provenance branch fixed is verified present
in the compiled text (Hopf rejection, generated protein tables, cover letter, availability
statement, abstract negative result). What is *not* fixed is that the short-form theory
section and the conclusion were never rewritten after the abstract was: the paper now
argues against its own threshold claim in the abstract and results while asserting it in
`theory_summary.tex:12` and `conclusion.tex:3`. Those two sentences, the anatomical
mislabel (T8–T10 is not the thoracolumbar junction), the 80 %/31.1 % pair, the 10-vs-12
count, and the "validated" wording are the whole remaining list. None requires new
analysis; all are text.

## Remaining submission blockers (t_810e86a2), in order

1. Apply patch §§1–6 to `~/life/manuscript/sections/` (author decision; staged file above).
2. `cd ~/life/manuscript && make all`; `pdftotext main.pdf - | grep -n` for the nine
   strings in this table — #1–#6 must return nothing, #9 must still be present.
3. `python3 ~/jupyterlab/scoliosis_publication_strategy/scripts/verify_claims.py` and
   `verify_bib.py` silent (both exit 0 on 2026-09-12 03:00 already).
4. Tag from HEAD (`v1.7-consistency` or similar), add it to `availability.tex`, update
   `scoliosis_publication_strategy/SUBMISSION_CHECKLIST.md` — it still names
   `submission_manuscript_v1.5.pdf` and tag `v1.5-scaling-falsification`.
5. Human: Editorial Manager upload (nothing on the box can do it); optional cover-letter
   line citing PMID 42711523 (Spine Deformity's own decade topic analysis) for fit.

## Not in scope, unchanged by this review

BrAIST IPD (t_3df16fb4) remains the only route to clinical validation; the manuscript's
limitations already say so. The 09-09 AlphaFold hardening and the two-state comparator did
not touch the manuscript and are not cited by it.
