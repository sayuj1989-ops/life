# Longevity-Counter-Curvature Framework

## Core Hypothesis

Repeated squat-to-stand transitions maintain spinal counter-curvature coupling strengths ($\chi_\kappa$, $\chi_M$), which would otherwise decay with age, by exercising the full mechanotransduction cascade from PIEZO channels through FOXO3/SIRT1 longevity pathways. The Okinawan practice of $\sim$50-100 floor-to-stand transitions daily preserves coupling at $>90\%$ of peak, compared to $\sim30\%$ in chair-sitting populations — this is the mechanistic basis of the SRT-longevity association.

---

## The Dissipation Functional and Longevity

The spine is a thermodynamic standing wave maintained by:

$$
\dot{F} = \int_{0}^{L} \left[ \eta_p \left| \frac{\partial \kappa}{\partial t} \right|^2 + \eta_a (\kappa - \kappa_{passive})^2 + \Gamma_m(s) \right] ds
$$

Each squat-to-stand cycle exercises all three terms:

| Term | Proteins | Cost During Cycle | Longevity Output |
| :--- | :--- | :--- | :--- |
| $\eta_p \left| \frac{\partial \kappa}{\partial t} \right|^2$ | PIEZO2, EGR3, RUNX3, NTRK3, PIEZO1 | **Peak** during transition (2-4s) | $Ca^{2+} \to$ Klotho |
| $\eta_a (\kappa - \kappa_{passive})^2$ | VIM, LMNA, FLNA, DMD, MYLK, LBX1, CAV1 | **High** during holding | Cytoskeletal tension $\to$ YAP1 |
| $\Gamma_m(s)$ | SIRT1, PPARGC1A, COL1A1, ARNTL, etc. | **Continuous** + exercise boost | NAD+ $\to$ SIRT1 $\to$ FOXO3 |

---

## Molecular Cascade: 28 Proteins

### Dissipation $\to$ Longevity Pathway

```text
Squat-to-Stand Cycle (thermodynamic perturbation of standing wave)
    |
    +── η_p activation: PIEZO2 → Ca²⁺ → EGR3/RUNX3 (proprioceptive refresh)
    |       |
    |       +→ Ca²⁺ → FGF23 → KLOTHO (anti-aging, anti-oxidant)
    |
    +── η_a activation: VIM/LMNA/FLNA (cytoskeletal tension)
    |       |
    |       +→ YAP1 nuclear translocation → CTGF/CYR61 (tissue repair)
    |       +→ muscle contraction → AMPK → FOXO3 (stress resistance)
    |
    +── Γ_m boost: NAD⁺ pulse from exercise
            |
            +→ SIRT1 → FOXO3 deacetylation (autophagy, DNA repair)
            +→ AMPK → PGC-1α (mitochondrial biogenesis)
```

### Complete Protein Table

**Demand side ($\eta_p$ + $\eta_a$): 12 proteins, mean anisotropy 3.32**

| Gene | Term | Anisotropy | pLDDT | Disorder | Longevity Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| PIEZO2 | $\eta_p$ | 4.44 | 79.4 | 14% | $Ca^{2+}$ influx $\to$ Klotho activation |
| EGR3 | $\eta_p$ | 3.76 | 50.0 | 64% | Spindle maintenance (proprioceptive quality) |
| RUNX3 | $\eta_p$ | 2.06 | 60.6 | 56% | Proprioceptive neuron survival |
| NTRK3 | $\eta_p$ | 1.94 | 76.8 | 20% | Neurotrophic support |
| PIEZO1 | $\eta_p$ | 3.90 | 72.0 | 17% | Membrane tension $\to$ scalar signal |
| VIM | $\eta_a$ | **7.47** | 77.1 | 24% | **First domino**: collapse $\to$ YAP exclusion |
| LMNA | $\eta_a$ | 4.75 | 76.4 | 26% | Nuclear mechanostat $\to$ gene access |
| FLNA | $\eta_a$ | 2.50 | 76.5 | 5% | Crosslinker (116 hinges) |
| CAV1 | $\eta_a$ | 3.98 | 78.4 | 3% | Membrane sensor $\to$ YAP/TAZ |
| DMD | $\eta_a$ | 1.32 | 76.3 | 18% | Force transmission to ECM |
| MYLK | $\eta_a$ | 1.46 | 65.8 | 35% | Tonic contraction $\to$ AMPK |
| LBX1 | $\eta_a$ | 2.27 | 66.9 | 26% | Paraspinal muscle specification |

