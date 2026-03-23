# Phase 1, Day 2: AIS Genetics and GWAS Hits

Adolescent Idiopathic Scoliosis (AIS) is a complex genetic trait with a strong heritable component. Over the past decade, large-scale Genome-Wide Association Studies (GWAS) have identified several highly replicable susceptibility loci. For Paper 4, we hypothesize that many of these loci correspond directly to structural or regulatory proteins that govern the efficiency of the proprioceptive system, thereby increasing the proprioceptive delay parameter ($\tau$) in the derivative gain gap model.

## Key GWAS Loci and Proposed Functions

### 1. GPR126 (ADGRG6)
*   **Gene:** Adhesion G-protein-coupled receptor G6.
*   **Genetic Evidence:** Highly replicable locus in multiple populations.
*   **Proposed Function in AIS:** GPR126 is heavily involved in Schwann cell myelination and the development of peripheral nerves, cartilage, and bone. We hypothesize that intronic or missense variants in GPR126 alter its signaling efficiency during the adolescent growth spurt, leading to suboptimal myelination of Group Ia/II afferent fibers. Thinner myelin sheaths reduce conduction velocity, thereby increasing **Afferent Conduction Delay ($\tau_{aff}$)**.

### 2. LBX1
*   **Gene:** Ladybird homeobox 1.
*   **Genetic Evidence:** One of the most significant and earliest identified AIS GWAS loci.
*   **Proposed Function in AIS:** LBX1 is a critical transcription factor specifying dorsal spinal cord interneuron fates, particularly those involved in proprioception (e.g., relay neurons in the spinocerebellar tracts). Dysregulation of LBX1 could alter the wiring or synaptic efficiency of these relay circuits, increasing **Spinal Relay Delay ($\tau_{spin}$)**.

### 3. PAX1
*   **Gene:** Paired box 1.
*   **Genetic Evidence:** Consistent GWAS hit for AIS.
*   **Proposed Function in AIS:** PAX1 is a key transcriptional regulator in somite development and the formation of the vertebral column. Unlike GPR126 or LBX1, PAX1 likely affects the structural geometry of the spine (the "plant" in the PID control model) rather than the neural "controller". Altered vertebral geometry could make the spine mechanically less stable and therefore more sensitive to an underlying delay $\tau$.

## References

```bibtex
@article{Bilgin_2025,
  title={Investigation of LBX1, TIMP2, GPR126 and CHD7 Gene Polymorphisms in Adolescent Idiopathic Scoliosis Patients},
  volume={16},
  ISSN={2192-5690},
  url={http://dx.doi.org/10.1177/21925682251356933},
  DOI={10.1177/21925682251356933},
  number={1},
  journal={Global Spine Journal},
  publisher={SAGE Publications},
  author={Bilgin, Erkan and Tezcan Unlu, Havva and Cecener, Gulsah and Aymelek, Huri Sema and Bilgin, Yucel and Akesen, Burak},
  year={2025},
  month=jul,
  pages={617–627}
}

@article{Sepich_2025,
  title={The importance of imperfect pre-clinical models in adolescent idiopathic scoliosis},
  volume={18},
  ISSN={1754-8411},
  url={http://dx.doi.org/10.1242/dmm.052438},
  DOI={10.1242/dmm.052438},
  number={8},
  journal={Disease Models & Mechanisms},
  publisher={The Company of Biologists},
  author={Sepich, Diane S. and Gray, Ryan S. and Ahituv, Nadav and Gurnett, Christina A. and Rios, Jonathan J. and Solnica-Krezel, Lila and Wise, Carol A.},
  year={2025},
  month=aug
}
```
