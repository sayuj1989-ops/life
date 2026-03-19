# Bolt-BioFold ⚡ Analysis Report

## Reproducibility Checklist
*   **Source:** Default Seed List
*   **Date:** 2026-03-19 19:29
*   **Commit:** a2b2b032c575f5572609c97588fa4b351982cb14
*   **Params:** pLDDT>=70 for geometry, strict segmentation, custom fast cross-products

## Results Table

| protein_id | uniprot | species | length | pLDDT_mean | pLDDT_median | pLDDT_fraction_high | pLDDT_fraction_ok | pLDDT_fraction_low | PAE_mean | PAE_domain_blockiness_score | predicted_domain_segments | disorder_fraction_proxy | hinge_candidates | backbone_principal_axis | radius_of_gyration | end_to_end_distance | curvature_summary | torsion_summary | anisotropy_index | bending_hotspots | exposed_surface_proxy | charged_patch_score | low_confidence_warning | multi_domain_uncertain | likely_IDR_heavy | confidence_level | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PIEZO2 | Q92508 | human | 2521 | 72.05 | 79.19 | 0.12 | 0.55 | 0.33 | 22.74 | 5.74 | 35 | 0.17 | 3 | [-0.270, -0.320, 0.908] | 58.85 | 29.95 | 0.34 | 1.18 | 3.90 | 458:0.44; 625:0.42; 513:0.41 | 0.46 | 0.27 | False | True | False | Medium | High anisotropy (3.90) indicates fibrous/extended morphology. Potential tension element or structural scaffold. Detected 3 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (5.74) suggests distinct dynamic domains. |
| LMNA | P02545 | human | 664 | 76.37 | 93.12 | 0.58 | 0.11 | 0.31 | 24.87 | 2.56 | 3 | 0.26 | 0 | [-0.668, -0.244, 0.703] | 71.25 | 278.06 | 0.34 | 1.19 | 4.75 | 508:0.40; 519:0.39; 30:0.38 | 0.87 | 0.40 | False | True | False | Medium | High anisotropy (4.75) indicates fibrous/extended morphology. Potential tension element or structural scaffold. High PAE blockiness (2.56) suggests distinct dynamic domains. |
| COL1A1 | P02452 | human | 1464 | 52.73 | 44.22 | 0.15 | 0.05 | 0.80 | 27.40 | 6.55 | 3 | 0.67 | 16 | [-0.475, 0.297, 0.828] | 23.46 | 48.98 | 0.30 | 1.86 | 2.80 | 1315:0.39; 1258:0.38; 1431:0.38 | 0.87 | 0.30 | True | True | True | Low | ⚠️ Low confidence (pLDDT mean 52.7). Structure may be unreliable. Detected 16 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (6.55) suggests distinct dynamic domains. |
| RUNX3 | Q13761 | human | 415 | 60.56 | 46.34 | 0.28 | 0.04 | 0.68 | 25.59 | 0.00 | 1 | 0.56 | 12 | [-0.510, 0.008, 0.860] | 15.81 | 52.97 | 0.28 | 1.96 | 2.06 | 159:0.39; 69:0.38; 54:0.38 | 0.78 | 0.37 | True | False | True | Low | ⚠️ Low confidence (pLDDT mean 60.6). Structure may be unreliable. Detected 12 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. |

## CSV Data

