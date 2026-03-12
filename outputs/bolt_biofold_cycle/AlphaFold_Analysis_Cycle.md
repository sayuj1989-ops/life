# Bolt-BioFold ⚡ Analysis Cycle Report

## Inputs & Parameters
No specific protein list was provided. Proceeding with explicit defaults:
* **Protein identifiers:** Default seed list (ECM, cytoskeleton, adhesion, cilia, growth plate/cartilage, morphogens)
* **Species:** Human
* **AlphaFold source:** AlphaFold DB
* **PAE matrices:** Used if available
* **Batch size limit:** 20 structures per cycle (Processing 8 defaults)

## A) Results Table

| protein_id      | species      |   length |   pLDDT_mean |   pLDDT_median |   pLDDT_fraction_high |   pLDDT_fraction_ok |   pLDDT_fraction_low |   PAE_mean |   PAE_domain_blockiness_score |   predicted_domain_segments |   disorder_fraction_proxy |   hinge_candidates | backbone_principal_axis   |   radius_of_gyration |   end_to_end_distance |   curvature_summary |   torsion_summary |   anisotropy_index | bending_hotspots                |   exposed_surface_proxy |   charged_patch_score | low_confidence_warning   | multi_domain_uncertain   | likely_IDR_heavy   |
|:----------------|:-------------|---------:|-------------:|---------------:|----------------------:|--------------------:|---------------------:|-----------:|------------------------------:|----------------------------:|--------------------------:|-------------------:|:--------------------------|---------------------:|----------------------:|--------------------:|------------------:|-------------------:|:--------------------------------|------------------------:|----------------------:|:-------------------------|:-------------------------|:-------------------|
| COL2A1 (P02458) | Homo sapiens |     1487 |        52.12 |          44.12 |                  0.13 |                0.06 |                 0.81 |      27.44 |                          5.9  |                           3 |                      0.69 |                 16 | [-0.434, -0.065, 0.899]   |                24.97 |                 45.38 |              0.2938 |            1.8702 |               2.65 | 1327:0.42; 1454:0.39; 1282:0.38 |                    0.87 |                  0.28 | True                     | True                     | True               |
| FN1 (P02751)    | Homo sapiens |     2477 |        69.65 |          75.38 |                  0.05 |                0.56 |                 0.39 |      27.08 |                          7.04 |                          49 |                      0.16 |                216 | [-0.808, 0.027, 0.589]    |                55.09 |                 66.77 |              0.2582 |            2.2568 |               2.44 | 1768:0.41; 2039:0.38; 959:0.38  |                    0.36 |                  0.32 | True                     | True                     | False              |
| ACTB (P60709)   | Homo sapiens |      375 |        95.2  |          97.44 |                  0.93 |                0.05 |                 0.03 |       5.03 |                          1.26 |                           2 |                      0.01 |                  1 | [0.835, 0.517, -0.187]    |                21.09 |                 42.74 |              0.3178 |            1.5512 |               2.19 | 335:0.39; 265:0.39; 258:0.38    |                    0.3  |                  0.34 | False                    | False                    | False              |
| ITGB1 (P05556)  | Homo sapiens |      798 |        85.87 |          89.84 |                  0.49 |                0.4  |                 0.11 |      18.24 |                          4.9  |                          10 |                      0.03 |                 10 | [-0.504, -0.483, 0.716]   |                45.83 |                 94.88 |              0.3054 |            1.7251 |               3.23 | 193:0.39; 474:0.38; 521:0.38    |                    0.34 |                  0.35 | False                    | True                     | False              |
| IFT88 (Q13099)  | Homo sapiens |      824 |        76.35 |          89.28 |                  0.47 |                0.25 |                 0.29 |      19.42 |                          2.43 |                           3 |                      0.23 |                  1 | [-0.626, -0.157, 0.764]   |                38.29 |                 92.39 |              0.3577 |            1.1214 |               2.8  | 315:0.38; 643:0.38; 426:0.38    |                    0.51 |                  0.44 | False                    | True                     | False              |
| SOX9 (P48436)   | Homo sapiens |      509 |        55.97 |          50.22 |                  0.11 |                0.05 |                 0.84 |      27.36 |                          0    |                           1 |                      0.49 |                  2 | [0.626, -0.097, -0.774]   |                16.63 |                 20.67 |              0.3406 |            1.2878 |               2.19 | 134:0.38; 147:0.38; 116:0.37    |                    0.92 |                  0.52 | True                     | False                    | True               |
| SHH (Q15465)    | Homo sapiens |      462 |        78.38 |          89.47 |                  0.47 |                0.27 |                 0.26 |      17.86 |                          6.13 |                           5 |                      0.16 |                  6 | [-0.774, -0.382, 0.505]   |                24.5  |                 31.2  |              0.3029 |            1.8096 |               2.12 | 48:0.40; 259:0.39; 174:0.39     |                    0.44 |                  0.33 | False                    | True                     | False              |
| WNT5A (O00462)  | Homo sapiens |      879 |        95.81 |          98.25 |                  0.95 |                0.02 |                 0.02 |       4.92 |                          1.5  |                           2 |                      0.02 |                  0 | [-0.666, -0.006, 0.746]   |                28.62 |                 64.39 |              0.2957 |            1.8176 |               1.81 | 44:0.42; 164:0.41; 506:0.39     |                    0.24 |                  0.33 | False                    | False                    | False              |

