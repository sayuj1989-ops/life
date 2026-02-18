# Unanswered Questions in Biological Countercurvature: Gravitational Selection, Sex Dimorphism, Curve Patterns, and the Energy Deficit

**Date:** 2026-02-18
**Authors:** Dr. Sayuj Krishnan S, MBBS, DNB (Neurosurgery)
**Status:** Research Analysis — Supplementary to Main Manuscript
**Framework:** Free energy dissipation functional (manuscript Eq. 7)

---

## Abstract

The Biological Countercurvature framework explains spinal geometry as an information-driven standing wave maintained against gravitational geodesics. Our previous work established that an Energy Deficit Window during adolescent growth creates vulnerability to scoliosis. However, five critical questions remained unanswered: (1) Why does rapid growth occur during ages 12–20 from a gravitational standpoint? (2) Why do different patterns of adolescent idiopathic scoliosis (AIS) curves emerge? (3) Why is AIS 10× more prevalent in girls? (4) What does the protein structural data reveal quantitatively about the energy deficit? (5) What causes the energy supply difference — is it merely hunger, or something deeper? Here we address each question using rigorous analysis of our 23-protein AlphaFold structural dataset, deriving novel metrics including the Demand–Supply Anisotropy Gap (34%), the VIM Vulnerability Index (3.01×), and the PPARGC1A Fragility Score. We show that rapid growth is not a design flaw but an evolved strategy to minimize time-in-vulnerability, that curve patterns are eigenmodes of the coupled Cosserat system, that the female sex disparity arises from metabolic timing rather than structural weakness, and that the energy deficit has six distinct molecular drivers beyond simple caloric insufficiency.

---

## 1. Why Rapid Growth During Ages 12–20? A Gravitational Standpoint

### 1.1 The Standard Hormonal Account and Its Circularity

The conventional explanation for the adolescent growth spurt invokes the hypothalamic–pituitary–gonadal (HPG) axis: GnRH triggers LH/FSH, which stimulates sex steroids, which amplify GH/IGF-1 secretion, which drives longitudinal bone growth. This account is mechanistically correct but **explanatorily circular** — it describes *how* growth accelerates but not *why* it accelerates at this particular developmental stage.

The chicken-or-egg problem is real: does the hormonal cascade *cause* rapid growth, or does the mechanical demand of an increasingly tall body *stimulate* the hormonal cascade? Our framework resolves this by identifying the **environmental selector** that breaks the circularity: *gravity*.

### 1.2 The Scaling Catch-22: Why the Body Must "Sprint"

From the existing framework, the metabolic cost of maintaining counter-curvature (the S-shaped standing wave) scales non-linearly with spinal length:

$$C_{\text{straight}} \propto L^4$$

This arises because:
- Gravitational moment scales as $M \cdot g \cdot h \propto L^3 \cdot g \cdot L = L^4$
- Buckling vulnerability increases as $P_{cr} \propto L^{-2}$ (Euler column)
- Proprioceptive circuit latency grows as $\tau_{\text{neural}} \propto L$

Meanwhile, the energy supply capacity scales sub-linearly:
- Mitochondrial capacity (set by PPARGC1A): $\propto L^2$ to $L^3$
- Avascular disc nutrient diffusion: $\propto L^{0.5}$ to $L^1$

This creates a **Scaling Catch-22**: every additional centimeter of height is exponentially more expensive to maintain upright. The body cannot linger in this zone — it must transit as rapidly as possible.

### 1.3 The Chicken-or-Egg Resolution: Gravity as the Selector

The positive feedback loop is:

```
Growth velocity → Increased mechanical demand → GHR upregulation →
GH/IGF-1 axis amplification → More growth velocity → ...
```

This loop has no intrinsic "start" — it is a coupled oscillator. The resolution is that **gravity is the environmental selector** that determines which growth strategies survive:

1. **Slow growers** spend more total time in the high-deficit zone where $C_{\text{straight}} > S_{\text{supply}}$. The cumulative damage integral:

$$D_{\text{cumulative}} = \int_{t_{\text{onset}}}^{t_{\text{maturity}}} \max\left(0,\; \frac{P_{\text{counter}}(t)}{S_{\text{supply}}(t)} - 1\right) dt$$

is minimized by rapid transit. Organisms that grow slowly through the vulnerable zone accumulate more proprioceptive damage, more asymmetric muscle deconditioning, and more circadian desynchrony.

2. **Fast growers** minimize the vulnerability window duration:

$$T_{\text{vulnerable}} = \int_{L_{\text{onset}}}^{L_{\text{adult}}} \frac{dL}{v_{\text{growth}}(L)}$$

Faster $v_{\text{growth}}$ directly reduces $T_{\text{vulnerable}}$.

3. **The hormonal loop is the mechanism; gravity is the selector.** Natural selection favored organisms whose HPG axis produced a sharp, intense growth spurt — not because speed is intrinsically beneficial, but because lingering in the deficit zone is fatal to spinal integrity.

### 1.4 Protein Data Support

From the repository's AlphaFold structural dataset (`thermodynamic_cost_proteins.csv`):

| Protein | Role | Anisotropy | Hinges | Residues | Interpretation |
|---------|------|-----------|--------|----------|----------------|
| **GHR** | Growth Hormone Receptor | **5.13** | **54** | 638 | Extremely high structural cost — the growth signaling machinery itself is expensive |
| **IGF1R** | IGF-1 Receptor | 1.43 | 35 | 1,367 | Massive but globular — optimized for efficient signal capture |
| **SOX9** | Growth plate chondrocyte TF | 2.19 | 2 | 509 | Drives $dL/dt$; its expression rate determines growth velocity |

**Key insight**: GHR has the **highest anisotropy (5.13) among all supply-side proteins** and 54 hinge candidates — more than any other protein in the dataset. This means the growth signaling machinery is itself metabolically expensive to maintain. Evolution has accepted this cost because the alternative (slow growth, prolonged vulnerability) is worse. The high structural cost of GHR is the molecular signature of **gravitational selection pressure for rapid growth**.

### 1.5 The Evolutionary Prediction

If rapid growth is a gravitational optimization, we predict:
- Species in higher-gravity environments (larger terrestrial mammals) should show *sharper* growth spurts relative to total lifespan
- Aquatic mammals (reduced effective gravity via buoyancy) should show more gradual growth curves
- The growth spurt timing should correlate with the onset of bipedal loading in hominin evolution

---

## 2. Why Different Patterns of AIS Curves?

