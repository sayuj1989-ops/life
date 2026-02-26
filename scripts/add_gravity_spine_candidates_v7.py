import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    new_candidates = [
        {
            "gene_symbol": "CACNA1S",
            "uniprot_id": "Q13698",
            "organism": "Homo sapiens",
            "pathway_tags": "Muscle,Ion_Channel,Mechanotransduction",
            "gravity_link": "Voltage-gated calcium channel essential for excitation-contraction coupling; acts as a voltage sensor for RyR1.",
            "spine_curvature_link": "Mutations cause Hypokalemic Periodic Paralysis; linked to muscle weakness and potential spinal deformities. (Review: Jurkat-Rott et al., 2000, PMID: 10978347)",
            "priority_score": "85",
            "justification": "Primary voltage sensor for muscle contraction."
        },
        {
            "gene_symbol": "LRRC8A",
            "uniprot_id": "Q8IWT6",
            "organism": "Homo sapiens",
            "pathway_tags": "Ion_Channel,Mechanotransduction,Bone",
            "gravity_link": "Volume-regulated anion channel (VRAC); activated by cell swelling and mechanical stress.",
            "spine_curvature_link": "Regulates osteoblast differentiation and bone formation; essential for skeletal development. (DOI: 10.1038/s41467-019-10515-3)",
            "priority_score": "85",
            "justification": "Mechanosensitive channel critical for bone cell volume regulation."
        },
        {
            "gene_symbol": "PKD2L1",
            "uniprot_id": "Q9P0X4",
            "organism": "Homo sapiens",
            "pathway_tags": "Ion_Channel,Cilia,Sensing",
            "gravity_link": "Polycystin-L; essential for CSF-contacting neurons sensing spinal curvature (in zebrafish).",
            "spine_curvature_link": "Loss leads to severe spinal curvature in zebrafish; potential role in human proprioception. (DOI: 10.1126/science.aaf9698)",
            "priority_score": "92",
            "justification": "Key sensor of spinal curvature in CSF-contacting neurons."
        },
        {
            "gene_symbol": "CFAP53",
            "uniprot_id": "Q96M91",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Motility",
            "gravity_link": "Cilia and flagella associated protein; essential for nodal cilia motility and L-R asymmetry.",
            "spine_curvature_link": "Mutations cause situs inversus and heterotaxy, frequently associated with spinal anomalies. (DOI: 10.1016/j.ajhg.2012.01.003)",
            "priority_score": "88",
            "justification": "Essential for nodal flow and L-R asymmetry."
        },
        {
            "gene_symbol": "ANKS6",
            "uniprot_id": "Q68DC2",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Signaling,Kidney",
            "gravity_link": "Ankyrin repeat protein; localizes to the inversin compartment of cilia; regulates NPHP signaling.",
            "spine_curvature_link": "Mutations cause Nephronophthisis with skeletal defects (ciliopathy). (DOI: 10.1038/ng.2638)",
            "priority_score": "85",
            "justification": "Ciliary protein linked to renal-skeletal ciliopathies."
        },
        {
            "gene_symbol": "MAPK7",
            "uniprot_id": "Q13164",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Mechanotransduction,Bone",
            "gravity_link": "Fluid flow sensing kinase in osteoblasts and endothelium; regulates bone mass.",
            "spine_curvature_link": "Essential for osteoblast response to mechanical loading; deletion leads to osteopenia. (DOI: 10.1073/pnas.1610766113)",
            "priority_score": "85",
            "justification": "Key kinase for fluid flow mechanotransduction in bone."
        },
        {
            "gene_symbol": "KLF2",
            "uniprot_id": "Q9Y5W3",
            "organism": "Homo sapiens",
            "pathway_tags": "Transcription_Factor,Flow_Sensing",
            "gravity_link": "Transcription factor induced by fluid shear stress; regulates endothelial and osteoblast function.",
            "spine_curvature_link": "Promotes osteoblast differentiation and bone formation under flow; essential for vascular-bone coupling. (DOI: 10.1073/pnas.1718047115)",
            "priority_score": "85",
            "justification": "Flow-responsive transcription factor."
        },
        {
            "gene_symbol": "KLF4",
            "uniprot_id": "O43474",
            "organism": "Homo sapiens",
            "pathway_tags": "Transcription_Factor,Flow_Sensing",
            "gravity_link": "Transcription factor induced by fluid shear stress; regulates osteoblast differentiation.",
            "spine_curvature_link": "Partner of KLF2 in flow sensing; regulates bone turnover. (DOI: 10.1073/pnas.1718047115)",
            "priority_score": "82",
            "justification": "Flow-responsive transcription factor."
        },
        {
            "gene_symbol": "MEF2C",
            "uniprot_id": "Q06413",
            "organism": "Homo sapiens",
            "pathway_tags": "Transcription_Factor,Muscle,Bone",
            "gravity_link": "MADS-box transcription factor; essential for muscle and bone development; activity modulated by HDACs.",
            "spine_curvature_link": "Regulates sclerotome differentiation and vertebral formation; deletion leads to severe skeletal defects. (DOI: 10.1016/j.devcel.2008.11.006)",
            "priority_score": "88",
            "justification": "Master regulator of muscle/bone fate linked to mechanics."
        },
        {
            "gene_symbol": "HDAC4",
            "uniprot_id": "P56524",
            "organism": "Homo sapiens",
            "pathway_tags": "Epigenetics,Mechanotransduction,Muscle",
            "gravity_link": "Class IIa HDAC; shuttles between nucleus/cytoplasm in response to mechanical stress/Ca2+.",
            "spine_curvature_link": "Represses MEF2C and Runx2; mechanical loading relieves repression to promote bone/muscle growth. (DOI: 10.1038/nature04179)",
            "priority_score": "88",
            "justification": "Mechanosensitive repressor shuttling in response to load."
        },
        {
            "gene_symbol": "HDAC5",
            "uniprot_id": "Q9UQL6",
            "organism": "Homo sapiens",
            "pathway_tags": "Epigenetics,Mechanotransduction,Muscle",
            "gravity_link": "Class IIa HDAC; shuttles between nucleus/cytoplasm; partner of HDAC4.",
            "spine_curvature_link": "Regulates muscle hypertrophy and bone remodeling under load. (DOI: 10.1073/pnas.1415705111)",
            "priority_score": "85",
            "justification": "Partner of HDAC4 in mechanosensing."
        },
        {
            "gene_symbol": "ANK1",
            "uniprot_id": "P16157",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Membrane,Muscle",
            "gravity_link": "Ankyrin-1; connects membrane proteins to the spectrin-actin cytoskeleton; essential for membrane mechanics.",
            "spine_curvature_link": "Mutations cause Spherocytosis; potential link to muscle membrane integrity and costameres. (PMID: 22267503)",
            "priority_score": "82",
            "justification": "Essential linker for membrane-cytoskeleton mechanics."
        },
        {
            "gene_symbol": "SPTA1",
            "uniprot_id": "P02549",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Membrane",
            "gravity_link": "Spectrin Alpha; forms the membrane skeleton maintaining cell shape and elasticity.",
            "spine_curvature_link": "Essential for erythrocyte deformability; potential role in non-erythroid cells under stress. (PMID: 1533966)",
            "priority_score": "80",
            "justification": "Key component of the membrane skeleton."
        },
        {
            "gene_symbol": "ANO1",
            "uniprot_id": "Q5XXA6",
            "organism": "Homo sapiens",
            "pathway_tags": "Ion_Channel,Mechanotransduction",
            "gravity_link": "Ca2+-activated Cl- channel; activated by membrane stretch and swelling.",
            "spine_curvature_link": "Regulates epithelial fluid secretion and cyst growth; potential role in notochord/disc fluid mechanics. (DOI: 10.1126/science.1162077)",
            "priority_score": "82",
            "justification": "Mechanosensitive chloride channel."
        },
        {
            "gene_symbol": "SORBS1",
            "uniprot_id": "Q9BX66",
            "organism": "Homo sapiens",
            "pathway_tags": "Adhesion,Mechanotransduction",
            "gravity_link": "Adaptor protein at focal adhesions; links insulin signaling to cytoskeleton.",
            "spine_curvature_link": "Regulates actin stress fiber formation and cell adhesion strength. (DOI: 10.1038/ncb2376)",
            "priority_score": "80",
            "justification": "Focal adhesion adaptor linking signaling to structure."
        },
        {
            "gene_symbol": "SORBS2",
            "uniprot_id": "O94875",
            "organism": "Homo sapiens",
            "pathway_tags": "Adhesion,Cytoskeleton",
            "gravity_link": "Adaptor protein; regulates actin dynamics and potentially mechanotransduction.",
            "spine_curvature_link": "Linked to intellectual disability and potential skeletal anomalies via cytoskeletal regulation. (DOI: 10.1016/j.ajhg.2016.03.022)",
            "priority_score": "80",
            "justification": "Cytoskeletal adaptor protein."
        },
        {
            "gene_symbol": "ABL1",
            "uniprot_id": "P00519",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Cytoskeleton,Mechanotransduction",
            "gravity_link": "Tyrosine kinase; regulates actin remodeling and mechanotransduction at adherens junctions.",
            "spine_curvature_link": "Activated by mechanical force; regulates cell shape and tension. (DOI: 10.1038/ncb2585)",
            "priority_score": "82",
            "justification": "Mechanosensitive kinase regulating actin dynamics."
        },
        {
            "gene_symbol": "BCAR1",
            "uniprot_id": "P56945",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Adhesion",
            "gravity_link": "Cas scaffolding protein; undergoes stretch-induced unfolding to recruit signaling effectors.",
            "spine_curvature_link": "Primary mechanosensor at focal adhesions; essential for force-dependent signaling. (DOI: 10.1038/nature05061)",
            "priority_score": "90",
            "justification": "Classic focal adhesion mechanosensor."
        },
        {
            "gene_symbol": "TLN2",
            "uniprot_id": "Q9Y4G6",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Adhesion",
            "gravity_link": "Cytoskeletal protein linking integrins to actin; force transmission molecule.",
            "spine_curvature_link": "Redundant with Talin-1 but higher affinity for integrins; essential for focal adhesion stability. (DOI: 10.1038/ncb2447)",
            "priority_score": "85",
            "justification": "Force transmission molecule at focal adhesions."
        },
        {
            "gene_symbol": "CRK",
            "uniprot_id": "P46108",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Mechanotransduction",
            "gravity_link": "Adaptor protein; binds phosphotyrosines on p130Cas upon stretching.",
            "spine_curvature_link": "Essential for transducing mechanical signals from p130Cas to downstream effectors (Rac1/Rap1). (DOI: 10.1016/j.devcel.2006.02.016)",
            "priority_score": "85",
            "justification": "Effector of p130Cas mechanosensing."
        }
    ]

    existing_genes = set()
    with open(MASTER_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_genes.add(row['gene_symbol'])

    count = 0
    with open(MASTER_FILE, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=["gene_symbol", "uniprot_id", "organism", "pathway_tags", "gravity_link", "spine_curvature_link", "priority_score", "justification"])
        # No header write, appending
        for c in new_candidates:
            if c['gene_symbol'] not in existing_genes:
                writer.writerow(c)
                count += 1
                print(f"Added {c['gene_symbol']}")
            else:
                print(f"Skipped {c['gene_symbol']} (already exists)")

    print(f"Added {count} new candidates.")

if __name__ == "__main__":
    main()
