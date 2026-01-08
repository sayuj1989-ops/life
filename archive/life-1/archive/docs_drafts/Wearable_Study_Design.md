# Wearable Study Design: Capturing Curvature Spectra for IEC/GOP Model Validation

## Overview

This document outlines the prototype wearable study design to capture spinal curvature spectra (κ(s,t)) for validating the sinusoidal stretch hypothesis and quantifying lifestyle-mediated IEC/GOP effects. The study aims to measure curvature dynamics during floor-sitting habits and validate predictions of the IEC framework.

---

## Study Objectives

### Primary Objective
To capture continuous spinal curvature spectra κ(s,t) during daily activities, focusing on floor-sitting transitions (sit-to-rise, rise-to-sit) and validate the sinusoidal stretch hypothesis.

### Secondary Objectives
1. Quantify daily STR transition frequency (f) in Japanese floor-sitting vs. Western chair-sitting populations
2. Measure curvature modulation amplitude A(t) and its temporal variation
3. Estimate IEC parameters (χ_κ, χ_f) from measured curvature spectra
4. Validate IEC model predictions against wearable sensor data

---

## Study Design

### Study Type
Prospective, cross-sectional, observational study with pilot validation phase

### Study Population
- **Pilot Phase:** n = 20 (10 Japanese floor-sitters, 10 Western chair-sitters)
- **Full Study:** n = 100 (50 Japanese floor-sitters, 50 Western chair-sitters)
- **Age Range:** 40-70 years (to capture age-related curvature changes)
- **Inclusion Criteria:**
  - Japanese cohort: Documented floor-sitting habits (≥20 years)
  - Western cohort: Primarily chair-sitting habits
  - Ability to perform STR movements independently
  - No history of spinal surgery or severe spinal deformity
  - Informed consent

### Study Duration
- **Pilot Phase:** 2 weeks (device validation, protocol refinement)
- **Full Study:** 7-day continuous monitoring per participant
- **Total Duration:** 6 months (recruitment + data collection)

---

## Device Specifications

### Wearable Sensor System

#### Core Components

1. **Inertial Measurement Units (IMUs)**
   - **Type:** 9-axis IMU (accelerometer, gyroscope, magnetometer)
   - **Placement:** 7-9 sensors along spinal arclength
     - C7 (cervical)
     - T3, T6, T9, T12 (thoracic)
     - L3, L5 (lumbar)
     - Optional: S1 (sacral)
   - **Sampling Rate:** 100 Hz (sufficient for curvature reconstruction)
   - **Specifications:**
     - Range: ±16g accelerometer, ±2000°/s gyroscope
     - Resolution: 16-bit ADC
     - Wireless: Bluetooth Low Energy (BLE) or Zigbee
     - Battery: 7-day continuous operation

2. **Pressure Sensors**
   - **Type:** Flexible pressure-sensitive arrays
   - **Placement:** Distributed along spine (intervertebral disc regions)
   - **Function:** Detect floor contact and loading patterns during floor-sitting
   - **Sampling Rate:** 50 Hz

3. **Data Logger**
   - **Type:** Centralized hub or distributed per-sensor
   - **Storage:** 32GB minimum (for 7-day continuous data)
   - **Synchronization:** Sub-millisecond timestamp accuracy across sensors
   - **Connectivity:** BLE/Zigbee for real-time monitoring, USB for data download

#### Recommended Devices

1. **Xsens MVN Awinda**
   - **Pros:** Established motion capture system, validated for biomechanics
   - **Cons:** Higher cost, may require custom spinal sensor configuration
   - **Suitability:** High (if budget allows)

2. **APDM Opal**
   - **Pros:** Designed for clinical biomechanics, validated algorithms
   - **Cons:** May require custom placement for spinal curvature
   - **Suitability:** High

3. **Custom IMU Array**
   - **Pros:** Optimal sensor placement, cost-effective
   - **Cons:** Requires custom firmware and data processing pipeline
   - **Suitability:** Medium (if engineering resources available)

---

## Measurement Protocol

### Pre-Study Calibration

1. **Anatomic Landmarks:**
   - Mark sensor positions on skin (C7, T3, T6, T9, T12, L3, L5)
   - Measure inter-sensor distances along spinal arclength
   - Validate sensor placement with radiographs (baseline)

2. **Sensor Calibration:**
   - Static calibration (neutral standing posture)
   - Dynamic calibration (known movements: flexion, extension, rotation)
   - Coordinate system alignment (global vs. local frames)

3. **Radiographic Validation:**
   - Baseline standing radiographs (AP and lateral)
   - Supine MRI (optional, for detailed curvature profiles)
   - Cross-reference sensor-derived curvature with radiographic measurements

### Data Collection Schedule

#### Day 1: Baseline Assessment
- **Morning:** Sensor placement, calibration, baseline measurements
- **Afternoon:** Radiographic assessment (standing radiographs)
- **Evening:** Begin continuous monitoring

