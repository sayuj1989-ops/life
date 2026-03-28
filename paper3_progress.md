# Paper 3: The Terminal Derivative Gain Gap - Progress Tracker

## Session History

### Date: 2026-03-28
**Phase Completed:** Phase 1, Day 1
**Key Findings / Decisions:**
- Conducted literature review on postural ageing using CrossRef via python API script.
- Confirmed that age-related proprioceptive decline correlates strongly with increased postural sway (e.g., Wingert et al., DOI: 10.1016/j.apmr.2013.08.012).
- Identified mechanistic evidence for vestibular degradation, such as transganglionic nerve degeneration, conceptually supporting a modelled age-related increase in delay ($\tau$).
- Wrote summary to `paper3_literature/day1_postural_ageing.md`.

**Issues / Questions for Dr. Sayuj K.S.:**
- The literature links cognitive/attentional demands to postural recovery in older adults. Do we want the PID model to purely remain low-level (spinal/cerebellar), or should we introduce a cognitive compensation term that delays the terminal gap onset?
- Should we focus exclusively on healthy ageing, or use pathology (e.g., diabetic neuropathy) as extreme parameters in our model simulations?

**Plan for Next Session:**
- Phase 1, Day 2: Search for papers on peripheral neuropathy and nerve conduction velocity changes with age. Quantify how $\tau$ increases with age. Save to `paper3_literature/day2_neuropathy_delay.md`.