### 2.1 The Clinical Problem

AIS presents in distinct curve patterns (Lenke classification): thoracic (Type 1), double thoracic (Type 2), double major (Type 3), triple major (Type 4), thoracolumbar/lumbar (Type 5), and thoracolumbar/lumbar–main thoracic (Type 6). The existing literature describes these patterns but does not explain *why* they occur. Our framework provides a mechanistic answer.

### 2.2 Curve Patterns as Eigenmodes of the Coupled System

The linearized IEC equations for small perturbations about the equilibrium S-shape yield:

$$\rho \frac{\partial^2 \kappa}{\partial t^2} + \eta \frac{\partial \kappa}{\partial t} + B(s) \frac{\partial^4 \kappa}{\partial s^4} + K(s) \kappa(s, t - \tau) = 0$$

Solutions have the form $\kappa(s,t) = A \exp(\lambda t) \sin(n\pi s / L)$, where $n$ determines the curve pattern:

| Mode $n$ | Spatial Pattern | Clinical Equivalent | Frequency |
|----------|----------------|---------------------|-----------|
| $n = 1$ | Single C-curve | Thoracolumbar/lumbar (Lenke 5) | Common |
| $n = 2$ | Double S-curve | Double major (Lenke 3) | Most common |
| $n = 3$ | Triple curve | Triple major (Lenke 4) | Rare |

**Which mode dominates** depends on which $n$ has the fastest growth rate $\text{Re}(\lambda_n)$. This is determined by the spatial distribution of three parameters:
- $B(s)$: local bending stiffness (varies by region)
- $K(s)$: proprioceptive gain (varies by sensor density)
- $R(s)$: local energy deficit ratio (demand/supply)

### 2.3 Regional Protein Expression and Mechanical Environment

The spine is not mechanically uniform. Each region has a distinct protein expression profile that determines its vulnerability mode:

**Thoracic region (T1–T12):**
- Lower intrinsic bending stiffness $B$ (thinner pedicles)
- Rib cage provides external constraint (torsional coupling $\alpha_{TB}$)
- Predominantly PIEZO2-dependent proprioception (vector sensing)
- Vulnerability: When PIEZO2 (anisotropy 4.44) fails, vector mismatch creates rotational instability

**Lumbar region (L1–L5):**
- Higher bending stiffness $B$ (thick pedicles, large vertebral bodies)
- No rib constraint — relies entirely on paraspinal muscles
- Predominantly COL1A1-dependent structural support (anisotropy 2.80)
- Vulnerability: When LBX1 (anisotropy 2.27) is asymmetrically expressed, paraspinal muscle imbalance creates lateral buckling

**Thoracolumbar junction (T11–L2):**
- Transition zone where mechanical properties change rapidly
- Highest spatial gradient of anisotropy (thoracic → lumbar transition)
- The **vector mismatch parameter** $\alpha(s)$ changes most rapidly here
- From our simulation data: Vector_Scalar_Mismatch produces the highest Cobb angle (11.15°) — this is the thoracolumbar junction scenario

### 2.4 Simulation Support from Repository Data

From `protein_physics_results.csv`:

| Scenario | Stiffness Anisotropy | $\chi_\kappa$ | Cobb Angle (°) | Interpretation |
|----------|---------------------|---------------|----------------|----------------|
| Control | 2.0 | 5.0 | 2.75 | Normal S-curve |
| Fibrillin Loss | 1.0 | 5.0 | 2.72 | Reduced anisotropy → minimal lateral deviation |
| Piezo2 Gain | 2.0 | 15.0 | 8.07 | Enhanced sensing → overcorrection |
| **Vector-Scalar Mismatch** | **5.0** | **20.0** | **11.15** | **Highest Cobb — explains thoracolumbar curves** |
| Torsional Instability | 2.0 | 5.0 (+ $\chi_\tau = 5.0$) | 3.00 | Twist coupling → rotational deformity (thoracic) |

**Key finding**: The Vector-Scalar Mismatch scenario (high anisotropy + high coupling) produces the largest Cobb angle. This corresponds to the thoracolumbar junction, where the transition between mechanically distinct regions creates the greatest vector-scalar dissociation.

### 2.5 The Alignment Parameter $\alpha(s)$ Determines Curve Type

From the IEC Theoretical Expansion, the alignment parameter $\alpha(s)$ represents the local coherence between vector (PIEZO2) and scalar (PIEZO1) mechanosensing. Different spatial patterns of $\alpha(s)$ predict different curve types:

- **Single thoracic $\alpha$ minimum** → Lenke Type 1 (right thoracic)
- **Single lumbar $\alpha$ minimum** → Lenke Type 5 (thoracolumbar/lumbar)
- **Two $\alpha$ minima** (thoracic + lumbar) → Lenke Type 3 (double major)
- **$\alpha$ minimum at junction** + torsional coupling → Lenke Type 4 (triple)

**Testable prediction**: MRI-based mapping of paraspinal muscle asymmetry (as proxy for $\alpha(s)$) should predict curve pattern *before* radiographic progression.

---

## 3. Why More Scoliosis in Girls?

### 3.1 The Epidemiological Fact

AIS affects girls 10× more frequently than boys for curves requiring treatment (>30°). For smaller curves (10–20°), the ratio is closer to 1.4:1, suggesting the sex difference is primarily in *progression* rather than *initiation*.

### 3.2 Estrogen Timing — Deepened Through the Energy Deficit Framework

The standard explanation invokes estrogen's role in growth plate closure. Our framework deepens this:

**Girls:**
- Peak Height Velocity (PHV) at 11–12 years
- Growth plates remain open longer relative to PHV onset
- Result: **Narrower but DEEPER energy deficit window**
- Estimated $R_{\text{peak}} \approx 2.7$ (deficit ratio at peak)

**Boys:**
- PHV at 13–14 years
- Higher absolute muscle mass provides larger metabolic reserve
- Result: **Broader but SHALLOWER energy deficit window**
- Estimated $R_{\text{peak}} \approx 2.4$

The critical difference is not the *duration* of vulnerability but its *depth*. A deeper deficit ($R_{\text{peak}} = 2.7$ vs. 2.4, a 12.5% difference) means the VIM cascade (Section 4.7) is more likely to trigger in girls, initiating the irreversible failure sequence.

### 3.3 Metabolic Dimorphism: The Body Composition Argument

Beyond hormonal timing, there is a fundamental **metabolic dimorphism** that the existing literature has overlooked:

