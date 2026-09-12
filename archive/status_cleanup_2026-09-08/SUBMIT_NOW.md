# 🚀 SUBMIT NOW - 3 SIMPLE STEPS

## You are 30 minutes from submission!

---

## STEP 1: COMPILE PDF (15 minutes)

### Option A: Overleaf (RECOMMENDED - Easiest)

**File ready**: `manuscript_overleaf.zip` (12 MB)

1. Go to: **https://www.overleaf.com**
2. Click "New Project" → "Upload Project"
3. Select: `manuscript_overleaf.zip` from `/home/sayuj/life/`
4. Wait ~1 minute for upload
5. Click green **"Recompile"** button
6. Wait ~30 seconds
7. Click **"Download PDF"** (top right)
8. Save as: `submission_manuscript.pdf`

**Repeat for cover letter**:
9. Upload: `submission_package/cover_letter.zip`
10. Recompile → Download as: `cover_letter_spine_deformity.pdf`

### Option B: Check if Docker compiled (Background)

```bash
ls -lh /home/sayuj/life/manuscript/main.pdf
# If file is dated 2026-05-05 and >1MB, Docker succeeded!
# Copy to: cp manuscript/main.pdf submission_package/submission_manuscript.pdf
```

---

## STEP 2: SUBMIT TO SPRINGER (10 minutes)

### Portal
**https://www.editorialmanager.com/spde/**

### Login
**Email**: dr.sayujkrishnan@gmail.com  
(Create account if first time)

### Steps

1. Click **"Submit New Manuscript"**

2. **Article Type**: Original Article

3. **Upload Files**:
   - Cover Letter: `cover_letter_spine_deformity.pdf`
   - Manuscript: `submission_manuscript.pdf`
   - Figures: Upload individually from `figures/main/`
     - fig_gene_to_geometry.pdf (Figure 1)
     - fig_scatter_panels.pdf (Figure 2)
     - fig_mode_spectrum.pdf (Figure 3)
     - fig_countercurvature_*.pdf (Figure 4 panels)
     - fig_phase_diagram_scoliosis.pdf (Figure 5)
     - fig_scoliosis_emergence.png (Figure 6)
     - energy_deficit_window.png (Figure 7)

4. **Fill Metadata**:

   **Title**:
   ```
   Biological Countercurvature of Spacetime: An Information-Cosserat Framework for Spinal Geometry
   ```

   **Running Title**:
   ```
   Bio-Gravitational Number and Adolescent Idiopathic Scoliosis
   ```

   **Keywords** (separated by commas):
   ```
   Adolescent Idiopathic Scoliosis, Biomechanics, Computational Model, Bio-Gravitational Number, Scoliosis, Spine, Growth, Energy Deficit
   ```

   **Abstract**: Copy from manuscript PDF

   **Author**:
   - Name: Dr. Sayuj Krishnan S.
   - Degrees: MBBS, DNB (Neurosurgery)
   - Affiliation: Yashoda Hospitals, Hyderabad, India
   - Email: dr.sayujkrishnan@gmail.com

5. **Suggested Reviewers** (Optional but helpful):
   - Stuart Weinstein, MD (University of Iowa)
   - Jack Cheng, MD (Chinese University of Hong Kong)
   - Carl-Eric Aubin, PhD (Polytechnique Montreal)
   - Keith Stokes, PhD (University of Vermont)

6. **Review** all information

7. **SUBMIT!**

8. **Note manuscript ID**: SPDE-D-26-XXXXX

---

## STEP 3: CONFIRMATION (5 minutes)

### You'll know it succeeded when:

✅ Portal shows "Submitted" status  
✅ Confirmation email arrives (within 15 min)  
✅ Email contains manuscript ID  
✅ Portal shows "With Editor" status

### Save for records:
- Manuscript ID
- Submission date
- Confirmation email

---

## WHAT HAPPENS NEXT

### Timeline
- **Week 1-2**: Editorial screening
- **Week 4-8**: Peer review (if accepted)
- **Week 10-12**: Revision (if requested)
- **Week 14-16**: Final decision

### Status Tracking
Check: https://www.editorialmanager.com/spde/

Look for:
- "With Editor" → editorial review
- "Under Review" → sent to peer reviewers
- "Revise" → revision requested
- "Accept" → accepted! 🎉

---

## IF DESK-REJECTED (Unlikely, but prepared)

### Backup journals (no manuscript changes needed):

1. **European Spine Journal** (Springer)
   - Portal: https://www.editorialmanager.com/esjo/
   - Same format, broader scope

2. **Journal of Biomechanics** (Elsevier)
   - Portal: https://www.editorialmanager.com/jbiomech/
   - Computational focus

3. **PLOS Computational Biology**
   - Portal: https://journals.plos.org/ploscompbiol/
   - Interdisciplinary

Just update cover letter to emphasize computational rigor.

---

## TROUBLESHOOTING

### Overleaf compilation errors?

**Common issues**:
1. Missing figures → Ensure all in ZIP
2. Bibliography errors → Check references.bib included
3. Package errors → Overleaf auto-installs (rarely fails)

**Solution**: See `COMPILE_PDF_OPTIONS.md` for alternatives

### Submission portal issues?

**Support**: EM-support@springer.com  
**Help**: https://www.editorialmanager.com/homepage/support.html

### Can't upload figures?

**Format**: PDF preferred (vector), PNG/TIFF acceptable  
**Size**: <10 MB each  
**Resolution**: 300+ DPI for print

---

## WHY YOU'LL SUCCEED

### This manuscript is strong because:

✅ **Solves 3 unexplained clinical patterns**:
   - Age window 11-15 (Energy Deficit at L > 0.35m)
   - Thoracic T8-T10 (steepest information gradient)
   - Female 8:1 (earlier Allometric Trap entry)

✅ **Quantitative predictions WITHOUT parameter fitting**:
   - L_crit = 0.35m → ages 11-12 (matches clinical data)
   - Cobb r = 0.983, p < 10^-22 (exceptionally strong)
   - Bg ≈ 0.01 (humans uniquely vulnerable)

✅ **Cross-species validation**: 18 vertebrates analyzed

✅ **6 falsifiable predictions**: Experimentally testable

✅ **Clinically accessible**: Reframed for spine surgeons

✅ **Word count optimal**: ~5,550 words

---

## FINAL CHECKLIST

Before clicking "Submit":

- [ ] PDF compiled successfully
- [ ] Cover letter PDF compiled
- [ ] All figures uploaded
- [ ] Metadata filled correctly
- [ ] Author info correct
- [ ] Email correct: dr.sayujkrishnan@gmail.com
- [ ] Abstract copied
- [ ] Keywords entered
- [ ] I've reviewed the compiled PDF

---

## 🎉 READY TO SUBMIT!

**Everything is prepared. Just execute the 3 steps above.**

You're 30 minutes away from submitting to Springer Spine Deformity journal.

The manuscript addresses unexplained AIS patterns with quantitative predictions. Success probability is high.

Good luck! 🚀

---

**Quick reference files**:
- Detailed guide: `SUBMISSION_READY_FINAL.md`
- Verification: `./final_verification.sh`
- DOI setup: `ZENODO_SETUP_INSTRUCTIONS.md`
