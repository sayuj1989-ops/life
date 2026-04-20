# Paper 3 Progress

## Completed
- Phase 1, Day 3 (2026-04-14): Researched sarcopenia, muscle force production decline, satellite cell exhaustion, and muscle spindle changes with age. Documented in `paper3_literature/day3_sarcopenia.md`. Mapped these physical degradations to the actuator gain and sensory inputs ($K_p, K_d$) in the PID model.
- Phase 1, Day 1: Searched for and summarised key papers on ageing and postural control (proprioceptive decline, vestibular degeneration, cerebellar atrophy).
- Phase 1, Day 2 (2026-04-13): Researched and documented peripheral neuropathy and nerve conduction velocity (NCV) changes with age, quantifying the impact on proprioceptive delay ($\tau$). Saved findings to `paper3_literature/day2_neuropathy_delay.md`. Added concrete citations with DOIs to address constraints.

## Next Steps
- Phase 1, Day 4: Search for papers on telomere biology in the nervous system — Schwann cells, DRG neurons, Purkinje cells, telomere length vs. nerve conduction. Save to `paper3_literature/day4_telomere_nervous.md`.

## Issues/Questions for Dr. Sayuj
- The specific mapping of age-dependent $\tau$ degradation in the PID model requires selecting a functional form (e.g. linear vs exponential past age 60) based on these NCV decreases. Should we strictly use empirical NCV decline slopes, or create an amplified "effective tau" representing both NCV and central processing delays?

- For sarcopenia, should we model actuator degradation purely as a reduced force multiplier (lower maximum torque), or also introduce a low-pass filter effect to represent the slower rate of force development?