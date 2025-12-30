# Final Manuscript Update Guide

## Quick Reference: Where to Paste Numbers

After running `bash RUN_FULL_SWEEPS.sh`, you'll get formatted sentences from `extract_anchor_numbers.py`. Here's exactly where to paste them in `manuscript/main_countercurvature.tex`:

---

## Results Section 3.1: "Gravity-selected vs information-selected curvature modes"

**Location:** Around line 280-283

**Current TODO:**
```latex
% TODO: After running extract_anchor_numbers.py, add specific values:
% - "D̂_geo ≈ 0.3" (from spine modes summary)
% - "max-to-RMS ratio ≈ 1.X" (from spine sine-mode analysis)
% - Sign change count (should be 1)
```

**What to add:**
- Paste the "SPINE S-CURVE: Sine-Like Mode Analysis" sentence from `extract_anchor_numbers.py`
- Add specific D̂_geo value
- Add max/RMS ratio
- Confirm sign change count = 1

**Example replacement:**
```latex
The stabilized sagittal S-curve is dominated by a single smooth sign-changing mode: 
κ_I(s) exhibits only one sign change along the axis and a max-to-RMS ratio of ≈1.23, 
consistent with a sine-like counter-curvature profile against gravity (D̂_geo ≈ 0.28).
```

---

## Results Section 3.2: "Persistence of information-driven shape in microgravity"

**Location:** Around line 299-302

**Current TODO:**
```latex
% TODO: After running extract_anchor_numbers.py, add specific values:
% - "As g decreases from 1.0 to 0.01, passive curvature energy falls by X%, while D̂_geo changes by only Y%"
% - "At g = 0.01, passive energy is reduced by X% compared to 1g, yet D̂_geo remains at Y"
% - Reference to Fig.~\ref{fig:countercurvature_main}, Panel D
```

**What to add:**
- Paste the "MICROGRAVITY SERIES" sentence from `extract_anchor_numbers.py`
- Add energy collapse percentage
- Add D_geo persistence ratio

**Example replacement:**
```latex
As g decreases from 1.0 to 0.01, passive curvature energy falls by 95%, 
while D̂_geo changes by only 8%, indicating that the information-selected 
'spinal wave' is largely preserved in microgravity (see Fig.~\ref{fig:countercurvature_main}, Panel D).
```

---

## Results Section 3.3: "Phase diagram of countercurvature regimes"

**Location:** Around line 308-312

**Current TODO:**
```latex
% TODO: After running extract_anchor_numbers.py, add three anchor points:
% - Gravity-dominated: "e.g., χ_κ = X.XXX, g = X.XX, D̂_geo ≈ 0.0X, S_lat < 0.01, Cobb < 3°"
% - Cooperative: "e.g., χ_κ = X.XXX, g = X.XX, D̂_geo ≈ 0.XX"
% - Information-dominated/scoliotic: "e.g., χ_κ = X.XXX, g = X.XX, D̂_geo > 0.3, S_lat ≳ 0.05, Cobb > 10°"
% - Reference to Fig.~\ref{fig:phase_diagram}
```

**What to add:**
- Paste the "PHASE DIAGRAM: Three Regimes" paragraph from `extract_anchor_numbers.py`
- Add three specific anchor points with (χ_κ, g) values

**Example replacement:**
```latex
In the gravity-dominated regime (e.g., χ_κ = 0.02, g = 9.81), we find D̂_geo ≈ 0.05, 
S_lat < 0.01, and Cobb-like angles < 3°. In the cooperative regime (χ_κ = 0.05, 
g = 4.9), D̂_geo ≈ 0.18. In contrast, in the information-dominated corner 
(χ_κ = 0.08, g = 2.45), D̂_geo > 0.3, S_lat ≳ 0.05, and Cobb-like angles exceed 10°, 
indicating a scoliosis-like symmetry-broken branch (see Fig.~\ref{fig:phase_diagram}).
```

---

## Quick Workflow

1. **Run full sweeps:**
   ```bash
   bash RUN_FULL_SWEEPS.sh
   ```

2. **Save output:**
   - Copy the terminal output from `extract_anchor_numbers.py`
   - Paste into `docs/anchor_numbers.log`

3. **Update manuscript:**
   - Open `manuscript/main_countercurvature.tex`
   - Find each TODO (use search for "TODO: After running")
   - Replace with corresponding sentence from the log
   - Remove the TODO comment

4. **Verify:**
   - No remaining TODOs in Results section
   - All numbers are consistent with extracted values
   - LaTeX compiles without errors

---

## Helper Script

You can also run:
```bash
python3 scripts/update_manuscript_with_numbers.py
```

This will show you exactly where each TODO is located in the manuscript.

---

## Status

✅ **Guide ready**  
⏳ **Waiting for full sweeps** - Run `bash RUN_FULL_SWEEPS.sh` first

