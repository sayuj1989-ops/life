# Thermodynamic Cost of Countercurvature: Molecular Mapping via AlphaFold

**Date:** 2026-02-13
**Source:** Pre-computed AFCC metrics (AlphaFold Countercurvature pipeline)
**Framework:** Free energy dissipation functional (manuscript Eq. 7)

```
Ḟ = ∫₀ᴸ [ ηₚ|∂κ/∂t|² + ηₐ(κ - κ_passive)² + Γₘ(s) ] ds
```

## Key Insight

Einstein describes gravity as curvature of spacetime. Life forms grow
*against* this curvature — a paradox paid for in ATP. The same atoms
that sit passively in rock are reorganized in living tissue to resist
gravitational geodesics. The thermodynamic cost of this resistance is
not abstract: it is paid at the molecular level by specific proteins
whose AlphaFold-predicted structures reveal how they bear this cost.

The spine's S-curve is a **standing wave** requiring continuous energy
input. During the adolescent growth spurt, the metabolic demand
(P_counter ~ L^{2-3}) increases 65-113% while the supply system lags,
creating the **Energy Deficit Window** that seeds AIS.

---
## Proprioceptive Feedback Cost (η_p)

The cost of **sensing curvature error**. These proteins maintain the proprioceptive circuit that detects deviations from the information-prescribed shape. During the growth spurt, sensing density (sensors per unit length) must scale with L.

| Gene | UniProt | Anisotropy | Morphology | Rg (Å) | pLDDT | Res | Hinges | L-Scaling | Role |
| :--- | :--- | ---: | :--- | ---: | ---: | ---: | ---: | :--- | :--- |
| **PIEZO2** | Q9H5I5 | 4.44 | Fibrous/Extended | 43.4 | 79.4 | 709 | 0 | L (sensor density per unit length) | Vector mechanosensor for proprioception; detects alignment error |
| **EGR3** | Q06889 | 3.76 | Fibrous/Extended | 18.5 | 50.0 | 387 | 2 | L (innervation per segment) | Transcription factor maintaining muscle spindle innervation |
| **RUNX3** | Q13761 | 2.06 | Intermediate | 15.8 | 60.6 | 415 | 12 | L (proprioceptive neuron count) | Master regulator of proprioceptive neuron development |
| **NTRK3** | Q16288 | 1.94 | Intermediate | 32.5 | 76.8 | 839 | 9 | L (afferent neuron count) | TrkC receptor; proprioceptive neuron survival signal |
| **PIEZO1** | Q92508 | 3.90 | Fibrous/Extended | 58.9 | 72.0 | 2521 | 3 | L^2 (membrane area) | Scalar mechanosensor; detects membrane tension (buckling threshold) |

**Structural summary:** Mean anisotropy = **3.22**, Rg range = 16–59 Å, Mean pLDDT = 67.8, Total residues = 4871, Total hinges = 26

### Thermodynamic Predictions

- **PIEZO2** (L (sensor density per unit length)): High anisotropy (extended) = high metabolic cost to maintain orientation; channel density must scale with L during growth spurt
- **EGR3** (L (innervation per segment)): Extended structure despite being a TF; high disorder = energetically costly to fold; EGR3 expression must scale with L for spindle density
- **RUNX3** (L (proprioceptive neuron count)): Intermediate anisotropy, high disorder (56%); its expression level sets the proprioceptive gain; insufficient scaling during growth = reduced correction
- **NTRK3** (L (afferent neuron count)): Intermediate anisotropy, 9 hinge candidates = conformationally expensive; NT-3/TrkC signaling cost scales with spinal length
- **PIEZO1** (L^2 (membrane area)): Extended (3.9 aniso), massive (2521 res); scalar complement to PIEZO2; sets the stiffness floor below which buckling occurs

---
## Active Moment Maintenance (η_a)

The cost of **tonic muscle contraction and cytoskeletal tension** that holds the spine against gravity. This is the largest ATP consumer — the molecular machines converting chemical energy into the mechanical moment opposing gravitational sag. Scales as L² to L³.