<details>
<summary>CSV Data Block</summary>

```csv
protein_id,species,length,pLDDT_mean,pLDDT_median,pLDDT_fraction_high,pLDDT_fraction_ok,pLDDT_fraction_low,PAE_mean,PAE_domain_blockiness_score,predicted_domain_segments,disorder_fraction_proxy,hinge_candidates,backbone_principal_axis,radius_of_gyration,end_to_end_distance,curvature_summary,torsion_summary,anisotropy_index,bending_hotspots,exposed_surface_proxy,charged_patch_score,low_confidence_warning,multi_domain_uncertain,likely_IDR_heavy
COL2A1 (P02458),Homo sapiens,1487,52.12,44.12,0.13,0.06,0.81,27.44,5.90,3,0.69,16,"[-0.434, -0.065, 0.899]",24.97,45.38,0.2938,1.8702,2.65,1327:0.42; 1454:0.39; 1282:0.38,0.87,0.28,True,True,True
FN1 (P02751),Homo sapiens,2477,69.65,75.38,0.05,0.56,0.39,27.08,7.04,49,0.16,216,"[-0.808, 0.027, 0.589]",55.09,66.77,0.2582,2.2568,2.44,1768:0.41; 2039:0.38; 959:0.38,0.36,0.32,True,True,False
ACTB (P60709),Homo sapiens,375,95.20,97.44,0.93,0.05,0.03,5.03,1.26,2,0.01,1,"[0.835, 0.517, -0.187]",21.09,42.74,0.3178,1.5512,2.19,335:0.39; 265:0.39; 258:0.38,0.30,0.34,False,False,False
ITGB1 (P05556),Homo sapiens,798,85.87,89.84,0.49,0.40,0.11,18.24,4.90,10,0.03,10,"[-0.504, -0.483, 0.716]",45.83,94.88,0.3054,1.7251,3.23,193:0.39; 474:0.38; 521:0.38,0.34,0.35,False,True,False
IFT88 (Q13099),Homo sapiens,824,76.35,89.28,0.47,0.25,0.29,19.42,2.43,3,0.23,1,"[-0.626, -0.157, 0.764]",38.29,92.39,0.3577,1.1214,2.80,315:0.38; 643:0.38; 426:0.38,0.51,0.44,False,True,False
SOX9 (P48436),Homo sapiens,509,55.97,50.22,0.11,0.05,0.84,27.36,0.00,1,0.49,2,"[0.626, -0.097, -0.774]",16.63,20.67,0.3406,1.2878,2.19,134:0.38; 147:0.38; 116:0.37,0.92,0.52,True,False,True
SHH (Q15465),Homo sapiens,462,78.38,89.47,0.47,0.27,0.26,17.86,6.13,5,0.16,6,"[-0.774, -0.382, 0.505]",24.50,31.20,0.3029,1.8096,2.12,48:0.40; 259:0.39; 174:0.39,0.44,0.33,False,True,False
WNT5A (O00462),Homo sapiens,879,95.81,98.25,0.95,0.02,0.02,4.92,1.50,2,0.02,0,"[-0.666, -0.006, 0.746]",28.62,64.39,0.2957,1.8176,1.81,44:0.42; 164:0.41; 506:0.39,0.24,0.33,False,False,False
```
</details>

