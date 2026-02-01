# Structure Cluster Analysis: The "Gravitational Tension Tether" Class

**Date:** 2026-02-01
**Source Data:** `outputs/afcc/2026-02-01/metrics.csv` (n=30 candidates)
**Method:** K-Means Clustering (k=3) on [Anisotropy, PAE Blockiness]

## Cluster Identification

We identified a distinct cluster ("Cluster 0") characterized by **extreme structural anisotropy**.

| Cluster | Avg Anisotropy | Avg Blockiness | Members (n) | Representative Proteins |
| :--- | :--- | :--- | :--- | :--- |
| **0** | **18.31** | 3.45 | 2 | **CDH23, POC5** |
| 1 | 3.26 | 1.94 | 10 | PIEZO2, LMNA, RUNX3 |
| 2 | 2.64 | 7.39 | 16 | PIEZO1, YAP1, FLNA |

## Cluster 0: "Gravitational Tension Tethers"

### Membership
- **CDH23 (Cadherin-23)**: The tip-link protein essential for vestibular mechanotransduction. It connects stereocilia and is pulled taut by the displacement of otoconia (gravity stones).
- **POC5 (Centriolar Protein)**: A core component of the centriole/cilium structure, essential for maintaining the linear geometry of the ciliary base.

### Structural Properties
- **Extreme Anisotropy (>18)**: These proteins are effectively 1D "cables" or "rods".
- **Mechanical Implication**: Structures with such high aspect ratios are mechanically unstable under compression (buckling) or zero-load (entropic coiling). They *require* tension to maintain their functional extended geometry.

### Hypothesis: Entropic Collapse
In a 1G environment, constant gravitational acceleration provides a baseline "pre-stress" (via otoconia weight for CDH23, or hydrostatic gradients for ciliary POC5) that keeps these tethers taut.
In microgravity, this pre-stress is removed. We hypothesize that these high-anisotropy proteins undergo **Entropic Collapse** (slackening), functionally disconnecting the mechanotransduction apparatus even if the protein expression levels remain normal.

This explains why vestibular dysfunction (CDH23) and ciliary defects (POC5) are strongly linked to scoliosis: the "hardware" goes slack.

## Proposed Test
**Experiment**: "Tether Tautness Check"
- **System**: iPSC-derived Vestibular Hair Cells (for CDH23) or Ciliated Fibroblasts (for POC5).
- **Condition**: Static culture (1G) vs. Clinorotation (Simulated Microgravity).
- **Readout**: FRET-based tension sensor inserted into the CDH23 ecodomain or POC5 rod domain.
- **Prediction**: FRET efficiency will increase in microgravity (indicating closer fluorophores -> slackening/coiling) compared to 1G control (extended/taut).