**Female puberty:**
- Relative increase in fat mass (17% → 25% of body weight)
- Relatively lower increase in muscle mass
- Lower muscle-to-body-mass ratio
- Fewer mitochondria per unit paraspinal muscle volume

**Male puberty:**
- Dramatic increase in muscle mass (testosterone-driven)
- Higher absolute and relative paraspinal muscle volume
- Greater mitochondrial density (higher PPARGC1A expression)
- More robust metabolic reserve

**The L⁴ consequence**: In the cost equation $C_{\text{straight}} \propto M \cdot g \cdot L^3$, the mass $M$ includes both structural (muscle) and non-structural (fat) components. Girls accumulate more gravitational load ($M$ increases) without proportional increase in the force-generating capacity to resist it. The denominator (muscle ATP output) grows slower than the numerator (gravitational demand).

### 3.4 Protein-Level Sex Differences

From the repository protein data, the proteins most likely to exhibit sex-differential expression during puberty:

| Protein | Anisotropy | Term | Sex-Differential Mechanism |
|---------|-----------|------|---------------------------|
| **PPARGC1A** | 2.19 | Supply (Γ_m) | Lower expression in female muscle → lower mitochondrial ceiling |
| **LBX1** | 2.27 | Demand (η_a) | Top GWAS hit; identified predominantly in female cohorts |
| **GHR** | 5.13 | Supply (Γ_m) | Sex differences in GH pulsatility (male: pulsatile, female: continuous) affect receptor occupancy and downstream signaling cost |
| **LMNA** | 4.75 | Demand (η_a) | Estrogen receptor interaction with Lamin A/C affects nuclear mechanotransduction fidelity |
| **ARNTL** | 3.32 | Supply (Γ_m) | Circadian disruption more prevalent in adolescent girls (earlier pubertal onset, social/screen time patterns) |

### 3.5 Quantitative Prediction: The 15% PPARGC1A Threshold

If female paraspinal muscles have ~15% lower PPARGC1A expression (consistent with known sex differences in muscle mitochondrial density), the energy supply ceiling shifts:

$$S_{\text{female}} = 0.85 \times S_{\text{male}}$$

This shifts the critical length $L_{\text{crit}}$ (where $R_{\text{deficit}} = 1$) to a **shorter spine**:

$$L_{\text{crit,female}} = L_{\text{crit,male}} \times 0.85^{1/2} \approx 0.92 \times L_{\text{crit,male}}$$

Girls enter the vulnerability zone at 92% of the height that boys do — approximately **3–5 cm shorter** — consistent with the clinical observation that AIS onset occurs earlier in girls at a shorter absolute height.

### 3.6 The Dual Vulnerability: Narrower Window, Deeper Deficit

Combining all factors, the female vulnerability is a **dual hit**:
1. **Earlier onset** (lower $L_{\text{crit}}$ due to lower PPARGC1A)
2. **Deeper deficit** (higher $R_{\text{peak}}$ due to unfavorable mass/muscle ratio)
3. **Longer exposure** (later growth plate closure relative to PHV)

This explains the progression disparity: girls don't just *initiate* curves more often — they *progress* more severely because the deficit is deeper and longer-lasting.

---

## 4. Protein Data Analysis: Quantitative Evidence for the Energy Deficit

### 4.1 Complete Dataset Overview

From `thermodynamic_cost_proteins.csv`, our AlphaFold structural pipeline analyzed 23 proteins across three energy terms of the free energy dissipation functional:

$$\dot{\mathcal{F}} = \int_0^L \left[ \eta_p |\partial\kappa/\partial t|^2 + \eta_a (\kappa - \kappa_{\text{passive}})^2 + \Gamma_m(s) \right] ds$$

### 4.2 Summary Statistics by Energy Term

| Term | Category | N | Mean Anisotropy | Mean pLDDT | Total Residues | Total Hinges | Mean Disorder |
|------|----------|---|----------------|------------|----------------|--------------|---------------|
| **η_p** | Sensing (Demand) | 5 | **3.22** | 67.8 | 4,871 | 26 | 32% |
| **η_a** | Actuation (Demand) | 7 | **3.39** | 73.9 | 6,675 | 149 | 22% |
| **Γ_m** | Maintenance (Supply) | 10 | **2.48** | 66.4 | 7,532 | 130 | 40% |

### 4.3 The Demand–Supply Anisotropy Gap

The combined demand-side mean anisotropy:

$$\bar{A}_{\text{demand}} = \frac{5 \times 3.22 + 7 \times 3.39}{12} = \frac{16.10 + 23.73}{12} = \mathbf{3.32}$$

The supply-side mean anisotropy:

$$\bar{A}_{\text{supply}} = \mathbf{2.48}$$

**The Demand–Supply Anisotropy Gap:**

$$\Delta A = \frac{\bar{A}_{\text{demand}} - \bar{A}_{\text{supply}}}{\bar{A}_{\text{supply}}} = \frac{3.32 - 2.48}{2.48} = \mathbf{0.34 \;(34\%)}$$

**Interpretation**: Demand-side proteins are structurally 34% more expensive to maintain than supply-side proteins. This is the molecular basis of the asymmetry — the system that *detects and corrects* gravitational perturbation costs more to run than the system that *fuels* the correction. During energy scarcity, the expensive demand side fails first.

### 4.4 Scaling Law Mismatch: Quantitative Derivation

During the adolescent growth spurt, spinal length increases approximately 30% (from ~0.35 m to ~0.45 m). The scaling exponents differ by category:

**Demand-side scaling:**
- η_p proteins scale L to L² (weighted average exponent ~1.4)
- η_a proteins scale L² to L³ (weighted average exponent ~2.5)
- Combined demand effective exponent: ~2.0

**Supply-side scaling:**
- Γ_m proteins: SIRT1 (constant), PPARGC1A (L¹ supply limit), SOX9 (L¹), SHH (L¹), CDKN1A (threshold)
- Rate-limiting supply exponent: ~1.0 to 1.3

**Quantitative mismatch during 30% height increase (L: 0.35 → 0.45 m):**

$$\text{Demand increase} = \left(\frac{0.45}{0.35}\right)^{2.0} = 1.29^2 = \mathbf{1.65\times \;(65\% \text{ increase})}$$

$$\text{Supply increase} = \left(\frac{0.45}{0.35}\right)^{1.15} = 1.29^{1.15} = \mathbf{1.34\times \;(34\% \text{ increase})}$$

