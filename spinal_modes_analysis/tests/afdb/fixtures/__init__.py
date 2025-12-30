"""Test fixtures and shared data for AFDB tests."""

# Mock API response for COL2A1 (current schema as of 2025)
MOCK_API_RESPONSE_COL2A1 = {
    "uniprotAccession": "P02458",
    "gene": "COL2A1",
    "organismScientificName": "Homo sapiens",
    "latestVersion": "4",
    "pdbUrl": "https://alphafold.ebi.ac.uk/files/AF-P02458-F1-model_v4.pdb",
    "cifUrl": "https://alphafold.ebi.ac.uk/files/AF-P02458-F1-model_v4.cif",
    "bcifUrl": "https://alphafold.ebi.ac.uk/files/AF-P02458-F1-model_v4.bcif",
    "paeImageUrl": "https://alphafold.ebi.ac.uk/files/AF-P02458-F1-predicted_aligned_error_v4.png",
    "paeDocUrl": "https://alphafold.ebi.ac.uk/files/AF-P02458-F1-predicted_aligned_error_v4.json",
}

# Mock API response for PIEZO1 (mechanosensor)
MOCK_API_RESPONSE_PIEZO1 = {
    "uniprotAccession": "Q92508",
    "gene": "PIEZO1",
    "organismScientificName": "Homo sapiens",
    "latestVersion": "4",
    "pdbUrl": "https://alphafold.ebi.ac.uk/files/AF-Q92508-F1-model_v4.pdb",
    "cifUrl": "https://alphafold.ebi.ac.uk/files/AF-Q92508-F1-model_v4.cif",
}
