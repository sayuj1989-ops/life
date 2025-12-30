import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import os

# --- 1. Load Bio-Parameters ---
def load_gene_params(csv_path="models/gene_mechanics_params.csv"):
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: {csv_path} not found. Run alphafold_analysis/map_structure_to_param.py first.")
        return None
        
    params = {}
    
    # Extract specific values for the "Global" material model
    # We take weighted averages or dominant components
    
    # 1. Stiffness (EI) - Driven by Collagen (COL2A1)
    col_row = df[df['Gene'] == 'COL2A1'].iloc[0]
    params['EI_BASE'] = col_row['Param_EI_Component'] * 2.0 # Scale up for physics
    
    # 2. Feedback Gain (G_mech) - Driven by Piezo (PIEZO1)
    # How much does stress affect growth?
    piezo_row = df[df['Gene'] == 'PIEZO1'].iloc[0]
    params['GAIN_MECH'] = piezo_row['Param_Growth_Tensor'] * 0.5
    
    # 3. Asymmetry/Initial Twist - Driven by Dynein (DNAH5)
    dnah_row = df[df['Gene'] == 'DNAH5'].iloc[0]
    params['EPSILON'] = dnah_row['Param_Epsilon']
    
    # 4. Volumetric Expansion - Driven by Aggrecan
    # Helps resist compression
    acan_row = df[df['Gene'] == 'ACAN'].iloc[0]
    params['GROWTH_RATE'] = acan_row['Param_Growth_Tensor'] * 0.1
    
    print("--- Loaded Genetic Parameters ---")
    for k, v in params.items():
        print(f"{k}: {v:.4f}")
    return params

# --- 2. Physics Engine (Quasi-Static Rod) ---

L = 1.0
N = 40
DS = L / N
RHO = 5.0
G_CONST = 9.81

def reconstruct_shape(thetas):
    x = np.zeros(N + 1)
    y = np.zeros(N + 1)
    dx = DS * np.cos(thetas)
    dy = DS * np.sin(thetas)
    x[1:] = np.cumsum(dx)
    y[1:] = np.cumsum(dy)
    return x, y

def total_energy(thetas, kappa0_current, EI):
    # Curvature
    d_theta = np.diff(thetas)
    kappa = d_theta / DS 
    # Interpolate k0 to junctions (approx)
    # kappa0_current is length N-1
    
    # Elastic Energy
    e_bend = np.sum(0.5 * EI * (kappa - kappa0_current)**2 * DS)
    
    # Gravitational Potential (Upright Column)
    x_nodes, y_nodes = reconstruct_shape(thetas)
    y_mid = 0.5 * (y_nodes[:-1] + y_nodes[1:])
    e_grav = np.sum(RHO * G_CONST * y_mid * DS)
    
    return e_bend + e_grav

def solve_equilibrium(kappa0, EI, prev_solution=None):
    if prev_solution is None:
        x0 = np.ones(N) * (np.pi / 2 - 0.01) # Near vertical
    else:
        x0 = prev_solution
        
    # Boundary condition: Base is vertical
    cons = ({'type': 'eq', 'fun': lambda t: t[0] - np.pi/2})
    
    res = minimize(total_energy, x0, args=(kappa0, EI), 
                   constraints=cons, method='SLSQP', options={'ftol': 1e-6, 'disp': False})
    return res.x

# --- 3. Growth & Development Loop ---

