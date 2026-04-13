# ARTIFACT 4 — DESK-REJECT RISK FLAGS + FIXES

## Self-Audit Scan of Artifact 1 (Final Manuscript — Post-Editorial Review)

| # | Risk Type | Location | Flagged Text | Severity | Status |
|---|---|---|---|---|---|
| 1 | Interpretive language in Results | Results §3.1 | "This suggests that individuals with greater intrinsic trunk stiffness possess a larger stability margin" | Critical | **Resolved** — Sentence moved to Discussion §5.1; Results now reports only simulation values |
| 2 | Interpretive language in Results | Results §3.3 | "broadly consistent with the reported 3:1 female-to-male ratio" | Critical | **Resolved** — Clinical comparison removed from Results; 2.8-fold result reported as "in the female model than in the male model"; clinical ratio comparison now in Discussion §5.2 |
| 3 | Interpretive language in Results | Results §3.4 | "This provides a mechanistic explanation for the clinical observation that curve progression in AIS typically ceases at skeletal maturity" | Critical | **Resolved** — Removed from Results; interpretation now in Discussion §5.2 |
| 4 | Interpretive language in Results | Results §3.5 | "This reinterpretation is consistent with the clinical observation that brace efficacy depends on compliance" | Critical | **Resolved** — Entire clinical-comparison paragraph removed from Results; brace literature comparison now in Discussion §5.2 |
| 5 | Interpretive language in Results | Results §3.6 | "This suggests that individuals with noisier proprioceptive signals—potentially due to genetic variants affecting mechanosensory channel function—may have a lower effective stability threshold" | Critical | **Resolved** — Speculative PIEZO2 interpretation removed from Results; now in Discussion §5.2 |
| 6 | Interpretive subsection heading | Results §3.5 | "Brace Mechanism Reinterpretation" | Major | **Resolved** — Renamed to "Simulated External Derivative Gain Augmentation" |
| 7 | Interpretive framing in Results | Results §3.5 | "Conventional understanding holds that braces work by applying corrective forces…Our model suggests an alternative" | Major | **Resolved** — Background/interpretive framing removed; Results now states simulation directly |
| 8 | Overclaiming in Discussion | Discussion §5.2 | "is a direct prediction of the model rather than an incidental association" | Major | **Resolved** — Softened to "is consistent with the model's prediction that the vulnerability window is temporally linked to peak growth velocity" |
| 9 | Interpretive figure caption | Figure 4 | "Brace mechanism reinterpretation: haptic K_d augmentation" | Minor | **Resolved** — Changed to "Simulated brace effect: haptic K_d augmentation" |
| 10 | Interpretive figure caption | Figure 5 | "suggesting that individuals with noisier proprioceptive channels (e.g., PIEZO2 variants) face elevated AIS risk" | Major | **Resolved** — Interpretive clause removed from figure legend |
| 11 | Missing hedge | Results §3.5 (original) | "the brace may function as a haptic augmentation of the derivative gain" | Minor | Acceptable — "may" provides adequate hedging |
| 12 | Overclaiming | Introduction (original) | "We demonstrate that this derivative gain gap creates…" | Resolved (prior round) | Changed to "The model suggests that this derivative gain gap creates…" |
| 13 | Overclaiming | Discussion (original) | "The model demonstrates that this gap creates a defined instability window" | Resolved (prior round) | Changed to "The model suggests that this gap may create a defined instability window" |
| 14 | Overclaiming | Results §3.6 (original) | "demonstrated that sensory noise substantially modulated the effective stability boundary" | Resolved (prior round) | Changed to "indicated that sensory noise substantially modulated…" |
| 15 | Missing hedge | Abstract Results (original) | "restored stability without altering intrinsic neuromuscular parameters" | Resolved (prior round) | Changed to "suggested that stability may be restored without altering intrinsic neuromuscular parameters" |
| 16 | Scope creep | Discussion (original) | "A Two-Layer Mechanistic Account" subsection | Resolved (prior round) | Removed — out of scope per §7 exclusions |

## Summary of Risk Types Scanned

1. **Overclaiming** — All instances of "demonstrates"/"we demonstrate" referring to this model's results have been replaced with hedged alternatives. ✅ No flags remain.

2. **Off-scope language** — No physics metaphors (spacetime, holography, Rindler, etc.) found. No unified-theory framing. No molecular causal proof in main text. ✅ No flags.

3. **Unsupported causal inference** — No therapeutic mechanism claims without validation. All clinical implications framed as testable hypotheses. ✅ No flags.

4. **Missing hedge** — One Minor flag remains (item #11: "may function as"). Adequate hedging present. ✅ No revision required.

5. **AlphaFold policy violation** — AlphaFold data absent from abstract, main results, and conclusions. ✅ No flags.

6. **Scope creep** — "Two-Layer Mechanistic Account" subsection removed in prior round. ✅ Resolved.

7. **Interpretive language in Results** — All clinical comparisons, mechanistic explanations, and speculative interpretations have been moved from Results to Discussion. Results now reports simulation outcomes only, with clinical proxies (onset age, sex ratio, curve magnitude) for contextualization. ✅ Resolved.

## Acceptance Gate Result

- **Critical flags:** 0 ✅
- **Major flags:** 0 ✅
- **Minor flags:** 1 (item #11 — adequately hedged with "may"; no revision required)

**The manuscript passes the acceptance gate with zero unresolved Critical or Major flags.**

### Recommended Manual Edits (Optional)

1. A final proofread for word-count compliance with *Spine Deformity* limits (~4,000 words excluding references/figures) is recommended before submission.
2. Consider whether Results §3.2 line "consistent with the magnitude of clinically significant scoliotic curves" (mapping 0.2 rad ≈ 11° to clinical proxy) is descriptive enough, or whether it should be a pure number report. Current framing is acceptable as a clinical proxy tie per §3.5 of the prompt.
