# 3. Results

## 3.1 The Proprioceptive Delay ($\tau$) Budget
Our systematic literature review allowed us to partition the total proprioceptive delay ($\tau$) into discrete, quantifiable components. For a typically developing, healthy adolescent measuring approximately 1.45 meters at peak height velocity, the theoretical baseline $\tau$ consists of: peripheral transduction ($\approx$ 2 ms), afferent neural conduction ($\approx$ 15 ms, traversing 0.85m at 55-60 m/s), spinal synaptic relay ($\approx$ 3-5 ms), cerebellar integration ($\approx$ 25 ms), efferent conduction ($\approx$ 15 ms), neuromuscular junction delay ($\approx$ 1 ms), and a dominant electromechanical coupling phase ($\approx$ 65 ms). Cumulatively, this establishes a healthy baseline delay of approximately 130-140 ms, which remains safely below the estimated 200 ms control-theoretic threshold for postural instability.

## 3.2 Mapping AIS GWAS Hits to $\tau$ Subcomponents
Our analysis demonstrated a precise correspondence between robust AIS susceptibility genes and the functional subdivisions of the $\tau$ budget.

- **PIEZO2 and Mechanotransduction ($\tau_{transduction}$):** PIEZO2 serves as the primary mechanosensitive channel in the muscle spindle. AlphaFold prediction (UniProt: Q9H5I5) of the human PIEZO2 structure highlights a trimeric propeller assembly surrounding a central pore. Missense variations near the extended blades or the beam connecting the blades to the pore alter the structural energy barrier to opening, directly delaying activation kinetics and functionally increasing $\tau_{transduction}$.
- **GPR126 (ADGRG6) and Myelination ($\tau_{afferent}$, $\tau_{efferent}$):** A crucial regulator of Schwann cell development, GPR126 signals via cyclic AMP to drive myelin protein expression. The AlphaFold model (UniProt: Q86SQ4) of the massive extracellular domain (ECD) reveals critical interaction motifs in the CUB and GAIN domains (pLDDT > 70). AIS risk variants (e.g., rs6570507) likely destabilize the ECD or impair its ability to undergo autoproteolysis, leading to suboptimal cAMP signaling. Functionally, this manifests as a failure of Schwann cells to rapidly upregulate myelination in response to the stretch induced by the pubertal growth spurt, transiently lowering nerve conduction velocity (NCV) and expanding $\tau_{afferent}$ and $\tau_{efferent}$.
- **LBX1 and Spinal Relay ($\tau_{spinal}$):** LBX1 specifies the dorsal horn interneuron populations (dI4–dI6) that form the critical proprioceptive relays into the spinocerebellar tract. Risk variants (e.g., rs11190870) mapping to putative enhancer regions alter developmental dosage, resulting in structurally sub-optimal synaptic connectivity in Clarke's column. This necessitates greater spatial and temporal summation for signal propagation, prolonging the synaptic integration time $\tau_{spinal}$.

**Table 1: Molecular Decomposition of Proprioceptive Delay**
| Component | Biological Process | Est. Baseline Delay | Modulating Gene | Proposed Effect of Variant |
| :--- | :--- | :--- | :--- | :--- |
| $\tau_{transduction}$ | Muscle Spindle Activation | 2.0 ms | *PIEZO2* | Altered activation kinetics |
| $\tau_{afferent}$ | Neural Conduction to Spinal Cord | 15.0 ms | *GPR126* | Slower NCV due to poor myelination remodeling |
| $\tau_{spinal}$ | Synaptic Integration in Dorsal Horn | 5.0 ms | *LBX1* | Slower integration due to altered circuitry |
| $\tau_{cerebellar}$ | Central Processing | 25.0 ms | *CHD7*? | Suboptimal predictive integration |
| $\tau_{efferent}$ | Descending Motor Command | 15.0 ms | *GPR126* | Slower NCV |
| $\tau_{NMJ}$ | Neuromuscular Transmission | 1.0 ms | - | - |
| $\tau_{EM}$ | Electromechanical Force Production | 65.0 ms | - | - |