## B) Key Plots Summary

Generated output files under `outputs/bolt_biofold_cycle/figures/`:

* Generated `*_plddt.png` for all proteins showing confidence vs threshold (70).
* Generated `*_pae.png` for key proteins (e.g. FN1, ITGB1) mapping domain interactions.
* Generated `*_curvature.png` for proteins showing backbone curvature for high-confidence regions.

## C) Interpretation

* **COL2A1 (P02458)**
  * **What we see:** Intermediate geometry, 16 hinge candidate(s) (Confidence: Low)
  * **Why it matters:** ECM structural component; crucial for maintaining mechanical stiffness and counteracting load during spine morphogenesis.
  * **Next test:** Check if COL2A1 hinges overlap with known clinically significant missense mutations in scoliosis patients.

* **FN1 (P02751)**
  * **What we see:** Intermediate geometry, 216 hinge candidate(s) (Confidence: Low)
  * **Why it matters:** ECM structural component; crucial for maintaining mechanical stiffness and counteracting load during spine morphogenesis.
  * **Next test:** Check if FN1 hinges overlap with known clinically significant missense mutations in scoliosis patients.

* **ACTB (P60709)**
  * **What we see:** Intermediate geometry, 1 hinge candidate(s) (Confidence: High)
  * **Why it matters:** Cytoskeleton/Adhesion; essential for translating ECM strains into intracellular mechanotransduction signals.
  * **Next test:** Check if ACTB hinges overlap with known clinically significant missense mutations in scoliosis patients.

* **ITGB1 (P05556)**
  * **What we see:** Highly elongated, 10 hinge candidate(s) (Confidence: Medium)
  * **Why it matters:** Cytoskeleton/Adhesion; essential for translating ECM strains into intracellular mechanotransduction signals.
  * **Next test:** Check if ITGB1 hinges overlap with known clinically significant missense mutations in scoliosis patients.

* **IFT88 (Q13099)**
  * **What we see:** Intermediate geometry, 1 hinge candidate(s) (Confidence: Medium)
  * **Why it matters:** Cilia component; likely acts as a flow/strain sensor during early symmetry breaking and development.
  * **Next test:** Check if IFT88 hinges overlap with known clinically significant missense mutations in scoliosis patients.

* **SOX9 (P48436)**
  * **What we see:** Intermediate geometry, 2 hinge candidate(s) (Confidence: Low)
  * **Why it matters:** Morphogen/Growth factor; signaling spatial orientation during cartilage formation.
  * **Next test:** Check if SOX9 hinges overlap with known clinically significant missense mutations in scoliosis patients.

* **SHH (Q15465)**
  * **What we see:** Intermediate geometry, 6 hinge candidate(s) (Confidence: Medium)
  * **Why it matters:** Morphogen/Growth factor; signaling spatial orientation during cartilage formation.
  * **Next test:** Check if SHH hinges overlap with known clinically significant missense mutations in scoliosis patients.

* **WNT5A (O00462)**
  * **What we see:** Intermediate geometry (Confidence: High)
  * **Why it matters:** Morphogen/Growth factor; signaling spatial orientation during cartilage formation.
  * **Next test:** Compare WNT5A geometry with orthologs to confirm evolutionary conservation of its structural mechanics.

## D) Best Next Move

**Prioritize highly structured, anisotropic proteins (like ITGB1 and ACTB) and cross-reference their high-confidence bending hotspots against GWAS scoliosis datasets to see if mechanical variants drive pathogenesis.**

---

## Quality & Reproducibility Checklist

* **Data source:** AlphaFold DB (fetched dynamically)
* **Date/time of run:** 2026-03-11 19:39:48
* **Code version:** scripts/run_bolt_analysis_cycle.py
* **Parameters:** pLDDT >= 70 threshold for structure/geometry computation.
* **Notes:** SASA not explicitly computed to adhere strictly to zero-new-dependencies rule; used coordinate-based neighborhood proxy instead.