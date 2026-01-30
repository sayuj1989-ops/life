# Structure Cluster: Flexible Levers
**Date:** 2026-01-30
**Method:** AFCC Metrics Analysis (Anisotropy vs. Hinge Count/Flexibility)

## 1. Cluster Definition
**Name:** Flexible Levers (Extended Articulated Sensors)
**Defining Metrics:**
- **Anisotropy Index:** > 3.0 (Extended)
- **Flexibility:** High Hinge Count (>5) OR Low Mean pLDDT (<60)
- **Feature:** Presence of multiple "beads-on-a-string" domains separated by flexible linkers.

## 2. Members
| Gene | Anisotropy | Hinge Candidates | pLDDT (Mean) | Role |
| :--- | :--- | :--- | :--- | :--- |
| **ADGRG6** (GPR126) | 3.06 | 12 | 73.7 | Mechanosensitive GPCR; Scoliosis Driver |
| **PTK7** | 7.45 | 20 | 82.7 | PCP Regulator; Ciliary Relay |
| **MESP2** | 4.03 | 1 (Low pLDDT) | 54.2 | Segmentation Clock |

## 3. Structural Synthesis
Unlike the "Rigid Tension Rods" (e.g., PIEZO2, POC5) which transmit force linearly, the "Flexible Levers" are characterized by a segmented architecture.
- **ADGRG6:** The large extracellular N-terminal domain is predicted to have 12 flexible hinge regions. This suggests it does not act as a stiff rod, but rather as a **tension-gated articulated lever**. Under low tension (unloading), the domain may collapse or fold; under physiological tension (gravity), it straightens to expose binding sites or exert torque on the transmembrane bundle.
- **PTK7:** With 20 potential hinges between its Ig domains, PTK7 likely acts as a **molecular ruler** that measures cell-cell spacing via unfolding.

## 4. Hypothesis: H_2026_01_30_Flexible_Lever
**Statement:**
Proteins in the "Flexible Lever" class (ADGRG6, PTK7) function as non-linear tension sensors where gravitational loading drives the *straightening* of the extracellular domain from a high-entropy "slack" state to a low-entropy "taut" state, which is required to align downstream signaling interfaces.

**Mechanism:**
In microgravity (unloading), the loss of tensile stress causes these "levers" to relax into their entropic collapsed state, effectively "silencing" the constitutive signal required for spinal straightness (e.g., ADGRG6->cAMP or PTK7->PCP). This differs from "Rod" failure (buckling) or "Block" failure (silencing), representing a "Slackening" failure mode.

**Testable Prediction:**
Introduction of rigid crosslinks (e.g., engineered disulfide bonds) across the predicted hinge regions of ADGRG6 will lock it in a "taut" (straight) conformation, rescuing downstream cAMP signaling even in the absence of mechanical tension (or in microgravity).

## 5. Next Steps
1.  **In Silico:** Map the 12 hinges of ADGRG6 to specific domain linkers (e.g., CUB-PTX-HormR).
2.  **In Vitro:** Design "Locked-Straight" vs "Locked-Bent" ADGRG6 variants.
3.  **In Vivo:** Express variants in *gpr126* mutant zebrafish and assay for spine straightening.
