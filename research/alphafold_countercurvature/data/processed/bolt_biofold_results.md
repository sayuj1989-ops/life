# Bolt-BioFold ⚡ Analysis Report

**Date:** 2026-03-13 07:05
**Source:** User Input
**Code Version:** Bolt-BioFold v1.0

## Results Table

| protein_id | uniprot | species | length | pLDDT_mean | pLDDT_median | pLDDT_fraction_high | pLDDT_fraction_ok | pLDDT_fraction_low | PAE_mean | PAE_domain_blockiness_score | predicted_domain_segments | disorder_fraction_proxy | hinge_candidates | backbone_principal_axis | radius_of_gyration | end_to_end_distance | curvature_summary | torsion_summary | anisotropy_index | bending_hotspots | exposed_surface_proxy | charged_patch_score | low_confidence_warning | multi_domain_uncertain | likely_IDR_heavy | confidence_level | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| YAP1 | P46937 | human | 504 | 57.40 | 51.56 | 0.02 | 0.25 | 0.74 | 27.50 | 9.26 | 5 | 0.45 | 2 | [-0.676, 0.732, 0.082] | 23.55 | 11.43 | 0.32 | 1.63 | 1.99 | 182:0.38; 241:0.38; 257:0.38 | 0.93 | 0.30 | True | True | True | Low | ⚠️ Low confidence (pLDDT mean 57.4). Structure may be unreliable. Detected 2 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (9.26) suggests distinct dynamic domains. |

## Key Plots Summary
*   Generated pLDDT profiles for all proteins.
*   Generated PAE heatmaps for proteins with available PAE data.

## Interpretations

### YAP1 (P46937)
*   **What we see:** pLDDT 57.4, Anisotropy 1.99. ⚠️ Low confidence (pLDDT mean 57.4). Structure may be unreliable. Detected 2 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (9.26) suggests distinct dynamic domains.
*   **Why it matters:** Globular domain likely involved in signaling or binding.
*   **Confidence:** Low
*   **Next Test:** Compare curvature under stress in simulation.

## Best Next Move
🚀 **Expand candidate list to include more cytoskeletal cross-linkers.**
