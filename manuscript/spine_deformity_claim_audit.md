# ARTIFACT 3 — CLAIM SAFETY AUDIT TABLE

| # | Claim (paraphrased) | Section | Evidence Type | Confidence | Risk Flag |
|---|---|---|---|---|---|
| 1 | The relationship between K_d and critical delay τ* is non-monotonic, with an optimal K_d maximizing the stability corridor | Results §3.1 | `[SIM]` | High | None |
| 2 | Growth-velocity-dependent K_d degradation drives the system trajectory across the Hopf bifurcation boundary when rapid growth co-occurs with elevated delay | Results §3.2 | `[SIM]` | Medium | None |
| 3 | The vulnerability window requires co-occurrence of rapid growth (>6 cm/yr) and elevated baseline delay (τ₀ > 180 ms); neither alone is sufficient | Results §3.2 | `[SIM]` | Medium | None |
| 4 | Model predicts female vulnerability at 10.6–11.8 years and male vulnerability at 12.2–14.2 years | Results §3.3 | `[SIM+LIT]` | Medium | None |
| 5 | Female preponderance (2.8-fold higher instability probability) is consistent with reported 3:1 female-to-male ratio | Results §3.3 | `[SIM+LIT]` | Medium | Caution — model ratio is approximate; depends on assumed differential β |
| 6 | Spontaneous stabilization at skeletal maturity arises from growth deceleration restoring K_d and τ to baseline | Results §3.4 | `[SIM+LIT]` | Medium | None |
| 7 | Brace may function as haptic augmentation of degraded K_d rather than (or in addition to) corrective force | Results §3.5 | `[SIM]` | Low | Caution — brace model is a simplified proxy; alternative interpretation of existing data |
| 8 | Stochastic noise modulates the effective stability boundary; individuals with noisier proprioceptive signals may have greater AIS susceptibility | Results §3.6 | `[SIM]` | Low | Caution — PIEZO2 link is speculative |
| 9 | Proprioceptive deficits documented in AIS patients are consistent with degraded K_d predicted by the model | Discussion §5.2 | `[SIM+LIT]` | Medium | None |
| 10 | PHV–AIS correlation is a direct prediction of the model | Discussion §5.2 | `[SIM+LIT]` | Medium | None |
| 11 | Brace efficacy dependence on compliance hours rather than corrective force is consistent with the haptic augmentation hypothesis | Discussion §5.2 | `[SIM+LIT]` | Medium | Caution — alternative explanations exist |
| 12 | Screening via proprioceptive velocity sensing tests may identify children entering the vulnerability window | Discussion §5.3 | `[EXP]` | Low | None — appropriately framed as hypothesis |
| 13 | Brace designs optimized for sensory feedback rather than corrective force may warrant investigation | Discussion §5.3 | `[EXP]` | Low | None — appropriately framed as hypothesis |
| 14 | Perturbation-based proprioceptive training during peripubertal period warrants investigation as preventive intervention | Discussion §5.3 | `[EXP]` | Low | None — appropriately framed as hypothesis |
| 15 | The derivative gain gap hypothesis may create a transient Hopf bifurcation instability explaining AIS onset | Conclusions | `[SIM]` | Medium | None — appropriately hedged with "generates the hypothesis" |

## Evidence Type Key

- `[SIM]` — Derived from the computational model in this paper
- `[LIT]` — Supported by cited published literature
- `[SIM+LIT]` — Simulation result consistent with published data
- `[EXP]` — Exploratory / hypothesis only — no direct support yet

## Confidence Key

- **High** — Direct simulation result; mathematically robust property of the governing equation class
- **Medium** — Simulation consistent with published literature, but no direct patient-level validation
- **Low** — Exploratory; depends on assumed parameters or speculative extensions

## Risk Flag Key

- **None** — Claim is appropriately hedged for a computational study
- **Caution** — Hedged language is present but the claim borders on overinterpretation; reviewer scrutiny likely
- **Critical** — Must revise or move to limitations (none found in final manuscript)
