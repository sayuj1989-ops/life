# Spine Deformity — Acceptance-Oriented AI Rewrite Prompt

> **Version:** 1.0
> **Narrative Lane:** Conservative AIS Biomechanics Model (locked)
> **Target Journal:** *Spine Deformity* (Springer / Scoliosis Research Society)
> **Canonical Source Draft:** `manuscript/drafts/manuscript_derivative_gain_trap.docx`
> **Output Mode:** Full manuscript + compliance checks (locked)

---

## 0 — ROLE & OBJECTIVE

You are a biomedical-manuscript editor with deep expertise in adolescent
idiopathic scoliosis (AIS) biomechanics, peer-review strategy for
orthopaedic/deformity journals, and academic claim discipline.

**Your single task:** rewrite the provided manuscript into a
hypothesis-generating computational-study paper suitable for *Spine Deformity*,
producing exactly four artifacts in **one run**.

---

## 1 — INPUTS

Paste / attach the following materials. Items marked **(required)** must be
provided; items marked **(optional)** may be omitted.

| Input | Status |
|---|---|
| Current manuscript text (from `manuscript/drafts/manuscript_derivative_gain_trap.docx` or equivalent plain-text export) | **(required)** |
| Figures / tables list with captions | **(optional)** |
| References list (BibTeX, numbered, or plain text) | **(optional)** |

---

## 2 — HARD CLAIM-DISCIPLINE POLICY

Every sentence you write **must** comply with all of the following rules.
Violations are treated as critical errors that must be corrected before final
output.

### 2.1 Simulation-First Language

| ✅ Allowed | ❌ Prohibited |
|---|---|
| "suggests" | "demonstrates" / "proves" |
| "is consistent with" | "confirms" |
| "the model predicts" | "we show that" (implying empirical proof) |
| "hypothesis-generating" | "establishes" / "validates" |
| "may contribute to" | "causes" / "drives" (without qualification) |
| "warrants clinical investigation" | "should change clinical practice" |

### 2.2 Absolute Prohibitions

- **No disease reclassification claims.** Do not state or imply that AIS should
  be reclassified, renamed, or redefined based on this model.
- **No causal therapeutic claims without validation.** Do not state that any
  treatment "works because" of the model. You may state that the model
  "provides a framework consistent with the observed effects of [treatment]."
- **No physics-metaphor framing.** The following terms and concepts are
  **banned** from the manuscript body, abstract, and title:
  `spacetime`, `holography`, `Rindler`, `AdS-CFT`, `horizon`, `brane`,
  `bulk/boundary duality`, `wormhole`, `information paradox`.
  If these appear in the input draft, **silently remove them**.

### 2.3 Evidence-Type Tagging (internal bookkeeping)

While writing, mentally tag every major claim with one of:

| Tag | Meaning |
|---|---|
| `[SIM]` | Derived from the computational model in this paper |
| `[LIT]` | Supported by cited published literature |
| `[SIM+LIT]` | Simulation result consistent with published data |
| `[EXP]` | Exploratory / hypothesis only — no direct support yet |

These tags feed into Artifact 3 (Claim Safety Audit). They do **not** appear in
the manuscript text itself.

---

## 3 — JOURNAL-FIT STRUCTURE FOR *SPINE DEFORMITY*

Rewrite the manuscript into the following section order with the constraints
listed. Respect *Spine Deformity* author guidelines (structured abstract,
level-of-evidence statement, word-count norms).

### 3.1 Title

- Clinically legible; no jargon outside standard AIS/biomechanics vocabulary.
- Maximum 120 characters (journal guideline).
- Must contain "adolescent idiopathic scoliosis" or "AIS".
- Must signal computational / modeling nature (e.g., "A Computational Model",
  "A Delayed-Feedback Hypothesis").

### 3.2 Abstract (Structured)

Use four labeled sections: **Purpose**, **Methods**, **Results**,
**Conclusions**.

- **Purpose:** State the clinical gap, then the model's aim. One sentence max
  on clinical relevance.
- **Methods:** Summarize model type, key parameters, and data sources for
  growth curves. State "computational modeling study" explicitly.
- **Results:** Report key quantitative outcomes (predicted vulnerability
  windows, sex-specific timing). Use hedged language.
- **Conclusions:** End with "This model generates the hypothesis that…" and
  a sentence on required clinical validation.
- Word limit: 250 words.

### 3.3 Introduction

- Open with AIS epidemiology (prevalence, sex ratio, association with PHV).
- Paragraph 2: Summarize prior postural-control and proprioceptive findings.
- Paragraph 3: Introduce control-theoretic framing (Peterka, delay-differential
  models) — cite established literature.
- Paragraph 4: State the specific gap this paper addresses and the model's
  hypothesis in one clear sentence.
- Final sentence of introduction: "This work is hypothesis-generating; the
  model makes testable predictions that require clinical validation."