def simulate_development(params, genotype_name="Wild Type"):
    """
    Simulates growth from T=0 (Infant) to T=Final.
    """
    print(f"\nStarting Simulation: {genotype_name}")
    
    TIME_STEPS = 20
    DT = 1.0
    
    # Initial State: "Infant Kyphosis" (C-shape)
    # kappa0 starts slightly positive (kyphotic/fetal) everywhere
    current_kappa0 = np.ones(N-1) * 1.0 
    
    # Target State: "Adult S-Curve" (Genetic Blueprint)
    # Lumbar Lordosis (negative) at bottom, Thoracic Kyphosis (positive) at top
    s_axis = np.linspace(0, L, N-1)
    target_kappa0 = 5.0 * np.sin(2 * np.pi * s_axis / L + np.pi) # S-shape
    
    # Storage
    shapes = []
    
    # Initial Solution
    current_thetas = solve_equilibrium(current_kappa0, params['EI_BASE'])
    
    for t in range(TIME_STEPS):
        # A. Solve Mechanics (Fast timescale)
        current_thetas = solve_equilibrium(current_kappa0, params['EI_BASE'], prev_solution=current_thetas)
        
        # B. Measure Biomechanical State
        d_theta = np.diff(current_thetas)
        current_curvature = d_theta / DS
        
        # C. Update Biology (Slow timescale - Growth Law)
        # dK0/dt = GeneticProgram + Feedback * (Error)
        
        # 1. Genetic Drive: Pushing towards the "Adult Target"
        growth_drive = 0.2 * (target_kappa0 - current_kappa0)
        
        # 2. Mechanosensing (Heuter-Volkmann-ish)
        # If curvature is too high (compression), reduce growth? 
        # Simplified: Stability feedback. If we are buckling away from 0 curvature, resist?
        # Actually, let's say feedback tries to minimize strain energy: move k0 towards k_actual
        # This is "Plasticity". High feedback means the bone remodels to the load.
        # Low feedback means it stays rigid to the blueprint.
        
        plastic_feedback = params['GAIN_MECH'] * (current_curvature - current_kappa0)
        
        # Update
        current_kappa0 += (growth_drive + plastic_feedback) * DT
        
        # Store for plotting
        if t % 4 == 0 or t == TIME_STEPS - 1:
            x, y = reconstruct_shape(current_thetas)
            shapes.append((t, x, y))
            
    return shapes

# --- 4. Main & Visualization ---

if __name__ == "__main__":
    # Load constraints
    base_params = load_gene_params()
    
    if base_params:
        # Scenario 1: Healthy
        res_healthy = simulate_development(base_params, "Healthy (Wild Type)")
        
        # Scenario 2: Pathological (Low Stiffness - e.g., EDS/Collagen Mut)
        mutant_params = base_params.copy()
        mutant_params['EI_BASE'] *= 0.3 # Weak Connective Tissue
        res_weak = simulate_development(mutant_params, "Mutant (Low Stiffness)")
        
        # Scenario 3: Bad Feedback (Piezo Loss)
        neu_params = base_params.copy()
        neu_params['GAIN_MECH'] = 0.0 # No mechanosensing
        res_no_sense = simulate_development(neu_params, "Mutant (No Feedback)")

        # --- Plotting ---
        fig, axes = plt.subplots(1, 3, figsize=(18, 8), sharey=True)
        
        scenarios = [
            (res_healthy, "Healthy\n(Stable S-Curve)", axes[0]),
            (res_weak, "Low Stiffness\n(Collagen Defect -> Collapse)", axes[1]),
            (res_no_sense, "No Feedback\n(Piezo Defect -> Rigid/Deviant)", axes[2])
        ]
        
        for res, title, ax in scenarios:
            colors = plt.cm.viridis(np.linspace(0, 1, len(res)))
            for i, (t, x, y) in enumerate(res):
                alpha = 0.3 if i < len(res)-1 else 1.0
                width = 1 if i < len(res)-1 else 3
                label = f"T={t}" if i == 0 or i == len(res)-1 else None
                ax.plot(x, y, color=colors[i], alpha=alpha, linewidth=width, label=label)
                ax.scatter(x[-1], y[-1], color=colors[i], s=20)
                
            ax.set_title(title, fontsize=14)
            ax.set_xlabel("X (m)")
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3)
            ax.axvline(0, linestyle=':', color='k')
            
        axes[0].set_ylabel("Z (m) - Vertical Height")
        plt.suptitle("Biological Counter-Curvature: Developmental Trajectories", fontsize=16)
        
        out_path = "figures/developmental_trajectory.png"
        plt.savefig(out_path, dpi=150)
        print(f"Simulation visualizations saved to {out_path}")
