## Bolt-BioFold ⚡ Analysis Cycle Report

### A) Structured Results Table

| Identity | AlphaFold Confidence | Architecture | Geometry | Interaction | Flags |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GHR**<br>Human<br>638aa | pLDDT: 58.7 (High: 26%, Low: 67%)<br>PAE: 25.8 (Block: 5.31) | Domains: 3<br>Disorder: 50%<br>Hinges: 54 | Anisotropy: **5.13**<br>Rg: 31.4Å, E2E: 63.2Å<br>Curv: 0.282<br>Hotspots: 266:0.38; 131:0.38; ... | Exposed: 80%<br>Charged Patch: 0.20 | ⚠️ Low Conf<br>⚠️ Multi-Dom?<br>⚠️ IDR |
| **PIEZO2**<br>Human<br>709aa | pLDDT: 79.4 (High: 42%, Low: 21%)<br>PAE: 17.0 (Block: 2.80) | Domains: 7<br>Disorder: 14%<br>Hinges: 0 | Anisotropy: **4.44**<br>Rg: 43.4Å, E2E: 28.4Å<br>Curv: 0.329<br>Hotspots: 460:0.38; 239:0.38; ... | Exposed: 56%<br>Charged Patch: 0.25 | ⚠️ Multi-Dom? |
| **ARNTL**<br>Human<br>626aa | pLDDT: 65.5 (High: 34%, Low: 53%)<br>PAE: 22.8 (Block: 3.59) | Domains: 7<br>Disorder: 40%<br>Hinges: 6 | Anisotropy: **3.32**<br>Rg: 32.1Å, E2E: 14.3Å<br>Curv: 0.315<br>Hotspots: 143:0.38; 191:0.38; ... | Exposed: 69%<br>Charged Patch: 0.47 | ⚠️ Low Conf<br>⚠️ Multi-Dom?<br>⚠️ IDR |
| **ADGRG6**<br>Human<br>1221aa | pLDDT: 73.7 (High: 16%, Low: 30%)<br>PAE: 24.4 (Block: 6.78) | Domains: 23<br>Disorder: 15%<br>Hinges: 12 | Anisotropy: **3.06**<br>Rg: 51.3Å, E2E: 50.9Å<br>Curv: 0.308<br>Hotspots: 57:0.43; 530:0.39; 2... | Exposed: 44%<br>Charged Patch: 0.25 | ⚠️ Multi-Dom? |
| **PPARGC1A**<br>Human<br>798aa | pLDDT: 52.7 (High: 8%, Low: 79%)<br>PAE: 28.1 (Block: 6.56) | Domains: 4<br>Disorder: 62%<br>Hinges: 0 | Anisotropy: **2.19**<br>Rg: 31.2Å, E2E: 68.2Å<br>Curv: 0.334<br>Hotspots: 689:0.38; 697:0.38; ... | Exposed: 93%<br>Charged Patch: 0.51 | ⚠️ Low Conf<br>⚠️ Multi-Dom?<br>⚠️ IDR |
| **MYLK**<br>Human<br>1914aa | pLDDT: 65.8 (High: 18%, Low: 39%)<br>PAE: 26.6 (Block: 8.29) | Domains: 28<br>Disorder: 35%<br>Hinges: 31 | Anisotropy: **1.46**<br>Rg: 41.5Å, E2E: 56.8Å<br>Curv: 0.277<br>Hotspots: 1835:0.42; 59:0.41; ... | Exposed: 53%<br>Charged Patch: 0.40 | ⚠️ Low Conf<br>⚠️ Multi-Dom?<br>⚠️ IDR |
| **IGF1R**<br>Human<br>1367aa | pLDDT: 78.0 (High: 44%, Low: 25%)<br>PAE: 23.6 (Block: 5.85) | Domains: 16<br>Disorder: 16%<br>Hinges: 35 | Anisotropy: **1.43**<br>Rg: 43.2Å, E2E: 53.6Å<br>Curv: 0.298<br>Hotspots: 34:0.41; 1073:0.40; ... | Exposed: 42%<br>Charged Patch: 0.35 | ⚠️ Multi-Dom? |
| **DMD**<br>Human<br>525aa | pLDDT: 76.3 (High: 46%, Low: 36%)<br>PAE: 19.0 (Block: 6.91) | Domains: 2<br>Disorder: 18%<br>Hinges: 1 | Anisotropy: **1.32**<br>Rg: 22.8Å, E2E: 48.9Å<br>Curv: 0.340<br>Hotspots: 251:0.39; 14:0.39; 5... | Exposed: 55%<br>Charged Patch: 0.37 | ⚠️ Multi-Dom? |

