# Bolt-BioFold ⚡ Analysis Report

**Date:** 2026-02-24 07:03
**Source:** User Input
**Code Version:** Bolt-BioFold v1.0

## Results Table

| protein_id | uniprot | species | length | pLDDT_mean | pLDDT_median | pLDDT_fraction_high | pLDDT_fraction_ok | pLDDT_fraction_low | PAE_mean | PAE_domain_blockiness_score | predicted_domain_segments | disorder_fraction_proxy | hinge_candidates | backbone_principal_axis | radius_of_gyration | end_to_end_distance | curvature_summary | torsion_summary | anisotropy_index | bending_hotspots | exposed_surface_proxy | charged_patch_score | low_confidence_warning | multi_domain_uncertain | likely_IDR_heavy | confidence_level | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FOXO3 | O43524 | human | 673 | 50.66 | 44.03 | 0.09 | 0.04 | 0.87 | 28.16 | 1.35 | 3 | 0.69 | 1 | [-0.468, 0.544, -0.696] | 16.51 | 24.44 | 0.33 | 1.36 | 2.44 | 218:0.38; 161:0.38; 155:0.38 | 0.94 | 0.32 | True | False | True | Low | ⚠️ Low confidence (pLDDT mean 50.7). Structure may be unreliable. Detected 1 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. |
| KL | Q9UEF7 | human | 1012 | 89.09 | 94.94 | 0.73 | 0.17 | 0.10 | 11.20 | 4.35 | 6 | 0.06 | 1 | [-0.722, -0.308, 0.619] | 36.85 | 73.31 | 0.32 | 1.50 | 2.97 | 254:0.43; 475:0.40; 926:0.39 | 0.31 | 0.33 | False | True | False | High | Detected 1 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (4.35) suggests distinct dynamic domains. |

## Key Plots Summary
*   Generated pLDDT profiles for all proteins.
*   Generated PAE heatmaps for proteins with available PAE data.

## Interpretations

### FOXO3 (O43524)
*   **What we see:** pLDDT 50.7, Anisotropy 2.44. ⚠️ Low confidence (pLDDT mean 50.7). Structure may be unreliable. Detected 1 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load.
*   **Why it matters:** High aspect ratio supports tension transmission.
*   **Confidence:** Low
*   **Next Test:** Compare curvature under stress in simulation.

### KL (Q9UEF7)
*   **What we see:** pLDDT 89.1, Anisotropy 2.97. Detected 1 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (4.35) suggests distinct dynamic domains.
*   **Why it matters:** High aspect ratio supports tension transmission.
*   **Confidence:** High
*   **Next Test:** Compare curvature under stress in simulation.

## Best Next Move
🚀 **Expand candidate list to include more cytoskeletal cross-linkers.**
