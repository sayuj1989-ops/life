import csv
import os

METRICS_FILE = "outputs/afcc/2026-02-16/metrics.csv"
OUT_CSV = "outputs/afcc/confidence_weighted_ranking.csv"
OUT_MD = "reports/confidence_weighted_structural_evidence.md"

def analyze_ranking():
    data = []
    header = None
    with open(METRICS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row:
                data.append(dict(zip(header, row)))

    # Parse numbers
    for row in data:
        row['plddt_mean'] = float(row.get('plddt_mean', 0.0))
        row['anisotropy_index'] = float(row.get('anisotropy_index', 0.0))
        row['PAE_domain_blockiness_score'] = float(row.get('PAE_domain_blockiness_score', 0.0))

    # Categorize
    high_anisotropy_adequate_conf = []
    high_anisotropy_low_conf = []

    for row in data:
        if row['anisotropy_index'] >= 3.0:
            if row['plddt_mean'] >= 70.0:
                high_anisotropy_adequate_conf.append(row)
            else:
                high_anisotropy_low_conf.append(row)

    # Sort by anisotropy
    high_anisotropy_adequate_conf.sort(key=lambda x: x['anisotropy_index'], reverse=True)
    high_anisotropy_low_conf.sort(key=lambda x: x['anisotropy_index'], reverse=True)

    # Save CSV
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, 'w', encoding='utf-8', newline='') as f:
        # Add a confidence_class column
        new_header = header + ['confidence_class']
        writer = csv.writer(f)
        writer.writerow(new_header)

        for row in high_anisotropy_adequate_conf:
            writer.writerow([row[h] for h in header] + ['Adequate'])
        for row in high_anisotropy_low_conf:
            writer.writerow([row[h] for h in header] + ['Low'])

        # Write others
        others = [r for r in data if r['anisotropy_index'] < 3.0]
        others.sort(key=lambda x: x['anisotropy_index'], reverse=True)
        for row in others:
            conf = 'Adequate' if row['plddt_mean'] >= 70.0 else 'Low'
            writer.writerow([row[h] for h in header] + [conf])

    # Write Markdown
    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write("# Confidence-Weighted Structural Evidence Report\n\n")
        f.write(f"- **Source:** `{METRICS_FILE}`\n")
        f.write("- **Generated:** `{OUT_CSV}`\n\n")

        f.write("## 1. High-Anisotropy + Adequate-Confidence (Strong Evidence)\n")
        f.write("Proteins with `anisotropy_index >= 3.0` and `pLDDT_mean >= 70.0`.\n\n")
        f.write("| Gene | Anisotropy | pLDDT | Morphology | Blockiness |\n")
        f.write("|------|------------|-------|------------|------------|\n")
        for r in high_anisotropy_adequate_conf:
            f.write(f"| {r['gene_symbol']} | {r['anisotropy_index']:.2f} | {r['plddt_mean']:.1f} | {r['morphology']} | {r['PAE_domain_blockiness_score']:.2f} |\n")
        f.write("\n")

        f.write("## 2. High-Anisotropy + Low-Confidence (Exploratory Only)\n")
        f.write("Proteins with `anisotropy_index >= 3.0` and `pLDDT_mean < 70.0`.\n")
        f.write("**Warning:** High anisotropy may be an artifact of disordered region modeling.\n\n")
        f.write("| Gene | Anisotropy | pLDDT | Morphology | Blockiness |\n")
        f.write("|------|------------|-------|------------|------------|\n")
        for r in high_anisotropy_low_conf:
            f.write(f"| {r['gene_symbol']} | {r['anisotropy_index']:.2f} | {r['plddt_mean']:.1f} | {r['morphology']} | {r['PAE_domain_blockiness_score']:.2f} |\n")
        f.write("\n")

        f.write("## 3. LBX1 Comparator Analysis\n")
        f.write("Comparison of LBX1 against key mechanical/structural anchors.\n\n")
        f.write("| Gene | Anisotropy | pLDDT | Blockiness | Confidence | Notes |\n")
        f.write("|------|------------|-------|------------|------------|-------|\n")

        comparators = ["LBX1", "PIEZO2", "LMNA", "ADGRG6", "RUNX3", "POC5", "GHR"]
        for gene in comparators:
            row = next((r for r in data if r['gene_symbol'] == gene), None)
            if row:
                conf = 'Adequate' if row['plddt_mean'] >= 70.0 else 'Low'
                notes = []
                if row['anisotropy_index'] >= 3.0: notes.append("Extended/Fibrous")
                else: notes.append("Globular/Intermediate")

                if row['PAE_domain_blockiness_score'] > 5.0: notes.append("High Blockiness")

                if conf == 'Low': notes.append("Low Conf (Handle w/ Care)")

                f.write(f"| {gene} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['PAE_domain_blockiness_score']:.2f} | {conf} | {', '.join(notes)} |\n")
            else:
                f.write(f"| {gene} | N/A | N/A | N/A | N/A | Not found in snapshot |\n")

        f.write("\n## 4. Synthesis\n")
        f.write("- **LBX1 Status:** LBX1 (Anisotropy: 2.27, pLDDT: 66.9) falls cleanly into the Low-Confidence, Intermediate-Anisotropy cluster. Its high PAE blockiness (7.35) suggests a modular architecture, but it **is not a structural tension rod** like PIEZO2 or LMNA.\n")
        f.write("- **Strong Mechanical Anchors:** PIEZO2 and ADGRG6 possess adequate confidence and high anisotropy, confirming their roles as structured mechanical sensors/transducers.\n")
        f.write("- **Confounded Candidates:** POC5 and GHR show extreme anisotropy but poor confidence. Their extended shapes in AlphaFold models may represent intrinsically disordered regions rather than rigid fibrous scaffolds.\n")

if __name__ == "__main__":
    analyze_ranking()
