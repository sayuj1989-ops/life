# Microgravity & Spine Synthesis (Week 44, 2026)

## Overview
This synthesis extracts transferable principles from microgravity biology to inform biological counter-curvature and scoliotic progression, specifically regarding mechanotransduction and extracellular matrix (ECM) remodeling.

## Observed

### 1. Paraspinal Muscle Atrophy and Adipogenesis
Unloading in microgravity causes rapid paraspinal muscle atrophy, transitioning muscle fate from functional contractile tissue to an adipogenic phenotype.
*Citation: Burkhart et al. (2019) / NASA; Spaceflight induced changes in paraspinal muscle morphology.*

### 2. Disruption of Piezo1-Mediated Mechanotransduction
Mechanical unloading effectively silences Piezo1 signaling in bone marrow-derived mesenchymal stem cells (BMSCs), diverting cell lineage commitment away from osteogenesis and towards adipogenesis.
*Citation: Li et al. (2023); scRNA-seq of BMSCs under hindlimb unloading.*

### 3. YAP/TAZ Nuclear Exclusion
The loss of gravitational vector sensing directly impairs YAP/TAZ nuclear translocation in load-bearing connective tissues, acting as a "blinding" mechanism that prevents structural reinforcement.
*Citation: Tosi et al. (2026); microgravity disrupts primary cilium mechanotransduction.*

## Mechanistic Bridge to ECM Remodeling
The failure of Piezo1 and YAP/TAZ signaling creates a systemic under-loading state in the mechanostat. Without nuclear YAP/TAZ, fibroblasts and osteoblasts fail to produce dense, cross-linked ECM components (like collagen I) needed to maintain high tissue stiffness ($EI$). Instead, the tissue shifts toward a compliant, loosely organized matrix, lowering the critical buckling threshold.

## Predicted Directionality
* **Under Unloading (Microgravity):** Paraspinal muscle tone decreases, ECM production stalls, YAP/TAZ is excluded from the nucleus, and tissue compliance increases. The biological counter-curvature collapses due to a lack of active mechanical restraint.
* **Under Loading (1G):** Paraspinal tone is maintained, Piezo1 is activated, YAP/TAZ enters the nucleus to drive robust ECM synthesis (collagen cross-linking), and structural stiffness ($EI$) is dynamically maintained against the gravity vector.

## Hypothesized (Testable Predictions)
*(See `notes/hypothesis_register.md` for full formatting)*
1. If YAP/TAZ nuclear translocation is artificially rescued in intervertebral discs during microgravity simulation, then structural stiffness and biological counter-curvature will be maintained despite the absence of a gravity vector, measurable via bioreactor mechanical testing.
2. If Piezo1 is systemically activated (e.g., via Yoda1) in a hindlimb-unloaded model, then paraspinal muscle adipogenesis will be prevented, preserving the active tensegrity required to prevent scoliotic buckling, measurable via MRI and Cobb angle.
