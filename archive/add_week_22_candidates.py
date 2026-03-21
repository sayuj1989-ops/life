import csv
import os
import sys

MASTER_FILE = "data/candidates_master.csv"

new_candidates = [
    {
        "gene_symbol": "VIM",
        "uniprot_id": "P08670",
        "organism": "Homo sapiens",
        "pathway_tags": "Cytoskeleton,Mechanotransduction,Structure",
        "gravity_link": "Vimentin intermediate filaments act as intracellular shock absorbers and strain gauges, stiffening under mechanical tension.",
        "spine_curvature_link": "Regulates cellular mechanotransduction during migration; its organization is altered under unloading conditions (microgravity). (PMID: 21915600)",
        "priority_score": 88,
        "justification": "Primary component of the intermediate filament network, central to cellular mechanoresistance."
    },
    {
        "gene_symbol": "DES",
        "uniprot_id": "P17661",
        "organism": "Homo sapiens",
        "pathway_tags": "Cytoskeleton,Muscle,Structure",
        "gravity_link": "Desmin intermediate filaments link the Z-disc to the sarcolemma in muscle, transmitting force and maintaining alignment under load.",
        "spine_curvature_link": "Mutations cause desminopathies, characterized by muscle weakness, myofibrillar disorganization, and frequent scoliosis. (PMID: 9536087)",
        "priority_score": 90,
        "justification": "Essential structural filament integrating the contractile apparatus of postural muscles."
    },
    {
        "gene_symbol": "PLEC",
        "uniprot_id": "Q15149",
        "organism": "Homo sapiens",
        "pathway_tags": "Cytoskeleton,Mechanotransduction,Structure",
        "gravity_link": "Plectin is a giant cytolinker that crosslinks intermediate filaments, microtubules, and actin, distributing mechanical stress across the cell.",
        "spine_curvature_link": "Mutations cause Epidermolysis bullosa with muscular dystrophy, presenting with severe structural and muscular instability. (PMID: 8896562)",
        "priority_score": 92,
        "justification": "The master crosslinker of the cytoskeleton, unifying cellular structural response to force."
    },
    {
        "gene_symbol": "DSC2",
        "uniprot_id": "Q02487",
        "organism": "Homo sapiens",
        "pathway_tags": "Adhesion,Mechanotransduction,Structure",
        "gravity_link": "Desmocollin-2 is a core desmosomal cadherin; desmosomes anchor intermediate filaments to resist mechanical shear between cells.",
        "spine_curvature_link": "Crucial for maintaining tissue integrity under high mechanical stress, notably in cardiac and potentially paraspinal tissues. (PMID: 16912043)",
        "priority_score": 83,
        "justification": "Primary intercellular adhesion molecule resisting mechanical shear force via intermediate filaments."
    },
    {
        "gene_symbol": "DSG2",
        "uniprot_id": "Q14126",
        "organism": "Homo sapiens",
        "pathway_tags": "Adhesion,Mechanotransduction,Structure",
        "gravity_link": "Desmoglein-2 partners with desmocollin in desmosomes, forming the intercellular adhesive bonds that distribute mechanical strain.",
        "spine_curvature_link": "Essential for robust tissue cohesion; mutations compromise the ability of tissues to endure cyclic mechanical loading. (PMID: 16505173)",
        "priority_score": 83,
        "justification": "Partner adhesion molecule in desmosomes, essential for force distribution across epithelia and myocardium."
    },
    {
        "gene_symbol": "PKP2",
        "uniprot_id": "O15118",
        "organism": "Homo sapiens",
        "pathway_tags": "Adhesion,Mechanotransduction,Cytoskeleton",
        "gravity_link": "Plakophilin-2 links desmosomal cadherins to the intermediate filament network, acting as a force-transducing scaffold.",
        "spine_curvature_link": "Disruptions lead to failure of intercellular mechanocoupling under stress, leading to tissue tearing and myopathy. (PMID: 15489853)",
        "priority_score": 85,
        "justification": "Crucial adapter organizing the desmosomal mechanotransduction complex."
    },
    {
        "gene_symbol": "DSP",
        "uniprot_id": "P15924",
        "organism": "Homo sapiens",
        "pathway_tags": "Adhesion,Mechanotransduction,Cytoskeleton",
        "gravity_link": "Desmoplakin directly anchors intermediate filaments to the desmosome, serving as the primary mechanical tether between cells.",
        "spine_curvature_link": "Mutations cause severe skin and heart fragility under mechanical stress (Carvajal syndrome). (PMID: 10839976)",
        "priority_score": 87,
        "justification": "The primary mechanotether integrating the intermediate filament networks of adjacent cells."
    },
    {
        "gene_symbol": "CFL1",
        "uniprot_id": "P23528",
        "organism": "Homo sapiens",
        "pathway_tags": "Cytoskeleton,Mechanotransduction,Motility",
        "gravity_link": "Cofilin-1 severs actin filaments, regulating cytoskeletal turnover and the dynamic response of the actin network to applied force.",
        "spine_curvature_link": "Essential for somite formation, neural crest migration, and dynamic mechanoadaptation during development. (PMID: 11110541)",
        "priority_score": 89,
        "justification": "Master regulator of actin filament dynamics, essential for cellular mechanical remodeling."
    },
    {
        "gene_symbol": "LIMK1",
        "uniprot_id": "P53667",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,Cytoskeleton,Signaling",
        "gravity_link": "LIM domain kinase 1 phosphorylates and inactivates cofilin, stabilizing the actin cytoskeleton in response to mechanical stimuli (via ROCK).",
        "spine_curvature_link": "Linked to Williams syndrome, which often features spinal deformities; stabilizes actin networks under stress. (PMID: 9662396)",
        "priority_score": 86,
        "justification": "Key regulatory kinase downstream of mechanosensitive GTPases that stabilizes the actin cytoskeleton."
    },
    {
        "gene_symbol": "WASF1",
        "uniprot_id": "Q92558",
        "organism": "Homo sapiens",
        "pathway_tags": "Cytoskeleton,Mechanotransduction,Signaling",
        "gravity_link": "WAVE1 activates the Arp2/3 complex to branch actin filaments, driving protrusive force at the leading edge against external resistance.",
        "spine_curvature_link": "Required for proper neurodevelopment and cellular migration during embryogenesis, influencing tissue architecture. (PMID: 12515822)",
        "priority_score": 82,
        "justification": "Regulator of branched actin networks, pushing against external physical barriers."
    },
    {
        "gene_symbol": "ARPC2",
        "uniprot_id": "O15144",
        "organism": "Homo sapiens",
        "pathway_tags": "Cytoskeleton,Mechanotransduction,Structure",
        "gravity_link": "Core component of the Arp2/3 complex, nucleating branched actin networks that determine cortical stiffness and resist compression.",
        "spine_curvature_link": "Crucial for establishing a rigid cellular cortex during morphogenesis and osteoblast function. (PMID: 10601321)",
        "priority_score": 85,
        "justification": "Core nucleator of the cortical actin network that provides cellular compressive strength."
    },
    {
        "gene_symbol": "MYBPC1",
        "uniprot_id": "Q00872",
        "organism": "Homo sapiens",
        "pathway_tags": "Muscle,Structure,Contractility",
        "gravity_link": "Slow skeletal myosin binding protein C regulates cross-bridge cycling and force generation in slow-twitch, fatigue-resistant (postural) muscles.",
        "spine_curvature_link": "Mutations cause distal arthrogryposis, altering muscle contractility and tone, frequently associated with scoliosis. (PMID: 18776911)",
        "priority_score": 90,
        "justification": "Crucial regulator of force generation specifically in the slow-twitch muscles maintaining postural tone against gravity."
    }
]

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        sys.exit(1)

    existing_symbols = set()
    file_fieldnames = []

    try:
        with open(MASTER_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            file_fieldnames = reader.fieldnames

            if not file_fieldnames or 'gene_symbol' not in file_fieldnames:
                print("Error: CSV missing header or 'gene_symbol' column.")
                sys.exit(1)

            for row in reader:
                if row['gene_symbol']:
                    existing_symbols.add(row['gene_symbol'].strip().upper())
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    added_count = 0
    skipped_count = 0

    try:
        with open(MASTER_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=file_fieldnames)

            for cand in new_candidates:
                symbol = cand['gene_symbol'].strip().upper()
                if symbol in existing_symbols:
                    print(f"Skipping {cand['gene_symbol']} (already exists)")
                    skipped_count += 1
                    continue

                row_to_write = {k: v for k, v in cand.items() if k in file_fieldnames}
                writer.writerow(row_to_write)
                print(f"Added {cand['gene_symbol']}")
                added_count += 1

    except Exception as e:
        print(f"Error writing to CSV: {e}")
        sys.exit(1)

    print(f"\nSummary: Added {added_count} candidates. Skipped {skipped_count} duplicates.")

if __name__ == "__main__":
    main()
