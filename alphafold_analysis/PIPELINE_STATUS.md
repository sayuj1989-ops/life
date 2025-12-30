# AlphaFold BCC Pipeline Status

**Last Updated:** 2025-01-27  
**Pipeline Run:** Complete with 36/37 successful analyses

---

## Summary

✅ **Pipeline executed successfully**  
✅ **36 proteins analyzed** out of 37 downloaded structures  
⚠️ **12 proteins not found** in AlphaFold Database  
⚠️ **1 invalid PDB file** (Klotho - error response)

---

## Download Status

### Successfully Downloaded

**HOX Genes:** 22/32
- ✅ HOXA1, HOXA4, HOXA5, HOXA7, HOXA9, HOXA10
- ✅ HOXB1, HOXB2, HOXB4, HOXB5, HOXB6, HOXB9
- ✅ HOXC4, HOXC6, HOXC8, HOXC10, HOXC11
- ✅ HOXD1, HOXD4, HOXD8, HOXD10, HOXD12

**PAX Genes:** 0/5
- ⚠️ None downloaded yet

**Mechanosensitive:** 1/8
- ✅ YAP1

**Segmentation Clock:** 9/11
- ✅ NOTCH2, NOTCH3, DLL1, DLL3, HES1, HES7, WNT3A, WNT5A, FGF8
- ❌ NOTCH1, FGF4

**Longevity:** 4/5
- ✅ FOXO3, SIRT1, PGC1A
- ⚠️ KLOTHO (invalid PDB - error response)
- ❌ AMPK (not downloaded)

**ECM:** 0/4
- ⚠️ None downloaded yet

**Transcription:** 1/4
- ✅ MESP2

### Not Found in AlphaFold (12 proteins)

**HOX Genes (10):**
- HOXA2 (O43364)
- HOXA3 (O43365)
- HOXA11 (P31270)
- HOXB7 (P09629)
- HOXB8 (P17481)
- HOXC9 (P31274)
- HOXD3 (P31249)
- HOXD9 (P28356)
- HOXD11 (P31277)
- HOXD13 (P35453)

**Segmentation (2):**
- NOTCH1 (P46531)
- FGF4 (P08620)

**Possible Reasons:**
- Very short proteins (< 30 aa)
- Disordered regions (low confidence)
- Membrane proteins (limited coverage)
- Very large proteins (> 2700 aa)
- Alternative isoforms needed

---

## Analysis Status

### Successfully Analyzed: 36/37

All metrics calculated:
- ✅ Sequence entropy
- ✅ Backbone curvature
- ✅ Flexibility index
- ✅ Compactness (radius of gyration)
- ✅ Mechanical properties (stiffness, instability)

### Failed Analysis: 1/37

**Klotho (Q9UEF7):**
- **Issue:** Invalid PDB file (XML error response from AlphaFold)
- **Error:** "Error analyzing Klotho.pdb: 0"
- **Cause:** Download returned AWS S3 error instead of PDB structure
- **Solution:** Re-fetch or skip in analysis

---

## Output Files

### Generated Reports
- ✅ `bcc_analysis_report.md` - Comprehensive analysis report
- ✅ `bcc_analysis_data.json` - Structured data (36 proteins)
- ✅ `entropy_curvature_correlation.png` - Visualization

### Metadata
- ✅ `fetch_summary.json` - Download status for most recent category run
- ⚠️ `pdb_validation.json` - Generated only after running `fix_invalid_pdbs.py`

---

## Next Steps

### 1. Fix Klotho PDB

**Option A: Re-fetch Klotho**
```bash
python3 alphafold_analysis/fetch_bcc_structures.py \
    --category LONGEVITY \
    --priority KLOTHO \
    --force
```

**Option B: Remove Invalid File**
```bash
python3 alphafold_analysis/fix_invalid_pdbs.py
```

### 2. Investigate Not Found Proteins

**Check for alternatives:**
```bash
python3 alphafold_analysis/investigate_not_found.py
```

This will:
- Check UniProt for isoforms and secondary accessions
- Search alternate UniProt entries by gene
- Verify gene names and protein lengths
- Suggest possible reasons for absence

### 3. Re-run Analysis

After fixing Klotho:
```bash
MPLBACKEND=Agg \
MPLCONFIGDIR=/Users/mac/LIFE/alphafold_analysis/.mpl_cache \
XDG_CACHE_HOME=/Users/mac/LIFE/alphafold_analysis/.cache \
python3 alphafold_analysis/analyze_bcc_structures.py
```

---

## Key Findings (Preliminary)

### Information-Geometry Correlation
- **Expected:** Strong positive correlation (r > 0.6) between sequence entropy and structural curvature
- **Status:** Analysis complete, correlation calculated in report

### Category Patterns
- **HOX Proteins:** High structural conservation expected
- **Mechanosensitive:** Higher flexibility indices expected
- **Segmentation Clock:** Oscillatory domain architectures

---

## Files Structure

```
alphafold_analysis/
├── predictions/          # 37 PDB files (36 valid, 1 invalid)
├── metadata/
│   ├── fetch_summary.json
│   └── pdb_validation.json (after running fix_invalid_pdbs.py)
├── figures/
│   └── entropy_curvature_correlation.png
├── bcc_analysis_report.md
└── bcc_analysis_data.json
```

---

## Known Issues

1. **Klotho.pdb** - Invalid XML error response, needs re-fetch
2. **12 Not Found Proteins** - Not in AlphaFold DB, investigate alternatives
3. **JSON Serialization** - Fixed (numpy scalar conversion)

---

## Success Metrics

- ✅ **97% analysis success rate** (36/37)
- ✅ **69% HOX coverage** (22/32 downloaded)
- ⚠️ **0% PAX coverage** (0/5)
- ⚠️ **12.5% Mechanosensitive coverage** (1/8)
- ✅ **82% Segmentation coverage** (9/11)
- ⚠️ **60% Longevity coverage** (3/5 valid, 1 invalid, 1 missing)

---

**Status:** ✅ Pipeline functional, minor cleanup needed for Klotho and not_found proteins