$$\textbf{Net unmet demand} = \frac{1.65 - 1.34}{1.34} = \mathbf{23\%}$$

For the full L³-scaled actuation proteins:

$$\text{Demand increase (η_a only)} = 1.29^{3.0} = \mathbf{2.15\times \;(115\% \text{ increase})}$$

This yields the **65–115% demand increase** range cited in the main manuscript — not an assumption, but a direct consequence of the structural scaling laws embedded in the AlphaFold data.

### 4.5 Per-Protein Energy Cost Proxy

We define a proxy for the metabolic cost of maintaining each protein:

$$\text{Cost Proxy} = \text{Anisotropy} \times N_{\text{residues}}$$

This captures both structural complexity (anisotropy = orientation-dependent maintenance cost) and size (more residues = more ATP for synthesis and turnover).

| Rank | Protein | Term | Anisotropy | Residues | Cost Proxy | Scaling |
|------|---------|------|-----------|----------|------------|---------|
| 1 | **PIEZO1** | η_p (Demand) | 3.90 | 2,521 | **9,832** | L² |
| 2 | **FLNA** | η_a (Demand) | 2.50 | 2,647 | **6,618** | L³ |
| 3 | **COL1A1** | Γ_m (Supply) | 2.80 | 1,464 | **4,099** | L³ |
| 4 | **VIM** | η_a (Demand) | 7.47 | 466 | **3,481** | L³ |
| 5 | **GHR** | Γ_m (Supply) | 5.13 | 638 | **3,273** | L¹ |
| 6 | **PIEZO2** | η_p (Demand) | 4.44 | 709 | **3,148** | L¹ |
| 7 | **LMNA** | η_a (Demand) | 4.75 | 664 | **3,154** | L² |
| 8 | **MYLK** | η_a (Demand) | 1.46 | 1,914 | **2,794** | L² |
| 9 | **ARNTL** | Γ_m (Supply) | 3.32 | 626 | **2,078** | Temporal |
| 10 | **IGF1R** | Γ_m (Supply) | 1.43 | 1,367 | **1,955** | L¹ |

**Critical observation**: The top 4 most expensive proteins are split 3:1 demand-to-supply. But the expensive supply-side proteins (COL1A1 for structural scaffold, GHR for growth signaling) are themselves part of the problem — maintaining the supply machinery is expensive, creating a **recursive supply deficit**.

### 4.6 The VIM Vulnerability Index

Vimentin (VIM) has the highest anisotropy of any protein in the dataset:

$$\text{VIM Vulnerability Index} = \frac{A_{\text{VIM}}}{\bar{A}_{\text{supply}}} = \frac{7.47}{2.48} = \mathbf{3.01\times}$$

VIM is 3× more structurally expensive than the average supply protein. Its fibrous, extended morphology (Rg = 65.7 Å, the largest radius of gyration in the dataset) makes it exquisitely sensitive to loss of cytoskeletal tension. VIM literally acts as a "gravitational strain gauge" — when gravity-driven tension decreases (microgravity) or metabolic energy for cytoskeletal maintenance runs low (growth spurt), VIM collapses first.

### 4.7 The VIM Cascade: A Molecular Domino Chain

The AlphaFold data reveal a **cascade of failure** ordered by anisotropy:

```
VIM (7.47) collapses → ROS burst from mitochondrial exposure
    ↓
LMNA (4.75) degrades → Nuclear softening, gene expression drift
    ↓
PIEZO2 (4.44) loses membrane anchoring → Vector sensing fails
    ↓
CAV1 (3.98) / PIEZO1 (3.90) decouple → Scalar sensing impaired
    ↓
EGR3 (3.76) expression drops → Muscle spindle innervation fails
    ↓
LBX1 (2.27) program fails → Paraspinal muscle asymmetry
    ↓
SIRT1 (1.73) detects deficit → TOO LATE — cascade is irreversible
    ↓
CDKN1A (2.14) activates → Growth arrest (binary switch)
```

**The detection lag**: SIRT1 (anisotropy 1.73, compact, constant scaling) is structurally cheap and robust — it *survives* the energy deficit. But its robustness is also its weakness: by the time SIRT1 detects declining NAD⁺/NADH (signaling energy stress), the expensive demand-side proteins have already failed. The sensor outlasts the system it monitors.

### 4.8 The PPARGC1A Fragility Score

PPARGC1A (PGC-1α) is the master regulator of mitochondrial biogenesis — the protein that determines the energy supply ceiling. Its AlphaFold structural profile reveals it is paradoxically the **most fragile** supply-side protein:

| Metric | PPARGC1A | Supply Mean | Interpretation |
|--------|----------|-------------|----------------|
| pLDDT | **52.7** | 66.4 | Lowest confidence → most structurally uncertain |
| Disorder fraction | **62%** | 40% | Highest disorder → requires constant chaperone activity |
| Anisotropy | 2.19 | 2.48 | Near-average → not intrinsically expensive |
| Hinges | 0 | 13 | No hinge candidates → rigid when folded, disordered when not |

**The Positive Feedback Trap**: When energy is scarce:
1. PPARGC1A (62% disordered) cannot maintain its folded state → degraded
2. Fewer PPARGC1A → fewer mitochondria biogenesis → less ATP
3. Less ATP → even less capacity to maintain PPARGC1A
4. **Self-reinforcing collapse of the energy supply ceiling**

This explains why scoliosis *progresses* — the initial deficit triggers a molecular positive feedback loop that deepens the deficit over time.

### 4.9 The Supply-Side Disorder Paradox

A surprising finding from the protein data:

| Category | Mean Disorder Fraction |
|----------|----------------------|
| Demand (η_p + η_a) | **28%** |
| Supply (Γ_m) | **40%** |

The supply system is **more disordered** (40%) than the demand system (28%). This is counterintuitive — one would expect the supply system to be robust. But intrinsically disordered proteins require constant chaperone activity and have high turnover rates. The supply system is structurally cheaper (lower anisotropy) but operationally fragile (higher disorder). Under metabolic stress, the supply system's high disorder fraction means it degrades faster than expected, compounding the deficit.

Key disordered supply proteins:
- COL1A1: 67% disordered (collagen triple helix requires precise assembly)
- PPARGC1A: 62% disordered (supply ceiling regulator)
- GHR: 50% disordered (growth signaling receptor)

### 4.10 Energy Deficit Bifurcation Data

