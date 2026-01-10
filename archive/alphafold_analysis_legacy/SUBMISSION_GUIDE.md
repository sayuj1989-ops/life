# AlphaFold Server Submission Guide

## Priority Proteins for Biological Counter-Curvature Study

### Tier 1: Core Developmental Proteins (Submit First)
These directly relate to spinal geometry and information-driven morphogenesis:

1. **PAX3** (P23760.json) - Critical for neural tube closure and spinal development
2. **PAX6** (P26367.json) - Master regulator of eye/neural development, geometric patterning
3. **HOXA1** (P49639.json) - Anterior-posterior axis specification
4. **HOXD1** (Q9GZZ0.json) - Vertebral column patterning

### Tier 2: Ciliary Proteins (Mechanical-Geometric Link)
Ciliary proteins demonstrate information→geometry coupling in mechanical systems:

5. **IFT88** (Q13099.json) - Intraflagellar transport, cilia assembly
6. **KIF3A** (Q9Y496.json) - Motor protein, directional transport
7. **RPGR** (Q92834.json) - Ciliary function regulator

### Tier 3: Additional Developmental Regulators

8. **PAX1** (P15863.json) - Vertebral column development
9. **PAX9** (P55771.json) - Skeletal patterning
10. **HOXB1** (P14653.json) - Hindbrain segmentation

## Recommended Submission Strategy

### Option A: Full Batch (All 10)
Upload all JSON files for comprehensive analysis. AlphaFold Server allows multiple submissions.

### Option B: Priority Subset (Top 4)
Start with PAX3, PAX6, HOXA1, HOXD1 for fastest results on key proteins.

## How to Upload

1. In AlphaFold Server, click "New Job" or "Upload JSON"
2. Navigate to: `/Users/mac/LIFE/alphafold_analysis/jobs/`
3. Select JSON files (can select multiple with Cmd+Click)
4. Submit and wait for predictions (~minutes to hours depending on queue)

## Why These Proteins?

- **PAX/HOX genes**: Encode transcription factors that translate genetic information into spatial body patterns
- **Ciliary proteins**: Demonstrate how molecular information creates mechanical geometry
- **Connection to manuscript**: These proteins exemplify how sequence information (entropy, motifs) manifests as 3D geometric structures that drive biological curvature

## After Predictions Complete

Download PDB files to `alphafold_analysis/predictions/` and run:
```bash
./.venv/bin/python3 alphafold_analysis/analyze_structures.py
```
