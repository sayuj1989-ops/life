# Zebrafish Motile Cilia Assay Standard Operating Procedures

## 1. Foxj1a Reporter Line Maintenance

### 1.1 Line Genotyping Protocol

**Purpose**: Confirm foxj1a::eGFP and foxj1a::ptk7 transgene presence

**Materials**:
- Genomic DNA extraction kit
- Foxj1a-specific primers (forward: 5'-ATGGCGAGCTGAAGGGCGAGG-3', reverse: 5'-TCACCTTCATGCCGAGAGTG-3')
- PCR master mix
- Gel electrophoresis equipment

**Procedure**:
1. Extract genomic DNA from fin clips using standard protocols
2. Perform PCR with foxj1a primers (95°C 5min, 35 cycles of 95°C 30s, 60°C 30s, 72°C 45s, 72°C 5min)
3. Analyze products on 1% agarose gel
4. Positive control: Expected band ~500bp for foxj1a::eGFP, ~800bp for foxj1a::ptk7

**Quality Control**: Include WT negative control and known transgenic positive control in each run

### 1.2 Husbandry Conditions

**Temperature Control**:
- Maintain programmable racks at 25°C (permissive) and 30°C (restrictive)
- Daily temperature logging with ±0.5°C accuracy
- Backup temperature monitoring system

**Water Quality**:
- Conductivity: 500-1500 μS/cm
- pH: 6.5-7.5
- Daily water quality testing and logging

## 2. CSF Flow Quantification Protocol

### 2.1 Fluorescent Bead Injection

**Materials**:
- Fluorescent microspheres (1μm diameter, red fluorescent, 580/605nm)
- Micromanipulator setup
- Glass capillary needles (1-2μm tip diameter)
- Anesthesia solution (0.02% tricaine)

**Procedure**:
1. Anesthetize zebrafish larvae (5-7 dpf) in tricaine solution
2. Position larvae ventral side up under dissecting microscope
3. Inject 0.5-1μL bead suspension into fourth ventricle using micromanipulator
4. Allow 30 minutes recovery in clean system water
5. Transfer to imaging chamber for flow analysis

**Quality Control**: 
- Verify bead injection success by confocal imaging
- Exclude larvae with injection artifacts or excessive bead clumping
- Maintain consistent injection volume across experiments

### 2.2 Live Imaging Setup

**Equipment**:
- Confocal microscope with 488nm laser
- 20x water immersion objective
- Temperature-controlled imaging chamber
- High-speed camera capability (≥30 fps)

**Imaging Parameters**:
- Excitation: 488nm
- Emission: 500-550nm (GFP channel)
- Z-stack: 20-30μm depth, 2μm steps
- Time series: 60 seconds duration, 1 frame/second
- Resolution: 512×512 pixels

**Procedure**:
1. Mount larvae in imaging chamber with minimal anesthesia
2. Focus on fourth ventricle region
3. Acquire time-lapse series of bead movement
4. Record environmental conditions (temperature, time, fish ID)

### 2.3 TrackMate Analysis Workflow

**Software Requirements**:
- FIJI/ImageJ with TrackMate plugin
- Custom Python scripts for trajectory analysis
- MATLAB for statistical analysis

**Analysis Steps**:
1. Import time-lapse series into FIJI
2. Apply TrackMate with parameters:
   - Spot detection: LoG detector, estimated blob diameter 2μm
   - Initial threshold: 0.5
   - Linking: Simple LAP tracker, max distance 5μm
3. Export trajectory data
4. Calculate metrics using Python scripts:
   - Mean velocity (μm/s)
   - Directional persistence (autocorrelation)
   - Flow coherence (vector alignment)

**Quality Control**:
- Manual verification of tracking accuracy
- Exclusion of trajectories <10 frames duration
- Statistical validation of flow directionality

## 3. Cilia Morphology Analysis

### 3.1 Immunofluorescence Staining

**Materials**:
- Primary antibodies: anti-acetylated tubulin (1:1000), anti-DNAH5 (1:500)
- Secondary antibodies: Alexa Fluor conjugates
- Fixative: 4% paraformaldehyde
- Permeabilization buffer: 0.1% Triton X-100

**Procedure**:
1. Fix larvae in 4% PFA for 2 hours at 4°C
2. Dehydrate through ethanol series (25%, 50%, 75%, 100%)
3. Embed in paraffin, section at 5μm thickness
4. Deparaffinize and rehydrate sections
5. Block in 5% normal goat serum for 1 hour
6. Incubate with primary antibodies overnight at 4°C
7. Wash 3×5 minutes in PBS
8. Incubate with secondary antibodies for 2 hours at room temperature
9. Mount with DAPI-containing mounting medium

### 3.2 Confocal Imaging and Analysis

**Imaging Parameters**:
- 63x oil immersion objective
- Z-stack: 10μm depth, 0.5μm steps
- Multi-channel acquisition (DAPI, GFP, Alexa Fluor)
- Resolution: 1024×1024 pixels