**Supply side ($\Gamma_m$): 10 proteins, mean anisotropy 2.48**

| Gene | Term | Anisotropy | pLDDT | Disorder | Longevity Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SIRT1 | $\Gamma_m$ | 1.73 | 65.0 | 47% | **Dual**: energy gauge + FOXO3 deacetylase |
| PPARGC1A | $\Gamma_m$ | 2.19 | 52.7 | **62%** | **Dual**: supply bottleneck + mitochondrial biogenesis |
| ARNTL | $\Gamma_m$ | 3.32 | 65.5 | 40% | Circadian entrainment by regular cycling |
| COL1A1 | $\Gamma_m$ | 2.80 | 52.7 | 67% | Loading-dependent collagen turnover |
| GHR | $\Gamma_m$ | 5.13 | 58.7 | 50% | Growth hormone signaling |
| COMP | $\Gamma_m$ | 1.72 | 88.1 | 6% | Disc ECM maintenance |
| SOX9 | $\Gamma_m$ | 2.19 | 56.0 | 49% | Growth plate cartilage |
| SHH | $\Gamma_m$ | 2.12 | 78.4 | 16% | Morphogen gradient maintenance |
| CDKN1A | $\Gamma_m$ | 2.14 | 69.0 | 25% | Senescence marker (suppressed by cycling) |
| IGF1R | $\Gamma_m$ | 1.43 | 78.0 | 16% | Growth factor receptor |

**Longevity downstream: 5 proteins (3 new + 2 dual-role)**

| Gene | UniProt | Upstream | Pathway | Status |
| :--- | :--- | :--- | :--- | :--- |
| FOXO3 | O43524 | $\eta_a \to$ AMPK + $\Gamma_m \to$ SIRT1 | Stress resistance, autophagy | NEW |
| SIRT1 | Q96EB6 | $\Gamma_m$ (NAD+ cycling) | FOXO3 deacetylation | DUAL-ROLE |
| KLOTHO | Q9UEF7 | $\eta_p \to$ PIEZO $\to Ca^{2+}$ | Anti-oxidant, vascular health | NEW |
| YAP1 | P46937 | $\eta_a \to$ VIM/LMNA tension | Tissue repair, proliferation | NEW |
| PGC-1$\alpha$ | Q9UBK2 | $\Gamma_m$ (AMPK activation) | Mitochondrial quality control | DUAL-ROLE |

---

## Coupling Decay Model

Without squat-to-stand cycling, coupling strengths decay exponentially:

$$
\chi(t) = \chi_0 \cdot \exp\left(-\frac{\Delta t}{\tau_{decay}}\right)
$$

Each cycle resets coupling. For N cycles/day, time-averaged coupling:

$$
\chi_{avg} = \chi_0 \cdot \left(\frac{\tau_{decay} \cdot N}{T_{day}}\right) \cdot \left(1 - \exp\left(-\frac{T_{day}}{N \cdot \tau_{decay}}\right)\right)
$$

**Quantitative predictions ($\tau_{decay} = 2$ hours):**

| Lifestyle | Cycles/day | $\chi_{avg}/\chi_0$ | SRT Prediction (age 70) |
| :--- | :--- | :--- | :--- |
| Bedridden | 0 | 0.0% | 0-1 |
| Sedentary | 1 | 8.3% | 1-2 |
| Chair-sitter | 3 | 24.5% | 2-4 |
| Active-sitter | 20 | 75.2% | 5-7 |
| Floor-sitter | 50 | 88.9% | 7-9 |
| Okinawan elder | 80 | 92.9% | 8-10 |

---

