# AI Prompt: JOR Spine Submission-Ready Manuscript

**Version:** 1.0
**Target Journal:** JOR Spine (Journal of Orthopaedic Research - Spine)
**Document Type:** Full research manuscript
**Output Format:** Word document (.docx)

---

## CONTEXT & RESEARCH OVERVIEW

You are generating a submission-ready research manuscript for **JOR Spine** (Wiley-Blackwell, IF 3.99, Q1 Orthopedics). The manuscript presents the **Information–Elasticity Coupling (IEC) Framework** for understanding vertebral geometry and adolescent idiopathic scoliosis (AIS) onset.

### Core Research

**Primary Thesis:** Adolescent idiopathic scoliosis emerges as an **energy deficit phenomenon** during rapid growth, when metabolic demands of maintaining spinal counter-curvature exceed supply capacity.

**Secondary Contribution:** The IEC framework (combining developmental patterning with Cosserat rod mechanics) explains how spinal S-curve geometry is maintained and becomes vulnerable to buckling during growth.

**Data Foundation:** AlphaFold v6 structural analysis of 23 mechanotransduction proteins demonstrates:
- **72% Demand–Supply Anisotropy Gap** (p = 0.011, Mann-Whitney U)
- VIM Cascade failure mechanism (highest anisotropy proteins fail first)
- Supply-side disorder paradox (cheaper but more fragile supply proteins)
- PPARGC1A as metabolic bottleneck (52.7 pLDDT, 61.9% disordered)

### Key Findings Summary

1. Demand-side proteins (mechanosensors, cytoskeletal): mean anisotropy = 3.08 ± 1.44
2. Supply-side proteins (metabolic regulators): mean anisotropy = 1.79 ± 0.56
3. Gap = 72.3% (significantly larger than initial 34% estimate)
4. VIM Vulnerability Index = 3.11× supply mean
5. Scoliosis emerges when spinal length exceeds critical threshold where metabolic cost exceeds supply

---

## JOURNAL SPECIFICATIONS

### JOR Spine Requirements

**Scope:** Basic and translational orthopaedic research of the spine covering:
- Biomechanics
- Mechanobiology
- Development, growth, deformity
- Structure-function relationships
- Pre-clinical and clinical studies

**Your Fit:** HIGH – computational biomechanics of spinal development with mechanobiological validation

**Manuscript Format:**
- Standard research article: ~6,000–8,000 words
- Include abstract (250 words max)
- 4-6 figures/tables
- No page limit but concise preferred
- References: 60-80 citations (cite seminal + recent works)

**Audience:**
- Spine biomechanics researchers
- Orthopedic clinicians
- Developmental/mechanobiology scientists
- Computational modelers

**Submission Ready:**
- Formatted for journal guidelines
- All figures in high-resolution PDF/PNG
- All references complete with DOI/URL
- No placeholder text
- Professional writing, clear methodology

---

## MANUSCRIPT STRUCTURE & CONTENT GUIDANCE

### 1. TITLE (15–20 words)

**Requirement:** Clear, specific, telegraphs main finding without jargon

**Suggested Variants:**
1. "Energy Deficit Window and Structural Anisotropy: An Information–Elasticity Framework for Adolescent Idiopathic Scoliosis Onset"
2. "Mechanotransduction Demand–Supply Mismatch Drives Scoliotic Buckling During Adolescent Growth"
3. "Information–Cosserat Framework Reveals Metabolic Basis of Adolescent Scoliosis: AlphaFold Structural Analysis of 23 Mechanotransduction Proteins"

**Choose the one that best reflects your emphasis.**

---

### 2. ABSTRACT (250 words, structured)

**Format:** Background | Methods | Results | Conclusions

**Background Section (~60 words):**
- Why is spinal geometry vulnerable during adolescence?
- Current models insufficient
- Need mechanistic explanation linking development + geometry + pathology

**Methods Section (~80 words):**
- Information–Elasticity Coupling framework (IEC)
- Cosserat rod mechanics with developmental information field I(s)
- AlphaFold v6 structural analysis of 23 proteins (anisotropy ratios, disorder fractions, pLDDT)
- Phase diagram analysis across coupling strength and gravitational load

**Results Section (~80 words):**
- IEC selects S-curve as energetically favorable ground state
- Reproduces normal lordosis (42°) and kyphosis (35°)
- 72% Demand–Supply Anisotropy Gap (p = 0.011)
- Scoliosis emerges at supercritical bifurcation when L > L_crit ≈ 0.38 m
- Energy Deficit Window quantifies vulnerable growth period

