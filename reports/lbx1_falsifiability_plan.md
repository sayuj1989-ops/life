# LBX1 Falsifiability Plan

## Overview
A critical vulnerability in the Biological Counter-Curvature hypothesis is treating LBX1—a transcription factor with a statically low-confidence (pLDDT < 70) and intermediate-anisotropy (~2.27) structural model—as an active geometric sensor purely based on in silico blockiness scores. To strengthen the evidence base, this plan establishes rigorous falsifiability criteria that would disprove or significantly weaken the assertion that LBX1's intrinsic structural geometry acts as a mechanical sensor.

The experiments below are designed to separate direct measurement from narrative inflation, providing concrete quantitative thresholds that would falsify the LBX1-mechanics link.

---

## Experiment 1: In Vitro Mechanical Perturbation (Nuclear Tension Modality)

**Hypothesis:** If LBX1's modular blockiness functions mechanically, increasing nuclear membrane tension (e.g., via LINC complex modulation or substrate stiffness) will directly alter its DNA-binding affinity, nuclear localization, or inter-domain distances, independently of post-translational cascades.

**Assay Design:**
- Culture osteoblast/somite-derived cells on polyacrylamide gels of varying physiological stiffness (e.g., 2 kPa vs 50 kPa).
- Perform FRAP (Fluorescence Recovery After Photobleaching) on GFP-tagged LBX1 to measure nuclear mobility.
- Perform FRET (Förster Resonance Energy Transfer) across LBX1's putative "blocky" domains to measure tension-induced conformational changes in live cells under cyclic stretch.

**Quantitative Readout:**
- Change in FRET efficiency ($\Delta E$) between the N-terminal and C-terminal domains under 10% cyclic stretch vs static conditions.
- Change in nuclear immobile fraction (from FRAP) across stiffness gradients.

**Expected Direction (if hypothesis is true):**
- FRET efficiency decreases under cyclic stretch, indicating domain separation or "unblocking".
- Nuclear mobility (immobile fraction) scales directly with substrate stiffness.

**Falsification Threshold:**
- If the change in FRET efficiency is $< 5\%$ under maximum physiological stretch, OR if the immobile fraction variance across 2 kPa vs 50 kPa substrates is statistically insignificant ($p > 0.05$), the hypothesis that LBX1 is structurally mechanosensitive is *falsified*. Its role is likely purely downstream/biochemical.

---

## Experiment 2: Truncation/Hinge-Deletion Mutagenesis

**Hypothesis:** If the specific high-PAE-blockiness architecture of LBX1 is required for mechanosensory function, then deleting the flexible "hinge" regions between its blocks will abolish its tension-dependent activity without destroying baseline biochemical function.

**Assay Design:**
- Synthesize an `LBX1-ΔHinge` mutant where the predicted unstructured regions separating its structural domains are replaced by a rigid alpha-helical linker (e.g., EAAAK repeats).
- Measure baseline transcription activity (using a luciferase reporter for a known downstream target) to confirm the mutant is biochemically competent.
- Compare wild-type vs `LBX1-ΔHinge` transcriptional output under low vs high fluid shear stress (FSS).

**Quantitative Readout:**
- Ratio of transcriptional output (Luciferase fold-change) under High FSS vs Static conditions for WT compared to `LBX1-ΔHinge`.

**Expected Direction (if hypothesis is true):**
- WT LBX1 shows a $> 2.0$ fold-change under FSS.
- `LBX1-ΔHinge` shows a basal transcription rate equivalent to WT but loses the FSS-dependent fold-change enhancement.

**Falsification Threshold:**
- If the `LBX1-ΔHinge` mutant retains the identical FSS-dependent fold-change as WT (difference $< 10\%$), the hypothesis that the specific blocky/hinged architecture is the mechanical sensor is *falsified*. The mechanical signal is coming from upstream effectors, not LBX1 geometry.

---

## Experiment 3: AlphaFold vs Ensemble Solution Scattering (SAXS)

**Hypothesis:** If LBX1's intermediate anisotropy (2.27) and high blockiness represent a stable physiological conformation rather than an AlphaFold predictive artifact of intrinsically disordered regions (IDRs), then experimental solution structure will match the AF model.

**Assay Design:**
- Purify full-length recombinant human LBX1 protein.
- Perform Small-Angle X-ray Scattering (SAXS) in solution to determine the experimental Radius of Gyration ($R_g$), maximum particle dimension ($D_{max}$), and Kratky plot profile.
- Compare the experimental SAXS envelope to the theoretical scattering profile of the AlphaFold 2026-02-16 model using CRYSOL.

**Quantitative Readout:**
- Chi-square ($\chi^2$) fit between the AF predicted scattering curve and the experimental SAXS curve.
- Experimental $R_g$ versus AF predicted $R_g$.

**Expected Direction (if hypothesis is true):**
- SAXS envelope reflects a multi-domain modular structure with intermediate elongation.
- Kratky plot shows distinct peaks indicating folded domains rather than a continuous monotonic plateau typical of random coils.

**Falsification Threshold:**
- If the Kratky plot demonstrates a classic random-coil/highly disordered profile, OR if the experimental $D_{max}$ deviates by $> 30\%$ from the AF model prediction ($\chi^2 > 5.0$), the hypothesis that LBX1 has a structurally deterministic "blocky" geometry is *falsified*. The AFCC metrics for LBX1 are artifacts of IDR misprediction.
