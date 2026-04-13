# ARTIFACT 3 — CLAIM SAFETY AUDIT TABLE

| # | Claim (paraphrased) | Section | Evidence Type | Confidence | Risk Flag |
|---|---|---|---|---|---|
| 1 | The relationship between K_d and critical delay τ* is non-monotonic, with an optimal K_d maximizing the stability corridor | Results §3.1 | `[SIM]` | High | None |
| 2 | Growth-velocity-dependent K_d degradation drives the system trajectory across the Hopf bifurcation boundary when rapid growth co-occurs with elevated delay | Results §3.2 | `[SIM]` | Medium | None |
| 3 | The vulnerability window requires co-occurrence of rapid growth (>6 cm/yr) and elevated baseline delay (τ₀ > 180 ms); neither alone is sufficient | Results §3.2 | `[SIM]` | Medium | None |
| 4 | Model predicts female vulnerability at 10.6–11.8 years and male vulnerability at 12.2–14.2 years | Results §3.3 | `[SIM]` | Medium | None — timing now reported as model output without clinical comparison in Results |
| 5 | Female instability probability 2.8-fold higher in the female model than in the male model | Results §3.3 | `[SIM]` | Medium | None — "in the female model than in the male model" qualifier added; clinical comparison moved to Discussion |
| 6 | Spontaneous stabilization at skeletal maturity arises from growth deceleration restoring K_d and τ to baseline | Results §3.4 | `[SIM]` | Medium | None — now reports model outcome only; clinical correspondence moved to Discussion |
| 7 | Simulated brace augmentation (K_d,ext = 3) restores operating point to stability corridor | Results §3.5 | `[SIM]` | Low | Caution — brace model is a simplified proxy; clinical comparison now in Discussion only |
| 8 | Stochastic noise modulates the effective stability boundary; suboptimal K_d + noise triggers instability in 70% of trials | Results §3.6 | `[SIM]` | Medium | None — PIEZO2 speculation moved to Discussion |
| 9 | Model's 2.8-fold female preponderance is broadly consistent with reported 3:1 ratio | Discussion §5.2 | `[SIM+LIT]` | Medium | Caution — model ratio depends on assumed differential β; now in Discussion with explicit caveat |
| 10 | Model prediction of stabilization at maturity is consistent with cessation of curve progression | Discussion §5.2 | `[SIM+LIT]` | Medium | None |
| 11 | Proprioceptive deficits documented in AIS patients are consistent with degraded K_d predicted by the model | Discussion §5.2 | `[SIM+LIT]` | Medium | None |
| 12 | PHV–AIS correlation is consistent with the model's predicted vulnerability window timing | Discussion §5.2 | `[SIM+LIT]` | Medium | None — softened from "direct prediction" to "consistent with" |
| 13 | Brace efficacy dependence on compliance hours is consistent with the haptic augmentation hypothesis | Discussion §5.2 | `[SIM+LIT]` | Medium | Caution — alternative explanations exist |
| 14 | Individuals with noisier proprioceptive signals (e.g., PIEZO2 variants) may have lower stability threshold | Discussion §5.2 | `[SIM+LIT]` | Low | Caution — speculative; appropriately placed in Discussion with hedging |
| 15 | Screening via proprioceptive velocity sensing tests may identify children entering the vulnerability window | Discussion §5.3 | `[EXP]` | Low | None — appropriately framed as hypothesis |
| 16 | Brace designs optimized for sensory feedback rather than corrective force may warrant investigation | Discussion §5.3 | `[EXP]` | Low | None — appropriately framed as hypothesis |
| 17 | Perturbation-based proprioceptive training during peripubertal period warrants investigation as preventive intervention | Discussion §5.3 | `[EXP]` | Low | None — appropriately framed as hypothesis |
| 18 | The derivative gain gap hypothesis may create a transient Hopf bifurcation instability explaining AIS onset | Conclusions | `[SIM]` | Medium | None — appropriately hedged with "generates the hypothesis" |

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
