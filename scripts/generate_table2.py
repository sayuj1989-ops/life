import pandas as pd

# List of requested proteins
requested_proteins = [
    "PIEZO2", "PIEZO1", "EGR3", "RUNX3", "NTRK3",
    "VIM", "LMNA", "CAV1", "FLNA", "LBX1",
    "COL1A1", "COMP", "SIRT1", "SOX9", "SHH", "CDKN1A"
]

# Mapping for terms to LaTeX symbols
term_map = {
    "eta_p": "$\\eta_p$",
    "eta_a": "$\\eta_a$",
    "Gamma_m": "$\\Gamma_m$"
}

# Mapping for specific formatting if needed (e.g. L-Scaling)
# I'll try to infer L-scaling or leave it if not in CSV (it is in CSV)

def main():
    try:
        df = pd.read_csv('outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv')
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return

    # Filter
    df_filtered = df[df['gene'].isin(requested_proteins)].copy()

    # Check for missing
    found = df_filtered['gene'].tolist()
    missing = set(requested_proteins) - set(found)
    if missing:
        print(f"Warning: Missing proteins in CSV: {missing}")

    # Sort by Term (eta_p, eta_a, Gamma_m) then Anisotropy (descending)
    # Custom sort for term
    term_order = ["eta_p", "eta_a", "Gamma_m"]
    df_filtered['term_rank'] = df_filtered['term'].apply(lambda x: term_order.index(x) if x in term_order else 99)
    df_filtered = df_filtered.sort_values(by=['term_rank', 'anisotropy'], ascending=[True, False])

    # Generate LaTeX rows
    print("\\begin{tabular}{llcclllc}")
    print("\\toprule")
    print("\\textbf{Gene} & \\textbf{UniProt} & \\textbf{Dissipation Term} & \\textbf{Anisotropy} & \\textbf{Morphology} & \\textbf{pLDDT} & \\textbf{Residues} & \\textbf{L-Scaling} \\\\")
    print("\\midrule")

    current_term = None
    for _, row in df_filtered.iterrows():
        term_sym = term_map.get(row['term'], row['term'])

        # Section headers
        if row['term'] != current_term:
            if row['term'] == 'eta_p':
                print("\\multicolumn{8}{l}{\\textit{Proprioceptive Channel Anchors ($\\eta_p$)}} \\\\")
            elif row['term'] == 'eta_a':
                print("\\multicolumn{8}{l}{\\textit{Active Maintenance Anchors ($\\eta_a$)}} \\\\")
            elif row['term'] == 'Gamma_m':
                print("\\multicolumn{8}{l}{\\textit{Metabolic Supply Scaling ($\\Gamma_m$)}} \\\\")
            current_term = row['term']

        # Format values
        gene = row['gene']
        uniprot = row['uniprot']
        ani = f"{row['anisotropy']:.2f}"
        morph = row['morphology'] if pd.notna(row['morphology']) else "N/A"
        # Simplify morphology: "Fibrous/Extended" -> "Fibrous" or "Extended" ?
        # The existing table uses "Fibrous", "Extended", "Intermediate".
        # I'll keep it as is or truncate if too long.
        # "Fibrous/Extended" is fine.

        plddt = f"{row['plddt_mean']:.1f}"
        res = int(row['n_residues'])
        scaling = row['scaling'] if pd.notna(row['scaling']) else ""
        # Clean scaling text (e.g. "L (sensor density...)" -> "$L$")
        if "L^3" in scaling: scaling_short = "$L^3$"
        elif "L^2" in scaling: scaling_short = "$L^2$"
        elif "L" in scaling: scaling_short = "$L$"
        elif "constant" in scaling: scaling_short = "Const"
        elif "threshold" in scaling: scaling_short = "Switch"
        else: scaling_short = "-"

        print(f"{gene} & {uniprot} & {term_sym} & {ani} & {morph} & {plddt} & {res} & {scaling_short} \\\\")

    print("\\bottomrule")
    print("\\end{tabular}")

if __name__ == "__main__":
    main()
