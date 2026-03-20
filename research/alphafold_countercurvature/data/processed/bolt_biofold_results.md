# Bolt-BioFold ⚡ Analysis Report

## Reproducibility Checklist
- **Source:** Default Seed List (AlphaFold DB)
- **Date:** 2026-03-20 19:39
- **Commit:** (Not checked dynamically in this script)
- **Params:** pLDDT threshold=70, smoothing_window=N/A, Segmentation rule=Consistent high pLDDT + PAE blockiness
- **Notes:** All requested artifacts successfully loaded.

## Results Table

| protein_id | uniprot | species | length | pLDDT_mean | pLDDT_median | pLDDT_fraction_high | pLDDT_fraction_ok | pLDDT_fraction_low | PAE_mean | PAE_domain_blockiness_score | predicted_domain_segments | disorder_fraction_proxy | hinge_candidates | backbone_principal_axis | radius_of_gyration | end_to_end_distance | curvature_summary | torsion_summary | anisotropy_index | bending_hotspots | exposed_surface_proxy | charged_patch_score | low_confidence_warning | multi_domain_uncertain | likely_IDR_heavy | confidence_level | what | why | next_test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COL1A1 | P02452 | human | 1464 | 52.73 | 44.22 | 0.15 | 0.05 | 0.80 | 27.40 | 6.55 | 3 | 0.67 | 16 | [-0.475, 0.297, 0.828] | 23.46 | 48.98 | 0.30 | 1.86 | 2.80 | 1315:0.39; 1258:0.38; 1431:0.38 | 0.87 | 0.30 | True | True | True | Low | pLDDT mean 52.7 indicates mostly low-confidence regions. Anisotropy index is 2.80. Detected 16 potential hinge(s). | Moderate anisotropy suggests a structural element. | Compare curvature under stress in simulation. |
| ILK | Q13418 | human | 452 | 88.17 | 92.62 | 0.63 | 0.30 | 0.07 | 14.31 | 4.32 | 4 | 0.04 | 2 | [-0.509, -0.524, 0.684] | 23.91 | 21.61 | 0.33 | 1.55 | 2.11 | 276:0.38; 312:0.38; 69:0.38 | 0.32 | 0.43 | False | True | False | High | High pLDDT mean (88.2) suggests well-structured regions. Anisotropy index is 2.11. Detected 2 potential hinge(s). | Moderate anisotropy suggests a structural element. | Compare curvature under stress in simulation. |
| BGN | P21810 | human | 368 | 85.59 | 96.28 | 0.78 | 0.03 | 0.19 | 11.02 | 1.74 | 2 | 0.17 | 0 | [-0.640, -0.157, 0.752] | 22.60 | 70.03 | 0.30 | 1.90 | 2.53 | 158:0.38; 203:0.38; 359:0.38 | 0.27 | 0.44 | False | True | False | High | High pLDDT mean (85.6) suggests well-structured regions. Anisotropy index is 2.53. | Moderate anisotropy suggests a structural element. | Check expression gradients in developing spine. |

### CSV-Ready Block
```csv
protein_id,uniprot,species,length,pLDDT_mean,pLDDT_median,pLDDT_fraction_high,pLDDT_fraction_ok,pLDDT_fraction_low,PAE_mean,PAE_domain_blockiness_score,predicted_domain_segments,disorder_fraction_proxy,hinge_candidates,backbone_principal_axis,radius_of_gyration,end_to_end_distance,curvature_summary,torsion_summary,anisotropy_index,bending_hotspots,exposed_surface_proxy,charged_patch_score,low_confidence_warning,multi_domain_uncertain,likely_IDR_heavy,confidence_level,what,why,next_test
COL1A1,P02452,human,1464,52.72999316939891,44.22,0.15027322404371585,0.045081967213114804,0.8046448087431693,27.395150273224044,6.553859379269947,3,0.6734972677595629,16,"[-0.475, 0.297, 0.828]",23.45619636653999,48.975483305425385,0.29542692309174906,1.8591542262564775,2.7970300386970957,1315:0.39; 1258:0.38; 1431:0.38,0.8722677595628415,0.3,True,True,True,Low,pLDDT mean 52.7 indicates mostly low-confidence regions. Anisotropy index is 2.80. Detected 16 potential hinge(s).,Moderate anisotropy suggests a structural element.,Compare curvature under stress in simulation.
ILK,Q13418,human,452,88.17367256637168,92.62,0.6261061946902655,0.30309734513274333,0.07079646017699115,14.310409977288746,4.324019761947581,4,0.04424778761061947,2,"[-0.509, -0.524, 0.684]",23.908666955275255,21.6108541478582,0.32758996153417,1.5459352818673304,2.107325035557057,276:0.38; 312:0.38; 69:0.38,0.3163716814159292,0.42735042735042733,False,True,False,High,High pLDDT mean (88.2) suggests well-structured regions. Anisotropy index is 2.11. Detected 2 potential hinge(s).,Moderate anisotropy suggests a structural element.,Compare curvature under stress in simulation.
BGN,P21810,human,368,85.59347826086957,96.28,0.782608695652174,0.029891304347826053,0.1875,11.015455163043478,1.7400850235620178,2,0.17119565217391305,0,"[-0.640, -0.157, 0.752]",22.599122460556917,70.02932748499016,0.3035444569303186,1.8978898522027727,2.5290981208231433,158:0.38; 203:0.38; 359:0.38,0.27445652173913043,0.4375,False,True,False,High,High pLDDT mean (85.6) suggests well-structured regions. Anisotropy index is 2.53.,Moderate anisotropy suggests a structural element.,Check expression gradients in developing spine.
```


## Key Plots Summary
*   Generated pLDDT profiles for all proteins.
*   Generated PAE heatmaps for proteins with available PAE data.

## Interpretations

### COL1A1 (P02452)
- **What we see:** pLDDT mean 52.7 indicates mostly low-confidence regions. Anisotropy index is 2.80. Detected 16 potential hinge(s).
- **Why it matters:** Moderate anisotropy suggests a structural element.
- **Confidence level:** Low
- **Next test:** Compare curvature under stress in simulation.

### ILK (Q13418)
- **What we see:** High pLDDT mean (88.2) suggests well-structured regions. Anisotropy index is 2.11. Detected 2 potential hinge(s).
- **Why it matters:** Moderate anisotropy suggests a structural element.
- **Confidence level:** High
- **Next test:** Compare curvature under stress in simulation.

### BGN (P21810)
- **What we see:** High pLDDT mean (85.6) suggests well-structured regions. Anisotropy index is 2.53.
- **Why it matters:** Moderate anisotropy suggests a structural element.
- **Confidence level:** High
- **Next test:** Check expression gradients in developing spine.

## Best Next Move
🚀 **Expand candidate list to include more cytoskeletal cross-linkers.**
