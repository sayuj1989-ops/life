# LBX1 Hypothesis Falsifiability Plan

**Generated:** 2026-02-26
**Target Hypothesis:** LBX1 acts as a "Condensate Sensor" of nuclear mechanical strain, where its Intrinsically Disordered Regions (IDRs) undergo phase separation in response to geometric deformation (buckling).

## 1. Core Falsification Logic
The "Stiff Caliper" hypothesis (LBX1 as a rigid rod) is **falsified by structural data** (Low Anisotropy, Low Confidence). The remaining viable hypothesis is the **Condensate Sensor**.
If LBX1 is a mechanosensor, its nuclear localization or transcriptional activity must be causally linked to physical forces, not just biochemical gradients.

## 2. Experiment A: The LINC Decoupling Test

**Hypothesis:** LBX1 sensing requires physical transmission of cytoskeletal strain to the nucleus via the LINC complex (Sun1/2, Nesprin).
**Assay:**
- **Model:** Human Paraxial Mesoderm (HPM) organoids or cyclic-stretched fibroblasts.
- **Perturbation:** siRNA knockdown of *SUN1* and *SUN2* (breaking the LINC bridge).
- **Stimulus:** Cyclic stretch (10%, 1Hz) or compressive loading.
- **Readout:** LBX1 nuclear intensity / Condensate number per nucleus.

**Falsification Criteria:**
- If *SUN1/2* knockdown **has no effect** on LBX1 nuclear accumulation under strain, the "Direct Mechanosensing" hypothesis is **FALSIFIED**.
- **Threshold:** < 20% reduction in nuclear LBX1 relative to control.

## 3. Experiment B: The IDR Deletion (Domain Analysis)

**Hypothesis:** The disordered N/C-terminal domains (IDRs) of LBX1 are necessary for phase separation and strain sensing.
**Assay:**
- **Constructs:** GFP-LBX1-WT vs GFP-LBX1-ΔIDR (structured Homeodomain only).
- **Stimulus:** Hyper-osmotic stress (mimicking crowding) or substrate stiffness gradient (2kPa vs 20kPa).
- **Readout:** Formation of puncta (condensates) and transcriptional output (target gene *GDF5*).

**Falsification Criteria:**
- If GFP-LBX1-ΔIDR (no IDR) **still forms condensates** or **responds to stiffness** identically to WT, the "Condensate Sensor" hypothesis is **FALSIFIED**.
- **Threshold:** Puncta count difference < 15% between WT and ΔIDR.

## 4. Experiment C: Chemical Condensate Dissolution

**Hypothesis:** LBX1 functional output depends on the physical integrity of liquid-liquid phase separated (LLPS) droplets.
**Assay:**
- **Treatment:** 1,6-Hexanediol (dissolves weak hydrophobic interactions in condensates) vs Digitonin control.
- **Timecourse:** 1 hour treatment during critical somite formation window in zebrafish or organoid.
- **Readout:** Spine curvature (Cobb angle equivalent) and LBX1 spatial distribution.

**Falsification Criteria:**
- If 1,6-Hexanediol dissolves LBX1 puncta but **does not induce scoliosis/defects** (or conversely, if scoliosis occurs without LBX1 disruption), the link between "LBX1 Condensates" and "Spine Straightening" is **WEAKENED/FALSIFIED**.
- **Threshold:** No significant correlation (R² < 0.3) between puncta loss and curvature phenotype.

## 5. Summary of Risks
| Experiment | Risk | Mitigation |
|---|---|---|
| A (LINC) | LINC KD is lethal/pleiotropic | Use inducible CRISPRi or dominant-negative KASH domain. |
| B (IDR) | ΔIDR protein is unstable | Check expression levels via Western Blot; use degron tag control. |
| C (Hexanediol) | Toxicity/Off-target effects | Use minimum effective dose; validate with optogenetic condensates (OptoDroplets). |

## 6. Decision Matrix
- **If A fails:** LBX1 is a biochemical responder, not a mechanical one. -> **Abandon Mechanical Hypothesis.**
- **If B fails:** The Homeodomain itself is the sensor (unlikely for stiffness). -> **Pivot to DNA-binding mechanics.**
- **If C fails:** Condensates are an artifact, not the function. -> **Focus on soluble fraction.**
