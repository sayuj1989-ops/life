# Next Step Evidence Summary

## Executive Summary
This audit and analysis cycle has clarified the structural basis of the Biological Countercurvature hypothesis. We have moved from broad "Tension Rod" classifications to a rigorous, confidence-weighted tier system.

## 1. What is Stronger Now
- **Confirmed Mechanosensors**: `PIEZO2` (Anisotropy 4.44, pLDDT 79.4), `LMNA` (Anisotropy 4.75, pLDDT 76.4), and `ADGRG6` (Anisotropy 3.06, pLDDT 73.7) are confirmed as high-confidence, high-anisotropy structures. Their geometric "rod-like" hypothesis is structurally sound.
- **New Candidates**: `CNNM2` (Anisotropy 8.54) and `FBLN5` (Anisotropy 7.05) emerged as overlooked strong candidates with high confidence.
- **Claims Discipline**: We established a "Claims Matrix" distinguishing verified structural features from speculative narrative.

## 2. What Remains Weak
- **LBX1 Structural Role**: LBX1 is **not** a tension rod (Anisotropy 2.27). It is an "Ambiguous Scaffold" with low confidence (pLDDT 66.9). Its metrics have been static across 21 runs, indicating no new structural insight has been generated recently.
- **Artifact Risk in Outliers**: `POC5` (Anisotropy 24.7) and `GHR` (Anisotropy 5.13) show extreme anisotropy but low confidence (<65 pLDDT), raising the risk that these are disordered regions (IDRs) misinterpreted as fibers.
- **Data Hygiene**: The audit revealed that 58/71 genes have identical metrics across all runs, and linked output artifacts (images) are missing from most run directories.

## 3. Top 3 Highest-Leverage Next Experiments

### 1. LBX1 "Blocky Scaffold" Validation (In Vivo)
**Goal**: Test if LBX1's specific modular geometry (blockiness) matters, or just its presence.
**Method**: Rescue *lbx1* null zebrafish with "Flex-Linker" vs "Rigid-Linker" variants.
**Success**: If geometry matters, variants should fail to rescue curvature.

### 2. POC5/GHR Biophysical Triage (In Vitro)
**Goal**: Resolve "Supported (Uncertain)" status. Are they fibers or disordered blobs?
**Method**: Recombinant protein expression + Atomic Force Microscopy (AFM) or TEM.
**Success**: Observation of actual filaments confirms "Tension Rod" status; amorphous aggregates refute it.

### 3. LBX1 Mechanocoupling Assay (Cellular)
**Goal**: Determine if LBX1 is a nuclear mechanosensor.
**Method**: Cyclic strain on chondrocytes with LINC complex (Sun/Kash) disruption.
**Success**: If LBX1 nuclear entry/activity is strain-dependent AND LINC-dependent, it is a mechanosensor.

## 4. Immediate Process Improvement
- **Fix Data Pipeline**: Ensure fresh AlphaFold runs are actually occurring (check cache invalidation) and that linked artifacts (PNGs/PDBs) are preserved.
- **Adopt Confidence Weighting**: All future "Tension Rod" candidates must meet the `Anisotropy > 3.0 AND pLDDT > 70` threshold to be promoted to "Confirmed".