## Evidence Base

### Epidemiological
- **De Brito et al. (2014):** SRT 0-3 $\to$ HR 5.44 for all-cause mortality; each 1-unit increase $\to$ 21% survival improvement (N=2,002, median follow-up 6.3 years)
- **Araújo et al. (2024):** Cardiovascular mortality HR 6.05 for lowest SRT performers (N=4,282, 12.3-year follow-up)
- **Okinawa Blue Zone:** Highest centenarian density globally; traditional floor-sitting lifestyle

### Molecular
- **PIEZO mechanotransduction:** Coste et al. (2010), PIEZO1/2 as mechanically-activated cation channels
- **YAP/TAZ:** Dupont et al. (2011, Nature), mechanical force $\to$ YAP nuclear translocation
- **FOXO3 longevity:** Willcox et al. (2008, PNAS), FOXO3A genotype $\to$ human longevity
- **SIRT1:** Satoh et al. (2013, Cell Metabolism), SIRT1 $\to$ life span extension in mice

### Microgravity (Zero-Cycling Endpoint)
- **NASA Twins Study:** Garrett-Bakelman et al. (2019, Science), accelerated aging markers in space
- **VIM collapse:** Vorselen et al. (2014), cytoskeletal reorganization in microgravity
- **YAP exclusion:** Thompson et al. (2022), mechanical unloading $\to$ YAP cytoplasmic sequestration

---

## Experimental Validation Roadmap

### Phase 1: Pilot (N=20, 6 months)
- IMU sensor validation (T1, T6, L3, sacrum)
- Curvature estimation algorithms for sit-rise detection
- Preliminary $D_{geo}$ vs SRT correlation
- Budget: $\sim$50K

### Phase 2: Full Study (N=200, 18 months)
- Stratified by SRT score: High (8-10), Mid (5-7), Low (0-4)
- 7-day wearable monitoring: sit-rise frequency, curvature spectra
- Optional: Phase-contrast MRI for CSF flow (N=40 subset)
- Primary outcome: SRT score vs mean $D_{geo}$ (Spearman $\rho < -0.5$)
- Budget: $\sim$400K (NIH R21)

### Phase 3: Cross-Cultural (N=200, 12 months)
- 100 Okinawan/Japanese (floor-sitting) vs 100 American (chair-sitting)
- Same IMU protocol
- Test: floor-sitters maintain higher $D_{geo}$ at equivalent ages
- Budget: $\sim$300K (international collaboration)

---

## Simulation Infrastructure

### Existing (Reused)
- `src/spinalmodes/countercurvature/coupling.py` — IEC coupling functions
- `src/spinalmodes/countercurvature/pyelastica_bridge.py` — Cosserat rod simulations
- `src/spinalmodes/countercurvature/info_fields.py` — Static and dynamic info fields
- `scripts/experiments/run_posture_sweep.py` — Static posture analysis
- `scripts/analysis/05_longevity_demo.py` — Synthetic survival analysis

### New (Built for Longevity Extension)
- `scripts/experiments/experiment_squat_stand_cycle.py` — Dynamic cycling simulation
- `scripts/experiments/experiment_longevity_proteins.py` — 28-protein analysis
- `research/longevity_squat_stand_feasibility.md` — Feasibility study document

---

## Key Insight: Same Physics, Opposite End of Lifespan

| Concept | Scoliosis (Development) | Longevity (Aging) |
| :--- | :--- | :--- |
| Energy deficit | Growth outpaces supply | Coupling decays without cycling |
| VIM cascade | Collapse $\to$ scoliosis | Collapse $\to$ YAP exclusion $\to$ senescence |
| PPARGC1A fragility | Supply bottleneck during growth | Mitochondrial decline during aging |
| Bio-gravitational number $\mathcal{B}_g$ | Controls C$\to$S transition in development | Controls S$\to$C regression in aging |
| Coupling strengths $\chi_\kappa, \chi_M$ | Set during development | Maintained by cycling, lost without it |

This is the same physics, same proteins, same functional — just viewed from the opposite end of the lifespan.
