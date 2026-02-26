import pandas as pd
import re
from pathlib import Path

CSV_FILE = Path("outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv")
NOTE_FILE = Path("notes/evidence/2026-02-07__thermodynamic_cost_proteins.md")

TERMS = {
    "eta_p": "## Proprioceptive Feedback Cost (η_p)",
    "eta_a": "## Active Moment Maintenance (η_a)",
    "Gamma_m": "## Basal Tissue Maintenance (Γ_m)"
}

def generate_table(df):
    lines = []
    lines.append("| Gene | UniProt | Anisotropy | Morphology | Rg (Å) | pLDDT | Res | Hinges | L-Scaling | Role |")
    lines.append("| :--- | :--- | ---: | :--- | ---: | ---: | ---: | ---: | :--- | :--- |")

    for _, row in df.iterrows():
        # Format numbers
        aniso = f"{row['anisotropy']:.2f}"
        rg = f"{row['rg']:.1f}"
        plddt = f"{row['plddt_mean']:.1f}"
        res = int(row['n_residues'])
        hinges = int(row['hinge_candidates'])

        line = f"| **{row['gene']}** | {row['uniprot']} | {aniso} | {row['morphology']} | {rg} | {plddt} | {res} | {hinges} | {row['scaling']} | {row['role']} |"
        lines.append(line)

    return "\n".join(lines)

def generate_summary(df):
    mean_aniso = df['anisotropy'].mean()
    min_rg = df['rg'].min()
    max_rg = df['rg'].max()
    mean_plddt = df['plddt_mean'].mean()
    total_res = df['n_residues'].sum()
    total_hinges = df['hinge_candidates'].sum()

    return f"**Structural summary:** Mean anisotropy = **{mean_aniso:.2f}**, Rg range = {min_rg:.0f}–{max_rg:.0f} Å, Mean pLDDT = {mean_plddt:.1f}, Total residues = {total_res}, Total hinges = {total_hinges}"

def main():
    if not CSV_FILE.exists():
        print("CSV file not found")
        return

    df = pd.read_csv(CSV_FILE)

    with open(NOTE_FILE, 'r') as f:
        content = f.read()

    summary_stats = {}

    for term_code, section_header in TERMS.items():
        term_df = df[df['term'] == term_code]
        if term_df.empty:
            continue

        # Sort by something? Maybe Gene name or just keep as is?
        # Typically sorted by Anisotropy or relevance. Let's sort by Anisotropy descending for tables
        # But wait, existing tables are not strictly sorted.
        # Let's keep existing order if possible, or sort by Gene.
        # Let's sort by Anisotropy desc to highlight structural cost.
        # Wait, the prompt didn't specify sorting.
        # I'll sort by Anisotropy desc as it's a "cost" metric.
        # Actually, let's stick to the CSV order but the CSV was appended.
        # Let's look at the existing file. It seems somewhat sorted by anisotropy or grouped.
        # I'll sort by Anisotropy descending.

        # Exception: For eta_p, PIEZO2 is first.
        # I'll rely on Anisotropy Descending.

        # term_df = term_df.sort_values('anisotropy', ascending=False)
        # Actually, let's preserve the manual order if possible? Too hard.
        # I will simply append the new ones to the end if I were editing manually, but generating fresh table is cleaner.
        # Sorting by Anisotropy is a good default for this context.

        new_table = generate_table(term_df)
        new_summary = generate_summary(term_df)

        summary_stats[term_code] = term_df['anisotropy'].mean()

        # Regex to replace table and summary
        # Pattern: header -> newline -> ... -> table end -> newline -> **Structural summary:** ... -> newline

        # Find start of section
        start_idx = content.find(section_header)
        if start_idx == -1:
            print(f"Section {section_header} not found")
            continue

        # Find the table start (first | after header)
        table_start_match = re.search(r"\| Gene \|", content[start_idx:])
        if not table_start_match:
            print(f"Table start not found in {section_header}")
            continue

        abs_table_start = start_idx + table_start_match.start()

        # Find end of table/summary block
        # We look for "### Thermodynamic Predictions" which follows the summary
        next_section_match = re.search(r"### Thermodynamic Predictions", content[abs_table_start:])

        if not next_section_match:
            print(f"End of section not found for {section_header}")
            continue

        abs_end = abs_table_start + next_section_match.start()

        # Construct replacement block
        # We need to preserve the text before the table
        # Actually, we replace from table start to before "### Thermodynamic Predictions"

        replacement = f"{new_table}\n\n{new_summary}\n\n"

        content = content[:abs_table_start] + replacement + content[abs_end:]
        print(f"Updated section {term_code}")

    # Update Synthesis Table
    synthesis_header = "## Synthesis: The Energy Deficit Window — A Molecular View"
    synth_start = content.find(synthesis_header)
    if synth_start != -1:
        # Find the table
        table_match = re.search(r"\| Term \| Mean Anisotropy \|", content[synth_start:])
        if table_match:
            table_start = synth_start + table_match.start()
            # Find end of table (double newline)
            table_end_match = re.search(r"\n\n", content[table_start:])
            if table_end_match:
                table_end = table_start + table_end_match.start()

                # Regenerate synthesis table
                synth_lines = []
                synth_lines.append("| Term | Mean Anisotropy | Structural Signature | Scaling |")
                synth_lines.append("| :--- | ---: | :--- | :--- |")

                # Hardcoded signatures/scaling based on existing file content I read earlier
                # eta_p (Sensing) | 3.22 | Extended sensors (PIEZO1/2) + disordered TFs (EGR3, RUNX3) | L to L²
                # eta_a (Actuation) | 3.39 | Fibrous scaffolds (LMNA) + crosslinkers (FLNA) + strain gauges (VIM) | L² to L³
                # Gamma_m (Maintenance) | 2.47 | Compact enzymes (SIRT1) + ECM (COL1A1) + morphogens (SHH) | L to L³

                # I will update the Mean Anisotropy values
                # And maybe signatures if I added new proteins?
                # DMD (globular), MYLK (globular) -> eta_a. Might lower mean anisotropy.
                # PPARGC1A (intermediate), etc -> Gamma_m.

                # I'll keep signatures text static for now unless I want to get fancy.
                # But Mean Anisotropy MUST be updated.

                row_p = f"| **η_p** (Sensing) | {summary_stats.get('eta_p', 0):.2f} | Extended sensors (PIEZO1/2) + disordered TFs (EGR3, RUNX3) | L to L² |"
                row_a = f"| **η_a** (Actuation) | {summary_stats.get('eta_a', 0):.2f} | Fibrous scaffolds (LMNA) + crosslinkers (FLNA) + strain gauges (VIM) | L² to L³ |"
                row_m = f"| **Γ_m** (Maintenance) | {summary_stats.get('Gamma_m', 0):.2f} | Compact enzymes (SIRT1) + ECM (COL1A1) + morphogens (SHH) | L to L³ |"

                new_synth_table = "\n".join([synth_lines[0], synth_lines[1], row_p, row_a, row_m])

                content = content[:table_start] + new_synth_table + content[table_end:]
                print("Updated Synthesis table")

    with open(NOTE_FILE, 'w') as f:
        f.write(content)
    print(f"Saved {NOTE_FILE}")

if __name__ == "__main__":
    main()
