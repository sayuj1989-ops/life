# Evidence Note: Piezo1, YAP, and the Cost of Dendritic Gain

**Date:** 2026-03-12
**Source:** Hu et al., *Nature Communications* (2025)
**Topic:** Osteocyte Dendrite Formation, Mechanotransduction Gain, and Metabolic Cost

## The Core Insight
Piezo1 is not just a "sensor" that fires when pulled; it is a **morphogen for its own antenna**. Hu et al. (2025) demonstrate that Piezo1 activation in late osteoblasts/osteocytes drives the formation of the dendritic network itself. This process is mediated by a specific signaling axis:
`Piezo1 -> YAP -> Secreted CCN1/2 (Cyr61/Ctgf) -> Integrin/Src -> Actin Polymerization -> Dendrite Extension`.

## Mechanism & Connection to Counter-Curvature
1.  **Gain Control ($\gamma$):** In our "Biological Counter-Curvature" framework, the stability of the spine depends on the proprioceptive gain $\gamma$. This paper provides the *physical basis* for that gain. The "dendritic network" is effectively the sensor array. A denser network = higher signal-to-noise ratio = higher $\gamma$.
2.  **The Supply-Side Constraint:** Dendrites are metabolically expensive (high surface-area-to-volume ratio requires massive membrane maintenance). The paper shows that *loss* of Piezo1 leads to "immature," round osteocytes with few dendrites. This implies that without constant mechanical stimulation (or if the metabolic cost of YAP/CCN1/2 secretion cannot be met), the sensor array collapses.
3.  **Wnt as a Symptom, Not a Driver:** The study finds that Wnt/$\beta$-catenin is *upregulated* when Piezo1 is lost, yet bone mass decreases. This resolves a paradox: Wnt is usually anabolic. Here, high Wnt signals a failure to differentiate (stuck in osteoblast state). The "mature" counter-curvature state requires *suppression* of Wnt (via Sost) and activation of YAP.

## Relevance to Scoliosis (AIS)
Adolescent Idiopathic Scoliosis (AIS) occurs during the rapid growth phase (Energy Deficit). If the metabolic cost of maintaining the YAP-CCN1/2-Dendrite axis becomes unsustainable during rapid somatic expansion, the first thing to be "cut" might be the expensive dendritic arbor.
*   **Result:** The osteocyte becomes "blind" (low $\gamma$).
*   **Outcome:** The spinal control system enters a drift/buckling regime ($L > L_{crit}$) because the error-correction gain has dropped below the threshold required to counter the growing gravitational moment.

## Proposed Test
**The Dendritic Collapse Assay:**
Compare osteocyte dendrite density (confocal/phalloidin) and serum CCN1 levels in adolescent mice during:
1.  Normal growth.
2.  Caloric restriction (Energy Deficit).
3.  Rapid catch-up growth (AIS model).
Prediction: Dendrite retraction precedes overt bone loss or curvature.

---

# Evidence Note: ADGRG6/GPR126 Mechanotransduction in Spine Alignment
**Date:** 2026-03-12
**Topic:** Gravity, Spine, Counter-Curvature

## Claim
The Adhesion G protein-coupled receptor G6 (ADGRG6/GPR126) functions as a critical mechanosensor in cartilaginous and dense connective tissues, translating mechanical forces (such as gravity) into biochemical signals necessary for maintaining spinal alignment.

## Mechanism
ADGRG6 is enriched in the intervertebral discs (IVDs) and surrounding dense connective tissues. It responds to mechanical strain by activating intracellular cAMP signaling pathways, which in turn regulate the extracellular matrix (ECM) composition. Loss or mutation of ADGRG6 leads to a failure in mechanotransduction, resulting in structurally deficient connective tissues that cannot properly resist mechanical loads, ultimately leading to scoliosis (Liu et al., 2021).

## Relevance to S-shaped Spinal Growth and Scoliosis
The spine must constantly adapt to the compressive and torsional forces of gravity during growth. ADGRG6 acts as a local sensor in the IVD and ligaments that detects these forces and modulates tissue stiffness and ECM integrity in response. In adolescent idiopathic scoliosis (AIS), defects in this mechanotransduction pathway mean the structural elements of the spine fail to remodel appropriately under the asymmetrical loads of the growing S-curve, leading to progressive buckling.

## Support for the Counter-Curvature Hypothesis
This finding directly supports the "biological counter-curvature" hypothesis, which posits that the spine maintains its geometry against gravity via an active, information-driven mechanosensory feedback loop. ADGRG6 serves as a molecular "strain antenna" (similar to high-anisotropy sensors like PIEZO2 or POC5) that provides the necessary proprioceptive/mechanical supply ($S_{proprio}$) to match the metabolic demand of maintaining the counter-curvature. Its failure during rapid growth creates the "Energy Deficit Window" where passive gravitational geodesics overcome active biological control.

## Open Question & Proposed Test
**Open Question:** Does the efficacy of ADGRG6 mechanotransduction depend on its structural anisotropy, and does unloading (microgravity) cause its mislocalization or functional decoupling from the ECM?

**Proposed Test:** Cultivate ADGRG6-expressing spinal fibroblasts or IVD cells in a simulated microgravity bioreactor (unloading) versus cyclic compression (loading). Measure ADGRG6 membrane localization, downstream cAMP levels, and the structural anisotropy of the surrounding collagen matrix to determine if the sensor's function degrades without a persistent gravitational vector.
