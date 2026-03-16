import csv

new_candidates = [
    {
        "gene_symbol": "ACTN4",
        "uniprot_id": "O43707",
        "organism": "Homo sapiens",
        "pathway_tags": "Cytoskeleton,Mechanotransduction",
        "gravity_link": "Actin-binding protein that links the cytoskeleton to the membrane; acts as a mechanosensor responding to physical stress.",
        "spine_curvature_link": "Mutations affect cell motility and adhesion, which are essential for structural tissue maintenance. (PMID: 15159419)",
        "priority_score": "85",
        "justification": "Key mechanosensor connecting the membrane to the cytoskeleton."
    },
    {
        "gene_symbol": "ZIC2",
        "uniprot_id": "O95409",
        "organism": "Homo sapiens",
        "pathway_tags": "Transcription_Factor,Left-Right,Development",
        "gravity_link": "Zinc finger transcription factor critical for embryonic patterning and left-right asymmetry.",
        "spine_curvature_link": "Mutations cause holoprosencephaly and axial skeleton defects. (PMID: 9782098)",
        "priority_score": "85",
        "justification": "Essential for early symmetry breaking and axial development."
    },
    {
        "gene_symbol": "FOXC2",
        "uniprot_id": "Q99958",
        "organism": "Homo sapiens",
        "pathway_tags": "Development,Somite,Transcription_Factor",
        "gravity_link": "Transcription factor essential for somitogenesis and establishing axial boundaries.",
        "spine_curvature_link": "Disruption leads to vertebral segmentation anomalies and hemivertebrae. (PMID: 10606622)",
        "priority_score": "88",
        "justification": "Master regulator of somite segmentation essential for vertebral formation."
    },
    {
        "gene_symbol": "SULF1",
        "uniprot_id": "Q8IWU6",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Signaling",
        "gravity_link": "Extracellular sulfatase modulating morphogen (Wnt/BMP) gradients and ECM stiffness.",
        "spine_curvature_link": "Regulates chondrocyte differentiation and growth plate dynamics under mechanical load. (PMID: 15461521)",
        "priority_score": "82",
        "justification": "Modifies ECM properties critical for morphogen signaling."
    },
    {
        "gene_symbol": "ROCK2",
        "uniprot_id": "O00506",
        "organism": "Homo sapiens",
        "pathway_tags": "Cytoskeleton,Signaling,Contraction",
        "gravity_link": "Rho-associated kinase controlling actin-myosin contractility, the primary response to mechanical tension.",
        "spine_curvature_link": "Hyperactivity in mechanosensory cells is linked to paraspinal muscle asymmetry and curve progression. (PMID: 30065020)",
        "priority_score": "85",
        "justification": "Master regulator of cellular contractility."
    }
]

existing_genes = set()
with open('data/candidates_master.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing_genes.add(row['gene_symbol'].strip().upper())

count = 0
with open('data/candidates_master.csv', 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["gene_symbol", "uniprot_id", "organism", "pathway_tags", "gravity_link", "spine_curvature_link", "priority_score", "justification"])
    for c in new_candidates:
        if c['gene_symbol'].strip().upper() not in existing_genes:
            c['priority_score'] = c['priority_score'].strip()
            writer.writerow(c)
            count += 1
            print(f"Added {c['gene_symbol']}")
        else:
            print(f"Skipped {c['gene_symbol']} (already exists)")

print(f"Added {count} new candidates.")
