# Hypothesis Register

| ID | Statement | Rationale | Verification | Status |
|----|-----------|-----------|--------------|--------|
| H_2024_05_21 | Loss of mechanosensitive feedback (PIEZO2) destabilizes spinal geometry against gravity, leading to buckling (scoliosis). | Clinical evidence (McMillin 2014) links PIEZO2 mutations to scoliosis; implies alignment is active. | PyElastica simulation: Rod with gravity + feedback controller. Set gain to 0 to simulate PIEZO2 loss; observe buckling. | Proposed |
| H_2024_10_18_A | MMP-3 inhibition preserves spinal disc ECM integrity under unloading conditions. | Unloading upregulates MMP-3 (Jin et al. 2013), causing GAG loss. Blocking this enzyme should decouple the mechanical signal from the catabolic outcome. | Expose spinal organoids to simulated microgravity +/- MMP-3 inhibitor. Measure GAG content and stiffness vs controls. | Proposed |
| H_2024_10_18_B | Constitutive TRAF6/ERK signaling prevents paraspinal muscle atrophy in microgravity. | Microgravity suppresses Pax7 via TRAF6/ERK downregulation (Zhang et al. 2024). Forcing this pathway on should rescue the stem cell pool. | Transfect paraspinal myocytes with constitutively active TRAF6 or Pax7; culture in clinostat. Measure fusion index and atrophy markers. | Proposed |
