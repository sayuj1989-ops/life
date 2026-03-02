import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    new_candidates = [
        {
            "gene_symbol": "VCAN",
            "uniprot_id": "P13611",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Mechanotransduction,Cartilage",
            "gravity_link": "Versican is a large chondroitin sulfate proteoglycan that provides compressive stiffness in connective tissues against gravity.",
            "spine_curvature_link": "Expressed in condensing mesenchyme of somites; dysregulation alters ECM viscoelasticity and is linked to connective tissue disorders with potential spinal effects. (PMID: 15302919)",
            "priority_score": "85",
            "justification": "Major proteoglycan dictating tissue stiffness and viscoelasticity in spine development."
        },
        {
            "gene_symbol": "DCN",
            "uniprot_id": "P07585",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Mechanotransduction,Collagen",
            "gravity_link": "Decorin binds to type I collagen fibrils, regulating their assembly and mechanical properties (tensile strength) against loading.",
            "spine_curvature_link": "Deficiency alters collagen network mechanics; Decorin is dysregulated in the intervertebral disc and scoliotic ligaments. (PMID: 25776595)",
            "priority_score": "85",
            "justification": "Key Small Leucine-Rich Proteoglycan (SLRP) regulating load-bearing collagen architecture."
        },
        {
            "gene_symbol": "ROCK2",
            "uniprot_id": "O15169",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Mechanotransduction,Contraction",
            "gravity_link": "ROCK2 is a major downstream effector of RhoA, driving actomyosin contractility to maintain tension and resist gravitational forces.",
            "spine_curvature_link": "Modulation of RhoA/ROCK signaling affects cell contractility and has been implicated in the pathogenesis of adolescent idiopathic scoliosis. (PMID: 30065020)",
            "priority_score": "82",
            "justification": "Primary driver of cellular tension responding to mechanical load."
        },
        {
            "gene_symbol": "ITGA1",
            "uniprot_id": "P56199",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Adhesion,Cartilage",
            "gravity_link": "Integrin alpha-1 is a major collagen receptor, transducing mechanical signals from the ECM stiffness to the cellular interior.",
            "spine_curvature_link": "Regulates chondrocyte differentiation and cartilage mechanical properties; essential for intervertebral disc response to loading. (PMID: 12181420)",
            "priority_score": "85",
            "justification": "Major mechanoreceptor linking the load-bearing ECM to chondrocyte responses."
        },
        {
            "gene_symbol": "IFT20",
            "uniprot_id": "Q8IY31",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Trafficking,Mechanotransduction",
            "gravity_link": "Intraflagellar transport protein 20 is essential for Golgi-to-cilia trafficking of mechanosensory receptors (e.g., polycystins).",
            "spine_curvature_link": "Deletion in osteochondroprogenitors disrupts ciliary signaling, leading to craniofacial and skeletal abnormalities including spine defects. (PMID: 27153396)",
            "priority_score": "85",
            "justification": "Crucial for delivering mechanosensors to the primary cilium."
        },
        {
            "gene_symbol": "GLI1",
            "uniprot_id": "P08151",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Hedgehog,Development",
            "gravity_link": "Transcriptional effector of the Hedgehog pathway, which is dependent on primary cilia (mechanosensors) for activation.",
            "spine_curvature_link": "Marks osteogenic progenitors in the spine; altered Hedgehog signaling causes vertebral malformations and syndromic scoliosis. (PMID: 23620023)",
            "priority_score": "85",
            "justification": "Key transcriptional target and effector of cilia-dependent mechanosignaling."
        },
        {
            "gene_symbol": "HOXD13",
            "uniprot_id": "P31276",
            "organism": "Homo sapiens",
            "pathway_tags": "Somite,Segmentation,Development",
            "gravity_link": "Specifies regional identity along the anteroposterior and proximodistal axes, dictating structural properties of skeletal segments.",
            "spine_curvature_link": "Mutations cause synpolydactyly; Hoxd genes collectively pattern the lumbosacral spine, essential for weight-bearing structure. (PMID: 8782827)",
            "priority_score": "80",
            "justification": "Regulator of structural identity in the load-bearing lower spine."
        },
        {
            "gene_symbol": "LUM",
            "uniprot_id": "P51884",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Mechanotransduction,Collagen",
            "gravity_link": "Lumican regulates collagen fibril assembly and interfibrillar spacing, determining the macroscopic stiffness of tissues.",
            "spine_curvature_link": "Mice deficient in Lumican exhibit skin laxity and tendon fragility; alterations in SLRPs are associated with scoliotic connective tissue mechanics. (PMID: 9482755)",
            "priority_score": "82",
            "justification": "Determines spacing and stiffness of the load-bearing collagen network."
        },
        {
            "gene_symbol": "DIAPH1",
            "uniprot_id": "O60610",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Mechanotransduction,Actin",
            "gravity_link": "mDia1 nucleates actin filaments downstream of RhoA, driving the formation of stress fibers that resist mechanical load.",
            "spine_curvature_link": "Mutations cause auditory and skeletal defects; actin dynamics are essential for correct osteoblast mechanotransduction in the spine. (PMID: 20560208)",
            "priority_score": "82",
            "justification": "Effector of RhoA responsible for building the tension-resisting actin network."
        }
    ]

    existing_genes = set()
    with open(MASTER_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_genes.add(row['gene_symbol'])

    count = 0
    with open(MASTER_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["gene_symbol", "uniprot_id", "organism", "pathway_tags", "gravity_link", "spine_curvature_link", "priority_score", "justification"])
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
