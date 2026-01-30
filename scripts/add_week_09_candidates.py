import csv
import os

MASTER_FILE = "data/candidates_master.csv"

new_candidates = [
    {
        "gene_symbol": "HDAC4",
        "uniprot_id": "P56524",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,Growth_Plate,Repressor",
        "gravity_link": "Mechanosensitive repressor of chondrocyte hypertrophy; regulated by mechanical stress.",
        "spine_curvature_link": "Deletion causes Brachydactyly Type E with short stature; essential for vertebral ossification. (PMID: 20691402)",
        "priority_score": 88,
        "justification": "Key regulator of growth plate mechanics and ossification under load."
    },
    {
        "gene_symbol": "TRPM7",
        "uniprot_id": "Q96QT4",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,Ion_Channel,Kinase",
        "gravity_link": "Mechanosensitive kinase/channel regulating actomyosin contractility and cell stiffness.",
        "spine_curvature_link": "Zebrafish trpm7 mutants exhibit scoliosis and skeletal defects. (PMID: 20506162)",
        "priority_score": 88,
        "justification": "Mechanosensitive channel essential for skeletal development and alignment."
    },
    {
        "gene_symbol": "COL12A1",
        "uniprot_id": "Q99715",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Muscle,Structure",
        "gravity_link": "FACIT collagen associated with Type I fibrils; regulates tissue elasticity and load bearing.",
        "spine_curvature_link": "Mutations cause Bethlem Myopathy and Ullrich CMD, often featuring scoliosis. (PMID: 24360824)",
        "priority_score": 85,
        "justification": "Structural collagen linking muscle and ECM mechanics."
    },
    {
        "gene_symbol": "DYNC1H1",
        "uniprot_id": "Q14204",
        "organism": "Homo sapiens",
        "pathway_tags": "Cytoskeleton,Motor_Protein,Transport",
        "gravity_link": "Cytoplasmic dynein motor; essential for retrograde transport of mechanosignals.",
        "spine_curvature_link": "Mutations cause SMA-LED with severe congenital scoliosis. (PMID: 22158540)",
        "priority_score": 88,
        "justification": "Motor protein essential for spinal motor neuron health and alignment."
    },
    {
        "gene_symbol": "SPP1",
        "uniprot_id": "P10451",
        "organism": "Homo sapiens",
        "pathway_tags": "Bone,Mechanotransduction,ECM",
        "gravity_link": "Highly mechanosensitive bone matrix protein; upregulated in unloading (microgravity).",
        "spine_curvature_link": "Expression correlates with curve severity in AIS; essential for bone remodeling. (PMID: 28431448)",
        "priority_score": 85,
        "justification": "Marker of bone response to mechanical unloading."
    },
    {
        "gene_symbol": "ROR2",
        "uniprot_id": "Q01974",
        "organism": "Homo sapiens",
        "pathway_tags": "PCP,Wnt_Signaling,Receptor",
        "gravity_link": "Receptor for Wnt5a; mediates non-canonical Wnt/PCP signaling (tissue polarity).",
        "spine_curvature_link": "Mutations cause Robinow Syndrome with hemivertebrae and scoliosis. (PMID: 10958648)",
        "priority_score": 88,
        "justification": "PCP receptor directly linked to vertebral segmentation defects."
    },
    {
        "gene_symbol": "LOXL3",
        "uniprot_id": "P58215",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Enzyme,Structure",
        "gravity_link": "Lysyl oxidase essential for collagen crosslinking and tissue stiffness.",
        "spine_curvature_link": "Mutations cause Stickler syndrome and early onset scoliosis. (PMID: 26805783)",
        "priority_score": 85,
        "justification": "Enzyme defining the mechanical properties of the spine."
    },
    {
        "gene_symbol": "FBLN4",
        "uniprot_id": "O95967",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Elasticity,Structure",
        "gravity_link": "Essential for elastic fiber assembly; provides recoil against gravity.",
        "spine_curvature_link": "Mutations cause Cutis Laxa with severe scoliosis/kyphosis. (PMID: 19442775)",
        "priority_score": 85,
        "justification": "Critical for elastic fiber integrity in the spine."
    },
    {
        "gene_symbol": "PLOD1",
        "uniprot_id": "Q02809",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Enzyme,Structure",
        "gravity_link": "Lysyl hydroxylase; determines collagen stiffness and stability.",
        "spine_curvature_link": "Mutations cause Ehlers-Danlos Kyphoscoliotic form (Type VI). (PMID: 18566912)",
        "priority_score": 88,
        "justification": "Defining gene for the 'Kyphoscoliotic' type of EDS."
    },
    {
        "gene_symbol": "TMEM63A",
        "uniprot_id": "Q9NQ10",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,Ion_Channel",
        "gravity_link": "Mammalian homolog of OSCA (plant mechanosensor); high-threshold mechanosensitive channel.",
        "spine_curvature_link": "Potential role in hearing/balance (gravity sensing); expressed in bone.",
        "priority_score": 80,
        "justification": "Evolutionarily conserved mechanosensitive channel."
    },
    {
        "gene_symbol": "TMC1",
        "uniprot_id": "Q8TDI8",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,Hearing,Gravity_Sensing",
        "gravity_link": "Pore-forming subunit of the hair cell mechanotransduction channel (gravity sensing).",
        "spine_curvature_link": "Essential for vestibular function; loss disrupts gravity reference frame.",
        "priority_score": 85,
        "justification": "Core component of the vestibular gravity sensing machinery."
    },
    {
        "gene_symbol": "GPC3",
        "uniprot_id": "P51654",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Development,Growth",
        "gravity_link": "Regulates Wnt/Hedgehog signaling; modulates growth plate response.",
        "spine_curvature_link": "Mutations cause Simpson-Golabi-Behmel syndrome (overgrowth, scoliosis). (PMID: 11242107)",
        "priority_score": 85,
        "justification": "Regulator of growth plate signaling and body size."
    },
    {
        "gene_symbol": "PAPPA2",
        "uniprot_id": "Q9BXP8",
        "organism": "Homo sapiens",
        "pathway_tags": "Growth,Signaling,Protease",
        "gravity_link": "Regulates IGF bioavailability; essential for bone growth under load.",
        "spine_curvature_link": "Mutations cause short stature and scoliosis. (PMID: 27077678)",
        "priority_score": 82,
        "justification": "Modulates IGF signaling in the growing spine."
    },
    {
        "gene_symbol": "MATN3",
        "uniprot_id": "O15232",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Cartilage,Structure",
        "gravity_link": "Forms filamentous networks in cartilage; contributes to stiffness.",
        "spine_curvature_link": "Mutations cause Multiple Epiphyseal Dysplasia (MED) with spinal involvement. (PMID: 11565066)",
        "priority_score": 82,
        "justification": "Structural component of cartilage matrix."
    },
    {
        "gene_symbol": "COL9A1",
        "uniprot_id": "P20849",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Cartilage,Structure",
        "gravity_link": "FACIT collagen bridging fibrils in cartilage; resists shear.",
        "spine_curvature_link": "Mutations cause Stickler syndrome and MED with scoliosis. (PMID: 8004098)",
        "priority_score": 85,
        "justification": "Key for cartilage mechanical integrity."
    },
    {
        "gene_symbol": "PRICKLE2",
        "uniprot_id": "Q7Z3G6",
        "organism": "Homo sapiens",
        "pathway_tags": "PCP,Signaling,Development",
        "gravity_link": "PCP component aligning cells against stress.",
        "spine_curvature_link": "Variants linked to Neural Tube Defects; PCP is essential for spine straightening. (PMID: 21670737)",
        "priority_score": 78,
        "justification": "PCP pathway component."
    },
    {
        "gene_symbol": "SMAD2",
        "uniprot_id": "Q15796",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Mechanotransduction",
        "gravity_link": "Downstream of TGF-beta; mechanically regulated.",
        "spine_curvature_link": "Mutations cause Loeys-Dietz syndrome (scoliosis). (PMID: 21782247)",
        "priority_score": 85,
        "justification": "Key effector of TGF-beta signaling linked to Loeys-Dietz."
    },
    {
        "gene_symbol": "TGFBR1",
        "uniprot_id": "P36897",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Receptor,Mechanotransduction",
        "gravity_link": "TGF-beta receptor; signaling is mechanically modulated.",
        "spine_curvature_link": "Mutations cause Loeys-Dietz syndrome (scoliosis). (PMID: 16928994)",
        "priority_score": 88,
        "justification": "Receptor for the load-dependent TGF-beta pathway."
    },
    {
        "gene_symbol": "ANKRD6",
        "uniprot_id": "Q9Y2G4",
        "organism": "Homo sapiens",
        "pathway_tags": "PCP,Wnt_Signaling",
        "gravity_link": "Regulates Wnt/PCP signaling.",
        "spine_curvature_link": "Polymorphisms associated with AIS severity. (PMID: 23637770)",
        "priority_score": 82,
        "justification": "Wnt/PCP regulator linked to AIS."
    },
    {
        "gene_symbol": "FKBP10",
        "uniprot_id": "Q96AY3",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Chaperone,ER",
        "gravity_link": "Chaperone for collagen/elastin; essential for tissue mechanics.",
        "spine_curvature_link": "Mutations cause Osteogenesis Imperfecta and Bruck Syndrome (scoliosis/contractures). (PMID: 20561519)",
        "priority_score": 85,
        "justification": "Essential for collagen processing and spinal stability."
    }
]

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    # Read existing
    existing_symbols = set()
    with open(MASTER_FILE, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            existing_symbols.add(row['gene_symbol'])

    # Append new
    with open(MASTER_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        count = 0
        for cand in new_candidates:
            if cand['gene_symbol'] in existing_symbols:
                print(f"Skipping {cand['gene_symbol']} (already exists)")
                continue

            writer.writerow(cand)
            print(f"Added {cand['gene_symbol']}")
            count += 1

    print(f"Successfully added {count} new candidates.")

if __name__ == "__main__":
    main()
