import csv
import os

MASTER_FILE = "data/candidates_master.csv"

new_candidates = [
    {
        "gene_symbol": "ITGAV",
        "uniprot_id": "P06756",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,Adhesion,Bone",
        "gravity_link": "Integrin alpha-V; essential for osteoclast function and bone resorption in unloading.",
        "spine_curvature_link": "Imbalance in resorption leads to osteopenia and vertebral compression fractures. (General Bone Bio)",
        "priority_score": 85,
        "justification": "Key receptor for bone resorption in microgravity."
    },
    {
        "gene_symbol": "ITGA5",
        "uniprot_id": "P08648",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,Development,Notochord",
        "gravity_link": "Integrin alpha-5; binds fibronectin; essential for notochord formation and mechanosensing.",
        "spine_curvature_link": "Loss leads to posterior truncation and somite defects; essential for spine formation. (DOI: 10.1242/dev.01806)",
        "priority_score": 88,
        "justification": "Critical integrin for notochordal mechanics and somitogenesis."
    },
    {
        "gene_symbol": "LATS1",
        "uniprot_id": "O95835",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,Hippo,Bone",
        "gravity_link": "Hippo pathway kinase; negative regulator of YAP/TAZ stiffness sensors.",
        "spine_curvature_link": "Regulates osteoblast differentiation; knockout mice develop osteopenia and skeletal defects. (DOI: 10.1128/MCB.01170-08)",
        "priority_score": 85,
        "justification": "Key regulator of the YAP/TAZ mechanotransduction axis."
    },
    {
        "gene_symbol": "DVL3",
        "uniprot_id": "Q92997",
        "organism": "Homo sapiens",
        "pathway_tags": "PCP,Wnt_Signaling,Development",
        "gravity_link": "Dishevelled-3; Wnt/PCP signaling effector aligning tissues against stress vectors.",
        "spine_curvature_link": "Mutations cause Robinow Syndrome (mesomelic dysplasia with vertebral segmentation defects). (DOI: 10.1038/ng.3511)",
        "priority_score": 90,
        "justification": "PCP effector directly linked to vertebral segmentation defects."
    },
    {
        "gene_symbol": "IFT80",
        "uniprot_id": "Q9NVS0",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Transport,Skeleton",
        "gravity_link": "Intraflagellar Transport 80; essential for ciliary assembly and sensing fluid flow/gravity.",
        "spine_curvature_link": "Mutations cause Jeune Asphyxiating Thoracic Dystrophy (JATD) with spinal changes. (DOI: 10.1038/ng.150)",
        "priority_score": 88,
        "justification": "Ciliary protein linked to severe skeletal dysplasia."
    },
    {
        "gene_symbol": "IFT172",
        "uniprot_id": "Q9UG01",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Transport,Skeleton",
        "gravity_link": "Intraflagellar Transport 172; essential for ciliary assembly and Hedgehog signaling.",
        "spine_curvature_link": "Mutations cause Mainzer-Saldino syndrome and JATD; severe skeletal dysplasia. (DOI: 10.1016/j.ajhg.2013.10.019)",
        "priority_score": 88,
        "justification": "IFT complex B component essential for skeletal formation."
    },
    {
        "gene_symbol": "MATN3",
        "uniprot_id": "O15232",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Cartilage,Structure",
        "gravity_link": "Matrilin-3; connects collagen fibrils and proteoglycans; maintains cartilage stiffness.",
        "spine_curvature_link": "Mutations cause Multiple Epiphyseal Dysplasia (MED) with irregular vertebral endplates. (DOI: 10.1038/ng762)",
        "priority_score": 85,
        "justification": "ECM component critical for cartilage mechanical integrity."
    },
    {
        "gene_symbol": "COL9A3",
        "uniprot_id": "Q14050",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Cartilage,Structure",
        "gravity_link": "Collagen Type IX Alpha 3; FACIT collagen stabilizing fibrils against load.",
        "spine_curvature_link": "Mutations cause Multiple Epiphyseal Dysplasia (MED) and Stickler syndrome. (DOI: 10.1086/302008)",
        "priority_score": 85,
        "justification": "Structural collagen associated with spinal flattening."
    },
    {
        "gene_symbol": "CDC42",
        "uniprot_id": "P60953",
        "organism": "Homo sapiens",
        "pathway_tags": "Cytoskeleton,PCP,Growth_Plate",
        "gravity_link": "Rho GTPase; regulates cytoskeleton organization and cell polarity (PCP).",
        "spine_curvature_link": "Essential for chondrocyte polarity and column formation in growth plate; loss leads to severe dysplasia. (DOI: 10.1038/nature05522)",
        "priority_score": 85,
        "justification": "Regulator of chondrocyte polarity and growth plate architecture."
    },
    {
        "gene_symbol": "CCN1",
        "uniprot_id": "O00622",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Mechanotransduction,Signaling",
        "gravity_link": "CYR61; mechanosensitive matricellular protein (YAP target) promoting adhesion.",
        "spine_curvature_link": "Essential for chondrocyte differentiation; null mice have skeletal defects. (DOI: 10.1083/jcb.200702006)",
        "priority_score": 85,
        "justification": "YAP target regulating skeletal development."
    },
    {
        "gene_symbol": "TTC21B",
        "uniprot_id": "Q7Z4L5",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Transport,Skeleton",
        "gravity_link": "IFT139; retrograde IFT component essential for ciliary signaling.",
        "spine_curvature_link": "Mutations cause Jeune syndrome and Nephronophthisis with skeletal defects. (DOI: 10.1038/ng.810)",
        "priority_score": 85,
        "justification": "Retrograde IFT protein linked to skeletal ciliopathies."
    },
    {
        "gene_symbol": "IGF1R",
        "uniprot_id": "P08069",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Growth,Bone",
        "gravity_link": "Receptor for IGF1; mechanosensitive growth pathway essential for loading response.",
        "spine_curvature_link": "Essential for skeletal growth; mutations cause growth retardation and potential asymmetry. (DOI: 10.1056/NEJMoa012691)",
        "priority_score": 85,
        "justification": "Key receptor for load-dependent skeletal growth."
    },
    {
        "gene_symbol": "BMP2",
        "uniprot_id": "P12643",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Bone,Mechanotransduction",
        "gravity_link": "Bone Morphogenetic Protein 2; mechanically induced osteogenic factor.",
        "spine_curvature_link": "Essential for bone formation and fracture healing; crucial for vertebral ossification. (DOI: 10.1016/S0021-9290(02)00244-9)",
        "priority_score": 85,
        "justification": "Potent osteogenic factor responsive to mechanical load."
    },
    {
        "gene_symbol": "SMAD2",
        "uniprot_id": "Q15796",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Mechanotransduction,TGF-beta",
        "gravity_link": "TGF-beta signaling effector; pathway activated by mechanical strain.",
        "spine_curvature_link": "Conditional deletion in cartilage leads to spinal deformity. (DOI: 10.1073/pnas.1513252112 context)",
        "priority_score": 85,
        "justification": "Effector of load-dependent TGF-beta signaling."
    },
    {
        "gene_symbol": "IGFBP3",
        "uniprot_id": "P17936",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Growth,Bone",
        "gravity_link": "IGF binding protein; modulates IGF1 bioavailability under load.",
        "spine_curvature_link": "Serum levels correlate with skeletal growth velocity; potential marker for curve progression.",
        "priority_score": 82,
        "justification": "Modulator of the IGF1 growth axis."
    },
    {
        "gene_symbol": "IGFBP5",
        "uniprot_id": "P24593",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Growth,Bone",
        "gravity_link": "IGF binding protein; expression is mechanically regulated in bone.",
        "spine_curvature_link": "Promotes osteoblast differentiation; cleaved by PAPPA2 (scoliosis gene). (DOI: 10.1056/NEJMoa1510985 context)",
        "priority_score": 85,
        "justification": "Mechanosensitive IGFBP linked to PAPPA2."
    },
    {
        "gene_symbol": "CCN3",
        "uniprot_id": "P48745",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Signaling,Bone",
        "gravity_link": "NOV; matricellular protein regulating Notch/BMP; mechanosensitive.",
        "spine_curvature_link": "Overexpression impairs osteogenesis; regulates disc homeostasis. (DOI: 10.1002/jbmr.264 context)",
        "priority_score": 82,
        "justification": "Regulator of osteogenesis and disc maintenance."
    },
    {
        "gene_symbol": "CCN4",
        "uniprot_id": "O95388",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Signaling,Bone",
        "gravity_link": "WISP1; Wnt-induced secreted protein; promotes osteogenesis under load.",
        "spine_curvature_link": "Promotes spinal fusion and bone formation; Wnt target. (DOI: 10.1086/521524 context)",
        "priority_score": 82,
        "justification": "Wnt target promoting bone formation."
    },
    {
        "gene_symbol": "CCN5",
        "uniprot_id": "O76076",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Signaling,Inhibitor",
        "gravity_link": "WISP2; Wnt-induced protein; inhibits cardiac hypertrophy (load response).",
        "spine_curvature_link": "Regulates mesenchymal stem cell differentiation; potential role in bone quality.",
        "priority_score": 80,
        "justification": "Regulator of MSC differentiation."
    },
    {
        "gene_symbol": "WNT5B",
        "uniprot_id": "Q9H1J7",
        "organism": "Homo sapiens",
        "pathway_tags": "PCP,Wnt_Signaling,Growth_Plate",
        "gravity_link": "Non-canonical Wnt ligand; regulates PCP and tissue elongation.",
        "spine_curvature_link": "Regulates chondrocyte proliferation/differentiation; overexpression causes dwarfism. (DOI: 10.1242/dev.01639)",
        "priority_score": 82,
        "justification": "PCP ligand regulating growth plate dynamics."
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
