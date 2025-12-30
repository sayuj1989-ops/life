# Functional Mobility and Biological Countercurvature: Interpreting Sit-Rise Performance Through an Information-Geometry Framework

**Extended Abstract / Outline**

**Authors:** Sayuj Krishnan S, MBBS, DNB (Neurosurgery), et al.
**Status:** Extended abstract — ready for full manuscript development
**Date:** 2025-11-18
**Target Journals:** Frontiers in Physiology (Gerontology), J Gerontology: Medical Sciences, Age and Ageing

---

## Abstract (250 words)

**Background:** The sitting-rising test (SRT)—a simple assessment of the ability to sit on the floor and rise to standing without hand support—predicts all-cause mortality in middle-aged and older adults with remarkable strength (hazard ratio 5.44 for lowest vs. highest performers). Despite robust epidemiological evidence, the mechanistic basis for this association remains unclear.

**Framework:** We apply a recently developed biological countercurvature framework—which treats spinal curvature as information-selected modes in an effective gravitational geometry—to interpret SRT performance. In this model, the spine embedded in gravity is treated as an analog spacetime with metric $d\ell_{\text{eff}}^2 = g_{\text{eff}}(s)\,ds^2$ shaped by an information field $I(s)$ representing developmental patterning, neural control, and proprioceptive feedback. A normalized geodesic curvature deviation $\widehat{D}_{\text{geo}}$ quantifies the "distance" between gravity-selected (passive sag) and information-selected (standing S-curve) equilibrium configurations.

**Interpretation:** We propose that sit-rise transitions functionally test the system's capacity to dynamically access multiple curvature modes: a flexed "ground mode" (lumbar flexion, posterior pelvic tilt) and an extended "standing countercurvature mode" (restored lumbar lordosis). Poor SRT performance may reflect restricted mode access due to age-related decay of information–curvature coupling, corresponding to movement toward gravity-dominated regime where countercurvature mechanisms fail.

**Validation Study:** We propose a prospective observational study (N=200, ages 50-80) using wearable IMU sensors to measure spinal curvature $\kappa(s,t)$ during sit-rise transitions and daily activities, testing whether SRT scores correlate with geodesic curvature deviation and curvature mode diversity.

**Significance:** This framework provides a quantitative geometric language for functional mobility, potentially guiding interventions that target information-curvature coupling to preserve postural control and extend healthspan.

---

## 1. Introduction

### 1.1 The Sit-Rise Test and Mortality Prediction

Simple functional mobility tests have emerged as powerful predictors of long-term health outcomes in aging populations. Among these, the sitting-rising test (SRT) stands out for both its simplicity and prognostic strength. The test requires individuals to sit down on the floor from standing and then rise back to standing, with scoring based on use of support (hand, knee, forearm) or loss of balance. Scores range from 0 (unable to sit or rise) to 10 (perfect performance without support).

In a landmark study of 2,002 adults aged 51-80 years followed for median 6.3 years, de Brito and colleagues demonstrated that SRT performance strongly predicts all-cause mortality:

- **SRT 0-3:** Hazard ratio **5.44** (95% CI 3.1-9.5) vs. reference
- **SRT 3.5-5.5:** Hazard ratio **3.44** (95% CI 2.0-5.9)
- **SRT 6-7.5:** Hazard ratio **1.84** (95% CI 1.1-3.0)
- **Each 1-unit increase:** **21% improvement** in survival (p < 0.001)

Extended follow-up studies (N=4,282, 12.3-year median) confirmed these findings and demonstrated similar associations with cardiovascular mortality specifically (HR 6.05 for lowest vs. highest performers).

### 1.2 The Mechanistic Gap

Despite robust epidemiological evidence, the mechanistic basis for the SRT-mortality association remains unclear. SRT is a composite measure reflecting:

- Lower-limb strength (quadriceps, gluteals, hip flexors)
- Spinal flexibility (lumbar/thoracic flexion and extension range)
- Core strength (abdominal and paraspinal muscles)
- Balance and proprioception
- Coordination and motor planning

Each component likely contributes to mortality risk through different pathways (cardiovascular fitness, fall risk, metabolic health, frailty). However, the integrated nature of the sit-rise movement—requiring whole-body postural transitions under gravitational loading—suggests a more unified mechanical perspective may be warranted.

