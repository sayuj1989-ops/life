# Claude Managed Cloud Agent — WP4 Independent Reconfirmation Prompt

**Purpose:** Paste this prompt into Claude's Managed Cloud Agent to independently reconfirm the WP4 AlphaFold Anisotropy Gap findings. The agent should re-derive everything from scratch using only the AlphaFold API and basic statistical tools — no pre-computed results.

---

## ROLE

You are a statistical bioinformatician tasked with an independent replication of a structural biology claim. You must reproduce the analysis from scratch, report any discrepancies, and provide an honest verdict.

## CLAIM TO RECONFIRM

The following claim was made in a manuscript on the "Allometric Trap" theory of Adolescent Idiopathic Scoliosis:

> **Demand-side mechanosensory proteins exhibit significantly higher AlphaFold-derived structural anisotropy than Supply-side metabolic regulators.** 
> (Mann-Whitney U, one-sided p = 0.002; Cohen's d = 1.11; Cliff's δ = 0.62; n = 31 proteins; gap = 70.4%; survives Bonferroni correction for 3 tests at α = 0.0167)

---

## TASK: Reproduce from scratch

### Step 1: Fetch all 31 protein structures from AlphaFold

For each protein below, download the PDB from `https://alphafold.ebi.ac.uk/api/prediction/{UniProt_ID}`, extract Cα coordinates and pLDDT (B-factor column), then compute:

- **Structural anisotropy** = √(λ₁/λ₃) from the gyration tensor eigenvalues (λ₁ ≥ λ₂ ≥ λ₃)
- **Disorder fraction** = fraction of residues with pLDDT < 50
- **Sequence length** (number of Cα atoms)

**Demand proteins (n=19):**

| Gene | UniProt | Subcategory |
|------|---------|-------------|
| PIEZO2 | Q9H5I5 | Proprioceptive |
| LBX1 | P52951 | Proprioceptive |
| DSTYK | Q6XUX3 | Proprioceptive |
| EGR3 | Q06889 | Proprioceptive |
| RUNX3 | Q13761 | Proprioceptive |
| ASIC3 | Q9UHC3 | Proprioceptive |
| KCNK2 | O95069 | Proprioceptive |
| TMC1 | Q8TDI8 | Proprioceptive |
| PAX1 | P15858 | Proprioceptive |
| VIM | P08670 | Cytoskeletal |
| LMNA | P02545 | Cytoskeletal |
| CAV1 | Q03135 | Cytoskeletal |
| PIEZO1 | Q92508 | Cytoskeletal |
| ADGRG6 | Q86SQ4 | Cytoskeletal |
| FBN2 | P35556 | Cytoskeletal |
| PTK7 | Q13308 | Cytoskeletal |
| TRPV4 | Q9HBA0 | Cytoskeletal |
| DPYSL4 | O14531 | Cytoskeletal |
| SCUBE3 | Q8IX30 | Cytoskeletal |

**Supply proteins (n=12):**

| Gene | UniProt | Subcategory |
|------|---------|-------------|
| GHR | P10912 | Metabolic |
| IGF1R | P08069 | Metabolic |
| PPARGC1A | Q9UBK2 | Metabolic |
| ARNTL | O00327 | Metabolic |
| SIRT1 | Q96EB6 | Metabolic |
| SOX9 | P48436 | Metabolic |
| SHH | Q15465 | Metabolic |
| CDKN1A | P38936 | Metabolic |
| COMP | P49747 | Metabolic |
| COL1A1 | P02452 | Metabolic |
| PLOD1 | Q02809 | Metabolic |
| BNC2 | Q6ZN30 | Metabolic |

Note: HSPG2 (P98160) was in the original panel but too large for the API. If it returns nothing, document this and proceed with n=31.

### Step 2: Compute the gyration tensor anisotropy

For each protein PDB:

```python
import numpy as np

# Parse Cα coordinates from PDB ATOM lines where atom name == "CA"
# Compute gyration tensor: G_jk = (1/N) Σ (r_i - r_mean)_j (r_i - r_mean)_k
# Get eigenvalues λ₁ ≥ λ₂ ≥ λ₃
# Anisotropy = sqrt(λ₁ / λ₃)
```

### Step 3: Run three statistical tests

1. **Mann-Whitney U test** (one-sided, alternative="greater"): Demand anisotropy > Supply anisotropy
2. **Mann-Whitney U test** (one-sided, alternative="less"): Demand disorder < Supply disorder  
3. **Fisher's exact test** (two-sided): AIS GWAS genes × high-anisotropy (above median)
   - GWAS genes: PAX1, LBX1, ADGRG6, BNC2, SCUBE3, FBN2, SOX9, SHH

For each test, report:
- Test statistic, p-value
- Effect size (Cohen's d, Cliff's delta for MWU; odds ratio for Fisher)
- Whether it survives Bonferroni correction (α = 0.05/3 = 0.0167)

### Step 4: Report

Produce a markdown table with columns: `Gene | Category | UniProt | SeqLen | pLDDT | Anisotropy | Disorder%`

Then report:
1. Do your anisotropy values match the original within ±5%? List any discrepancies > 5%.
2. Does the Mann-Whitney U test for anisotropy remain significant at p < 0.05? At p < 0.0167 (Bonferroni)?
3. Is the effect size still "large" (Cohen's d > 0.8)?
4. What is the gap percentage?
5. **Verdict:** CONFIRMED / PARTIALLY CONFIRMED / REFUTED

---

## OPERATING RULES

1. Do NOT use any pre-existing results from the repository. Fetch everything fresh from the AlphaFold API.
2. Show all code. Every calculation must be reproducible.
3. If any protein fails to download, document it and adjust n accordingly.
4. If your results differ from the claimed values, investigate why (e.g., different AlphaFold version, different fragment) and report the discrepancy explicitly.
5. Be honest. If the result does not replicate, say so.

---

**Begin by fetching all 31 protein structures. Report progress as you go.**