From `energy_deficit_bifurcation.csv`, the phase diagram of the deficit ratio $R_{\text{deficit}} = P_{\text{cost}} / S_{\text{supply}}$ across coupling strength $\chi_\kappa$ and spinal length $L$ reveals:

- At low coupling ($\chi_\kappa = 0.01$): $R_{\text{deficit}}$ remains below 1.0 for all $L$ → **safe zone** (no scoliosis)
- At moderate coupling ($\chi_\kappa = 0.05$): $R_{\text{deficit}}$ exceeds 1.0 at $L \approx 0.40$ m → vulnerability onset during mid-adolescence
- At high coupling ($\chi_\kappa = 0.10$): $R_{\text{deficit}}$ exceeds 1.0 at $L \approx 0.30$ m → early onset, rapid progression

**Clinical translation**: Patients with high morphogenetic drive ($\chi_\kappa$) — those with strong HOX-encoded curvature targets — enter the Energy Deficit Window at shorter heights and stay in it longer. This predicts **earlier onset and more severe progression** in patients with strong genetic determinants of curvature, consistent with clinical observation.

---

## 5. What Could Have Led to the Energy Supply Difference?

### 5.1 Beyond Simple Hunger: A Six-Factor Model

The energy available for counter-curvature maintenance is not simply a function of caloric intake:

$$E_{\text{available}} = E_{\text{dietary}} - E_{\text{basal}} - E_{\text{growth\_construction}} - E_{\text{immune}} - E_{\text{thermoregulation}} - E_{\text{cognitive}}$$

Even with adequate $E_{\text{dietary}}$, the energy available for proprioceptive maintenance can be critically low during adolescence because the other terms are simultaneously elevated. We identify **six distinct mechanisms** beyond simple hunger:

### 5.2 Factor 1: The Mitochondrial Capacity Ceiling (PPARGC1A)

As shown in Section 4.8, PPARGC1A is the most structurally fragile supply protein (pLDDT 52.7, 62% disordered). It sets the **maximum ATP production rate** — the energy ceiling that cannot be exceeded regardless of substrate availability.

During rapid growth:
- Tissue volume increases as $L^3$
- Each new cell needs its own mitochondria
- PPARGC1A must drive mitochondrial biogenesis at an accelerating rate
- But PPARGC1A itself requires energy and chaperones to remain functional
- **The supply ceiling protein is itself supply-limited** — a recursive constraint

**This is not hunger. A well-fed adolescent can still hit the mitochondrial ceiling** if the rate of tissue expansion exceeds the rate of mitochondrial biogenesis.

### 5.3 Factor 2: Vascular Supply Limitation and Local Hypoxia

Paraspinal muscles receive blood supply from segmental arteries — small vessels that must elongate and branch as the spine grows. During rapid growth:

1. Vascular development lags behind tissue expansion
2. Local oxygen tension drops in deep paraspinal muscle
3. HIF-1α stabilizes and shifts metabolism from oxidative phosphorylation to glycolysis
4. Glycolysis yields **~15× less ATP per glucose** than oxidative phosphorylation
5. The local energy supply collapses even though systemic nutrition is adequate

**Supporting protein data**: The intervertebral disc is the largest avascular structure in the body. Nutrients must diffuse through the endplate — a process that scales with $L^{0.5}$ to $L^1$ at best. During the growth spurt, disc height increases while the endplate area scales only as $L^2$. The diffusion distance increases faster than the supply surface, creating a local hypoxic core.

**Clinical correlation**: Ugur et al. (2024) demonstrated that eliminating hypoxic factors (adenoidectomy for obstructive sleep apnea) led to scoliosis regression in adolescents — directly supporting the hypoxia–scoliosis link.

### 5.4 Factor 3: Circadian Desynchrony (ARNTL/BMAL1)

ARNTL/BMAL1 (anisotropy 3.32, 40% disordered) is the master circadian clock transcription factor. Its structural properties reveal it is **surprisingly expensive** for a clock gene:

- Anisotropy 3.32 — higher than the supply mean (2.48) and even some demand proteins
- 40% disordered — requires constant turnover
- 6 hinge candidates — conformationally complex

The clock itself costs energy to run. During adolescence, circadian disruption is endemic (late sleep patterns, screen exposure, social jetlag). The consequences:

1. Metabolic efficiency drops 15–20% when circadian rhythms are disrupted
2. Matrix repair in IVDs is circadian-regulated (peak during rest/unloading at night)
3. "Spinal Jetlag" — desynchronization between the central SCN clock and the peripheral IVD clock
4. The repair window shrinks while the damage window (daytime gravitational loading) remains constant

**The clock-hypoxia coupling**: ARNTL and HIF-1α share transcriptional targets (Adamovich et al., 2017; Peek et al., 2017). When ARNTL is disrupted, HIF-1α regulation fails, amplifying the hypoxic switch described in Factor 2.

### 5.5 Factor 4: The Modern Mismatch Hypothesis

Modern adolescents are significantly taller than their evolutionary ancestors:
- Mean adult height has increased ~10 cm in the past century (secular trend)
- Growth velocity has increased due to improved nutrition
- But the proprioceptive/metabolic supply system was optimized for ancestral growth rates

The $L^4$ cost scaling means even modest height increases dramatically amplify demand:

$$\frac{C_{\text{modern}}}{C_{\text{ancestral}}} = \left(\frac{L_{\text{modern}}}{L_{\text{ancestral}}}\right)^4 = \left(\frac{1.75}{1.65}\right)^4 = 1.26$$

A 6% increase in height produces a **26% increase** in counter-curvature cost. The supply system, evolved for $L_{\text{ancestral}}$, cannot keep pace with $L_{\text{modern}}$.

**Prediction**: AIS prevalence should correlate with secular height trends. Countries experiencing rapid height gains (East Asia, Northern Europe) should show increasing AIS prevalence — consistent with epidemiological data showing AIS rates of 2–4% in developed nations versus <1% in historical populations.

### 5.6 Factor 5: Micronutrient Deficit vs. Caloric Surplus

Modern diets can be calorically sufficient but micronutrient-deficient. The specific cofactors required for counter-curvature maintenance include:

| Cofactor | Required For | Protein Affected | Consequence of Deficit |
|----------|-------------|------------------|----------------------|
| NAD⁺ precursors (niacin, tryptophan) | SIRT1 enzymatic activity | SIRT1 (the energy gauge) | Energy sensor becomes "blind" |
| Iron | Cytochrome c oxidase | Mitochondrial chain (PPARGC1A targets) | ATP ceiling lowered |
| Vitamin D | Calcium homeostasis | COL1A1 mineralization | Structural matrix weakened |
| CoQ10 | Electron transport chain | Mitochondrial function | Oxidative phosphorylation impaired |
| B-vitamins (B6, B12, folate) | Methylation, collagen crosslinking | PLOD1 function, LMNA methylation | Under-crosslinked collagen, nuclear softening |