### 1.3 Toward a Geometric-Mechanical Framework

We propose that sit-rise performance fundamentally tests the capacity to **dynamically access and control multiple spinal curvature modes under gravity**. From a geometric-mechanical perspective:

- **Sitting phase:** Transition from standing S-curve (cervical lordosis, thoracic kyphosis, lumbar lordosis) to flexed "ground mode" (posterior pelvic tilt, flattened lumbar lordosis, controlled descent)

- **Rising phase:** Reverse transition from ground mode to standing countercurvature mode, requiring:
  - Hip extension initiation
  - Lumbar lordosis restoration
  - Trunk-limb coordination
  - Active anti-gravity muscle recruitment

Successful transitions imply the neuromuscular-skeletal system can:
1. Access a repertoire of distinct postural configurations
2. Switch between them under gravitational constraint
3. Stabilize each configuration through active control

We interpret this capacity through a **biological countercurvature framework** recently developed to model spinal geometry as information-selected modes in an effective gravitational spacetime.

### 1.4 Goals of This Work

This paper aims to:

1. **Interpret SRT performance** through the countercurvature framework, mapping functional mobility to curvature mode access

2. **Propose mechanistic hypotheses** linking SRT to information-curvature coupling decay, CSF flow dynamics, and age-related degeneration

3. **Design a validation study** using wearable IMU sensors to measure $\kappa(s,t)$ during sit-rise and test predicted correlations with $\widehat{D}_{\text{geo}}$

4. **Explore cross-cultural predictions**: Do floor-sitting populations (e.g., Japan, India) preserve countercurvature capacity and SRT performance into later life?

---

## 2. Framework: Biological Countercurvature

### 2.1 Core Concepts (Brief Recap)

We treat a spine-like elastic rod embedded in gravity as an **analog spacetime**, where:

**Information field** $I(s)$: Represents spatial patterns of biological activity along body axis $s \in [0,L]$:
- Developmental gene expression gradients (HOX/PAX patterning)
- Neural control signals from CNS
- Proprioceptive feedback from mechanoreceptors
- CSF flow gradients driven by ciliary beating

