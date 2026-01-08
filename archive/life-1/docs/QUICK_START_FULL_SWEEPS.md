# Quick Start: Run Full Sweeps & Extract Numbers

## One-Command Solution

```bash
bash RUN_FULL_SWEEPS.sh
```

This script runs all full-resolution experiments and extracts anchor numbers automatically.

**Expected runtime:** 40-70 minutes

---

## What Gets Generated

### CSV Files (Source of Truth)
- `outputs/experiments/spine_modes/spine_modes_results.csv` - Curvature profiles, I(s), dIds
- `outputs/experiments/spine_modes/spine_modes_summary.csv` - D_geo_norm, metrics per χ_κ
- `outputs/experiments/microgravity/microgravity_summary.csv` - D_geo_norm vs g
- `outputs/experiments/phase_diagram/phase_diagram_data.csv` - Full (χ_κ, g) grid with S_lat, Cobb

### Figures
- `outputs/figs/fig_countercurvature_metrics.png` - 4-panel main figure
- `outputs/experiments/phase_diagram/phase_diagram.png` - Phase diagram with scoliosis regime

### Extracted Numbers
The `extract_anchor_numbers.py` script prints formatted sentences ready to paste into your manuscript.

---

## Manual Extraction (If Script Fails)

See `docs/full_sweeps_extraction_guide.md` for detailed Python snippets to extract:
- Microgravity persistence numbers
- Phase diagram regime anchor points  
- Spine S-curve sine-mode characteristics

---

## Next Steps After Extraction

1. **Copy extracted sentences** into `manuscript/main_countercurvature.tex` (replace TODOs)
2. **Update cover letter** key claims with real numbers
3. **Final manuscript polish** - Replace all placeholders

---

## Status

✅ **Scripts ready**: `RUN_FULL_SWEEPS.sh` and `scripts/extract_anchor_numbers.py`  
⏳ **Waiting for full sweeps** - Run to get actual numbers