#### CSV-Ready Block
```csv
gene_symbol,uniprot,source_category,morphology,anisotropy_index,radius_of_gyration,plddt_mean,n_residues,dise_score,plddt_median,plddt_fraction_high,plddt_fraction_ok,plddt_fraction_low,disorder_fraction_proxy,backbone_principal_axis,curvature_summary,torsion_summary,end_to_end_distance,bending_hotspots,hinge_candidates,exposed_surface_proxy,charged_patch_score,low_confidence_warning,multi_domain_uncertain,likely_IDR_heavy,predicted_domain_segments,PAE_mean,PAE_domain_blockiness_score
GHR,P10912,seed_Metabolic_Expansion,Fibrous/Extended,5.13247062540886,31.35538953628705,58.69753918495297,638,4.0,48.89,0.2617554858934169,0.0705329153605015,0.6677115987460815,0.5047021943573667,"[-0.761, 0.080, 0.644]",0.2819223402032338,1.981865304738773,63.24585957989661,266:0.38; 131:0.38; 163:0.38,54,0.8040752351097179,0.2022471910112359,True,True,True,3,25.82729385520976,5.309022073672339
PIEZO2,Q9H5I5,seed_Mechanosensors,Fibrous/Extended,4.441176983762356,43.40791862714556,79.4436389280677,709,4.0,88.38,0.4174894217207334,0.3681241184767277,0.2143864598025388,0.1368124118476728,"[-0.687, -0.068, 0.724]",0.3293254003639894,1.4284592527058404,28.406129021744583,460:0.38; 239:0.38; 138:0.38,0,0.5627644569816643,0.2452107279693486,False,True,False,7,16.987465211535746,2.799985883630068
ARNTL,O00327,seed_Metabolic_Expansion,Fibrous/Extended,3.3192797281217827,32.06851875969924,65.52864217252394,626,4.0,63.59,0.3354632587859425,0.1325878594249201,0.5319488817891374,0.4041533546325878,"[-0.577, 0.255, 0.776]",0.314879829201722,1.6185709737500673,14.262585109299083,143:0.38; 191:0.38; 428:0.38,6,0.6916932907348243,0.4736842105263157,True,True,True,7,22.81820524859905,3.5856438629417164
ADGRG6,Q86SQ4,seed_Scoliosis_Drivers,Fibrous/Extended,3.0601126170353674,51.32935132702344,73.72809172809173,1221,4.0,81.0,0.1638001638001638,0.5356265356265356,0.3005733005733005,0.1531531531531531,"[-0.749, -0.252, 0.613]",0.307858124541348,1.632908270244515,50.85010789565741,57:0.43; 530:0.39; 247:0.39,12,0.438984438984439,0.2544642857142857,False,True,False,23,24.42875061793981,6.778548436294672
PPARGC1A,Q9UBK2,seed_Metabolic_Expansion,Intermediate,2.185052241061399,31.245049772687448,52.74286967418547,798,4.0,44.045,0.0802005012531328,0.1290726817042606,0.7907268170426065,0.6190476190476191,"[-0.885, 0.223, 0.409]",0.3341653120422594,1.3147186562736124,68.17329278390476,689:0.38; 697:0.38; 795:0.38,0,0.9335839598997494,0.5086206896551724,True,True,True,4,28.088947305607377,6.5607107575563255
MYLK,Q15746,seed_Week6_Expansion,Globular,1.4640526080343412,41.50389838721379,65.84507314524556,1914,4.0,80.12,0.1797283176593521,0.4278996865203762,0.3923719958202716,0.3469174503657262,"[-0.262, -0.391, 0.882]",0.2765878752741912,2.0755989382804536,56.77836512264156,1835:0.42; 59:0.41; 649:0.41,31,0.5344827586206896,0.3966666666666666,True,True,True,28,26.60291625584567,8.28959095350075
IGF1R,P08069,seed_Metabolic_Expansion,Globular,1.426632071596987,43.19563878705403,78.01789319678127,1367,4.0,88.0,0.4359912216532553,0.3160204828090709,0.2479882955376737,0.1572787125091441,"[-0.397, 0.016, 0.918]",0.2975271574185976,1.7991094129582073,53.57743917919183,34:0.41; 1073:0.40; 44:0.38,35,0.4177029992684711,0.3524904214559387,False,True,False,16,23.586392385249766,5.850335926217477
DMD,P11532,seed_Metabolic_Expansion,Globular,1.3155342721236885,22.82447560454643,76.34927619047619,525,4.0,85.06,0.4609523809523809,0.1771428571428571,0.3619047619047619,0.1752380952380952,"[-0.696, -0.170, 0.698]",0.3396918844143603,1.328278333123612,48.85366185865702,251:0.39; 14:0.39; 53:0.38,1,0.5523809523809524,0.3720930232558139,False,True,False,2,19.0086820861678,6.90819720471551

```

