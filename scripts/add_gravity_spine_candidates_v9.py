import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    new_candidates = [
        {
            "gene_symbol": "ROCK2",
            "uniprot_id": "O75116",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Cytoskeleton,Signaling",
            "gravity_link": "Rho-associated protein kinase 2; key effector of RhoA in regulating actin cytoskeleton tension and focal adhesion formation in response to mechanical stress.",
            "spine_curvature_link": "Implicated in mechanotransduction pathways affecting osteogenesis; ROCK inhibitors affect bone formation and potentially spinal alignment. (PMID: 25892552)",
            "priority_score": "86",
            "justification": "Crucial kinase linking mechanical tension to cytoskeletal remodeling in structural tissues."
        },
        {
            "gene_symbol": "DCN",
            "uniprot_id": "P07585",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Proteoglycan,Collagen",
            "gravity_link": "Decorin; regulates collagen fibrillogenesis and matrix assembly, essential for tissue tensile strength against gravity.",
            "spine_curvature_link": "Decorin-deficient mice show fragile skin and altered bone structure; ECM defects are heavily linked to AIS. (PMID: 9114002)",
            "priority_score": "88",
            "justification": "Core proteoglycan regulating structural integrity and mechanics of the spine."
        },
        {
            "gene_symbol": "LUM",
            "uniprot_id": "P51884",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Proteoglycan,Collagen",
            "gravity_link": "Lumican; controls collagen fibril assembly and tissue hydration, contributing to mechanical resilience of connective tissues.",
            "spine_curvature_link": "Knockout models exhibit joint laxity and connective tissue defects; related to scoliosis etiology. (PMID: 9478951)",
            "priority_score": "85",
            "justification": "Important for collagen fibril organization and connective tissue biomechanics."
        },
        {
            "gene_symbol": "FMOD",
            "uniprot_id": "Q06828",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Proteoglycan,Collagen",
            "gravity_link": "Fibromodulin; interacts with collagen type I and II fibrils, modulating their formation and responding to mechanical loads.",
            "spine_curvature_link": "Mice lacking FMOD show altered tendon strength and bone structure, potentially contributing to spinal deformities. (PMID: 10467140)",
            "priority_score": "85",
            "justification": "Modulates collagen cross-linking and tissue mechanical properties."
        },
        {
            "gene_symbol": "VCAN",
            "uniprot_id": "P13611",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Proteoglycan,Development",
            "gravity_link": "Versican; large chondroitin sulfate proteoglycan providing hydration and compressive resistance to tissues under load.",
            "spine_curvature_link": "Mutations are associated with Wagner syndrome and structural anomalies; involved in precartilaginous condensations during spine development. (PMID: 16155189)",
            "priority_score": "84",
            "justification": "Provides compressive stiffness in cartilage and intervertebral discs."
        },
        {
            "gene_symbol": "BMP2",
            "uniprot_id": "P12643",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Bone,Development",
            "gravity_link": "Bone morphogenetic protein 2; its expression is mechanically responsive and essential for load-induced bone formation.",
            "spine_curvature_link": "Critical for osteoblast differentiation and spine fusion; altered BMP signaling is observed in AIS patients. (PMID: 21908061)",
            "priority_score": "90",
            "justification": "Mechanosensitive morphogen crucial for vertebral bone development and remodeling."
        },
        {
            "gene_symbol": "FGF2",
            "uniprot_id": "P09038",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Growth_Plate,Mechanotransduction",
            "gravity_link": "Fibroblast growth factor 2; mechanically stimulated release from ECM promotes cell proliferation and matrix synthesis.",
            "spine_curvature_link": "Regulates chondrocyte proliferation in the growth plate; asymmetric growth plate dynamics drive scoliosis. (PMID: 26051563)",
            "priority_score": "88",
            "justification": "Key regulator of growth plate dynamics linked to mechanotransduction."
        },
        {
            "gene_symbol": "LEF1",
            "uniprot_id": "Q9UJU2",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Wnt,Transcription_Factor",
            "gravity_link": "Lymphoid enhancer-binding factor 1; mediates Wnt signaling which is sensitive to mechanical loading in bone.",
            "spine_curvature_link": "Wnt/beta-catenin signaling regulates bone mass and osteoblast function; linked to pathogenesis of AIS. (PMID: 23150244)",
            "priority_score": "86",
            "justification": "Downstream effector of mechanosensitive Wnt signaling in bone."
        },
        {
            "gene_symbol": "TCF7L2",
            "uniprot_id": "Q9NQB0",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Wnt,Transcription_Factor",
            "gravity_link": "Transcription factor 7-like 2; another key effector of Wnt signaling involved in responding to mechanical strain.",
            "spine_curvature_link": "Genetic variants are associated with bone mineral density and potential susceptibility to spinal deformities. (PMID: 25150284)",
            "priority_score": "85",
            "justification": "Important transcription factor for mechanically-regulated Wnt pathway."
        },
        {
            "gene_symbol": "CHAD",
            "uniprot_id": "O15335",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Cartilage,Adhesion",
            "gravity_link": "Chondroadherin; mediates adhesion of isolated chondrocytes to extracellular matrix proteins, important in load-bearing cartilage.",
            "spine_curvature_link": "Highly expressed in the intervertebral disc; plays a role in transmitting mechanical signals to cells in the spine. (PMID: 15305141)",
            "priority_score": "84",
            "justification": "Mediates cell-matrix interactions in load-bearing spinal tissues."
        }
    ]

    existing_genes = set()
    with open(MASTER_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_genes.add(row['gene_symbol'].strip().upper())

    count = 0
    with open(MASTER_FILE, 'a', newline='') as f:
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

if __name__ == "__main__":
    main()