```csv
protein_id,uniprot,species,length,pLDDT_mean,pLDDT_median,pLDDT_fraction_high,pLDDT_fraction_ok,pLDDT_fraction_low,PAE_mean,PAE_domain_blockiness_score,predicted_domain_segments,disorder_fraction_proxy,hinge_candidates,backbone_principal_axis,radius_of_gyration,end_to_end_distance,curvature_summary,torsion_summary,anisotropy_index,bending_hotspots,exposed_surface_proxy,charged_patch_score,low_confidence_warning,multi_domain_uncertain,likely_IDR_heavy,confidence_level,interpretation
PIEZO2,Q92508,human,2521,72.0459182863943,79.19,0.11939706465688218,0.5537485124950416,0.32685442284807614,22.743295862553047,5.738877788747343,35,0.1701705672352241,3,"[-0.270, -0.320, 0.908]",58.854216254576635,29.952230718262037,0.3413845615077925,1.181661841789843,3.896259474160542,458:0.44; 625:0.42; 513:0.41,0.45735819119397064,0.26963906581740976,False,True,False,Medium,High anisotropy (3.90) indicates fibrous/extended morphology. Potential tension element or structural scaffold. Detected 3 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (5.74) suggests distinct dynamic domains.
LMNA,P02545,human,664,76.37072289156627,93.12,0.5813253012048193,0.11295180722891567,0.3057228915662651,24.874845768616634,2.562202816305735,3,0.2575301204819277,0,"[-0.668, -0.244, 0.703]",71.24585834790787,278.06200657227515,0.34356676954830484,1.1944328264571509,4.751667397697646,508:0.40; 519:0.39; 30:0.38,0.8704819277108434,0.3973333333333333,False,True,False,Medium,High anisotropy (4.75) indicates fibrous/extended morphology. Potential tension element or structural scaffold. High PAE blockiness (2.56) suggests distinct dynamic domains.
COL1A1,P02452,human,1464,52.72999316939891,44.22,0.15027322404371585,0.045081967213114756,0.8046448087431693,27.395150273224044,6.553859379269947,3,0.6734972677595629,16,"[-0.475, 0.297, 0.828]",23.45619636653999,48.975483305425385,0.29542692309174906,1.8591542262564775,2.7970300386970957,1315:0.39; 1258:0.38; 1431:0.38,0.8722677595628415,0.3,True,True,True,Low,⚠️ Low confidence (pLDDT mean 52.7). Structure may be unreliable. Detected 16 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (6.55) suggests distinct dynamic domains.
RUNX3,Q13761,human,415,60.564096385542165,46.34,0.2819277108433735,0.03855421686746988,0.6795180722891566,25.59002467702134,0.0,1,0.5614457831325301,12,"[-0.510, 0.008, 0.860]",15.814810367547928,52.973654367053065,0.2843747847575885,1.964747553996119,2.0611670656856456,159:0.39; 69:0.38; 54:0.38,0.7831325301204819,0.37209302325581395,True,False,True,Low,⚠️ Low confidence (pLDDT mean 60.6). Structure may be unreliable. Detected 12 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load.
```

## Key Plots Summary
*   Generated pLDDT profiles for all proteins.
*   Generated PAE heatmaps for proteins with available PAE data.

## Interpretations

### PIEZO2 (Q92508)
*   **What we see:** pLDDT 72.0, Anisotropy 3.90. High anisotropy (3.90) indicates fibrous/extended morphology. Potential tension element or structural scaffold. Detected 3 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (5.74) suggests distinct dynamic domains.
*   **Why it matters:** High aspect ratio (3.90) supports role as a robust tension-transmitting element critical for counter-curvature mechanics in spine morphogenesis. Presence of 3 potential hinge regions may allow nonlinear responses to mechanical load (e.g., buckling).
*   **Confidence:** Medium
*   **Next Test:** Simulate load to identify critical buckling thresholds for these hinges, predicting macroscopic scoliotic deformations.

### LMNA (P02545)
*   **What we see:** pLDDT 76.4, Anisotropy 4.75. High anisotropy (4.75) indicates fibrous/extended morphology. Potential tension element or structural scaffold. High PAE blockiness (2.56) suggests distinct dynamic domains.
*   **Why it matters:** High aspect ratio (4.75) supports role as a robust tension-transmitting element critical for counter-curvature mechanics in spine morphogenesis.
*   **Confidence:** Medium
*   **Next Test:** In vitro stretching assay to confirm force-transmitting capacity along the principal axis.

### COL1A1 (P02452)
*   **What we see:** pLDDT 52.7, Anisotropy 2.80. ⚠️ Low confidence (pLDDT mean 52.7). Structure may be unreliable. Detected 16 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load. High PAE blockiness (6.55) suggests distinct dynamic domains.
*   **Why it matters:** Moderate aspect ratio (2.80) suggests a possible intermediate structural role in the ECM or cytoskeleton during axial elongation. Presence of 16 potential hinge regions may allow nonlinear responses to mechanical load (e.g., buckling).
*   **Confidence:** Low
*   **Next Test:** Analyze temporal expression gradients in developing somites.

### RUNX3 (Q13761)
*   **What we see:** pLDDT 60.6, Anisotropy 2.06. ⚠️ Low confidence (pLDDT mean 60.6). Structure may be unreliable. Detected 12 potential hinge(s) (flexible regions in stiff segments). Candidate for curvature regulation under load.
*   **Why it matters:** Moderate aspect ratio (2.06) suggests a possible intermediate structural role in the ECM or cytoskeleton during axial elongation. Presence of 12 potential hinge regions may allow nonlinear responses to mechanical load (e.g., buckling).
*   **Confidence:** Low
*   **Next Test:** Analyze temporal expression gradients in developing somites.

## Best Next Move
🚀 **Simulate mechanical load on high-anisotropy candidates: PIEZO2, LMNA**