**Conclusions Section (~30 words):**
- Spinal geometry as thermodynamic standing wave
- Growth rate trades off against proprioceptive maturation
- Specific testable predictions

---

### 3. INTRODUCTION (1,200–1,400 words)

**Subsection 3.1: The Gravity-Information Equivalence** (~350 words)
- Biological organisms resist gravity through active information-driven geometry
- Spinal S-curve is mechanically unstable (would sag to C-shape passively)
- Healthy spine maintains complex sagittal profile despite gravitational moment
- Segmental identity (HOX genes) alone insufficient—need continuous patterning mechanism
- Introduce the "Translation Problem": discrete genetic code → continuous 3D geometry

**Subsection 3.2: Mechanosensory Band-Pass Filter** (~300 words)
- Cells sense deformation, not gravity directly
- Two sensor classes:
  - **Phasic Vector Sensors** (Piezo2, muscle spindles): detect strain rate, directional → expensive
  - **Tonic Scalar Sensors** (Piezo1, Lamin A/C): detect hydrostatic pressure, omnidirectional → cheaper
- Healthy morphogenesis requires coherent integration (Vector–Scalar Match)
- Proprioceptive dysfunction → "Vector-Scalar Mismatch" → geometric instability

**Subsection 3.3: The Thermodynamic Standing Wave** (~350 words)
- Spine is NOT passive mechanical equilibrium
- Spine is **dissipative structure** (Prigogine) maintained by continuous ATP expenditure
- Thermodynamic Cost of Counter-Curvature: P_counter scales with L^2–L^3
- Allometric mismatch: gravitational moment scales L^3, nutrient transport L^2
- Energy Deficit Window emerges when metabolic demand exceeds supply

**Subsection 3.4: Critical Predictions** (~400 words)
- Three specific falsifiable predictions distinguishing IEC from pure mechanical buckling
- Prediction 1: Piezo1 silencing phenocopies microgravity osteopenia
- Prediction 2: High-anisotropy proteins ("Mechanical Antennas") collapse in energy deficit
- Prediction 3: Circadian clock resynchronization rescues scoliosis progression
- Five longstanding AIS questions addressed:
  1. Why rapid growth during adolescence?
  2. Why distinct curve patterns (Lenke types)?
  3. Why ~10× female predominance?
  4. Quantitative molecular evidence for energy deficit?
  5. Root causes of energy supply failure?

---

### 4. METHODS (800–1,000 words)

**Subsection 4.1: Information–Elasticity Coupling Framework**
- Define biological information field I(s) emerging from HOX patterning
- Information-modified effective metric: g_eff(s) = 1 + β₁I(s) + β₂I(s)²
- Cosserat rod free energy functional: U_IEC = elastic bending + information coupling + gravitational potential
- Dimensionless coupling strengths χ_κ (curvature), χ_E (extensibility)

**Subsection 4.2: Computational Implementation**
- Linearized eigenvalue problem for mode selection
- Full 3D Cosserat rod simulations using PyElastica (cite Gazzola et al.)
- Parameter space: χ_κ ∈ [0.01, 0.15], g ∈ [0, 1.0]
- Sensitivity analysis: ±10% parameter variation

**Subsection 4.3: AlphaFold Structural Analysis**
- Fetched 23 proteins from AlphaFold Database v6
- Computed structural metrics from Cα coordinates:
  - **Anisotropy Ratio:** √(λ₁/λ₃) from gyration tensor eigenvalues
  - **Disorder Fraction:** residues with pLDDT < 50
  - **Mean pLDDT:** AlphaFold confidence score
  - **Hinge Candidates:** potential flexible hinges (pLDDT < 60 flanked by confident regions)
- Categorized as Demand (mechanosensors, cytoskeletal, n=12) vs Supply (metabolic, n=11)

**Subsection 4.4: Statistical Methods**
- Mann-Whitney U test (one-sided) for Demand vs Supply anisotropy
- Welch's t-test for unequal variances
- Cohen's d for effect size
- Sensitivity analysis via parameter sweeps

**Subsection 4.5: Model Validation**
- Compare predicted lordosis/kyphosis angles to clinical norms
- Reproduce scoliosis onset timing (Cobb angle emergence at L_crit)
- Phase diagram predictions: three regimes (gravity-dominated, cooperative, information-dominated)
- AlphaFold predictions consistent with published epidemiology (sex differences, age of onset)

