# Bolt-BioFold ⚡ Analysis Report

**Quality & Reproducibility Checklist:**
- **Data Source:** AlphaFold DB (v6 endpoint)
- **Date/time of run:** `$(date -u)`
- **Code Version / Parameters:** pLDDT ≥ 70 for geometry computations; PCA for principal axis/anisotropy; curvature approximation via vector derivatives.
- **Notes:** MESP2 was skipped due to HTTP 404 on the AlphaFold DB for the queried identifer. Seed list defaults (LBX1, POC5, ADGRG6) used as no custom protein IDs were provided. PAE matrices were downloaded but due to IDR dominance and length limits in two out of three proteins, the metrics rely strictly on 3D geometry from high-confidence coordinates.

## A) Results Table

| protein | uniprot | length | pLDDT_mean | pLDDT_median | pLDDT_frac_high | pLDDT_frac_ok | pLDDT_frac_low | Rg | end_to_end | anisotropy_index | curvature_mean | low_confidence | IDR_heavy |
|---------|---------|--------|------------|--------------|-----------------|---------------|----------------|----|------------|------------------|----------------|----------------|-----------|
| LBX1 | P52954 | 281 | 66.87 | 60.25 | 0.23 | 0.16 | 0.61 | 22.69 | 54.39 | 2.71 | 0.33 | True | False |
| POC5 | Q8NA72 | 575 | 63.97 | 50.91 | 0.33 | 0.06 | 0.61 | 87.28 | 39.39 | 102.15 | 0.36 | True | True |
| ADGRG6 | Q86SQ4 | 1221 | 73.73 | 81.00 | 0.16 | 0.54 | 0.30 | 51.33 | 94.46 | 4.30 | 0.30 | False | False |

**CSV-ready Block:**
```csv
protein,uniprot,length,pLDDT_mean,pLDDT_median,pLDDT_fraction_high,pLDDT_fraction_ok,pLDDT_fraction_low,Rg,end_to_end,anisotropy_index,curvature_mean,low_confidence_warning,likely_IDR_heavy
LBX1,P52954,281,66.86779359430605,60.25,0.2313167259786477,0.15658362989323843,0.6120996441281139,22.694646921843987,54.39289469222979,2.7115218109036294,0.32743200035154035,True,False
POC5,Q8NA72,575,63.974834782608696,50.91,0.33217391304347826,0.06086956521739131,0.6069565217391304,87.28345622547697,39.38945682539936,102.15388336220066,0.35989167252270965,True,True
ADGRG6,Q86SQ4,1221,73.72809172809173,81.0,0.1638001638001638,0.5356265356265356,0.30057330057330056,51.329351327023446,94.45647863963593,4.296379746708081,0.29977804065392494,False,False
```

## B) Key Plots Summary

* **pLDDT vs Residue Index Plot (`plddt_vs_residue.png`) generated:** Plots the per-residue confidence scores for LBX1, POC5, and ADGRG6 overlaid with a threshold line at pLDDT = 70.
  * LBX1 and POC5 show long unstructured stretches with narrow, high-confidence domain peaks.
  * ADGRG6 maintains >70 confidence across much of its large multi-domain architecture.

## C) Interpretation

* **LBX1 (P52954):**
  * *What we see:* Highly disordered overall (61% low confidence) with a compact, structured homeobox domain (Rg=22.6, anisotropy=2.7).
  * *Why it matters:* As a top GWAS hit for AIS, its function relies on this rigid, compact DNA-binding module directing somite/proprioceptor migration, while the IDRs likely facilitate flexible protein-protein interactions.
  * *Confidence:* Low globally, but High for the geometric domain core.
  * *Next test:* Map known AIS missense mutations to the high-confidence domain to see if they disrupt the local binding geometry.

* **POC5 (Q8NA72):**
  * *What we see:* Severe global disorder (61% low confidence, labeled IDR-heavy) but the structured core is extremely elongated/anisotropic (anisotropy index ~102) with a large Rg (~87).
  * *Why it matters:* This massive anisotropy indicates a rod-like structural role, perfectly suited for the ciliary scaffold where POC5 is known to operate. Cilia are the primary load/flow sensors in mechanotransduction, which aligns mechanically with the biological countercurvature hypothesis.
  * *Confidence:* Low globally, High for the anisotropic rod segment.
  * *Next test:* Compare the Rg and anisotropy of POC5 orthologs in species that do not experience axial gravity loads.

* **ADGRG6 / GPR126 (Q86SQ4):**
  * *What we see:* Mostly well-structured (mean pLDDT > 73) large receptor (1221 residues). Structurally it's mildly anisotropic (anisotropy ~4.3) with a massive end-to-end distance (~94.5), reflecting its long multi-domain architecture (e.g. extracellular stalk).
  * *Why it matters:* As an essential GPCR for myelination and mechanotransduction, this rigid, extended topology would theoretically allow it to act as a tension-sensing "spring" in the ECM, translating mechanical stretching into a proprioceptive delay signal ($\tau_{\text{afferent}}$).
  * *Confidence:* Medium-High.
  * *Next test:* Calculate the sequence of hinge regions (low pLDDT boundaries between high pLDDT domains) and run a targeted simulation testing the physical compliance of this extended extracellular structure under tension.

## D) Best Next Move

* **Correlate curvature metrics with known phenotype genes:** Expand this geometric analysis pipeline (particularly the extreme anisotropy index found in POC5) against the entire pool of 30 top candidate genes in `data/candidates_master.csv` to see if high anisotropy + high IDR fraction uniquely fingerprints ciliary/mechanotransduction scoliosis targets.