#### Days 2-7: Continuous Monitoring
- **Daily:** 7-day continuous data collection
- **Self-Report:** Daily activity log (floor-sitting frequency, STR transitions)
- **Compliance Check:** Sensor connectivity monitoring, data quality checks

#### Day 8: Post-Study Assessment
- **Morning:** Sensor removal, final measurements
- **Afternoon:** Data download and preliminary quality check

---

## Data Processing Pipeline

### 1. Raw Data Preprocessing

**Input:** Raw IMU data (accelerometer, gyroscope, magnetometer) from all sensors

**Steps:**
1. **Noise Filtering:**
   - Low-pass filter (cutoff: 10 Hz) for accelerometer
   - High-pass filter (cutoff: 0.1 Hz) for gyroscope drift removal
   - Magnetometer calibration (hard/soft iron correction)

2. **Sensor Fusion:**
   - Complementary or Kalman filter for orientation estimation
   - Quaternion representation of sensor orientations
   - Coordinate system transformation (sensor → global → spinal)

3. **Synchronization:**
   - Timestamp alignment across all sensors
   - Interpolation to common time base (100 Hz)

### 2. Curvature Reconstruction

**Input:** Sensor orientations (quaternions) at each spinal level

**Steps:**
1. **Spinal Centerline Estimation:**
   - Calculate 3D positions of sensors along spine
   - Fit smooth spline curve through sensor positions
   - Extract centerline r(s) where s = arclength

2. **Curvature Calculation:**
   - Compute curvature κ(s) = ||d²r/ds²||
   - Compute torsion τ(s) for 3D analysis
   - Extract curvature components:
     - Sagittal plane curvature κ_sag(s)
     - Coronal plane curvature κ_cor(s)
     - Axial rotation (if applicable)

3. **Temporal Curvature Spectra:**
   - Generate κ(s,t) matrix (curvature vs. arclength vs. time)
   - Time resolution: 0.01 s (100 Hz)
   - Spatial resolution: 0.01 m (inter-sensor distance)

### 3. STR Transition Detection

**Input:** Curvature spectra κ(s,t), pressure sensor data, accelerometer data

**Steps:**
1. **Event Detection:**
   - Detect STR transitions using:
     - Vertical acceleration (upward movement)
     - Pressure sensor activation (floor contact)
     - Curvature change patterns (flexion → extension)

2. **Transition Classification:**
   - Sit-to-rise (STR)
   - Rise-to-sit (RTS)
   - Floor-sitting postures (seiza, agura, yoko-zuwari)

3. **Frequency Calculation:**
   - Count daily STR transitions
   - Calculate transition frequency f (transitions/day)
   - Extract temporal patterns (diurnal variation)

### 4. IEC Parameter Estimation

**Input:** Curvature spectra κ(s,t), STR transition frequency f, baseline curvature κ_0(s)

**Steps:**
1. **Curvature Modulation Analysis:**
   - Extract modulation amplitude A(t) = max(κ(s,t)) - min(κ(s,t))
   - Calculate temporal variation in amplitude
   - Identify sinusoidal patterns in curvature dynamics

2. **IEC-1 Parameter Estimation (χ_κ):**
   - Fit target curvature bias: κ̄(s) = κ_0(s) + χ_κ · ∂I/∂s
   - Estimate χ_κ from curvature shifts during STR transitions
   - Validate against model predictions

3. **IEC-3 Parameter Estimation (χ_f):**
   - Fit active moment: M_act(s) = χ_f · ∇I(s)
   - Estimate χ_f from curvature changes during active movements
   - Validate against model predictions

4. **Information Field Estimation:**
   - Reconstruct I(s,t) from measured curvature spectra
   - Calculate gradient ||∇I(s,t)||
   - Extract spatial and temporal patterns

---

## Validation Metrics

### 1. Curvature Accuracy

**Metric:** Root-mean-square error (RMSE) between sensor-derived and radiographic curvature

**Target:** RMSE < 0.05 m⁻¹ (5% error in curvature)

**Validation:** Compare baseline curvature κ(s) from sensors vs. radiographs

### 2. Temporal Accuracy

**Metric:** STR transition detection accuracy

**Target:** >95% sensitivity and specificity for STR detection

**Validation:** Manual annotation of STR events from video recordings

### 3. IEC Parameter Consistency

**Metric:** Coefficient of variation (CV) of IEC parameter estimates across participants

**Target:** CV < 20% for χ_κ and χ_f within each cohort

**Validation:** Compare parameter distributions between cohorts

### 4. Model Prediction Accuracy

**Metric:** Correlation between measured and predicted curvature spectra

**Target:** R² > 0.80 for curvature prediction

**Validation:** Fit IEC model to training data, validate on test data

---

## Expected Outcomes

### 1. Curvature Spectra Differences

**Hypothesis:** Japanese floor-sitters show higher curvature modulation amplitude A(t)

