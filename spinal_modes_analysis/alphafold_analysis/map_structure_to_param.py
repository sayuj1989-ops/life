import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. Mock Data Generator (Simulation of AlphaFold Analysis) ---
# In a real scenario, this would import 'analyze_structures.py' and parse actual PDBs.
# Here, we simulate the *outputs* of that analysis for our specific gene list.

def get_simulated_protein_data():
    """
    Returns a DataFrame of simulated structural metrics for key 'Antigravity' proteins.
    Metrics:
    - helicity: Fraction of residues in alpha-helices (Stiffness proxy)
    - disorder: Fraction of disordered residues (Flexibility/Signaling proxy)
    - asymmetry: Chirality metric (Motor strength proxy)
    - hydrophobicity: GRAVY score (Core stability)
    """
    data = {
        "Gene": ["COL2A1", "ACAN", "DNAH5", "HOXA10", "PIEZO1"],
        "Protein": ["Collagen II", "Aggrecan", "Dynein HC", "HOX A10", "Piezo1"],
        "Helicity": [0.95, 0.10, 0.40, 0.60, 0.70],  # Collagen is a triple helix (modeled as high order)
        "Disorder": [0.02, 0.80, 0.10, 0.30, 0.15],  # Aggrecan is highly disordered/glycosylated
        "Asymmetry": [0.01, 0.05, 0.95, 0.10, 0.40], # Dynein is the chiral motor
        "BetaSheet": [0.0, 0.05, 0.30, 0.05, 0.10],
        "BuriedSurface": [0.8, 0.2, 0.7, 0.6, 0.5]
    }
    return pd.DataFrame(data)

# --- 2. Transfer Functions (The Biological Counter-Curvature Logic) ---

def map_to_mechanics(df):
    """
    Maps structural metrics to Macroscopic Mechanical Parameters.
    
    1. Stiffness (EI): Proportional to Helicity and BuriedSurface (Packing).
    2. Torsion/Chirality (epsilon): Proportional to Asymmetry * MotorPotential.
    3. Growth Gain (G): Proportional to Disorder (Interaction surface) and Hydrophilicity.
    4. Rest Curvature (kappa0_reliability): Inverse of Disorder (Binding precision).
    """
    
    # Mechanical Stiffness EI (Normalized 0-1)
    # Collagen (COL2A1) should be max.
    df['Param_EI_Component'] = (df['Helicity'] * 2.0 + df['BuriedSurface']) / 3.0
    
    # Symmetry Breaking Parameter epsilon
    # DNAH5 should be max.
    df['Param_Epsilon'] = df['Asymmetry']
    
    # Elastic Stability of Gene Expression (Kappa0 Precision)
    # HOX genes need high precision -> Low disorder in binding domain.
    # Note: Full protein might have IDRs, but here we model the generic relationship.
    df['Param_Kappa_Precision'] = 1.0 - df['Disorder']
    
    # Volume/Growth Potential (swelling)
    # Aggrecan (ACAN) should be high -> High Disoder/Surface area for GAGs
    df['Param_Growth_Tensor'] = df['Disorder'] + (1.0 - df['BuriedSurface'])
    
    return df

# --- 3. Visualization & Output ---

def generate_mapping_report(df):
    print("--- AlphaFold to Mechanics Map ---")
    print(df[['Gene', 'Protein', 'Param_EI_Component', 'Param_Epsilon', 'Param_Growth_Tensor']].round(3))
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    params = ['Param_EI_Component', 'Param_Epsilon', 'Param_Growth_Tensor']
    x = np.arange(len(df))
    width = 0.25
    
    for i, col in enumerate(params):
        ax.bar(x + i*width, df[col], width, label=col)
        
    ax.set_xticks(x + width)
    ax.set_xticklabels(df['Gene'])
    ax.set_ylabel("Normalized Parameter Value (0-1)")
    ax.set_title("Gene-to-Mechanics Transfer Function")
    ax.legend()
    
    output_path = "figures/structure_param_map.png"
    plt.savefig(output_path, dpi=150)
    print(f"\nFigure saved to {os.path.abspath(output_path)}")

if __name__ == "__main__":
    df = get_simulated_protein_data()
    df_mapped = map_to_mechanics(df)
    generate_mapping_report(df_mapped)
    
    # Save CSV for the main model to consume
    df_mapped.to_csv("models/gene_mechanics_params.csv", index=False)
    print("Parameters saved to models/gene_mechanics_params.csv")
