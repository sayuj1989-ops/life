# Bolt-BioFold ⚡ Analysis Report (BLOCKED)

**Status**: ⛔ BLOCKED

## 1. Issue Description
Unable to perform analysis cycle. The AlphaFold Database (AFDB) is unreachable from this environment.

- **Proteins Selected**: PIEZO2, LBX1, IFT88, PIEZO1, LMNA, FBN1, YAP1, POC5, ITGB1, METTL3.
- **Data Source Attempts**:
  - **API**: `https://alphafold.ebi.ac.uk/api/prediction/{UNIPROT}` returned 404/Empty for all targets.
  - **File Download (v4/v3)**: `https://alphafold.ebi.ac.uk/files/AF-{UNIPROT}-F1-model_v4.pdb` returned 404 or Timeout.
  - **RCSB Mirror**: `https://files.rcsb.org/download/AF_AF{UNIPROT}F1.pdb` returned 404.
- **Local Data**: Verified `research/alphafold_countercurvature/data/raw/afdb/` is empty (files listed in manifest are missing from disk).

## 2. Missing Artifacts
- PDB structure files for all 10 candidates.
- PAE JSON files.

## 3. Smallest Fix
- **Network Check**: Verify if `alphafold.ebi.ac.uk` is blocked or rate-limited.
- **API Update**: If the AFDB API has permanently changed (post-v4), `src/afcc/afdb.py` needs to be updated with the new endpoint schema.
- **Manual Ingestion**: Manually download the PDB files for the target list and place them in `research/alphafold_countercurvature/data/raw/afdb/{UNIPROT}/{UNIPROT}.pdb`.

## 4. Best Next Move
**Check network connectivity to EBI or manually provision PDB files.**
