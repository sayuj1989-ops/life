# Microgravity & Spine Synthesis: Week 10, 2026

## Key Findings & Transferable Principles

1. **Paraspinal Muscle Atrophy & Fate Switch**
   * *Observed:* Microgravity induces rapid paraspinal muscle atrophy characterized by a shift from myogenic to adipogenic lineages (fatty infiltration).
   * *Mechanistic Bridge:* Mechanical unloading removes the tension signal required by mechanosensors (like PIEZO1/YAP), disrupting Wnt/β-catenin signaling. This reduces structural strain on the extracellular matrix (ECM) and leads to PPARG-driven adipogenesis.
   * *Predicted Directionality:* Unloading -> Low Tension -> Downregulation of PIEZO1/YAP -> Adipogenesis. Loading -> High Tension -> Upregulation of PIEZO1/YAP -> Myogenesis.
   * *Citation:* (Wuest et al., 2025; Li et al., 2023)

2. **Intervertebral Disc (IVD) Degeneration via Convective Shutdown**
   * *Observed:* IVDs in microgravity suffer from matrix degradation, hyper-hydration (swelling), and altered cell viability.
   * *Mechanistic Bridge:* Loss of cyclic compressive loading (gravity) causes "convective shutdown", reducing fluid flow and nutrient transport. This stasis upregulates matrix metalloproteinases (MMPs, e.g., MMP1/3) which degrade the ECM, specifically the annulus fibrosus, reducing torsional stiffness.
   * *Predicted Directionality:* Unloading (Static) -> Loss of Flow -> MMP Upregulation -> ECM Softening (Torsional failure). Loading (Dynamic) -> Nutrient Flow -> ECM Maintenance.
   * *Citation:* (Chen et al., 2025; Sato et al., 2025)

3. **Cilio-Nuclear Decoupling & Mechanosensor Failure**
   * *Observed:* Unloading leads to primary cilia shortening, nuclear flattening (loss of Lamin A/C), and generalized mechanosensory deafness.
   * *Mechanistic Bridge:* High-anisotropy "Tension Rod" proteins (e.g., POC5, PIEZO2, LMNA) act as a continuous tether. Microgravity removes the prestress, causing these rods to undergo entropic collapse. This decouples the cilium from the nucleus, inhibiting mechano-transduction and preventing ECM remodeling responses.
   * *Predicted Directionality:* Loading -> Structural Extension -> High Sensitivity. Unloading -> Entropic Collapse -> Loss of Sensitivity (Mechanoblindness).
   * *Citation:* (Camberos et al., 2019; Nava et al., 2020)

4. **Glymphatic Stasis & Asymmetric Inflammation**
   * *Observed:* Loss of gravity-dependent hydrostatic pressure causes lymphatic/glymphatic stagnation in the spinal cord.
   * *Mechanistic Bridge:* Vertebral lymphatic valves rely on a pressure head to prevent reflux. In microgravity, this pump fails, leading to metabolic waste accumulation. The resulting localized inflammation triggers reactive astrogliosis and alters the mechanical properties of the surrounding ECM.
   * *Predicted Directionality:* Loading -> Forward Flow -> Clearance. Unloading -> Stagnation/Reflux -> Inflammation/Astrogliosis.
   * *Citation:* (Mader et al., 2026; Jacob et al., 2019)

## Falsifiable Tests (added to registry)

- **H_2026_10_30_Microgravity_Adipose_Switch**: *Proposed*
- **H_2026_10_30_IVD_Torsional_Decay**: *Proposed*

## Datasets
Added DS_027 (JAXA Mouse Habitat Unit Paraspinal Muscle RNA-seq) to `data/datasets_registry.md`.