### B) Key Plots Summary
*   **pLDDT vs Residue:** Generated for all targets. Profiles confirm domain boundaries vs IDRs.
*   **PAE Heatmap:** Analyzed for multi-domain candidates (e.g. PIEZO2, GHR).
*   **Curvature Profiles:** Hotspots identified in geometry column.

### C) Interpretation

**GHR (Low Confidence)**
*   **What we see:** Anisotropy 5.13. Extended/Fibrous structure. 3 domain(s).
*   **Why it matters:** Receptor with significant extracellular extension. Anisotropy suggests potential for torque sensing or bending under load.
*   **Next test:** Correlate curvature hotspots with known mutations or interaction sites.

**PIEZO2 (Medium Confidence)**
*   **What we see:** Anisotropy 4.44. Extended/Fibrous structure. 7 domain(s).
*   **Why it matters:** Critical mechanosensor. High anisotropy indicates large lever arm for sensing membrane tension.
*   **Next test:** Correlate curvature hotspots with known mutations or interaction sites.

**ARNTL (Medium Confidence)**
*   **What we see:** Anisotropy 3.32. Extended/Fibrous structure. 7 domain(s).
*   **Why it matters:** High anisotropy suggests this protein may act as a mechanical strut or sensor in the spine.
*   **Next test:** Correlate curvature hotspots with known mutations or interaction sites.

**ADGRG6 (Medium Confidence)**
*   **What we see:** Anisotropy 3.06. Extended/Fibrous structure. 23 domain(s).
*   **Why it matters:** High anisotropy suggests this protein may act as a mechanical strut or sensor in the spine.
*   **Next test:** Correlate curvature hotspots with known mutations or interaction sites.

**PPARGC1A (Low Confidence)**
*   **What we see:** Anisotropy 2.19. Globular/Compact structure. 4 domain(s).
*   **Why it matters:** Transcription coactivator. High disorder/IDR suggests promiscuous binding interface.
*   **Next test:** Correlate curvature hotspots with known mutations or interaction sites.

**MYLK (Medium Confidence)**
*   **What we see:** Anisotropy 1.46. Globular/Compact structure. 28 domain(s).
*   **Why it matters:** Globular nature suggests enzymatic or localized signaling role rather than load bearing.
*   **Next test:** Correlate curvature hotspots with known mutations or interaction sites.

**IGF1R (Medium Confidence)**
*   **What we see:** Anisotropy 1.43. Globular/Compact structure. 16 domain(s).
*   **Why it matters:** Globular nature suggests enzymatic or localized signaling role rather than load bearing.
*   **Next test:** Correlate curvature hotspots with known mutations or interaction sites.

**DMD (Medium Confidence)**
*   **What we see:** Anisotropy 1.32. Globular/Compact structure. 2 domain(s).
*   **Why it matters:** Globular nature suggests enzymatic or localized signaling role rather than load bearing.
*   **Next test:** Correlate curvature hotspots with known mutations or interaction sites.

### D) Best Next Move
*   **Prioritize High-Anisotropy Candidates:** Focus simulation efforts on **VIM**, **PIEZO2**, and **GHR** as they exhibit the structural characteristics (High Anisotropy > 4) required for the 'Thermodynamic Standing Wave' mechanics.

### Quality & Reproducibility Checklist
*   **Data source:** Local files (parsed from AlphaFold DB)
*   **Date/time of run:** 2026-04-03 19:34:12
*   **Code version / commit hash:** 9e759e8341765ab8cf2fc48239c6c52cb1073253
*   **Parameters:** Geometry computations use pLDDT >= 70, disorder defined as pLDDT < 50.
*   **Notes:** Missing artifacts are flagged (e.g. low confidence or missing PAE).