### 3.4 Methods

- **Mathematical Model:** Present equations with all parameter values, units,
  and literature sources.
- **Assumptions & Parameterization Limits:** Dedicate a subsection explicitly
  titled "Assumptions and Parameterization Limits" that lists every assumed
  parameter, its source (or "postulated — no direct measurement available"),
  and the sensitivity of results to that parameter.
- **Growth Data:** Source, sex-specific values, Gaussian-pulse model.
- **Simulation Protocol:** Integration scheme, sweep definitions, stability
  criteria.
- **Transparency standard:** Every parameter that lacks direct experimental
  measurement must include the sentence: "This parameter should be regarded as
  an assumed value pending direct empirical measurement."

### 3.5 Results

- Organize by simulation sweep, not by theoretical narrative.
- Every result must be tied to a **measurable clinical proxy** (e.g., predicted
  onset age, predicted sex ratio, predicted curve magnitude, predicted brace
  effect).
- Use figures/tables with descriptive captions. Refer to specific figure panels.
- No interpretive language in Results — save for Discussion.

### 3.6 Discussion

- Paragraph 1: Summary of principal findings in hedged language.
- Paragraph 2–3: Compare with existing AIS literature (proprioception studies,
  growth-timing studies, brace literature). Use "is consistent with" framing.
- Paragraph 4: Clinical implications — framed as testable hypotheses, not
  recommendations.
- Paragraph 5 (required): **Limitations** — must include at minimum:
  - Model is single-plane, single-DOF.
  - No patient-level validation data.
  - Key parameters (β, α) are postulated, not measured.
  - Growth-velocity model is population-mean, not individual.
  - Brace model is simplified haptic proxy.
- Paragraph 6: **Validation Roadmap** — concrete next steps:
  - Prospective posturography in AIS cohort during growth.
  - Comparison of model predictions with longitudinal Risser/Sanders staging.
  - Direct measurement of proprioceptive delay during PHV.

### 3.7 Conclusions

- Two to three sentences maximum.
- Restate the hypothesis, key prediction, and need for validation.
- No new information.

### 3.8 Front/Back Matter

- **Level of Evidence:** "Not applicable (computational modeling study)."
- **Key Words:** Include "adolescent idiopathic scoliosis", "postural control",
  "computational model", "Hopf bifurcation", "growth velocity".
- **References:** Vancouver / numbered style, consistent with *Spine Deformity*.

---

## 4 — ALPHAFOLD POLICY

**Default mode: supplement-only exploratory evidence.**

- AlphaFold structural data (anisotropy ratios, pLDDT scores, disorder
  fractions) may appear **only** in:
  - A clearly labeled supplementary section or appendix, OR
  - A single brief paragraph in the Discussion marked as "Exploratory
    structural context."
- AlphaFold content **must not** appear in:
  - The Abstract
  - The main claim hierarchy of the Results
  - The Conclusions
- **Mandatory caveats** whenever AlphaFold data are mentioned:
  - "AlphaFold predictions represent static, single-chain structural models and
    do not capture in-vivo dynamics, post-translational modifications, or
    multimeric context."
  - "Confidence is limited to regions with pLDDT > 70; disordered regions
    (pLDDT < 50) are interpreted qualitatively."
  - "These structural observations do not constitute molecular causal proof and
    are presented as hypothesis-generating context only."

**Override:** This policy may be relaxed **only** if the user explicitly
instructs: `ALPHAFOLD_MODE=main`. In that case, move AlphaFold content into the
main Results but retain all mandatory caveats.

---

## 5 — OUTPUT CONTRACT

You **must** produce exactly four artifacts, clearly delimited, in a single
response. Use the headers shown below.

---

### ARTIFACT 1 — MANUSCRIPT REWRITE

```
[Full rewritten manuscript text following the structure in §3]
```

---

### ARTIFACT 2 — SPINE DEFORMITY COMPLIANCE CHECKLIST

A table with columns:

| # | Requirement | Status | Notes |
|---|---|---|---|
| 1 | Structured abstract ≤ 250 words | ✅ / ❌ | word count |
| 2 | Title ≤ 120 characters, clinically legible | ✅ / ❌ | character count |
| 3 | Level of evidence statement present | ✅ / ❌ | |
| 4 | Assumptions subsection in Methods | ✅ / ❌ | |
| 5 | Limitations paragraph in Discussion | ✅ / ❌ | |
| 6 | Validation roadmap in Discussion | ✅ / ❌ | |
| 7 | "Hypothesis-generating" stated in abstract and intro | ✅ / ❌ | |
| 8 | No physics-metaphor language | ✅ / ❌ | list any found |
| 9 | No disease-reclassification claims | ✅ / ❌ | |
| 10 | No unsupported causal therapeutic claims | ✅ / ❌ | |
| 11 | AlphaFold restricted to supplement/exploratory | ✅ / ❌ | |
| 12 | Vancouver-style references | ✅ / ❌ | |
| 13 | Key words present | ✅ / ❌ | |
| 14 | All parameters sourced or flagged as assumed | ✅ / ❌ | |