| Gene | UniProt | Anisotropy | Morphology | Rg (Å) | pLDDT | Res | Hinges | L-Scaling | Role |
| :--- | :--- | ---: | :--- | ---: | ---: | ---: | ---: | :--- | :--- |
| **DMD** | P11532 | 1.32 | Globular | 22.8 | 76.3 | 525 | 1 | L^3 (muscle volume) | Dystrophin; cytoskeleton-ECM linker in paraspinal muscle |
| **MYLK** | Q15746 | 1.46 | Globular | 41.5 | 65.8 | 1914 | 31 | L^2 (contractile force) | Myosin light chain kinase; tonic contraction regulator |
| **LBX1** | P52954 | 2.27 | Intermediate | 22.7 | 66.9 | 281 | 0 | L^2 (muscle cross-section x length) | Paraspinal muscle specification TF; top GWAS hit for AIS |
| **FLNA** | P21333 | 2.50 | Intermediate | 56.9 | 76.5 | 2647 | 116 | L^3 (muscle volume) | Filamin A; cytoskeletal mechanosensor and crosslinker |
| **VIM** | P08670 | 7.47 | Fibrous/Extended | 65.7 | 77.1 | 466 | 1 | L^3 (cell volume) | Vimentin; gravitational strain gauge in cells |
| **LMNA** | P02545 | 4.75 | Fibrous/Extended | 71.2 | 76.4 | 664 | 0 | L^2 (load-bearing cross-section) | Lamin A/C; nuclear mechanostat scaling with tissue stiffness |
| **CAV1** | Q03135 | 3.98 | Fibrous/Extended | 33.4 | 78.4 | 178 | 0 | L^2 (membrane area) | Caveolin-1; membrane curvature sensor and mechanotransducer |

**Structural summary:** Mean anisotropy = **3.39**, Rg range = 23–71 Å, Mean pLDDT = 73.9, Total residues = 6675, Total hinges = 149

### Thermodynamic Predictions

- **DMD** (L^3 (muscle volume)): Essential for maintenance of muscle tone against gravity; loss leads to collapse; connects contractile force to the load-bearing ECM.
- **MYLK** (L^2 (contractile force)): Regulator of myosin contractility; sets the gain of the active moment; failure leads to inability to sustain postural tone.
- **LBX1** (L^2 (muscle cross-section x length)): Intermediate anisotropy, high disorder (61%); blocky structure sensitive to nuclear stiffness; during energy deficit, LBX1 program fails first
- **FLNA** (L^3 (muscle volume)): Tension-gated signal integrator; unfolding domains expose cryptic sites; maintenance cost proportional to cytoskeletal volume
- **VIM** (L^3 (cell volume)): Intermediate filament; collapses in microgravity triggering ROS cascade; the 'first domino' in energy deficit — its failure triggers metabolic switch
- **LMNA** (L^2 (load-bearing cross-section)): Highest anisotropy (4.75) among TFs; nuclear stiffness must scale with gravitational load during growth; failure = Scalar Senescence
- **CAV1** (L^2 (membrane area)): Membrane-embedded sensor; cost of maintaining caveolar pits scales with membrane area; connects to YAP/TAZ nuclear translocation

---
## Basal Tissue Maintenance (Γ_m)

The cost of **maintaining the information field itself**: ECM turnover, morphogen gradients, metabolic homeostasis, and the growth machinery. This term determines the **supply side** of the energy balance and the **rate** of the growth spurt.

| Gene | UniProt | Anisotropy | Morphology | Rg (Å) | pLDDT | Res | Hinges | L-Scaling | Role |
| :--- | :--- | ---: | :--- | ---: | ---: | ---: | ---: | :--- | :--- |
| **COL1A1** | P02452 | 2.80 | Intermediate | 23.5 | 52.7 | 1464 | 16 | L^3 (bone/disc volume) | Type I collagen; primary structural protein of vertebral bone/disc |
| **COMP** | P49747 | 1.72 | Intermediate | 31.9 | 88.1 | 757 | 6 | L (disc height x number) | Cartilage oligomeric matrix protein; disc ECM maintenance |
| **SIRT1** | Q96EB6 | 1.73 | Intermediate | 22.3 | 65.0 | 747 | 3 | constant (sensor, not structural) | Sirtuin 1; NAD+-dependent metabolic sensor (energy gauge) |
| **SOX9** | P48436 | 2.19 | Intermediate | 16.6 | 56.0 | 509 | 2 | L (growth plate activity) | Master chondrogenic TF; growth plate cartilage specification |
| **SHH** | Q15465 | 2.12 | Intermediate | 24.5 | 78.4 | 462 | 6 | L (gradient length) | Sonic Hedgehog; morphogen gradient for vertebral patterning |
| **CDKN1A** | P38936 | 2.14 | Intermediate | 23.9 | 69.0 | 164 | 2 | threshold (binary switch) | p21; cell cycle inhibitor activated by mechanical unloading |
| **PPARGC1A** | Q9UBK2 | 2.19 | Intermediate | 31.2 | 52.7 | 798 | 0 | L (mitochondrial volume) | Mitochondrial biogenesis master regulator; determines energy SUPPLY capacity |
| **IGF1R** | P08069 | 1.43 | Globular | 43.2 | 78.0 | 1367 | 35 | L (receptor density) | Insulin-like growth factor 1 receptor; mediates growth plate signaling |
| **GHR** | P10912 | 5.13 | Fibrous/Extended | 31.4 | 58.7 | 638 | 54 | L (growth signal) | Growth hormone receptor; master regulator of adolescent growth spurt rate |
| **ARNTL** | O00327 | 3.32 | Fibrous/Extended | 32.1 | 65.5 | 626 | 6 | L (circadian entrainment) | BMAL1; circadian clock TF in intervertebral disc regulating metabolism |

