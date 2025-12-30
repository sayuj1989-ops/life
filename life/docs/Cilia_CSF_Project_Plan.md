# Cilia–CSF Idiopathic Scoliosis Program Plan

## 1. Revised Grant/Protocol Aims

| Aim | Central Hypothesis & Objectives | Inclusion Criteria | Primary Quantitative Readouts | Milestones & Owners |
| --- | --- | --- | --- | --- |
| **Aim 1**<br>Define how motile-cilia gene perturbations disrupt CSF flow and trigger scoliosis. | Loss of motile-cilia function (ptk7, ccdc40, ccdc151, dyx1c1, c21orf59) reduces ventricular CSF flow, initiating adolescent-onset curvature. | Zebrafish genotypes: WT, ptk7-/-, Tg(foxj1a::ptk7) rescue, c21orf59^TS, dyx1c1-/-, ccdc40-/-, ccdc151-/-.<br>Age window: 19–34 dpf.<br>Exclusion: congenital vertebral malformations, incomplete temperature-shift history. | • Ventricular bead-tracking velocity (mean, vector persistence).<br>• Foxj1a::eGFP cilia density/orientation indices.<br>• Hydrocephalus index (ventricle volume/body length). | Draft protocol language and data dictionary (Lead: D. Grimes) – **due 1 week**.<br>Finalize SOPs with zebrafish core (Lead: C. Boswell) – **due 2 weeks**. |
| **Aim 2**<br>Define the temporal requirement for motile-cilia function during rapid growth. | There is a discrete developmental window where motile-cilia activity is essential; restoring function within this window prevents curve progression. | c21orf59^TS cohorts subjected to temperature shifts at 19, 24, 29, 34 dpf and permissive-shift rescues at curve initiation.<br>Sample size ≥12 per condition.<br>Growth-rate records required. | • Longitudinal CSF flow recovery curves post-shift.<br>• μCT Cobb-like curvature angles, vertebral rotation metrics.<br>• Growth velocity (length/week). | Incorporate temperature-shift matrix & imaging schedule into protocol (Lead: N. Morante) – **due 10 days**.<br>Define statistical analysis plan (Lead: Bioinformatics core) – **due 3 weeks**. |
| **Aim 3**<br>Evaluate translational biomarkers of CSF dysregulation in human IS. | CSF flow irregularities and ciliary biomarkers measured around peak growth velocity predict curve initiation and progression. | Adolescents 9–16 years: preclinical high-risk, newly diagnosed mild curves, mid-progression (Cobb 15–35°), matched controls.<br>Exclusion: neuromuscular/congenital scoliosis, prior spinal surgery. | • Phase-contrast MRI flow (aqueduct, fourth ventricle, cervical canal).<br>• Serum/CSF ciliary proteins (FOXJ1 targets, DNAH5).<br>• Nasal epithelial cilia beat frequency/ultrastructure.<br>• Curve progression rate (ΔCobb°/year). | Draft IRB amendment & consent modifications (Lead: Clinical research office) – **due 2 weeks**.<br>Establish data-sharing agreement with radiology (Lead: R. Boswell) – **due 4 weeks**. |

**Distribution Plan**  
- Circulate this aims table with narrative protocol updates to co-investigators, zebrafish core, and regulatory staff by **[D+0]** (owner: Project Manager).  
- Collect written feedback by **[D+7]**; schedule 60-minute review meeting **[D+8/9]**.  
- Submit consolidated revisions to the IRB/grants office by **[D+14]**.

## 2. Zebrafish Assay Readiness Plan

**Reagent & Line Procurement**
- Order/confirm availability of Tg(foxj1a::eGFP) and Tg(foxj1a::ptk7) breeders (contact: Zebrafish Core Logistics, PO submission **[D+2]**).
- Prepare capped mRNA synthesis for PTK7 as backup; validate by qPCR and in situ expression.

**Instrumentation & SOPs**
- Reserve imaging time blocks: confocal bead-tracking (2 × 4 h slots/week), SEM (monthly), μCT (weekly).  
- Finalize SOPs covering bead injection, imaging settings, TrackMate analysis, hydrocephalus measurement, and μCT reconstruction; store in shared drive **[D+5]**.

**PTK7 Rescue Reproducibility Pilot**
- Cohorts: WT (n≥10), ptk7-/- (n≥10), ptk7-/-;Tg(foxj1a::ptk7) (n≥10).  
- Success benchmarks:  
  1. Mean CSF velocity ≥80% of WT with p<0.05 difference vs untreated mutants.  
  2. Hydrocephalus index within 1 SD of WT.  
  3. Cobb-like μCT angle <10° in ≥80% of rescues.  
- Compile pilot report with raw data, QC metrics, and troubleshooting guide **[D+21]**.

**Risk Mitigation**
- Maintain backup imaging slots; implement environmental monitoring (temperature, conductivity) with daily log.  
- Establish reagent redundancy (duplicate mRNA aliquots, spare bead batches).

## 3. Clinical Coordination Plan

**Kickoff Meeting**
- Participants: radiology lead, pediatric orthopedics, neurology, biobank manager, data manager, regulatory lead.  
- Agenda: longitudinal schedule (6-month intervals from Risser 0–3), MRI protocol harmonization, biospecimen pipeline, consent updates.  
- Schedule meeting by **[D+3]**; circulate pre-read (current protocol, proposed updates) 48 h prior.

**Imaging Protocols**
- Radiology to draft standardized phase-contrast MRI parameters (aqueduct, fourth ventricle, cervical canal) and test-retest reliability plan **[D+10]**.  
- Define image storage, anonymization, and quantitative analysis workflow (e.g., MATLAB/Python scripts for flow metrics).

**Biospecimen Workflow**
- Biospecimens per visit: serum, nasal epithelial brushings, optional CSF when clinically indicated.  
- Biobank to supply kits, processing SOPs, and chain-of-custody forms **[D+12]**.  
- Ensure assays for ciliary biomarkers (ELISA/LC-MS) and high-speed video microscopy capacity are available or contracted.

**Regulatory Alignment**
- Update consent/assent documents to reflect additional imaging frequency and sample collection; submit IRB amendment **[D+14]**.  
- Draft data-use agreements covering MRI and biomarker datasets (legal review **[D+18]**).  
- Set up REDCap (or equivalent) project with fields for growth metrics, imaging, biomarker data, and visit tracking **[D+15]**.

**Communication & Reporting**
- Weekly 30-minute stand-up (Fridays) for cross-functional updates starting **[D+7]**.  
- Monthly integrated report summarizing zebrafish assay status, clinical recruitment, imaging compliance, and regulatory milestones.

