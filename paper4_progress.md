# Paper 4: The Molecular Basis of $\tau$ - Progress Log

## Phase 1: Literature Review — Decomposing $\tau$

### Date: 2024-05-18 (Phase 1, Day 1)

**Task:** Decomposition of proprioceptive delay into components — quantify each sub-delay from published electrophysiology (peripheral transduction, afferent conduction, spinal relay, cerebellar processing, efferent conduction, NMJ, electromechanical). Build a $\tau$ budget.

**Key Findings:**
- The overall baseline proprioceptive delay for a complex predictive response (incorporating a cerebellar loop) can be decomposed into:
  - Peripheral Transduction ($\tau_{transduction}$, Piezo2): ~2 ms
  - Afferent Conduction ($\tau_{afferent}$): ~12 ms
  - Spinal Relay ($\tau_{spinal}$): ~1 ms
  - Cerebellar Processing ($\tau_{cerebellar}$): ~15 ms
  - Efferent Conduction ($\tau_{efferent}$): ~15 ms
  - Neuromuscular Junction ($\tau_{NMJ}$): ~1 ms
  - Electromechanical Delay ($\tau_{EM}$): ~40 ms
- The baseline total is ~86 ms. The difference between this normative adult baseline and the >200 ms instability threshold in Paper 2 provides the "gap" where developmental changes or polysynaptic path lengths might introduce instability.

**Decisions Made:**
- Documented findings with DOIs in `paper4_literature/day1_tau_decomposition.md`.
- Kept the budget focused on the shortest proprioceptive-cerebellar-motor loop to establish a clear physiological baseline.

**Issues/Questions for Dr. Sayuj:**
- The normative adult $\tau$ total is ~86 ms, but the instability threshold from Paper 2 is >200 ms. Does the 200ms threshold implicitly include visual/vestibular processing delays, or should we model the growth spurt as pushing this 86ms baseline drastically upward due to stretched axons/delayed myelination? Should we also account for slower polysynaptic spinal pathways?

**Next Session's Plan (Day 2):**
- Comprehensive review of AIS GWAS hits (GPR126, LBX1, PAX1, etc.).
- For each locus, extract risk allele, effect size, population frequency, and proposed biological function.
- Create `paper4_literature/day2_ais_gwas.md`.