---

### 5. RESULTS (1,200–1,600 words)

**Subsection 5.1: Mode Spectrum and S-Curve Selection**
- Figure: Eigenvalues as function of χ_κ
- Passive beam ground state: monotonic C-shaped sag
- As χ_κ increases: S-shaped mode becomes lowest energy
- Quantitative: S-mode eigenvalue decreases 30% relative to C-mode in cooperative regime
- Conclusion: Spinal curve is gravity-selected eigenmode of information-coupled system

**Subsection 5.2: 3D Cosserat Rod Solutions**
- Figure: Equilibrium spine shape (3D visualization)
- Predicted lumbar lordosis: 42° ± 5° (clinical norm: 40–60°)
- Predicted thoracic kyphosis: 35° ± 4° (clinical norm: 20–45°)
- Robustness: geodesic deviation D_geo = 0.113 ± 0.011 across parameter variations
- Microgravity persistence: S-curve maintained even as g → 0 (explains astronaut observations)

**Subsection 5.3: Phase Diagrams**
- Figure: State diagram across (χ_κ, g) space
- Three regimes clearly delineated
- Gravity-dominated (low χ_κ, high g): passive C-shape, D_geo ≈ 0.059
- Cooperative (χ_κ ≈ 0.05, g = 1.0): stable S-curve, D_geo ≈ 0.150
- Information-dominated (high χ_κ): over-sensitive, D_geo > 0.3

**Subsection 5.4: Scoliosis Emergence via Bifurcation**
- Figure: Cobb angle vs asymmetry strength, parameterized by χ_κ
- Supercritical bifurcation at χ_κ ≈ 0.06
- In cooperative regime (χ_κ < 0.06): 5% asymmetry → Cobb < 5°
- In information-dominated regime (χ_κ > 0.08): 5% asymmetry → Cobb > 15°
- Clinical threshold for intervention (~15°) matches model prediction

**Subsection 5.5: Growth Dynamics and Adolescent Onset**
- Figure: Cobb angle vs spinal length, showing bifurcation window
- Growth spurt (L: 0.35 → 0.45 m) simulates pubertal elongation
- At L < L_crit ≈ 0.38 m: system stable, asymmetries suppressed
- At L > L_crit: supercritical bifurcation, scoliosis amplification
- Matches clinical AIS onset window (age 10–14 years, rapid growth)

**Subsection 5.6: Thermodynamic Cost and Energy Deficit Window**
- Figure: Metabolic demand P_counter vs proprioceptive supply S_proprio vs spinal length L
- P_counter ∝ L² (under isometric growth assumptions)
- S_proprio ∝ L^0.5 (sublinear)
- Energy Deficit Window: L > L_crit ≈ 0.35 m (approx. 35 cm spine)
- At L = 0.45 m: metabolic demand exceeds supply by 45.8% (P_counter ≈ 1.46 S_proprio)