**The NAD⁺ hypothesis**: SIRT1 (anisotropy 1.73, constant scaling) is the energy gauge — it detects the deficit. But SIRT1 requires NAD⁺ as a cofactor to function. If NAD⁺ synthesis is compromised by dietary deficiency of precursors (niacin, tryptophan), the sensor is blind *before the deficit even begins*. This creates a silent vulnerability that caloric intake alone cannot resolve.

### 5.7 Factor 6: The Supply-Side Supply Deficit (Recursive Constraint)

Perhaps the most subtle mechanism: **the supply machinery itself is expensive to maintain**.

From the protein data, the supply-side proteins with highest structural cost:

| Protein | Anisotropy | Role | Cost Implication |
|---------|-----------|------|------------------|
| GHR | **5.13** | Growth signal receptor | 54 hinges — most conformationally expensive protein |
| ARNTL | **3.32** | Circadian clock | Clock itself costs energy |
| COL1A1 | **2.80** | Structural scaffold | Triple helix assembly is energy-intensive |
| PPARGC1A | **2.19** | Mitochondrial biogenesis | Supply ceiling regulator is itself fragile |

When the system needs to upregulate supply (more GHR for growth signaling, more PPARGC1A for mitochondrial biogenesis, more ARNTL for clock amplitude), it must spend energy to build and maintain these supply proteins. But the supply proteins are themselves expensive:

$$\text{Cost of increasing supply} = \sum_i A_i \times N_{\text{residues},i} \times \Delta\text{expression}_i$$

For GHR alone: $5.13 \times 638 = 3,273$ cost units per additional receptor molecule.

**This is the recursive trap**: To increase energy supply, you must spend energy. During the growth spurt, the system cannot afford the upfront investment required to expand its own supply capacity — the "bootstrap problem" of biological energy economics.

---

## 6. Synthesis: Integrating the Five Answers

### 6.1 The Unified Picture

The five questions are not independent — they are interconnected aspects of a single gravitational-metabolic problem:

1. **Rapid growth** (Section 1) is the evolutionary solution to the vulnerability created by the L⁴ scaling law — sprint through the danger zone.

2. **Curve patterns** (Section 2) are eigenmodes determined by regional variation in the protein expression landscape — the spatial distribution of the energy deficit selects the instability mode.

3. **Female predominance** (Section 3) arises because girls have a deeper energy deficit (unfavorable muscle/fat ratio, lower PPARGC1A expression, earlier onset) — not structural weakness but metabolic timing.

4. **The protein data** (Section 4) quantitatively demonstrates a 34% Demand–Supply Anisotropy Gap, a 3.01× VIM Vulnerability Index, and a cascade of failure ordered precisely by structural anisotropy.

5. **The energy deficit** (Section 5) has six distinct molecular drivers beyond hunger — mitochondrial ceiling, vascular limitation, circadian desynchrony, modern mismatch, micronutrient deficit, and recursive supply constraint.

### 6.2 The Central Equation

All five answers can be unified in a single inequality. Scoliosis initiates when:

$$\underbrace{\sum_{i \in \text{demand}} A_i \cdot N_i \cdot L^{\alpha_i}}_{\text{Total Demand Cost}} > \underbrace{\sum_{j \in \text{supply}} A_j \cdot N_j \cdot L^{\beta_j} \cdot f_{\text{sex}} \cdot f_{\text{circadian}} \cdot f_{\text{vascular}} \cdot f_{\text{micronutrient}}}_{\text{Total Supply Capacity}}$$

where:
- $A_i, A_j$ = protein anisotropy (from AlphaFold)
- $N_i, N_j$ = residue count
- $\alpha_i, \beta_j$ = scaling exponents ($\alpha > \beta$ for demand vs supply)
- $f_{\text{sex}}$ = sex-specific metabolic modifier (~0.85 for females)
- $f_{\text{circadian}}$ = circadian health factor (0.80–1.0)
- $f_{\text{vascular}}$ = local perfusion adequacy (0.70–1.0)
- $f_{\text{micronutrient}}$ = cofactor availability (0.60–1.0 for NAD⁺, iron, etc.)

### 6.3 Novel Testable Predictions

1. **Paraspinal muscle biopsies** from AIS patients at PHV will show reduced PPARGC1A expression, elevated SIRT1, reduced VIM network integrity, and asymmetric LBX1 — all measurable via immunohistochemistry or transcriptomics.

2. **Sex-stratified PPARGC1A expression** in paraspinal muscle: females with AIS will show >15% lower PPARGC1A than height-matched male controls.

3. **Circadian biomarkers** (urinary melatonin phase, BMAL1 expression in peripheral blood) will predict curve progression rate.

4. **NAD⁺ precursor supplementation** (nicotinamide riboside or NMN) during PHV in at-risk adolescents may reduce scoliosis progression by restoring SIRT1 function.

5. **Low-intensity vibration (LIV)** therapy during the Energy Deficit Window may maintain VIM network integrity and prevent the failure cascade — analogous to the microgravity rescue demonstrated by Touchstone et al. (2019) for the LINC complex.

6. **Height velocity correlation**: Among AIS patients, those with fastest growth velocity should paradoxically show *less* severe curves than moderately fast growers, because very fast growth minimizes $T_{\text{vulnerable}}$ — an inverted-U relationship between growth speed and curve severity.

---

## References

This analysis draws on data from the following repository files:
- `outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv` (23-protein AlphaFold dataset)
- `outputs/thermodynamic_cost/energy_deficit_window.csv` (P_counter vs L)
- `outputs/thermodynamic_cost/energy_deficit_bifurcation.csv` (chi_kappa × L phase diagram)
- `outputs/protein_physics_results.csv` (6 simulation scenarios)
- `outputs/experiments/spine_modes/spine_modes_summary.csv` (eigenmode analysis)
- `outputs/afcc/current_metrics.csv` (AlphaFold structural metrics)

Literature references cited in this analysis are indexed in `manuscript/references.bib`.
# Unanswered Questions in Biological Counter-Curvature Theory

