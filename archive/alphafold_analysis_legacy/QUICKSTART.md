# AlphaFold BCC Research - Quick Start Guide

This guide will help you fetch and analyze protein structures relevant to Biological Countercurvature research using AlphaFold.

## Prerequisites

```bash
# Ensure you have required packages
pip install biopython numpy scipy matplotlib requests
```

## Step 1: Review Protein Database

The comprehensive protein database includes:
- **HOX genes** (30+ proteins): Developmental patterning
- **PAX genes** (5 proteins): Segmentation and vertebral identity
- **Mechanosensitive proteins** (8 proteins): YAP/TAZ, Piezo, Integrins
- **Segmentation clock** (12 proteins): Notch, Wnt, FGF signaling
- **Longevity proteins** (5 proteins): FOXO3, SIRT1, Klotho, etc.

View the database:
```bash
python alphafold_analysis/bcc_protein_database.py
```

## Step 2: Fetch Protein Structures

### Option 0: Refresh Corrected Proteins (If you've updated UniProt IDs)

If you've just corrected UniProt IDs in the database:

```bash
# Re-fetch structures for corrected proteins only
python3 alphafold_analysis/refresh_corrected_proteins.py
```

This will refresh the 12 proteins with corrected UniProt IDs.

### Option A: Fetch All Proteins (Recommended for Full Analysis)

```bash
# Fetch all proteins (this will take time - ~60+ proteins)
python alphafold_analysis/fetch_bcc_structures.py --category all

# Or fetch by category
python alphafold_analysis/fetch_bcc_structures.py --category HOX
python alphafold_analysis/fetch_bcc_structures.py --category MECHANOSENSITIVE
```

### Option B: Fetch Priority Proteins First

Start with the most critical proteins for BCC research:

```bash
# Priority: HOX genes (cervical/lumbar identity)
python alphafold_analysis/fetch_bcc_structures.py \
    --category HOX \
    --priority HOXA1 HOXA9 HOXA10 HOXB1 HOXB8 HOXC8 HOXC9 HOXD8 HOXD9 HOXD10

# Priority: Mechanosensitive proteins
python alphafold_analysis/fetch_bcc_structures.py \
    --category MECHANOSENSITIVE \
    --priority YAP1 TAZ PIEZO1 PIEZO2

# Priority: Segmentation clock
python alphafold_analysis/fetch_bcc_structures.py \
    --category SEGMENTATION \
    --priority NOTCH1 DLL1 HES7 WNT3A FGF8
```

### Option C: Test with Limited Set

```bash
# Fetch just 5 proteins to test
python alphafold_analysis/fetch_bcc_structures.py --category HOX --limit 5
```

**Output:** Structures will be saved to `alphafold_analysis/predictions/`

## Step 3: Analyze Structures

Once you have PDB files, run comprehensive analysis:

```bash
python alphafold_analysis/analyze_bcc_structures.py
```

This will:
- Calculate sequence entropy (information content)
- Measure backbone curvature (geometric properties)
- Estimate flexibility and mechanical properties
- Generate correlation plots
- Create comprehensive report

**Output:**
- `alphafold_analysis/bcc_analysis_report.md` - Detailed analysis report
- `alphafold_analysis/bcc_analysis_data.json` - Structured data
- `alphafold_analysis/figures/entropy_curvature_correlation.png` - Visualization

## Step 4: Review Evidence Document

Read the comprehensive evidence document:

```bash
cat alphafold_analysis/BCC_ALPHAFOLD_EVIDENCE.md
```

This document connects protein structures to the BCC framework and provides:
- Detailed analysis of each protein category
- Structural properties and BCC relevance
- Integration with theoretical framework
- Experimental predictions

## Workflow Example

```bash
# 1. Check what proteins are available
python alphafold_analysis/bcc_protein_database.py

# 2. Fetch priority proteins (HOX + Mechanosensitive)
python alphafold_analysis/fetch_bcc_structures.py \
    --category HOX \
    --priority HOXA1 HOXA9 HOXA10 HOXB8 HOXC8 HOXD9 HOXD10

python alphafold_analysis/fetch_bcc_structures.py \
    --category MECHANOSENSITIVE \
    --priority YAP1 TAZ PIEZO1

# 3. Analyze structures
python alphafold_analysis/analyze_bcc_structures.py

# 4. Review results
cat alphafold_analysis/bcc_analysis_report.md
open alphafold_analysis/figures/entropy_curvature_correlation.png
```

## Troubleshooting

### No PDB files found
- Run `fetch_bcc_structures.py` first to download structures
- Check that files are in `alphafold_analysis/predictions/`

### API errors
- AlphaFold API may be rate-limited; add delays between requests
- Some proteins may not be in AlphaFold DB (check UniProt IDs)

### Analysis errors
- Ensure PDB files are valid (not corrupted downloads)
- Check that BioPython is installed correctly

## Next Steps

1. **Expand Analysis:** Add more proteins from the database
2. **Custom Analysis:** Modify `analyze_bcc_structures.py` for specific metrics
3. **Integration:** Connect findings to manuscript sections
4. **Visualization:** Create additional plots for specific protein categories

## File Structure

```
alphafold_analysis/
├── bcc_protein_database.py      # Protein database
├── fetch_bcc_structures.py      # Structure fetcher
├── analyze_bcc_structures.py    # Comprehensive analysis
├── BCC_ALPHAFOLD_EVIDENCE.md    # Evidence document
├── QUICKSTART.md                 # This file
├── predictions/                  # PDB files (downloaded)
├── metadata/                     # API metadata
├── figures/                      # Generated plots
└── bcc_analysis_report.md        # Analysis results
```

## Integration with Manuscript

The AlphaFold evidence supports:
- **Theory Section:** Information-geometry coupling at molecular level
- **Methods Section:** Structural analysis pipeline
- **Results Section:** Correlation between information and geometry
- **Discussion:** Molecular basis for BCC framework

See `BCC_ALPHAFOLD_EVIDENCE.md` for detailed integration points.

---

**Questions?** Check the main README or the evidence document for more details.