**Subsection 5.7: AlphaFold Structural Analysis - Demand vs Supply**
- Table 1: Complete metrics for all 23 proteins (anisotropy, pLDDT, disorder, Rg, hinges)
- Figure: Anisotropy bar chart (all proteins sorted, color-coded Demand/Supply)
- Demand mean anisotropy: 3.08 ± 1.44 (n=12)
- Supply mean anisotropy: 1.79 ± 0.56 (n=11)
- **Gap = 72.3%** (p = 0.011, Mann-Whitney U, Cohen's d = 1.19) ✓ SIGNIFICANT

**Subsection 5.8: VIM Cascade Failure Sequence**
- Figure: Anisotropy (bars) + disorder fraction (line) for 7 cascade proteins
- VIM (5.57) → LMNA (4.71) → PIEZO2 (3.45) → CAV1 (2.52) → PIEZO1 (3.14) → EGR3 (1.56) → LBX1 (1.36)
- Vulnerability Index: VIM/supply_mean = 3.11×
- Predicted failure sequence matches theoretical cascade

**Subsection 5.9: Supply-Side Disorder Paradox**
- Figure A: Grouped bar chart (Anisotropy, Disorder %, pLDDT) Demand vs Supply
- Figure B: Spotlight on fragile supply proteins (PPARGC1A, COL1A1, SOX9, GHR, SIRT1)
- PPARGC1A confirmed as bottleneck: pLDDT = 52.7, 61.9% disordered
- Positive feedback trap: energy scarcity → PGC-1α degradation → fewer mitochondria → less ATP

---

### 6. DISCUSSION (1,400–1,800 words)

**Subsection 6.1: Interpreting Biological Counter-Curvature**
- Spine as standing wave vs passive equilibrium
- Information field as warped effective metric
- Organism actively modifies internal geometry to survive
- S-curve is biological geodesic (path of least physiological resistance)
- Counter-curvature as dissipative structure (Prigogine framework)

**Subsection 6.2: The Energy Deficit Window and AIS Vulnerability**
- Bifurcation at L_crit corresponds to energy deficit window
- Metabolic cost scaling explains temporal vulnerability
- Supply-demand mismatch during 2–3 year growth spurt
- Adolescents with high basal metabolic capacity (athletic) partially protected
- Metabolic/nutritional deficiencies increase risk

**Subsection 6.3: Molecular Evidence from AlphaFold**
- Demand proteins costly to maintain (high anisotropy)
- Supply proteins individually cheap but collectively constrained by bottleneck (PPARGC1A)
- Structural hierarchy explains vulnerability cascade
- VIM as first-failing sensor (highest anisotropy, extreme cost)

**Subsection 6.4: Why Different AIS Curve Patterns?**
- Curve patterns are eigenmodes of coupled Cosserat system
- Linearized system: κ(s,t) = A exp(λt) sin(nπs/L)
- Mode number n corresponds to Lenke type:
  - n=1: Type 5 (single C-curve)
  - n=2: Type 3 (double major, most common)
  - n=3: Type 4 (triple curve, rare)
- Regional variation in bending stiffness, proprioceptive gain, energy deficit explains pattern selection

**Subsection 6.5: Why More Scoliosis in Girls?**
- Girls reach PHV earlier (11–12 vs 13–14 years), deeper metabolic trough (R_peak ≈ 2.7 vs 2.4)
- Three compounding factors:
  1. Metabolic dimorphism (higher body fat %, less favorable mass-to-force ratio)
  2. PPARGC1A expression ~15% lower in female paraspinal muscles
  3. Sex differences in GH secretion pattern (continuous vs pulsatile)
- Female vulnerability: earlier onset (lower L_crit), deeper deficit (higher R_peak), longer exposure

**Subsection 6.6: Six Mechanisms of Energy Supply Failure**
- (i) Mitochondrial biogenesis ceiling (PPARGC1A paradox)
- (ii) Vascular supply limitation (segmental artery elongation lags tissue expansion)
- (iii) Circadian desynchrony (Spinal Jetlag, disrupted matrix repair)
- (iv) Modern mismatch (secular height increase exceeds evolutionary optimization)
- (v) Micronutrient deficit (NAD+, Vitamin D, iron, B-vitamins)
- (vi) Recursive supply constraint (supply machinery itself expensive)

**Subsection 6.7: Alternative Mechanisms and Discrimination**
- Address alternative hypotheses: active muscle tone, disc wedging, ligament pre-stress
- Discriminating experiments:
  - Longitudinal imaging during development (in utero ultrasound/MRI)
  - Ex vivo biomechanical testing of isolated segments
  - Finite element patient-specific modeling with IEC parameter fitting

**Subsection 6.8: Why Rapid Adolescent Growth?**
- Cost of maintaining counter-curvature ∝ L^4
- Scaling Catch-22: every centimeter exponentially more expensive
- Natural selection favored rapid transit through deficit zone (minimize damage accumulation)
- GHR (highest supply anisotropy) as molecular signature of gravitational selection pressure

**Subsection 6.9: Limitations and Model Assumptions**
- Information field I(s) treated as static; in reality emergent from reaction-diffusion
- Simplified continuous rod approximation; vertebral anatomy complex
- Mapping genes → I(s) remains phenomenological
- AlphaFold v6 may fragment large proteins (PIEZO1, PIEZO2); full-length structures preferred
- Parameter identifiability challenges; inverse problem requires clinical imaging data

**Subsection 6.10: Testable Predictions and Experimental Validation**
- **HOX Perturbation:** Hoxc9 knockout in lumbar somites → 20° reduction in lordosis
- **Microgravity Persistence:** Astronaut spinal MRI showing D_geo > 0.15 despite 100% gravitational unloading
- **Scoliosis Biomarkers:** High-χ_κ patients (inferred from FE fitting) → 2× faster progression
- **Zebrafish:** Ciliary flow perturbation → scoliosis only during somitogenesis (24–36 hpf), not post-segmentation

**Subsection 6.11: Future Directions and Clinical Translation**
- Patient-specific IEC parameter estimation from MRI/EOS imaging
- Predictive risk stratification for AIS progression
- Therapeutic interventions targeting PPARGC1A (mitochondrial biogenesis enhancers) or circadian synchronization
- Coupling IEC to volumetric growth laws for full developmental time-course modeling

---

### 7. CONCLUSIONS (300–400 words)

Synthesize findings into impact statement:
- Spinal geometry maintained as thermodynamic standing wave (dissipative structure)
- Energy deficit window explains why adolescence is vulnerable
- 72% Demand–Supply Anisotropy Gap quantifies molecular basis of AIS susceptibility
- VIM Cascade identifies first-failing mechanotransduction proteins
- Framework generates testable predictions across multiple scales (molecular, structural, clinical)
- Opens new therapeutic avenues (metabolic/circadian intervention, not just mechanical bracing)

---

### 8. REFERENCES (60–80 citations)

**Reference Categories (ensure broad coverage):**

**Foundational Spine Biomechanics (5-8):**
- Goriely 2017 (Mathematics of vertebrate morphogenesis)
- Moulton 2013 (Morphoelastic rod theory)
- Gazzola 2018 (Elastica computational framework)
- O'Reilly 2017 (Cosserat rod mechanics)

**Spinal Development and HOX (5-7):**
- Wellik 2007 (HOX genes and vertebral identity)
- Pourquié 2011 (Vertebrate somitogenesis)
- Kmita & Duboule 2003 (Collinearity and temporal colinearity)

**Mechanotransduction and Proprioception (8-10):**
- Ranade 2014 (Piezo2 as proprioceptor)
- Swift 2013 (Lamin A/C and nuclear mechanotransduction)
- Vogel & Sheetz 2006 (Cell mechanotransduction)
- Ingber 2006 (Cellular tensegrity)

**Scoliosis - Genetic and Clinical (8-10):**
- Cheng 2015 (AIS epidemiology)
- Weinstein 2008 (Natural history of AIS)
- Wise et al. 2020 (Genetic susceptibility loci)
- Gorman et al. 2021 (AIS etiology review)

**AlphaFold and Protein Structure (5-7):**
- Jumper et al. 2021 (AlphaFold2 methods)
- Varadi et al. 2022 (AlphaFold Database)
- Nava et al. 2020 (Protein disorder and function)

**Thermodynamics and Dissipative Structures (4-6):**
- Prigogine & Nicolis 1977 (Self-organizing systems)
- Parrondo et al. 2015 (Thermodynamics of computation)
- England 2013 (Statistical mechanics of dissipation)

**Growth and Allometry (3-5):**
- West et al. 1997 (Scaling laws in biology)
- Rolfe & Brown 1997 (Cellular metabolism)
- Thompson 1917 (On Growth and Form)

**Circadian Biology and Bone (4-6):**
- Bass & Takahashi 2010 (Circadian physiology)
- Dudek et al. 2017 (Circadian regulation of bone)
- Takahashi 2017 (Molecular genetics of the clock)

**Recent High-Impact AIS Research (5-7):**
- Boswell & Gray 2024 (Ciliary flow and scoliosis)
- Grimes et al. 2016 (Zebrafish scoliosis model)
- Ugur et al. 2024 (Hypoxia and scoliosis prevention)

**Additional Key Citations:**
- Taber 1995 (Biomechanics of morphogenesis)
- Beloussov 1998 (Morphomechanics)
- Discher et al. 2005 (Matrix mechanics and cell behavior)
- Levin 2012 (Morphogenetic fields)

---

## FIGURES & TABLES

### Required Figures (6 total, all as high-res PDF + PNG)

1. **Figure 1: IEC Framework Schematic**
   - Panel A: Spinal column with information field I(s) overlaid
   - Panel B: Effective metric g_eff(s) showing increased arc-length in lordotic/kyphotic zones
   - Panel C: Free energy landscape (passive C vs IEC-driven S)

2. **Figure 2: Mode Spectrum and Phase Diagram**
   - Panel A: Eigenvalue spectrum as function of χ_κ (shows S-mode becoming ground state)
   - Panel B: Phase diagram (χ_κ vs g) showing three regimes with D_geo contours
   - Panel C: Representative equilibrium shapes in each regime

3. **Figure 3: 3D Cosserat Rod Solutions**
   - Panel A: Predicted spine shape (superior view showing S-curve)
   - Panel B: Sagittal profile with annotated lordosis/kyphosis angles
   - Panel C: Robustness to parameter variation (D_geo vs parameter sweeps)
   - Panel D: Microgravity persistence (D_geo vs g, showing maintained curvature at g→0)

4. **Figure 4: AlphaFold Anisotropy Bar Chart**
   - All 23 proteins sorted by anisotropy (descending)
   - Color-coded: Demand (red), Supply (blue)
   - Demand mean line, Supply mean line, annotated 72% gap
   - Highest: VIM, PTK7, LMNA; Lowest: COL1A1, SOX9, SIRT1

5. **Figure 5: Scatter Panels**
   - Panel A: Anisotropy vs Disorder Fraction (with protein labels for outliers)
   - Panel B: Anisotropy vs pLDDT (confidence vs structure)
   - Panel C: Box plot + individual points showing Mann-Whitney U test (p=0.011)

6. **Figure 6: Growth Dynamics & Scoliosis Emergence**
   - Panel A: Cobb angle vs spinal length (bifurcation at L_crit)
   - Panel B: Energy Deficit Window (metabolic demand vs supply vs L)
   - Panel C: Heatmap of pLDDT per-residue for VIM vs PPARGC1A (showing fragility contrast)

### Required Tables (2–3 total)

1. **Table 1: AlphaFold Structural Metrics (23 proteins)**
   - Columns: Gene, UniProt ID, Category, Role, Seq Length, Mean pLDDT, Anisotropy, Disorder %, Rg (Å), Hinges
   - Rows: Demand first (sorted by anisotropy desc), then Supply
   - Caption: Methods, data source, interpretation

2. **Table 2: Comparison of Predicted vs Clinical Spinal Angles**
   - Rows: Lumbar lordosis, Thoracic kyphosis
   - Columns: Model Prediction (mean ± SD), Clinical Norm Range, n=studies
   - Shows validation against literature

---

## WRITING STYLE & TONE

- **Audience:** Spine biomechanics researchers + orthopedic clinicians
- **Tone:** Professional, data-driven, accessible (avoid jargon unless defined)
- **Active voice preferred** except in methods
- **Clarity over elegance:** Direct statements, short sentences
- **Quantitative:** All claims supported by model results or citations
- **Clinical relevance emphasized:** Tie computational findings to AIS pathophysiology

---

## CRITICAL REQUIREMENTS

✅ **Must Include:**
- All 23 AlphaFold proteins with corrected metrics (72% gap, not 34%)
- Statistical tests (Mann-Whitney U p-value, Cohen's d)
- 3 specific falsifiable predictions for experimental validation
- Clear connection between energy deficit window and AIS onset age
- Discussion of sex differences rooted in metabolic dimorphism
- Comparison of predicted lordosis/kyphosis to clinical norms
- VIM Cascade failure sequence as central mechanism
- Acknowledgment of limitations (AlphaFold v6 fragmentation, static I(s) assumption, inverse problem)

✅ **Formatting:**
- Times New Roman 12pt or Arial 11pt
- 1.5 line spacing
- 1" margins
- Section headings numbered (Introduction 1.0, 1.1, 1.2, etc.)
- Figures embedded at end (or as separate PDF appendix)
- References in numbered format [1], [2], etc.

✅ **Tone:**
- Avoid overselling ("groundbreaking," "revolutionary")
- Acknowledge complexity ("model simplifications," "future work needed")
- Emphasize testable predictions ("can be validated by...")
- Bridge to clinicians ("implications for early detection...")

---

## DELIVERABLE

**Output:** Single Word document (.docx)
- Fully formatted, submission-ready
- All sections complete, no placeholder text
- Figures integrated (high-resolution, labeled)
- References complete with DOI/URL
- Ready to copy-paste into journal submission system

**File Name:** `JOR_Spine_Biological_Countercurvature_IEC_Framework_FINAL.docx`

---

## ADDITIONAL NOTES

- If narrative feels repetitive between sections, consolidate
- Ensure mathematical notation is consistent (use subscripts for clarity)
- Clinical examples in Discussion should resonate with spine surgeon audience
- Consider adding a "Graphical Abstract" (one-page visual summary) if journal supports it
- All figure captions should be self-contained (reader can understand figure from caption alone)

---

**Ready to generate. Use this prompt to create a comprehensive, journal-ready manuscript.**
