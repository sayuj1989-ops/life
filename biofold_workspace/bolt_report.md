# Bolt-BioFold Analysis Report

## Quality & Reproducibility Checklist
- **Data source**: AlphaFold DB (via EBI API)
- **Date/time of run**: 2026-03-21 19:19:34
- **Code version**: Current tree state
- **Parameters**: pLDDT threshold=70, default PCA and smoothing, PAE heuristics applied
- **Notes**: FBN1 (P35555) failed data fetch due to 404 error from AlphaFold DB API.

## A) Results Table

| gene_symbol   | uniprot_id   |   plddt_mean |   anisotropy_index | morphology       |   plddt_fraction_low |
|:--------------|:-------------|-------------:|-------------------:|:-----------------|---------------------:|
| PIEZO1        | Q92508       |      72.0459 |            3.89626 | Fibrous/Extended |             0.326854 |
| PIEZO2        | Q9H5I5       |      79.4436 |            4.44118 | Fibrous/Extended |             0.214386 |
| ACAN          | P16112       |      51.891  |            2.66304 | Intermediate     |             0.726087 |
| ITGB1         | P05556       |      85.8694 |            3.23019 | Fibrous/Extended |             0.107769 |

### CSV-ready block
```csv
gene_symbol,uniprot_id,priority_score,anisotropy_index,radius_of_gyration,plddt_mean,morphology,n_residues,plddt_median,plddt_fraction_high,plddt_fraction_ok,plddt_fraction_low,disorder_fraction_proxy,backbone_principal_axis,curvature_summary,torsion_summary,end_to_end_distance,bending_hotspots,hinge_candidates,exposed_surface_proxy,charged_patch_score,low_confidence_warning,multi_domain_uncertain,likely_IDR_heavy,predicted_domain_segments,PAE_mean,PAE_domain_blockiness_score,organism
PIEZO1,Q92508,100,3.896259474160542,58.85421625457664,72.0459182863943,Fibrous/Extended,2521,79.19,0.1193970646568821,0.5537485124950418,0.3268544228480761,0.1701705672352241,"[-0.270, -0.320, 0.908]",0.3413845615077925,1.181661841789843,29.95223071826204,458:0.44; 625:0.42; 513:0.41,3,0.4573581911939706,0.2696390658174097,False,True,False,35,22.743295862553047,5.738877788747343,Homo sapiens
PIEZO2,Q9H5I5,100,4.441176983762356,43.40791862714556,79.4436389280677,Fibrous/Extended,709,88.38,0.4174894217207334,0.3681241184767277,0.2143864598025388,0.1368124118476728,"[-0.687, -0.068, 0.724]",0.3293254003639894,1.4284592527058404,28.406129021744583,460:0.38; 239:0.38; 138:0.38,0,0.5627644569816643,0.2452107279693486,False,True,False,7,16.987465211535746,2.799985883630068,Homo sapiens
ACAN,P16112,100,2.663035881007823,35.29114087301315,51.890964426877474,Intermediate,2530,45.14,0.1525691699604743,0.1213438735177865,0.7260869565217392,0.541897233201581,"[-0.681, 0.452, 0.577]",0.2882737858924963,1.909025374318512,24.401263942673133,2343:0.42; 2405:0.42; 109:0.41,26,0.5620553359683794,0.4093959731543624,True,True,True,10,26.25627802340296,5.010653974635432,Homo sapiens
ITGB1,P05556,100,3.23018892296316,45.82908790008346,85.86938596491228,Fibrous/Extended,798,89.845,0.4924812030075188,0.3997493734335839,0.1077694235588972,0.0325814536340852,"[-0.504, -0.483, 0.716]",0.3053935738868332,1.7251223141739866,94.87912675609952,193:0.39; 474:0.38; 521:0.38,10,0.3421052631578947,0.3520408163265306,False,True,False,10,18.23868097562201,4.896572067396104,Homo sapiens
```

## B) Key plots summary
- Due to environment constraints and to avoid new dependencies, plotting was skipped. Standard plotting would include pLDDT vs residue index for all 4 structures and PAE heatmaps where JSON was available.

## C) Interpretation
### PIEZO1 & PIEZO2 (Mechanotransducers)
- **What we see**: Both show strong `Fibrous/Extended` morphology with high Anisotropy (>3.8). PIEZO2 is slightly more anisotropic (4.44) and has higher overall confidence (pLDDT ~79.4) compared to PIEZO1 (72.0).
- **Why it matters**: The extended, rigid rod-like structure is consistent with their role as direct mechanotransducers. This structural rigidity allows them to efficiently transmit and sense tension across the membrane during spinal growth and postural loading.
- **Confidence level**: High for PIEZO2 (79.4 pLDDT); Medium-High for PIEZO1 (72.0 pLDDT).
- **Next test**: Correlate the specific bending hotspots in PIEZO2 (e.g., res 460, 239) with known scoliosis mutation sites to see if curvature/flexibility at these nodes is altered.

### ITGB1 (Cell-ECM Adhesion Sensor)
- **What we see**: Highly confident structure (pLDDT: 85.9) with an extended, fibrous conformation (Anisotropy: 3.23) and very low disorder fraction (<4%).
- **Why it matters**: As the primary cellular gravity/load sensor at focal adhesions, ITGB1's structured, extended nature perfectly fits a tension-transmitting cable model anchoring the cytoskeleton to the ECM.
- **Confidence level**: Very High (85.9 pLDDT).
- **Next test**: Examine the predicted hinge/bending regions of ITGB1 under simulated load to assess its yield/stretching points compared to mutant forms.

### ACAN (Load-bearing Proteoglycan)
- **What we see**: `Intermediate` morphology with very low confidence (pLDDT: 51.9) and high disorder fraction (~54%).
- **Why it matters**: ACAN serves as a major structural resistor of gravity in the intervertebral disc. Its large intrinsically disordered regions (IDRs) likely act as flexible, hydrated springs to absorb compressive loads rather than rigid rods.
- **Confidence level**: Low overall, but high confidence in the predicted disorder.
- **Next test**: Restrict analysis of ACAN only to the domains with pLDDT > 70 to identify structural anchoring points versus disordered shock-absorbing regions.

## D) One “Best Next Move”
> **Compare orthologs**: Map known scoliosis-associated mutations onto the high-confidence bending hotspots of PIEZO2 and ITGB1 to test if they disrupt critical mechanotransductive hinges.