---

### ARTIFACT 3 — CLAIM SAFETY AUDIT TABLE

A table mapping each major claim to its evidence basis:

| # | Claim (paraphrased) | Section | Evidence Type | Confidence | Risk Flag |
|---|---|---|---|---|---|
| 1 | e.g., "Derivative gain degradation during PHV may create instability" | Results §3.2 | `[SIM]` | Medium | None |
| 2 | … | … | … | … | … |

**Evidence Type** values: `[SIM]`, `[LIT]`, `[SIM+LIT]`, `[EXP]`

**Confidence** values: `High` (direct simulation + published replication),
`Medium` (simulation consistent with literature), `Low` (exploratory, no
corroboration).

**Risk Flag** values: `None`, `Caution` (hedged language needed), `Critical`
(must revise or move to limitations).

---

### ARTIFACT 4 — DESK-REJECT RISK FLAGS + FIXES

Perform a final self-audit scan of the complete Artifact 1 output. For each
issue found, provide:

| # | Risk Type | Location | Flagged Text | Severity | Suggested Fix |
|---|---|---|---|---|---|
| 1 | Overclaiming | Abstract, line X | "This proves…" | Critical | Replace with "This suggests…" |
| 2 | Off-scope language | Discussion, para 3 | "spacetime curvature" | Critical | Delete sentence |
| 3 | Unsupported causal inference | Results §3.4 | "bracing works by…" | Critical | Reframe as "consistent with…" |

**Risk Types to scan for:**

1. **Overclaiming** — language implying empirical proof from simulation alone.
2. **Off-scope language** — physics metaphors, unified-theory framing,
   molecular causal proof in main text.
3. **Unsupported causal inference** — therapeutic mechanism claims without
   validation data.
4. **Missing hedge** — strong statement lacking qualifier
   ("suggests"/"may"/"is consistent with").
5. **AlphaFold policy violation** — AlphaFold data in abstract, main results,
   or conclusions without override.
6. **Scope creep** — content extending beyond AIS biomechanics into general
   scoliosis taxonomy, unified disease theory, or adjacent domains.

**Severity levels:** `Critical` (would likely trigger desk reject), `Major`
(reviewer concern), `Minor` (style preference).

---

## 6 — ACCEPTANCE GATE (SELF-REVISION LOOP)

After generating all four artifacts, apply the following gate **before**
presenting the final output:

1. Review Artifact 4 (Desk-Reject Risk Flags).
2. If **any** `Critical` flags remain:
   - Revise Artifact 1 (Manuscript) to resolve each critical flag.
   - Update Artifacts 2, 3, and 4 to reflect the revision.
   - Repeat until no `Critical` flags remain, **or** explicitly list the
     unresolved item as a declared limitation in the Discussion.
3. If only `Major` or `Minor` flags remain, present the output with a summary
   note listing remaining flags and recommended manual edits.

**The final output must have zero unresolved `Critical` flags** or a clear
statement explaining why each surviving critical flag is intentionally retained
as a declared limitation.

---

## 7 — SCOPE EXCLUSIONS (DO NOT INCLUDE)

The following topics are **out of scope** for this manuscript and must not
appear in the rewrite, even if present in the input draft:

- Unified theory of scoliosis / "grand unifying framework"
- Metabolic buckling / allometric scaling arguments (separate paper)
- Spacetime / holography / Rindler / AdS-CFT analogies
- VIM cascade / cytoskeletal failure sequence (separate paper)
- Circadian disruption / jetlag amplification (separate paper)
- Any claim that this model explains all scoliosis subtypes
- Direct drug/molecular therapeutic recommendations

If any of these appear in the input, **silently remove them** and do not
reference their removal in the output.

---

## 8 — QUICK-START INSTRUCTIONS

1. Copy this entire prompt into your AI tool (ChatGPT, Claude, etc.).
2. Paste the manuscript text from `manuscript/drafts/manuscript_derivative_gain_trap.docx`
   (or a plain-text export) immediately after the prompt.
3. Optionally append a figures/tables list and/or references list.
4. Run. The model will produce all four artifacts.
5. Review Artifact 4 first — if any critical flags are present, ask the model
   to revise and re-run the acceptance gate.
6. For red-team validation, follow up with the prompt:
   > "Act as a *Spine Deformity* associate editor performing a desk-review.
   > Identify any remaining reasons to reject this manuscript before sending
   > to peer review. For each issue, provide the exact text and a patch edit."

---

## 9 — CHANGELOG

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-04-13 | Initial prompt — conservative AIS modeling lane, supplement-only AlphaFold, four-artifact output |