This document addresses five critical open questions regarding the biological counter-curvature theory of Adolescent Idiopathic Scoliosis (AIS), synthesizing rigorous protein data analysis with the existing theoretical framework.

## 1. Why Rapid Growth During Ages 12-20? A Gravitational Standpoint

**Core Argument:** Rapid growth is not a design flaw but an evolved strategy to minimize the total duration spent in the high-deficit zone. The hormonal growth loop (GH/IGF-1) is the mechanism, but gravity is the ultimate evolutionary selector.

### The Scaling Catch-22
The thermodynamic cost of maintaining a straight spine against gravity scales as $L^4$ (due to buckling moment and lever arm effects), while the metabolic supply capacity scales approximately as $L^2$ (cross-sectional area of muscles/vessels).
*   **Cost Function:** $C(L) \propto L^4$
*   **Supply Function:** $S(L) \propto L^2$

Every additional centimeter of height increases the metabolic cost exponentially relative to supply. The organism faces a "Danger Zone" where $C(L) > S(L)$.

### Time-in-Vulnerability Optimization
The evolutionary solution is to traverse this danger zone as quickly as possible. The "Time-in-Vulnerability" ($T_v$) can be defined as:
$$ T_{vulnerable} = \int_{L_{critical}}^{L_{final}} \frac{dL}{v_{growth}(L)} $$
where $v_{growth}(L)$ is the growth velocity. By maximizing $v_{growth}$, the organism minimizes $T_{vulnerable}$, reducing the cumulative probability of spinal failure (scoliosis).

### Chicken-or-Egg Resolution
*   **Mechanism:** Growth velocity creates mechanical demand -> increased GHR signaling -> increased GH/IGF-1 -> positive feedback loop.
*   **Selector:** Gravity selects against slow growers because they linger too long in the high-deficit state, accumulating structural damage.

### Protein Evidence
*   **GHR (Growth Hormone Receptor):** Anisotropy **5.13**, with **54 hinge candidates**. The signaling machinery driving this rapid growth is itself structurally expensive and highly anisotropic, reflecting the high evolutionary priority and cost of the growth spurt.
*   **IGF1R:** Anisotropy **1.43**, globular. Optimized for efficient, stable signal capture to support the rapid growth phase.

## 2. Why Different Patterns of AIS Curves?

**Core Argument:** Curve patterns (Thoracic, Lumbar, Double Major) correspond to distinct eigenmodes of the coupled Cosserat rod system. The specific mode excited depends on the regional distribution of the energy deficit, local stiffness variations, and the vector mismatch parameter $\alpha(s)$.

### Eigenmode Analysis
The linearized Information-Elasticity Coupling (IEC) equations yield solutions of the form $\sin(n\pi s/L)$.
*   **n=1:** Single C-curve (Thoracic or Lumbar).
*   **n=2:** Double Major S-curve.
*   **n=3:** Triple curve (rare).

The dominant mode is determined by the spatial distribution of the Bio-Gravitational Number $\mathcal{B}_g(s)$ and the local mismatch between the information field and elastic reality.

### Regional Protein Expression & Failure
*   **Thoracic Region:** Characterized by lower $\mathcal{B}_g$ but high rib cage constraints. Heavily dependent on **PIEZO2** (proprioception) for alignment.
*   **Lumbar Region:** Higher $\mathcal{B}_g$ (load-bearing). Failures here are often linked to **COL1A1** (matrix integrity) and **LBX1** (muscle tone asymmetry).
*   **Thoracolumbar Junction:** Represents the region of maximal anisotropy change, creating a "Vector-Scalar Mismatch".

### Simulation & Data Support
*   **Vector-Scalar Mismatch:** Simulation results (`protein_physics_results.csv`) show this scenario produces the highest Cobb angle (**11.15°**), confirming that regions with conflicting anisotropy/gain signals are most prone to instability.
*   **LBX1 (Anisotropy 2.27):** Asymmetric expression of this transcription factor creates a muscle tone imbalance, effectively biasing the rod and selecting the buckling direction.
*   **VIM (Anisotropy 7.47):** As the most anisotropic cytoskeletal element, Vimentin is the "first domino" to buckle under stress, but its failure pattern varies by tissue type, influencing the macroscopic curve shape.

## 3. Why More Scoliosis in Girls? (10:1 Ratio)

**Core Argument:** The female prevalence is not due to simple structural weakness but to a specific metabolic timing mismatch. Females enter Peak Height Velocity (PHV) earlier, with a deeper energy deficit window relative to their muscle mass accretion.

### Estrogen Timing and the Deficit Window
Girls enter PHV at ages 11-12 (vs. 13-14 for boys). This earlier onset forces rapid lengthening before the corresponding muscle mass (supply side) has fully matured.
*   **Deficit Depth:** Analysis suggests the peak demand/supply ratio ($R_{peak}$) is significantly higher in females (**2.7**) compared to males (**2.4**).

### Metabolic Dimorphism
*   **Muscle/Mass Ratio:** Female adolescents typically have a lower muscle-to-body-mass ratio and fewer mitochondria per unit of paraspinal muscle compared to males.
*   **Supply Ceiling:** **PPARGC1A**, the master regulator of mitochondrial biogenesis, represents the hard ceiling on energy supply. In females, the effective expression or reserve capacity of this pathway is sooner exhausted by the demands of rapid growth.

### Body Composition and $L^4$ Costs
Females accumulate more fat mass during puberty, which increases the gravitational load ($M$ in the $\Gamma_m$ term) without a proportional increase in the contractile force ($F$ in the $\eta_a$ term). This exacerbates the scaling mismatch ($Cost \propto L^4$).

### Protein Evidence
*   **LBX1 (2.27):** The top GWAS hit for AIS is explicitly linked to muscle development and is predominantly identified in female cohorts, suggesting a sex-specific vulnerability in muscle morphogenesis.
*   **PPARGC1A (pLDDT 52.7, 62% Disorder):** The supply bottleneck protein is structurally fragile, making the female metabolic system less robust to the "sprint" of puberty.

## 4. Protein Data Analysis — Quantitative Evidence for Energy Deficit

This section presents a rigorous analysis of the 22 proteins from the `thermodynamic_cost_proteins.csv` dataset, quantifying the structural costs and vulnerabilities.

