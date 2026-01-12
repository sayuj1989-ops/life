# AlphaFold Protein Analysis Workflow

Analysis of ciliary proteins, HOX1, and PAX genes to study information-geometry relationships.

## Quick Start

### 1. Retrieve Sequences (✅ Complete)
```bash
./.venv/bin/python3 alphafold_analysis/protein_sequences.py
```
**Status**: Retrieved 10 protein sequences saved to `sequences.fasta`

### 2. Generate Job Files (✅ Complete)
```bash
./.venv/bin/python3 alphafold_analysis/generate_af_jobs.py
```
**Status**: 10 JSON job files created in `jobs/` directory

### 3. Submit to AlphaFold Server (⏳ Manual Step)
1. Visit https://alphafoldserver.com
2. Upload JSON files from `alphafold_analysis/jobs/`
3. Download predictions (PDB files) to `alphafold_analysis/predictions/`

### 4. Analyze Structures (⏳ After predictions)
```bash
./.venv/bin/python3 alphafold_analysis/analyze_structures.py
```
**Output**: 
- `analysis_report.md` - Detailed analysis with information-geometry correlations
- `figures/entropy_curvature_correlation.png` - Visualization

## Proteins Analyzed

### Ciliary Proteins (3)
- **IFT88** (Q13099): Intraflagellar transport protein 88
- **KIF3A** (Q9Y496): Kinesin-like protein KIF3A
- **RPGR** (Q92834): Retinitis pigmentosa GTPase regulator

### HOX1 Genes (3)
- **HOXA1** (P49639): Homeobox protein Hox-A1
- **HOXB1** (P14653): Homeobox protein Hox-B1
- **HOXD1** (Q9GZZ0): Homeobox protein Hox-D1

### PAX Genes (4)
- **PAX1** (P15863): Paired box protein Pax-1
- **PAX3** (P23760): Paired box protein Pax-3
- **PAX6** (P26367): Paired box protein Pax-6
- **PAX9** (P55771): Paired box protein Pax-9

## Analysis Metrics

- **Sequence Entropy**: Shannon entropy of amino acid distribution (information content)
- **Backbone Curvature**: Local curvature of protein backbone (geometric property)
- **Correlation**: Statistical relationship between information and geometry
- **Instability Index**: Protein stability metric
- **GRAVY**: Hydrophobicity index

## Research Questions

1. How does sequence information (entropy) correlate with structural curvature?
2. Do HOX and PAX proteins show distinct geometric signatures?
3. How does ciliary protein geometry relate to mechanical function?

## Integration with Manuscript

Findings will be integrated into:
- **Theory Section**: Protein structure as example of information-geometry coupling
- **Methods Section**: AlphaFold analysis pipeline description
- **Results Section**: Correlation data and structural analysis
- **Discussion**: Connection to biological counter-curvature framework