**Quantification Metrics**:
1. Cilia density: Number of cilia per 100μm² ependymal surface
2. Cilia length: Average length from base to tip
3. Orientation index: Vector analysis of cilia alignment
4. Foxj1a expression: Fluorescence intensity quantification

**Analysis Software**:
- FIJI for image processing and measurement
- Custom MATLAB scripts for orientation analysis
- GraphPad Prism for statistical analysis

## 4. Micro-CT Skeletal Analysis

### 4.1 Sample Preparation

**Materials**:
- 4% paraformaldehyde fixative
- 70% ethanol storage solution
- Micro-CT compatible mounting system

**Procedure**:
1. Fix larvae in 4% PFA for 24 hours at 4°C
2. Transfer to 70% ethanol for storage
3. Mount in micro-CT compatible holder
4. Ensure minimal air bubbles around sample

### 4.2 Micro-CT Scanning Parameters

**Equipment**: Bruker Skyscan 1272 or equivalent

**Scanning Parameters**:
- Voltage: 50kV
- Current: 200μA
- Resolution: 5μm voxel size
- Rotation: 180° with 0.3° steps
- Exposure time: 1 second per projection
- Filter: 0.5mm aluminum

### 4.3 Image Reconstruction and Analysis

**Reconstruction Software**: NRecon (Bruker) or equivalent

**Parameters**:
- Ring artifact correction: 5
- Beam hardening correction: 20%
- Smoothing: 0
- Output format: 16-bit TIFF

**Analysis Workflow**:
1. Import reconstructed images into CTAn (Bruker) or equivalent
2. Define region of interest (ROI) encompassing entire spine
3. Apply threshold for bone segmentation
4. Generate 3D model
5. Calculate metrics:
   - Cobb-like angle measurement
   - Vertebral rotation indices
   - Kyphosis/lordosis measurements
   - Spine length and curvature radius

**Quality Control**:
- Verify reconstruction quality (no artifacts, proper contrast)
- Calibrate measurements using phantom standards
- Inter-observer reliability testing for angle measurements

## 5. Hydrocephalus Index Calculation

### 5.1 Ventricular Volume Measurement

**Method**: Confocal imaging of brain ventricles

**Procedure**:
1. Image fixed larvae with DAPI staining
2. Define ventricular boundaries manually
3. Calculate ventricular volume using 3D reconstruction
4. Normalize to body length (snout to tail tip)

**Formula**: Hydrocephalus Index = Ventricular Volume (mm³) / Body Length (mm)

**Quality Control**:
- Consistent imaging parameters across samples
- Blinded measurement by multiple observers
- Statistical validation of measurement reliability

## 6. Temperature-Shift Experiments

### 6.1 Temperature-Sensitive Allele Protocol

**Materials**: c21orf59^TS zebrafish line

**Procedure**:
1. Maintain embryos at permissive temperature (25°C) until desired shift time
2. Transfer to restrictive temperature (30°C) at specified developmental stages:
   - 19 dpf (early shift)
   - 24 dpf (mid-shift)
   - 29 dpf (late shift)
   - 34 dpf (very late shift)
3. Monitor for phenotypic development
4. For rescue experiments, shift back to permissive temperature at first signs of curvature

**Data Collection**:
- Daily phenotypic assessment
- Growth measurements (length, weight)
- CSF flow analysis at multiple time points
- Skeletal analysis at endpoint

### 6.2 Environmental Monitoring

**Requirements**:
- Continuous temperature logging (±0.1°C accuracy)
- Daily water quality testing
- Growth rate documentation
- Mortality tracking

**Documentation**:
- Temperature logs with timestamps
- Water quality parameters
- Fish identification and lineage tracking
- Experimental timeline documentation

## 7. Data Management and Quality Control

### 7.1 Data Organization

**File Naming Convention**:
- Genotype_Date_ExperimentType_FishID
- Example: ptk7mut_20241201_CSFflow_F001

**Database Fields**:
- Fish ID and genotype
- Experimental conditions (temperature, age)
- Imaging parameters
- Quantitative measurements
- Quality control flags

### 7.2 Statistical Analysis Plan

**Primary Endpoints**:
- CSF flow velocity (continuous variable)
- Hydrocephalus index (continuous variable)
- Cobb-like angle (continuous variable)

**Statistical Tests**:
- ANOVA for multiple group comparisons
- Post-hoc testing with Bonferroni correction
- Correlation analysis for temporal relationships
- Power analysis for sample size determination

**Sample Size Calculation**:
- Power: 80%
- Alpha: 0.05
- Effect size: Based on pilot data
- Minimum n=10 per group (increased for multiple comparisons)

### 7.3 Quality Control Metrics

**Inclusion Criteria**:
- Successful bead injection
- Complete imaging series
- No technical artifacts
- Appropriate developmental stage

**Exclusion Criteria**:
- Injection failures
- Imaging artifacts
- Developmental abnormalities unrelated to genotype
- Mortality before endpoint

**Blinding Protocol**:
- Genotype blinding during imaging
- Blinded analysis of quantitative metrics
- Independent verification of measurements

This SOP provides comprehensive protocols for all major zebrafish motile cilia assays, ensuring reproducibility and quality control across the research program.