**Predicted Values:**
- **Floor-sitters:** A = 0.15-0.25 m⁻¹ (peak modulation)
- **Chair-sitters:** A = 0.05-0.10 m⁻¹ (reduced modulation)

### 2. STR Transition Frequency

**Hypothesis:** Japanese floor-sitters show higher daily STR transition frequency f

**Predicted Values:**
- **Floor-sitters:** f = 20-40 transitions/day
- **Chair-sitters:** f = 5-15 transitions/day

### 3. IEC Parameter Estimates

**Hypothesis:** Japanese floor-sitters show higher χ_κ and χ_f values

**Predicted Values:**
- **χ_κ (floor-sitters):** 0.04-0.08 m
- **χ_κ (chair-sitters):** 0.02-0.04 m
- **χ_f (floor-sitters):** 0.05-0.1 N·m
- **χ_f (chair-sitters):** 0.01-0.05 N·m

### 4. Temporal Signatures

**Hypothesis:** Curvature modulation shows diurnal variation, peaking during active floor-sitting periods

**Predicted Patterns:**
- **Peak Times:** Morning (6-8 AM), evening (6-8 PM)
- **Reduced Times:** Night (midnight-6 AM)
- **Diurnal Amplitude:** 20-30% variation in modulation amplitude

---

## Statistical Analysis Plan

### 1. Descriptive Statistics

- **Cohort Comparison:**
  - Mean ± SD for curvature modulation amplitude A
  - Mean ± SD for STR transition frequency f
  - Mean ± SD for IEC parameters (χ_κ, χ_f)

- **Temporal Analysis:**
  - Diurnal variation in curvature modulation
  - STR transition patterns (frequency, timing)

### 2. Inferential Statistics

- **Primary Comparison:**
  - Independent t-test or Mann-Whitney U test for cohort differences
  - Effect size (Cohen's d) for curvature modulation amplitude

- **Secondary Analysis:**
  - Linear regression: IEC parameters vs. age, floor-sitting frequency
  - Correlation analysis: χ_κ vs. χ_f, A vs. f

### 3. Model Validation

- **Cross-Validation:**
  - Leave-one-out or k-fold cross-validation for IEC parameter estimation
  - R², RMSE for curvature prediction accuracy

- **Sensitivity Analysis:**
  - Parameter uncertainty quantification
  - Model robustness to sensor placement variations

---

## Ethical Considerations

### 1. Informed Consent

- Detailed explanation of sensor placement and data collection
- Privacy and data security measures
- Right to withdraw at any time

### 2. Data Privacy

- De-identification of participant data
- Secure data storage and transmission
- Limited access to identifiable information

### 3. Safety

- Sensor placement guidelines (avoid skin irritation)
- Daily compliance checks (sensor connectivity, participant comfort)
- Emergency contact procedures

---

## Timeline and Resources

### Phase 1: Pilot Study (Weeks 1-4)

- **Week 1:** Device procurement and setup
- **Week 2:** Pilot participant recruitment (n=5)
- **Week 3:** Pilot data collection and protocol refinement
- **Week 4:** Data analysis and validation

### Phase 2: Full Study (Weeks 5-24)

- **Weeks 5-8:** Full participant recruitment (n=100)
- **Weeks 9-20:** Data collection (7 days per participant)
- **Weeks 21-24:** Data analysis and manuscript preparation

### Resources Required

- **Equipment:** IMU sensors (7-9 per participant), data loggers, calibration equipment
- **Personnel:** Research coordinator, data analyst, technical support
- **Budget:** ~$50,000-100,000 (device costs, participant compensation, personnel)

---

## Deliverables

1. **Pilot Validation Report:**
   - Device validation results
   - Protocol refinements
   - Preliminary curvature spectra

2. **Full Study Dataset:**
   - Curvature spectra κ(s,t) for all participants
   - STR transition data
   - IEC parameter estimates

3. **Validation Analysis:**
   - Comparison of sensor-derived vs. radiographic curvature
   - IEC model validation results
   - Statistical analysis of cohort differences

4. **Publication:**
   - Manuscript describing wearable study design and results
   - Validation of sinusoidal stretch hypothesis
   - IEC parameter estimates for lifestyle-mediated effects

---

## References

1. **Xsens Technologies.** MVN Awinda User Manual. [Online] Available: https://www.xsens.com/

2. **APDM Wearable Technologies.** Opal User Manual. [Online] Available: https://www.apdm.com/

3. **Favre J, Aissaoui R, Jolles BM, et al.** Functional calibration procedure for 3D knee joint angle description using inertial sensors. *J Biomech*. 2009;42(14):2330-2335.

4. **Seel T, Raisch J, Schauer T.** IMU-based joint angle measurement for gait analysis. *Sensors*. 2014;14(4):6891-6909.

---

*Document prepared: [Date]*  
*Status: Study Design - Prototype Phase*

