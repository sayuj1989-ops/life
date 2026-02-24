Starting Bolt-BioFold Analysis Cycle on 9 proteins...
Processing FBN1 (P35555)...
Querying API for P35555...
API Error for P35555: 404
Skipping FBN1 - data fetch failed.
Processing COL1A1 (P02452)...
Processing PIEZO2 (Q9H5I5)...
Processing YAP1 (P46937)...
Processing PKD2 (Q13563)...
Processing IGF1R (P08069)...
Processing LBX1 (P52954)...
Processing ADGRG6 (Q7Z2K8)...
Processing DMD (P11532)...

### Results Table
| protein_id | species | length | pLDDT_mean | pLDDT_median | pLDDT_fraction_high | pLDDT_fraction_ok | pLDDT_fraction_low | PAE_mean | PAE_domain_blockiness_score | predicted_domain_segments | disorder_fraction_proxy | hinge_candidates | morphology | backbone_principal_axis | radius_of_gyration | end_to_end_distance | curvature_summary | torsion_summary | anisotropy_index | bending_hotspots | exposed_surface_proxy | charged_patch_score | low_confidence_warning | multi_domain_uncertain | likely_IDR_heavy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COL1A1 (P02452) | Homo sapiens | 1464 | 52.73 | 44.22 | 0.15 | 0.05 | 0.80 | 27.40 | 6.55 | 3 | 0.67 | 16 | Intermediate | [-0.475, 0.297, 0.828] | 23.46 | 48.98 | 0.2954 | 1.8592 | 2.80 | 1315:0.39; 1258:0.38; 1431:0.38 | 0.87 | 0.30 | True | True | True |
| PIEZO2 (Q9H5I5) | Homo sapiens | 709 | 79.44 | 88.38 | 0.42 | 0.37 | 0.21 | 16.99 | 2.80 | 7 | 0.14 | 0 | Fibrous/Extended | [-0.687, -0.068, 0.724] | 43.41 | 28.41 | 0.3293 | 1.4285 | 4.44 | 460:0.38; 239:0.38; 138:0.38 | 0.56 | 0.25 | False | True | False |
| YAP1 (P46937) | Homo sapiens | 504 | 57.40 | 51.56 | 0.02 | 0.25 | 0.74 | 27.50 | 9.26 | 5 | 0.45 | 2 | Intermediate | [-0.676, 0.732, 0.082] | 23.55 | 11.43 | 0.3206 | 1.6285 | 1.99 | 182:0.38; 241:0.38; 257:0.38 | 0.93 | 0.30 | True | True | True |
| PKD2 (Q13563) | Homo sapiens | 968 | 70.12 | 78.22 | 0.37 | 0.21 | 0.42 | 21.67 | 3.03 | 4 | 0.29 | 1 | Intermediate | [-0.531, 0.110, 0.840] | 36.70 | 20.44 | 0.3339 | 1.2877 | 2.70 | 349:0.39; 309:0.39; 374:0.38 | 0.68 | 0.32 | False | True | False |
| IGF1R (P08069) | Homo sapiens | 1367 | 78.02 | 88.00 | 0.44 | 0.32 | 0.25 | 23.59 | 5.85 | 16 | 0.16 | 35 | Globular | [-0.397, 0.016, 0.918] | 43.20 | 53.58 | 0.2975 | 1.7991 | 1.43 | 34:0.41; 1073:0.40; 44:0.38 | 0.42 | 0.35 | False | True | False |
| LBX1 (P52954) | Homo sapiens | 281 | 66.87 | 60.25 | 0.23 | 0.16 | 0.61 | 25.08 | 7.35 | 3 | 0.26 | 0 | Intermediate | [-0.222, -0.149, 0.964] | 22.69 | 51.86 | 0.3435 | 1.1726 | 2.27 | 83:0.39; 37:0.39; 34:0.38 | 0.93 | 0.36 | True | True | False |
| ADGRG6 (Q7Z2K8) | Homo sapiens | 1008 | 43.72 | 41.34 | 0.01 | 0.02 | 0.97 | 28.68 | 0.00 | 1 | 0.84 | 0 | Intermediate | [-0.667, -0.157, 0.728] | 13.28 | 31.94 | 0.3568 | 0.9412 | 2.69 | 948:0.38; 930:0.38; 933:0.37 | 1.00 | 0.42 | True | False | True |
| DMD (P11532) | Homo sapiens | 525 | 76.35 | 85.06 | 0.46 | 0.18 | 0.36 | 19.01 | 6.91 | 2 | 0.18 | 1 | Globular | [-0.696, -0.170, 0.698] | 22.82 | 48.85 | 0.3397 | 1.3283 | 1.32 | 251:0.39; 14:0.39; 53:0.38 | 0.55 | 0.37 | False | True | False |