**Information-Elasticity Coupling (IEC):** $I(s)$ modulates mechanical properties through dimensionless couplings:
- $\chi_{\kappa}$: Curvature coupling (modifies rest curvature $\kappa_{\text{rest}}(s)$)
- $\chi_E$: Stiffness coupling (modifies Young's modulus $E_{\text{eff}}(s)$)
- $\chi_M$: Active moment coupling (adds torques $M_{\text{info}}(s)$)

**Effective metric:** The information field defines an effective geometry:
$$d\ell_{\text{eff}}^2 = g_{\text{eff}}(s)\,ds^2, \quad g_{\text{eff}}(s) = \exp[2\phi(s)]$$
where $\phi(s) = \beta_1 \tilde{I}_{\text{centered}}(s) + \beta_2 \tilde{I}'(s)$ weights regions of high information density or gradient.

**Geodesic curvature deviation:** Quantifies "distance" between equilibrium curvatures:
$$\widehat{D}_{\text{geo}} = \frac{1}{\sqrt{\int_0^L g_{\text{eff}}(s)\,\kappa_0(s)^2\,ds}}\int_0^L g_{\text{eff}}(s)\,[\kappa_I(s) - \kappa_0(s)]^2\,ds$$
where $\kappa_0$ is gravity-only (passive) curvature and $\kappa_I$ is information-coupled curvature.

### 2.2 Countercurvature Regimes

The framework identifies three regimes in $(\chi_{\kappa}, g)$ parameter space:

1. **Gravity-dominated** ($\widehat{D}_{\text{geo}} < 0.1$): Rod follows passive gravitational sag (C-curve), information plays minimal role

2. **Cooperative** ($0.1 < \widehat{D}_{\text{geo}} < 0.3$): Information reshapes curvature within gravitational background (human-like S-curve)

3. **Information-dominated** ($\widehat{D}_{\text{geo}} > 0.3$): Countercurvature governs geometry, enables symmetry breaking (scoliosis-like patterns when asymmetries present)

### 2.3 Application to Postural Configurations

**Standing S-curve:** Cooperative regime where information field $I(s)$ with lumbar/cervical peaks selects a robust sinusoidal countercurvature mode against gravity. $\widehat{D}_{\text{geo}} \approx 0.14$ indicates this is not a small perturbation of passive sag but a distinct information-selected geodesic.

**Ground mode (sitting):** Requires active flexion (posterior pelvic tilt, lumbar flattening) corresponding to *different* information field configuration $I_{\text{sitting}}(s,t)$ with reduced lumbar peak amplitude and increased thoracic flexion bias.

**Transition dynamics:** Sit-rise movement corresponds to continuous evolution $I(s,t)$ from standing field to sitting field and back, with $\kappa(s,t)$ following time-dependent geodesics in $g_{\text{eff}}(s,t)$ landscape.

---

## 3. Interpretation: SRT as Curvature Mode Access Test

### 3.1 High SRT Performance (8-10 points)

**Mechanical signature:**
- Smooth, controlled transitions between standing and ground modes
- No external support required
- Minimal balance loss

**Framework interpretation:**
- **Broad curvature mode access:** System can navigate large region of configuration space in $g_{\text{eff}}(s)$ metric
- **Preserved coupling:** Strong $\chi_{\kappa}$ and $\chi_M$ allow dynamic modulation of $I(s,t)$ to select and stabilize multiple equilibrium curvatures
- **Low transition cost:** Small $\widehat{D}_{\text{geo}}$ within available mode repertoire (easy to move between standing S-curve and flexed ground mode)

**Biological correlates:**
- Intact neuromuscular control pathways
- Preserved spinal segment mobility
- Maintained proprioceptive feedback loops
- Healthy CSF flow dynamics supporting dynamic information gradients

### 3.2 Poor SRT Performance (0-3 points)

**Mechanical signature:**
- Requires hand/knee support to sit or rise
- Slow, effortful transitions
- Loss of balance common

**Framework interpretation:**
- **Restricted mode access:** System confined to smaller region of configuration space, cannot reach or stabilize ground mode without support
- **Degraded coupling:** Reduced $\chi_{\kappa}$ and $\chi_M$ due to:
  - Age-related motor unit loss
  - Spinal degeneration (disc height loss, facet arthritis)
  - Proprioceptive decline
  - Neuromuscular disease
- **High transition cost:** Large $\widehat{D}_{\text{geo}}$ between attempted and achieved curvatures during transitions (system "fights" against gravity more than information can compensate)

**Biological correlates:**
- Sarcopenia (muscle mass/quality loss)
- Spinal stiffness (reduced range of motion)
- Impaired CSF flow (vascular or ciliary dysfunction)
- Central motor control deficits (cerebellar, basal ganglia)

### 3.3 Key Hypothesis

**We propose that SRT score inversely correlates with the "geometric barrier" between standing and ground curvature modes**, operationalized as:

$$\text{SRT score} \propto -\widehat{D}_{\text{geo}}(\text{standing} \to \text{ground})$$

High performers have small $\widehat{D}_{\text{geo}}$ (modes are "close" in effective metric, easy transitions). Low performers have large $\widehat{D}_{\text{geo}}$ (modes are "far apart," difficult or impossible transitions without external support lowering the barrier).

This is **testable**: measure $\kappa(s,t)$ during sit-rise with IMU sensors, compute $\widehat{D}_{\text{geo}}$ time series, correlate with SRT score.

---

## 4. Mechanistic Hypotheses

### 4.1 Age-Related Coupling Decay

**Upstream mechanism:** Developmental patterning (HOX/PAX genes) establishes baseline information field topology during growth. In adulthood, coupling strengths $\chi_{\kappa}$, $\chi_M$ maintained by:
- Motor unit integrity (neuromuscular junction health)
- Spinal segment mobility (disc hydration, ligament elasticity)
- Proprioceptive sensitivity (mechanoreceptor density/function)

**Aging cascade:**
1. Motor unit loss (5-10% per decade after age 50)
2. Intervertebral disc degeneration (proteoglycan breakdown, height loss)
3. Facet joint arthritis (reduced segmental motion)
4. Proprioceptive threshold increase (declining afferent signaling)
→ **Result:** Progressive decay of $\chi_{\kappa}$, $\chi_M$ → shift toward gravity-dominated regime

**Testable predictions:**
- Longitudinal SRT decline correlates with:
  - EMG-measured motor unit number
  - MRI-measured disc height index
  - Joint ROM measurements
  - Vibration perception thresholds (proprioception proxy)

### 4.2 CSF Flow and Dynamic Information Gradients

**Upstream mechanism:** Cerebrospinal fluid flow driven by ependymal cilia generates:
- Spatial information gradients (morphogen/signaling molecule concentration differences)
- Mechanical signals (shear stress on neural tissues)

Evidence from zebrafish scoliosis models: disrupted ciliary flow → abnormal CSF flow → asymmetric information fields → spinal curvature defects.

**Human extension:** CSF flow is pulsatile (cardiac-driven), affected by:
- Vascular compliance (arterial stiffness with age)
- Venous drainage efficiency
- Physical activity (postural changes modulate CSF dynamics)

**Hypothesis:** Healthy CSF flow supports *temporal modulation* of $I(s,t)$ required for postural transitions. Age-related vascular stiffness → reduced CSF pulsatility → impaired dynamic information field updates → restricted curvature mode access.

**Testable predictions:**
- Phase-contrast MRI measures of CSF flow velocity/pulsatility correlate with:
  - SRT scores (higher flow → higher SRT)
  - $\widehat{D}_{\text{geo}}$ during transitions (higher flow → lower $\widehat{D}_{\text{geo}}$)
- Exercise interventions that improve vascular compliance → improved SRT performance

### 4.3 Cross-Cultural Hypothesis: Floor-Sitting Habits

**Observation:** Traditional floor-sitting cultures (Japan, India, Middle East) maintain regular sit-rise practice throughout lifespan, unlike chair-sitting Western populations.

**Hypothesis:** Habitual sit-rise transitions provide:
- **Mechanical training:** Repeated curvature mode cycling preserves $\chi_{\kappa}$, $\chi_M$ coupling strength
- **Information field maintenance:** Regular dynamic modulation of $I(s,t)$ prevents "mode pruning" (use-it-or-lose-it)
- **CSF flow stimulation:** Postural variety promotes healthy CSF dynamics

**Predicted outcomes in floor-sitting populations:**
- Higher SRT scores at equivalent ages vs. chair-sitting populations
- Preserved lumbar lordosis in elderly (delayed age-related flattening)
- Lower scoliosis prevalence (maintained symmetric information fields)
- Reduced fall risk and disability (broader postural repertoire)

**Testable via:**
- Cross-cultural cohort studies: Japan vs. US/Europe
- Within-culture comparisons: traditional vs. Westernized lifestyles
- Intervention trials: floor-sitting training in chair-accustomed adults

---

## 5. Proposed Validation Study

### 5.1 Design Overview

**Type:** Prospective observational cohort with wearable sensor monitoring

**Primary Aim:** Test correlation between SRT score and geodesic curvature deviation $\widehat{D}_{\text{geo}}$ during sit-rise transitions

**Secondary Aims:**
1. Quantify curvature mode diversity in daily life
2. Relate CSF flow metrics to curvature dynamics (subset with MRI)
3. Cross-cultural comparisons (if feasible)

### 5.2 Participants

**Sample size:** N = 200 adults

**Inclusion criteria:**
- Age 50-80 years
- Ambulatory, community-dwelling
- Able to attempt sit-rise test (even if low score)

**Stratification:**
- SRT score groups: High (8-10), Mid (5-7), Low (0-4)
- ~70 high, 70 mid, 60 low (enriched for low performers to ensure power)

**Optional cross-cultural arm:**
- 100 Western (US/Europe, chair-sitting)
- 100 Asian (Japan/India, floor-sitting habits)

### 5.3 Measurements

#### Baseline (1 session, ~2 hours)

1. **SRT assessment:**
   - Video-recorded from 3 angles (sagittal, frontal, lateral)
   - Scored by 2 independent raters
   - Record time to complete, support used, balance loss

2. **Demographics and health:**
   - Age, sex, BMI, comorbidities
   - Medications (especially affecting balance/strength)
   - Physical activity questionnaire
   - Floor-sitting habits questionnaire (frequency, duration)

3. **Physical function battery:**
   - Timed Up-and-Go (TUG)
   - Single-leg stance time
   - Grip strength (handheld dynamometry)
   - Gait speed (4-meter walk)

4. **Radiographic spinal curvature** (optional, subset):
   - Standing lateral X-ray or EOS imaging
   - Measure Cobb angles, lumbar lordosis, thoracic kyphosis
   - Disc height index at L4-L5, L5-S1

5. **CSF flow MRI** (optional, subset N=40-60):
   - Phase-contrast MRI at cervical level (C2-C3)
   - Measure peak CSF velocity, stroke volume, pulsatility index

#### 7-Day Continuous Monitoring

**Wearable IMU sensors:**
- Placement: T1 (upper thoracic), T6 (mid-thoracic), L3 (lumbar), sacrum
- Measure: 3D acceleration, angular velocity (100 Hz sampling)
- Transmission: Bluetooth to smartphone app (data uploaded nightly)

**Derived measures:**
- **Spinal curvature $\kappa(s,t)$:** Compute from inter-sensor angles
- **Sit-rise event detection:** Automated algorithm identifies floor-to-stand transitions
- **Curvature spectra:** Fourier decomposition of $\kappa(s,t)$ into mode amplitudes
- **Geodesic deviation:** Compute $\widehat{D}_{\text{geo}}$ for each sit-rise event

**Participant diary:**
- Log activities (walking, sitting, lying, exercise)
- Note any floor-sitting or ground activities
- Report falls, near-falls, or balance difficulties

### 5.4 Outcomes and Analysis

#### Primary Outcome

**Correlation between SRT score and mean $\widehat{D}_{\text{geo}}$ during sit-rise transitions**

- Extract all sit-rise events from 7-day monitoring (typically 0-10 per day in Western populations, 5-30 in floor-sitting populations)
- Compute $\widehat{D}_{\text{geo}}(t)$ time series for each event
- Average across events: $\langle \widehat{D}_{\text{geo}} \rangle_{\text{sit-rise}}$
- **Hypothesis:** SRT score inversely correlates with $\langle \widehat{D}_{\text{geo}} \rangle_{\text{sit-rise}}$ (Spearman $\rho < -0.5$, p < 0.001)

#### Secondary Outcomes

1. **Curvature mode diversity:**
   - Shannon entropy of curvature mode amplitudes over 7 days
   - **Hypothesis:** High SRT → high entropy (broad mode usage)

2. **CSF flow correlation (subset):**
   - Peak CSF velocity vs. SRT score
   - Peak CSF velocity vs. $\langle \widehat{D}_{\text{geo}} \rangle_{\text{sit-rise}}$
   - **Hypothesis:** Higher CSF flow → lower $\widehat{D}_{\text{geo}}$, higher SRT

3. **Cross-cultural comparison:**
   - SRT scores: floor-sitting > chair-sitting at equivalent ages
   - Sit-rise frequency: floor-sitting 5-10× higher
   - Curvature mode diversity: floor-sitting > chair-sitting

#### Statistical Analysis

- **Mixed-effects models:** Account for repeated measures (multiple sit-rise events per person)
- **Covariates:** Age, sex, BMI, physical activity, comorbidities
- **Mediation analysis:** Test whether $\widehat{D}_{\text{geo}}$ mediates relationship between age and SRT score
- **Power:** N=200 provides 90% power to detect $|\rho| > 0.25$ at $\alpha=0.05$

### 5.5 Timeline and Budget

**Phase 1: Pilot (6 months, N=20):**
- Validate IMU sensor protocol
- Test curvature estimation algorithms
- Refine sit-rise detection
- Budget: ~$50K (sensors, personnel, analysis)

**Phase 2: Full Study (18 months, N=200):**
- Recruitment: 6 months
- Data collection: 12 months (rolling enrollment)
- Analysis: 6 months (overlaps with collection)
- Budget: ~$400K (sensors, personnel, MRI, imaging, analysis, publication)

**Funding sources:**
- NIH R21 (Exploratory/Developmental)
- NIA R03 (Small grants in aging)
- Foundation grants (Glenn Foundation, AFAR)

---

## 6. Limitations and Cautions

### 6.1 Framework Limitations

**Phenomenological information field:**
- $I(s)$ is not derived from first principles
- Form chosen to match observed curvatures (circular risk)
- Couplings $\chi_{\kappa}$, $\chi_M$ are effective parameters, not directly measurable biological quantities

**Effective metric construction:**
- $g_{\text{eff}}(s)$ formula is heuristic (weights $\beta_1$, $\beta_2$ empirically set)
- Not derived from fundamental physics (analog spacetime, not actual GR)
- Appropriate for organizing mechanical behavior, not predictive ab initio

### 6.2 Observational Study Limitations

**Association ≠ Causation:**
- Proposed validation study is observational (cannot prove $\widehat{D}_{\text{geo}}$ causes SRT changes)
- Residual confounding possible despite covariate adjustment
- Would require RCT (e.g., balance training intervention) to establish causality

**SRT is composite:**
- Conflates multiple systems (strength, flexibility, balance, motor control)
- Framework focuses on spinal curvature, but hip/knee/ankle biomechanics also critical
- Cannot isolate "pure" curvature mode access from other contributors

**IMU curvature estimation:**
- 4 sensors provide coarse spatial resolution (~3-4 spinal segments)
- Cannot resolve individual vertebral level curvatures
- Validated against reference standards (motion capture, radiography) needed

### 6.3 Cross-Cultural Hypothesis Limitations

**Floor-sitting ≠ Japanese:**
- Original hypothesis focused on Japanese populations, but de Brito study was Brazilian
- Floor-sitting common in many cultures (India, Middle East, East Asia)
- Within-culture variation likely large (urban vs. rural, traditional vs. Westernized)

**Lifestyle confounders:**
- Floor-sitting populations may differ in:
  - Diet (Mediterranean, Asian patterns)
  - Physical activity patterns (walking, agriculture)
  - Genetics (body proportions, bone density)
  - Healthcare access
- Need careful matching or statistical control

### 6.4 Clinical Translation Limitations

**Interventions unclear:**
- If $\widehat{D}_{\text{geo}}$ correlates with SRT, what interventions target it?
- Balance training, strength training improve SRT but mechanism unclear
- Cannot directly "increase $\chi_{\kappa}$" pharmacologically (yet)

**Individual variability:**
- Framework predicts population-level associations
- Individual predictions (e.g., mortality risk from $\widehat{D}_{\text{geo}}$) not validated
- Clinical use requires personalized cutoffs, validation in diverse populations

---

## 7. Significance and Broader Impact

### 7.1 Theoretical Contribution

This work extends the biological countercurvature framework from:
- **Static equilibrium** (standing S-curve, scoliosis patterns)
- To **dynamic postural transitions** (sit-rise, gait, reaching)

Demonstrates that information-geometry perspective applies not only to pathological curvature (scoliosis) but also to **functional capacity and aging**, linking theory to clinically relevant outcomes.

### 7.2 Clinical Implications

If validated, framework suggests:

1. **Novel intervention targets:**
   - Therapies to preserve $\chi_{\kappa}$, $\chi_M$ coupling (pharmacological, exercise-based)
   - CSF flow enhancement (vascular training, manual therapy, medications)

2. **Monitoring tools:**
   - Wearable sensors quantify $\widehat{D}_{\text{geo}}$ as longitudinal biomarker of "curvature health"
   - Track response to interventions objectively

3. **Personalized rehabilitation:**
   - Identify specific mode deficits (e.g., lumbar flexion vs. extension)
   - Target training to expand accessible mode repertoire

### 7.3 Cross-Cultural and Public Health

**If floor-sitting hypothesis confirmed:**
- Simple lifestyle modification (daily floor-sitting practice) could preserve mobility and reduce fall/disability risk in aging populations
- Culturally tailored interventions (reintroduce traditional practices lost to Westernization)
- Public health campaigns promoting postural diversity

**Broader implication:**
- "Postural monoculture" (prolonged chair-sitting) as modifiable risk factor for functional decline
- Environmental design: incorporate floor-level surfaces, varied seating heights in homes, workplaces, public spaces

---

## 8. Next Steps

### 8.1 Immediate (Post-PRX Life Submission)

1. **Literature expansion:**
   - Systematic review of all SRT studies (mortality, disability, functional correlates)
   - Search for spinal curvature + SRT correlation studies
   - Compile cross-cultural sitting habit data

2. **Simulation work:**
   - PyElastica models of sit-rise transitions
   - Generate $\kappa(s,t)$ trajectories for high vs. low SRT performers
   - Compute $\widehat{D}_{\text{geo}}(t)$ time series, energy landscapes

3. **Pilot sensor validation:**
   - Test IMU sensor placement, calibration on N=5-10 volunteers
   - Validate curvature estimation against motion capture reference
   - Refine sit-rise detection algorithm

### 8.2 Medium-Term (3-6 months)

1. **Full manuscript draft:**
   - Expand this extended abstract to 6000-8000 words
   - Add simulation results (figures of curvature trajectories, $\widehat{D}_{\text{geo}}$ plots)
   - Write detailed Methods and Results sections

2. **Collaborator recruitment:**
   - Gerontologist (functional assessment expertise)
   - Physical therapist (sit-rise biomechanics)
   - Cross-cultural health researcher (Japan/Asia connections)
   - Neuroradiologist (CSF flow MRI)

3. **Grant preparation:**
   - NIH R21 (Exploratory/Developmental): $275K, 2 years
   - Target submission: February 2026 (after PRX Life acceptance)

### 8.3 Long-Term (6-18 months)

1. **Pilot data collection** (N=20):
   - Proof of concept for IMU protocol
   - Preliminary $\widehat{D}_{\text{geo}}$ vs. SRT correlation
   - Use for grant applications and manuscript strengthening

2. **Manuscript submission:**
   - Target: Frontiers in Physiology (Gerontology section)
   - Timeline: 6 months after PRX Life acceptance (momentum from main paper)

3. **Full validation study:**
   - Pending R21 funding approval
   - N=200, 18-month study
   - Results inform R01 for intervention trial

---

## 9. Target Journals and Publication Strategy

### Primary Target: **Frontiers in Physiology** (Gerontology and Geriatric Physiology section)

**Rationale:**
- Open access (broad readership)
- Interdisciplinary scope (biomechanics + gerontology + theoretical framework)
- 2-3 month review (faster than traditional journals)
- Accepts "hypothesis and theory" articles (our extended abstract fits this format)

**Submission format:**
- Hypothesis and Theory article (3000-5000 words)
- Can submit extended abstract version initially, then expand if accepted

### Secondary Targets:

1. **Journals of Gerontology: Medical Sciences**
   - High-impact gerontology (IF ~6)
   - Strong functional assessment focus
   - 4-6 month review
   - Use if Frontiers rejects or if we expand to full research article with pilot data

2. **Age and Ageing**
   - Clinical gerontology focus
   - European audience
   - Good for cross-cultural work
   - 3-5 month review

3. **PLOS ONE**
   - Open access, broad readership
   - Accepts theoretical/methods papers
   - Very fast review (2-3 months)
   - Lower bar but wide dissemination

### Publication Timeline:

- **Now:** Extended abstract complete
- **1-2 months:** Expand to full manuscript with simulations
- **3-4 months:** Submit to Frontiers (after PRX Life submitted)
- **6-9 months:** Revision, acceptance
- **9-12 months:** Published (online)

---

## 10. Summary

This extended abstract presents a novel interpretation of the sit-rise test through a biological countercurvature framework. We propose that SRT performance reflects the capacity to dynamically access curvature modes in an information-shaped effective gravitational geometry, operationalized as geodesic curvature deviation $\widehat{D}_{\text{geo}}$.

**Key contributions:**
- First mechanistic geometric framework for SRT-mortality association
- Testable hypotheses linking information-curvature coupling to functional mobility
- Concrete validation study design using wearable sensors
- Cross-cultural predictions (floor-sitting hypothesis)

**Next milestone:** Develop full manuscript with simulation results, submit to Frontiers in Physiology within 3-6 months (post-PRX Life).

This work bridges fundamental biophysics (countercurvature theory), clinical gerontology (functional assessment), and public health (lifestyle interventions), with potential to reshape how we understand and preserve mobility in aging.

---

**Document status:** Extended abstract — ready for manuscript development
**Last updated:** 2025-11-18
**Contact:** dr.sayujkrishnan@gmail.com
