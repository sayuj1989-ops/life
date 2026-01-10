# Ralph Loop: Complete Biological Countercurvature Research

## Current State

The research has the following completed components:
- ✅ Theory complete (IEC framework, Cosserat mechanics)
- ✅ Manuscript draft complete (MANUSCRIPT_COMPLETE.md)
- ✅ Simulation data generated (sweep_grid.csv, etc.)
- ✅ Figures generated (5 main figures)
- ✅ Publication-ready longevity repo created (life-paper/)

## Remaining Tasks

Complete the following in order. Check off each task by verifying the output exists and is correct.

### Phase 1: Expand AlphaFold Dataset (Priority: HIGH)

1. **Find missing longevity protein KLOTHO**
   - Search AlphaFold with UniProt ID Q9UEF7 (human Klotho)
   - If not found, try alternative IDs or ColabFold
   - Add to `life-paper/data/processed/bcc_analysis_data.json`

2. **Expand longevity dataset to n ≥ 6**
   - Add: TERT (telomerase), IGF1R, APOE, CETP
   - Use UniProt IDs for robust matching
   - Re-run longevity analysis

3. **Update correlations with expanded dataset**
   - Run: `cd life-paper && make reproduce`
   - Verify r, p-values in results/longevity/longevity_metrics.json

### Phase 2: Category-Stratified Analysis

4. **Implement category comparison**
   - Compare longevity vs HOX vs mechanosensitive categories
   - Report category-specific r values
   - Test if longevity is significantly different (ANOVA or permutation)

5. **Generate category comparison figure**
   - Bar plot of r by category with 95% CI
   - Save to results/longevity/fig_category_corr.pdf

### Phase 3: Integrate with Main Manuscript

6. **Update countercurvature manuscript**
   - Add longevity results to MANUSCRIPT_COMPLETE.md
   - Update AlphaFold section with expanded dataset
   - Add category comparison results

7. **Cross-reference figures**
   - Copy final figures from life-paper to countercurvature/assets/
   - Verify all figure references in manuscript

### Phase 4: Comparative Genomics (if time permits)

8. **HOX expression boundaries**
   - Collect cross-species HOX boundary data
   - Correlate with curvature patterns
   - Add validation section to manuscript

### Phase 5: Final Polish

9. **Complete references**
   - Verify all citations in references.bib
   - Add any missing recent papers (post-2022)
   - Target 35+ references

10. **Run full reproducibility check**
    - `cd countercurvature && make all`
    - Verify all figures regenerate
    - Verify all CSVs regenerate

## Completion Criteria

Output `<promise>RESEARCH_COMPLETE</promise>` when:
- [ ] Longevity dataset has n ≥ 5 proteins
- [ ] Longevity correlation reported with Fisher CI
- [ ] Category comparison implemented
- [ ] Manuscript updated with new results
- [ ] All figures regenerate from `make all`
- [ ] 35+ references in bibliography

## Files to Modify

- `life-paper/data/processed/bcc_analysis_data.json` (expand dataset)
- `life-paper/analysis/longevity/longevity_deep_dive.py` (category comparison)
- `countercurvature/MANUSCRIPT_COMPLETE.md` (integrate results)
- `countercurvature/references.bib` (add citations)

## How to Run This Loop

```bash
/ralph-loop "Complete the research tasks in RALPH_RESEARCH_PROMPT.md. Read the file, check current state, complete next unchecked task, verify output, update progress. Output <promise>RESEARCH_COMPLETE</promise> when all criteria met." --completion-promise "RESEARCH_COMPLETE" --max-iterations 30
```

