# Bolt-BioFold ⚡ Analysis Report

**Date:** 2026-02-06 19:36
**Source:** Default Seed List
**Code Version:** Bolt-BioFold v1.0

## Results Table

| protein_id | uniprot | species | length | pLDDT_mean | pLDDT_median | pLDDT_fraction_high | pLDDT_fraction_ok | pLDDT_fraction_low | PAE_mean | PAE_domain_blockiness_score | predicted_domain_segments | disorder_fraction_proxy | hinge_candidates | backbone_principal_axis | radius_of_gyration | end_to_end_distance | curvature_summary | torsion_summary | anisotropy_index | bending_hotspots | exposed_surface_proxy | charged_patch_score | low_confidence_warning | multi_domain_uncertain | likely_IDR_heavy | confidence_level | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PIEZO2 | Q92508 | human | 2521 | 72.05 | 79.19 | 0.12 | 0.55 | 0.33 | 22.74 | 5.74 | 35 | 0.17 | 3 | [-0.270, -0.320, 0.908] | 58.85 | 29.95 | 0.34 | 1.18 | 3.90 | 458:0.44; 625:0.42; 513:0.41 | 0.46 | 0.27 | False | True | False | Medium | High anisotropy (3.90) indicates fibrous/extended morphology. Potential tension element or structural scaffold. Detected 3 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (5.74) suggests distinct dynamic domains. |
| LMNA | P02545 | human | 664 | 76.37 | 93.12 | 0.58 | 0.11 | 0.31 | 24.87 | 2.56 | 3 | 0.26 | 0 | [-0.668, -0.244, 0.703] | 71.25 | 278.06 | 0.34 | 1.19 | 4.75 | 508:0.40; 519:0.39; 30:0.38 | 0.87 | 0.40 | False | True | False | Medium | High anisotropy (4.75) indicates fibrous/extended morphology. Potential tension element or structural scaffold. High PAE blockiness (2.56) suggests distinct dynamic domains. |
| COL1A1 | P02452 | human | 1464 | 52.73 | 44.22 | 0.15 | 0.05 | 0.80 | 27.40 | 6.55 | 3 | 0.67 | 16 | [-0.475, 0.297, 0.828] | 23.46 | 48.98 | 0.30 | 1.86 | 2.80 | 1315:0.39; 1258:0.38; 1431:0.38 | 0.87 | 0.30 | True | True | True | Low | ⚠️ Low confidence (pLDDT mean 52.7). Structure may be unreliable. Detected 16 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (6.55) suggests distinct dynamic domains. |
| RUNX3 | Q13761 | human | 415 | 60.56 | 46.34 | 0.28 | 0.04 | 0.68 | 25.59 | 0.00 | 1 | 0.56 | 12 | [-0.510, 0.008, 0.860] | 15.81 | 52.97 | 0.28 | 1.96 | 2.06 | 159:0.39; 69:0.38; 54:0.38 | 0.78 | 0.37 | True | False | True | Low | ⚠️ Low confidence (pLDDT mean 60.6). Structure may be unreliable. Detected 12 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. |

## Key Plots Summary
*   Generated pLDDT profiles for all proteins.
*   Generated PAE heatmaps for proteins with available PAE data.

## Interpretations

### PIEZO2 (Q92508)
*   **What we see:** pLDDT 72.0, Anisotropy 3.90. High anisotropy (3.90) indicates fibrous/extended morphology. Potential tension element or structural scaffold. Detected 3 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (5.74) suggests distinct dynamic domains.
*   **Why it matters:** High aspect ratio supports tension transmission.
*   **Confidence:** Medium
*   **Next Test:** Compare curvature under stress in simulation.

### LMNA (P02545)
*   **What we see:** pLDDT 76.4, Anisotropy 4.75. High anisotropy (4.75) indicates fibrous/extended morphology. Potential tension element or structural scaffold. High PAE blockiness (2.56) suggests distinct dynamic domains.
*   **Why it matters:** High aspect ratio supports tension transmission.
*   **Confidence:** Medium
*   **Next Test:** Check expression gradients in spine.

### COL1A1 (P02452)
*   **What we see:** pLDDT 52.7, Anisotropy 2.80. ⚠️ Low confidence (pLDDT mean 52.7). Structure may be unreliable. Detected 16 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (6.55) suggests distinct dynamic domains.
*   **Why it matters:** High aspect ratio supports tension transmission.
*   **Confidence:** Low
*   **Next Test:** Compare curvature under stress in simulation.

### RUNX3 (Q13761)
*   **What we see:** pLDDT 60.6, Anisotropy 2.06. ⚠️ Low confidence (pLDDT mean 60.6). Structure may be unreliable. Detected 12 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load.
*   **Why it matters:** High aspect ratio supports tension transmission.
*   **Confidence:** Low
*   **Next Test:** Compare curvature under stress in simulation.

## Best Next Move
🚀 **Simulate mechanical load on high-anisotropy candidates: PIEZO2, LMNA**