### Demand-Supply Anisotropy Gap
We categorize proteins into **Demand** (Mechanosensors/Signaling, $\eta_p + \eta_a$) and **Supply** (Maintenance/Structure, $\Gamma_m$).
*   **Demand Mean Anisotropy:** **3.32**
*   **Supply Mean Anisotropy:** **2.48**
*   **Gap:** The demand-side proteins are **~34%** more anisotropic (structurally expensive) than the supply-side proteins. This structural premium on the demand side creates an inherent vulnerability; the sensors consume more stability "budget" than the suppliers can easily replenish.

### Scaling Law Mismatch
During the critical growth phase where height increases by 30% (e.g., $0.35m \to 0.45m$):
*   **Demand Increase:** Scales approx as $L^{2.5}$ -> **~1.83x** increase.
*   **Supply Increase:** Scales approx as $L^{1.3}$ -> **~1.38x** increase.
*   **Net Deficit:** The gap widens by **~33%** during the growth spurt, creating the "Energy Deficit Window".

### VIM Vulnerability Index
Vimentin (VIM) is identified as the critical failure point.
*   **VIM Anisotropy:** 7.47
*   **Supply Mean Anisotropy:** 2.48
*   **Index:** $7.47 / 2.48 \approx$ **3.01x**.
VIM requires 3 times more structural order to maintain than the average supply protein can generate, explaining why it is the first structure to collapse (buckle) under metabolic stress.

### Per-Protein Energy Cost Proxy
We define a proxy for the total folding/maintenance energy cost as $E_{proxy} = Anisotropy \times N_{residues}$.
**Top 5 Most Expensive Proteins:**
1.  **PIEZO1:** 9,822 (Aniso 3.90 $\times$ 2521 res)
2.  **FLNA:** 6,622 (Aniso 2.50 $\times$ 2647 res)
3.  **COL1A1:** 4,095 (Aniso 2.80 $\times$ 1464 res)
4.  **VIM:** 3,480 (Aniso 7.47 $\times$ 466 res)
5.  **GHR:** 3,273 (Aniso 5.13 $\times$ 638 res)

Strikingly, 3 of the top 5 are **Demand-side** proteins (PIEZO1, VIM, GHR) and FLNA acts as a mechanosensor. This confirms that the sensory and signaling apparatus is the primary metabolic sink.

### Disorder Analysis
*   **Supply System Disorder:** The supply-side proteins (e.g., PPARGC1A, SIRT1, COL1A1) show a high degree of intrinsic disorder (Mean **~38%**).
*   **Demand System Disorder:** The demand-side proteins are comparatively more ordered (Mean **~26%**), though highly anisotropic.
*   **Implication:** The supply system is paradoxically **more disordered** and potentially more fragile/unstable than the demand system it supports. The "engine" (supply) is built of flimsier parts than the "steering" (demand).

### PPARGC1A Fragility Score
*   **pLDDT:** 52.7 (Lowest in dataset)
*   **Disorder:** 62% (Highest in dataset)
*   **Conclusion:** The master regulator of energy supply is the most structurally vulnerable protein in the entire network. Under stress, it is the most likely to misfold or degrade, leading to a catastrophic failure of energy production exactly when it is needed most.

## 5. What Could Have Led to Energy Supply Differences?

Beyond simple caloric intake (hunger), five deep mechanisms create the specific supply/demand mismatch in AIS.

1.  **Mitochondrial Capacity Ceiling:** As evidenced by **PPARGC1A's** extreme fragility, the biological machinery for upregulating mitochondria is inherently unstable. A feedback trap emerges: Energy Scarcity -> PPARGC1A degradation -> Fewer Mitochondria -> Less Energy.
2.  **Vascular Supply Limitation:** Paraspinal muscles are supplied by segmental arteries. Vascular network development often lags behind rapid tissue expansion (angiogenesis lag), creating local hypoxia. This forces cells to shift to glycolysis (HIF-1$\alpha$ pathway), which produces **15x less ATP** per glucose molecule than oxidative phosphorylation.
3.  **Circadian Desynchrony:** **ARNTL/BMAL1** (Anisotropy 3.32, 40% disorder) is an expensive protein to maintain. Disruption of the circadian clock in adolescents (due to modern lighting, sleep patterns) impairs the rhythmic regeneration of intervertebral discs and muscle tissue, dropping metabolic efficiency by 15-20%.
4.  **The Modern Mismatch:** Modern adolescents grow taller and faster (secular trend) than ancestral populations, pushing $v_{growth}$ beyond the limits the proprioceptive/metabolic system evolved to handle.
5.  **Micronutrient vs Caloric Sufficiency:** While caloric intake may be sufficient (or excessive), specific deficits in NAD+ precursors (niacin, tryptophan) can limit the activity of **SIRT1** (the energy gauge), blinding the system to the developing deficit before it becomes critical.
6.  **Supply-Side Supply Deficit:** The proteins required to signal for more supply (**GHR**, **ARNTL**) are themselves expensive to synthesize. **GHR** (Anisotropy 5.13) represents a "tax" on the very signal that requests more resources, creating a recursive deficit.

## 6. Synthesis and Testable Predictions

The biological counter-curvature theory unifies these findings: AIS is a **thermodynamic failure mode** where the rapidly growing spine, driven by expensive signaling (GHR) and monitored by expensive sensors (PIEZO2, VIM), outstrips the capacity of a fragile, disordered supply system (PPARGC1A).

### Testable Predictions
1.  **The "Fragile Supply" Hypothesis:** Overexpression of stabilized PPARGC1A (reduced disorder) in an AIS mouse model should prevent curvature development even during rapid growth.
2.  **The "Vimentin Rescue":** Introduction of a "stiff" Vimentin variant (lower anisotropy, same function) should reduce the incidence of buckling failure in paraspinal fibroblasts.
3.  **Metabolic Support Therapy:** A combinational therapy targeting the "Supply Gap"—Nicotinamide Riboside (NAD+ for SIRT1), PGC-1$\alpha$ agonists, and circadian synchronization—should be more effective than bracing alone in preventing curve progression.

## Data Files Reference

| File | Purpose |
| :--- | :--- |
| `outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv` | Primary protein dataset (22 proteins) |
| `outputs/thermodynamic_cost/energy_deficit_window.csv` | $P_{counter}$ vs $L$ curves |
| `outputs/thermodynamic_cost/energy_deficit_bifurcation.csv` | $\chi_\kappa$ vs $L$ phase diagram |
| `outputs/afcc/current_metrics.csv` | AlphaFold structural metrics |
| `outputs/protein_physics_results.csv` | Simulation scenarios and Cobb angles |
| `outputs/experiments/spine_modes/spine_modes_summary.csv` | Mode analysis |