### CSV Output
```csv
protein_id,species,length,pLDDT_mean,pLDDT_median,pLDDT_fraction_high,pLDDT_fraction_ok,pLDDT_fraction_low,PAE_mean,PAE_domain_blockiness_score,predicted_domain_segments,disorder_fraction_proxy,hinge_candidates,morphology,backbone_principal_axis,radius_of_gyration,end_to_end_distance,curvature_summary,torsion_summary,anisotropy_index,bending_hotspots,exposed_surface_proxy,charged_patch_score,low_confidence_warning,multi_domain_uncertain,likely_IDR_heavy
COL1A1 (P02452),Homo sapiens,1464,52.73,44.22,0.15,0.05,0.80,27.40,6.55,3,0.67,16,Intermediate,"[-0.475, 0.297, 0.828]",23.46,48.98,0.2954,1.8592,2.80,1315:0.39; 1258:0.38; 1431:0.38,0.87,0.30,True,True,True
PIEZO2 (Q9H5I5),Homo sapiens,709,79.44,88.38,0.42,0.37,0.21,16.99,2.80,7,0.14,0,Fibrous/Extended,"[-0.687, -0.068, 0.724]",43.41,28.41,0.3293,1.4285,4.44,460:0.38; 239:0.38; 138:0.38,0.56,0.25,False,True,False
YAP1 (P46937),Homo sapiens,504,57.40,51.56,0.02,0.25,0.74,27.50,9.26,5,0.45,2,Intermediate,"[-0.676, 0.732, 0.082]",23.55,11.43,0.3206,1.6285,1.99,182:0.38; 241:0.38; 257:0.38,0.93,0.30,True,True,True
PKD2 (Q13563),Homo sapiens,968,70.12,78.22,0.37,0.21,0.42,21.67,3.03,4,0.29,1,Intermediate,"[-0.531, 0.110, 0.840]",36.70,20.44,0.3339,1.2877,2.70,349:0.39; 309:0.39; 374:0.38,0.68,0.32,False,True,False
IGF1R (P08069),Homo sapiens,1367,78.02,88.00,0.44,0.32,0.25,23.59,5.85,16,0.16,35,Globular,"[-0.397, 0.016, 0.918]",43.20,53.58,0.2975,1.7991,1.43,34:0.41; 1073:0.40; 44:0.38,0.42,0.35,False,True,False
LBX1 (P52954),Homo sapiens,281,66.87,60.25,0.23,0.16,0.61,25.08,7.35,3,0.26,0,Intermediate,"[-0.222, -0.149, 0.964]",22.69,51.86,0.3435,1.1726,2.27,83:0.39; 37:0.39; 34:0.38,0.93,0.36,True,True,False
ADGRG6 (Q7Z2K8),Homo sapiens,1008,43.72,41.34,0.01,0.02,0.97,28.68,0.00,1,0.84,0,Intermediate,"[-0.667, -0.157, 0.728]",13.28,31.94,0.3568,0.9412,2.69,948:0.38; 930:0.38; 933:0.37,1.00,0.42,True,False,True
DMD (P11532),Homo sapiens,525,76.35,85.06,0.46,0.18,0.36,19.01,6.91,2,0.18,1,Globular,"[-0.696, -0.170, 0.698]",22.82,48.85,0.3397,1.3283,1.32,251:0.39; 14:0.39; 53:0.38,0.55,0.37,False,True,False

```

Saved plot to outputs/bolt_biofold_plddt.png

### Interpretation
- **COL1A1**: (Low Confidence). We see: Intermediate shape, 16 potential hinge(s), High local curvature. Matters: ECM structural component; anisotropy defines load-bearing axis and tissue stiffness. Next: Test mechanical gating/unfolding under force.
- **PIEZO2**: (Low Confidence). We see: Highly elongated/Fibrous, High local curvature. Matters: Mechanosensitive channel; curvature/hinges likely relate to gating mechanics under membrane tension. Next: Compare with orthologs to check conservation of geometry.
- **YAP1**: (Low Confidence). We see: Intermediate shape, 2 potential hinge(s), High local curvature. Matters: Mechanotransducer; structural disorder likely facilitates binding versatility under stress. Next: Analyze IDR phase separation potential.
- **PKD2**: (Low Confidence). We see: Intermediate shape, 1 potential hinge(s), High local curvature. Matters: Structural metrics imply role in mechanical integrity or sensing. Next: Test mechanical gating/unfolding under force.
- **IGF1R**: (Low Confidence). We see: Globular, 35 potential hinge(s), High local curvature. Matters: Structural metrics imply role in mechanical integrity or sensing. Next: Compare with orthologs to check conservation of geometry.
- **LBX1**: (Low Confidence). We see: Intermediate shape, High local curvature. Matters: Structural metrics imply role in mechanical integrity or sensing. Next: Compare with orthologs to check conservation of geometry.
- **ADGRG6**: (Low Confidence). We see: Intermediate shape, High local curvature. Matters: Structural metrics imply role in mechanical integrity or sensing. Next: Analyze IDR phase separation potential.
- **DMD**: (Low Confidence). We see: Globular, 1 potential hinge(s), High local curvature. Matters: Muscle-ECM linker; massive length and flexibility essential for shock absorption. Next: Compare with orthologs to check conservation of geometry.

### Best Next Move
Correlate curvature metrics (especially hinge locations) with known pathogenic variants in these genes.