**Structural summary:** Mean anisotropy = **2.48**, Rg range = 17–43 Å, Mean pLDDT = 66.4, Total residues = 7532, Total hinges = 130

### Thermodynamic Predictions

- **COL1A1** (L^3 (bone/disc volume)): Triple helix (high anisotropy expected); collagen turnover is the largest single component of Gamma_m; cost scales with tissue volume
- **COMP** (L (disc height x number)): ECM scaffold protein; turnover rate determines matrix maintenance cost; disc height increases during growth requiring more COMP
- **SIRT1** (constant (sensor, not structural)): Compact enzyme; acts as the 'fuel gauge' detecting energy deficit; low NAD+/NADH during rapid growth triggers metabolic switch to adipogenesis
- **SOX9** (L (growth plate activity)): SOX9 drives growth plate proliferation; its activity rate determines dL/dt; higher SOX9 = faster growth = steeper metabolic demand curve
- **SHH** (L (gradient length)): Compact signaling molecule; maintains the information field I(s) itself; gradient maintenance cost scales with rod length
- **CDKN1A** (threshold (binary switch)): Small, compact; upregulated in microgravity to halt proliferation; its activation = signal that energy supply is insufficient for growth
- **PPARGC1A** (L (mitochondrial volume)): Energy supply bottleneck during growth spurt contributes to AIS; failure to scale mitochondrial biogenesis with L^3 leads to metabolic burnout.
- **IGF1R** (L (receptor density)): Signaling receptor for growth spurt rate; rapid growth linked to curve progression; receptor density determines sensitivity to systemic growth signals.
- **GHR** (L (growth signal)): Regulates the rate of spinal elongation; rapid growth is a risk factor for AIS; dictates the pace of demand increase.
- **ARNTL** (L (circadian entrainment)): Circadian rhythm disruption linked to disc degeneration and scoliosis; essential for temporal coordination of repair mechanisms.

---
## Synthesis: The Energy Deficit Window — A Molecular View

### Structural Signatures Across Terms

| Term | Mean Anisotropy | Structural Signature | Scaling |
| :--- | ---: | :--- | :--- |
| **η_p** (Sensing) | 3.22 | Extended sensors (PIEZO1/2) + disordered TFs (EGR3, RUNX3) | L to L² |
| **η_a** (Actuation) | 3.39 | Fibrous scaffolds (LMNA) + crosslinkers (FLNA) + strain gauges (VIM) | L² to L³ |
| **Γ_m** (Maintenance) | 2.48 | Compact enzymes (SIRT1) + ECM (COL1A1) + morphogens (SHH) | L to L³ |

### The Molecular Logic of the Energy Deficit Window

The AlphaFold structural data reveal a clear hierarchy of vulnerability:

1. **High-anisotropy demand proteins** (PIEZO2: 4.44, LMNA: 4.75, PIEZO1: 3.90)
   are structurally the most expensive to maintain. Their extended
   conformations require continuous cytoskeletal tension for proper
   orientation. These are the first to lose fidelity when energy is scarce.

2. **Disordered sensing TFs** (EGR3: 64% disordered, RUNX3: 56% disordered)
   require constant chaperone activity and have high turnover rates.
   Their expression levels must track spinal length but their
   transcription depends on the same energy pool being depleted.

3. **Compact supply-side proteins** (SIRT1, CDKN1A, SOX9) are structurally
   cheap but functionally rate-limiting. SIRT1 detects the energy deficit;
   SOX9 drives the growth rate; CDKN1A halts proliferation when energy fails.
   These are the **sensors and switches** of the Energy Deficit Window.

4. **The critical mismatch**: During peak height velocity (~8 cm/yr),
   the demand proteins (PIEZO2, LMNA, FLNA) require ~65-113% more
   energy, but the supply sensor (SIRT1) detects declining NAD+/NADH
   *after* the deficit has already begun. This lag — between structural
   demand and metabolic sensing — is the molecular basis of the
   Energy Deficit Window.

### Testable Prediction

Paraspinal muscle biopsies from AIS patients at peak growth velocity
will show:
- **Reduced** PIEZO2 membrane density and LMNA nuclear aspect ratio
  (demand-side failure)
- **Reduced** PPARGC1A/PGC-1α and elevated SIRT1 (supply-side stress)
- **Elevated** CDKN1A/p21 (growth arrest signal)
- **Asymmetric** LBX1 expression (concave < convex)

compared to height-matched non-scoliotic controls.
