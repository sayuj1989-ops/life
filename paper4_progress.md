# Paper 4 Progress: The Molecular Basis of τ

## Phase 1: Literature Review — Decomposing τ
- **Day 1:** Completed. Decomposed proprioceptive delay ($\tau$) into its physiological components (transduction, afferent conduction, spinal relay, cerebellar processing, efferent conduction, NMJ, electromechanical delay) and established a baseline $\tau$ budget.
  - **Key findings:** Baseline $\tau$ is approx 100-150ms. The PID model from Paper 2 uses a critical threshold of $\tau > 200$ms combined with high growth velocity. The goal is to see how genetic variants push $\tau$ toward this threshold.
  - **Issues/Questions:** Need to systematically map AIS GWAS hits to these specific delay components.
  - **Next Steps:** Proceed to Day 2: Comprehensive review of AIS GWAS hits (GPR126, LBX1, PAX1, etc.) and their proposed biological functions.

- **Days 2-5:** Completed. Conducted a deep dive literature review of the major AIS genetic loci and mapped them onto the $\tau$ components.
  - **Key findings:**
    - GPR126 (ADGRG6) directly affects Schwann cell myelination, mapping to $\tau_{afferent}$.
    - LBX1 affects dorsal interneuron specification in the spinal cord, mapping to $\tau_{spinal}$.
    - Piezo2 is the principal mechanotransducer; Chesler (2016) shows Piezo2 knockouts have severe proprioceptive deficits AND progressive scoliosis, providing extreme-phenotype validation. Channel kinetics map to $\tau_{transduction}$.
    - PAX1 is a skeletal transcription factor, likely altering the mechanical "plant" rather than the neural "controller."
    - NaV channel variants could alter axon conduction velocity ($\tau_{afferent}$).
  - **Issues/Questions for Dr. Sayuj:** How do we model polygenic risk where a patient has mild delays in multiple components (e.g., a GPR126 variant + an LBX1 variant)? Does the simulation need to account for non-linear interactions between these delays?
  - **Next Steps:** Proceed to Phase 2 (Days 6-9) to investigate the temporal dynamics of myelination during adolescence, specifically looking for normative nerve conduction velocity data across the growth spurt to see if myelination transiently "lags" behind bone growth.
