# Fig 1 caption vs image (ledger R-9) — options note, author decision

Date: 2026-09-24. Scope: `manuscript/sections/figures.tex:5–10` (`fig:allometric_trap`)
vs `manuscript/figures/fig_gene_to_geometry.pdf`. No edits made; decision requested.

## Verified facts

1. **The mismatch is original, not a lost figure.** `fig_gene_to_geometry.pdf` was added in
   `286f10a2` (2025-12-20) and its extracted text is byte-for-byte the same three panels —
   (A) HOX expression domains, (B) information field I(s) + dI/ds, (C) g_eff(s) — at every
   later revision checked (`89d4908e`, `79c523db`, HEAD). The "Allometric Trap … passive beam
   … B_g … Energy Deficit Window" caption was already paired with this same image by
   `2f5e52dc` (2026-03-07). **Git history contains no earlier fig-1 file matching the caption.**
2. **The figure is never cited.** `\ref{fig:allometric_trap}` appears nowhere in
   `manuscript/sections/*.tex` or `main.tex` — it compiles as an orphan float.
3. **The caption's own content is stale, not just mismatched.** It says Energy Deficit Window
   "L^3 vs L^2". The closest existing artifact, `Fig1_energy_deficit_window.pdf`, draws demand
   as **L^4** vs supply L^2 (`pdftotext`: "Pcounter L^4 Ssupply L^2"), while the current
   generator `scripts/experiments/experiment_energy_deficit_window.py` computes
   `P_counter ∝ L^2` (line 133, labeled `L^2`). Three different exponents (L^2 script /
   L^3 caption / L^4 old figure) — the demand exponent is an open scientific question, so the
   deficit panel cannot simply be "regenerated as intended".
4. **The B_g panel candidate exists but carries R-1 constraints.** `fig_bg_phylogeny.pdf`
   (species CC/B_g) exists, but any reuse must (i) NOT draw 0.1 as a threshold (R-1 retraction)
   and (ii) use Human-Child B_g = 0.0201 (author ruling, ledger R-9).

## Option 1 — rewrite the caption to describe the actual image (recommended)

New caption describes: (A) schematic HOX paralog domains along the column; (B) information
field I(s) derived from HOX/somite patterning with gradient dI/ds; (C) effective metric factor
g_eff(s) and biological line element. All three panels are schematics from
`generate_figure1_gene_geometry.py` — the caption can and should say "schematic" to avoid
implying measurement.
- Cost: one caption edit + recompile + `pdftotext` verify.
- Risk: none new. Matches the abstract's strand "segment-wise stiffness is set by developmental
  HOX-domain patterning". No retired-claim exposure.
- Sub-decision for the author: since the float is uncited, you may equally **delete it** (or
  cite it in the intro where HOX patterning is discussed). Keeping an uncited figure is the
  only variant reviewers will notice.

## Option 2 — rebuild the captioned 3-panel figure (passive beam / B_g / deficit window)

No such composite ever existed; it must be assembled from scratch:
- Panel A (passive C-sag vs active S-curve): needs a new beam-plots script (fig_mode_spectrum
  is not it).
- Panel B (B_g across species): reuse `fig_bg_phylogeny.pdf` data, with the no-0.1-threshold
  and 0.0201 constraints above.
- Panel C (Energy Deficit Window): **blocked on the demand-exponent question (L^2 vs L^3 vs
  L^4)** — the old Fig1 pdf, the current script, and the caption disagree; picking one is a
  physics decision with knock-on text edits (biophysical_origins.tex says supply L^2/L^2.25;
  it is ORPHANED so cannot absorb an edit).
- Cost: new scripts, an open scientific decision, and re-audit of any new numbers. High.

## Recommendation

**Option 1**, with the author also deciding cite-vs-delete for the orphan float. Option 2
requires resolving the L^2/L^3/L^4 demand-exponent inconsistency before a single panel can be
drawn, and the caption's three claimed panels are not load-bearing for any current argument.
