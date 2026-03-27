# Spine Deformity Submission Checklist

**Target**: Spine Deformity (Springer Nature) — Official Journal of the Scoliosis Research Society
**Article Type**: Original Article (Computational/Basic Science)
**Manuscript**: "The Derivative Gain Gap: A Control-Theoretic Mechanism for Adolescent Idiopathic Scoliosis"

---

## Pre-Submission Checklist

### Manuscript Package
- [ ] Title page (title, all authors, affiliations, corresponding author details)
- [ ] Structured abstract (Purpose, Methods, Results, Conclusions — 250 words max)
- [ ] Main text (Introduction, Methods, Results, Discussion, Limitations, Conclusions)
- [ ] References (Vancouver style, numbered in order of appearance)
- [ ] Figure legends
- [ ] Tables with legends

### Critical Content Checks
- [ ] NO spacetime/countercurvature/holographic/AdS/CFT language anywhere
- [ ] NO AlphaFold protein analysis in main text (separate paper)
- [ ] NO allometric scaling across species (keep focused on human AIS)
- [ ] Framed as "hypothesis-generating computational model" NOT "settled theory"
- [ ] Honest Limitations section (computational only, no patient data, simplified model)
- [ ] Conservative language throughout ("suggests", "consistent with", "warrants testing")
- [ ] 8 specific falsifiable predictions listed
- [ ] Brace mechanism reinterpretation included
- [ ] Sex-specific timing matches published AIS epidemiology

### Figures (5 total)
- [ ] Fig 1: Kd–τ* stability map (heatmap with Hopf bifurcation boundary)
- [ ] Fig 2: Growth-phase trajectory through parameter space
- [ ] Fig 3: Sex-specific vulnerability windows (age vs stability margin)
- [ ] Fig 4: Brace mechanism reinterpretation
- [ ] Fig 5: Model overview schematic (block diagram)
- [ ] All figures 300 DPI, TIFF or EPS format
- [ ] Figure text legible at print size (8-10pt minimum)

### Cover Letter
- [ ] Address to Editor-in-Chief
- [ ] State manuscript is not under consideration elsewhere
- [ ] Explain why Spine Deformity is the right venue
- [ ] Highlight clinical relevance and testable predictions
- [ ] Ethics statement (computational only, no IRB required)
- [ ] No competing interests declaration

### Springer Nature Requirements
- [ ] Word count 3500-5000 (excluding references)
- [ ] Vancouver reference style
- [ ] Author ORCID (if available)
- [ ] Data availability statement pointing to GitHub repo
- [ ] Code availability statement pointing to GitHub repo
- [ ] Conflict of interest statement
- [ ] Funding statement (none received)

### Repository Cleanup
- [ ] README updated to reflect the derivative-gain focus (not spacetime theory)
- [ ] Simulation code documented and runnable
- [ ] All figure-generation scripts in scripts/
- [ ] License file present
- [ ] .gitignore excludes build artifacts

### After Submission
- [ ] Note manuscript ID from editorial system
- [ ] Set up reviewer response template
- [ ] Prepare supplementary material if requested (AlphaFold analysis as supplement)

---

## Key References to Cite

1. Peterka RJ (2002) "Sensorimotor integration in human postural control" J Neurophysiol 88:1097-1118
2. Cheng JC et al (2015) "Adolescent idiopathic scoliosis" Nat Rev Dis Primers 1:15030
3. Grivas TB et al (2006) "The incidence of idiopathic scoliosis in various geographic areas"
4. Negrini S et al (2018) "2016 SOSORT guidelines" Scoliosis Spinal Disord 13:3
5. Machida M (1999) "Cause of idiopathic scoliosis" Spine 24:2576-2583
6. Burwell RG et al (2009) "Pathogenesis of AIS in girls" Scoliosis 4:24
7. Latalski M et al (2017) "Current insights into the aetiology of AIS" Arch Orthop Trauma Surg 137:1327-1333

## Key Claims to Defend

| Claim | Evidence | Strength |
|---|---|---|
| Delayed PID model of postural control | Peterka 2002, established literature | Strong |
| Growth-velocity dependent Kd degradation | Novel hypothesis, computationally demonstrated | Moderate |
| Sex-specific timing matches AIS epidemiology | Published growth curves + model output | Strong |
| Brace augments derivative gain via haptic feedback | Novel reinterpretation, testable | Moderate |
| Hopf bifurcation creates instability window | Mathematical proof from DDE analysis | Strong |

## What NOT to Claim

- This is NOT the "settled etiology" of AIS — it's a hypothesis
- This does NOT replace genetic/molecular research — it provides a framework to interpret it
- This does NOT prove causation — it demonstrates consistency with known epidemiology
- The model is simplified and NOT validated against clinical cohort data yet
