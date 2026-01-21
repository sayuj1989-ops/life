import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import os

# --- Constants & Parameters ---
L = 0.7  # Length of spine (m)
N = 50   # Number of segments
DS = L / N
EI_0 = 1.0  # Bending stiffness (N*m^2)
RHO = 2.0   # Linear density (kg/m)
G = 9.81    # Gravity (m/s^2)

# --- Helper Functions ---

def reconstruct_shape(thetas):
    """
    Integrates angles to get (x, y) coordinates.
    thetas: array of N angles (radians) relative to horizontal.
    Assumes fixed base at (0,0).
    """
    x = np.zeros(N + 1)
    y = np.zeros(N + 1)
    
    # Cumulative sum to get positions
    # x[i] is position of node i. Segment i connects node i and i+1.
    # Actually, let's say theta[i] is angle of segment i (between node i and i+1)
    
    dx = DS * np.cos(thetas)
    dy = DS * np.sin(thetas)
    
    x[1:] = np.cumsum(dx)
    y[1:] = np.cumsum(dy)
    
    return x, y

def total_energy(thetas, kappa0_func):
    """
    Calculates Total Potential Energy = Elastic + Gravitational
    """
    # 1. Curvature calculation: kappa ~ d(theta)/ds
    # Forward difference for curvature between segments
    # kappa[i] corresponds to junction between segment i and i+1
    d_theta = np.diff(thetas)
    kappa = d_theta / DS 
    
    # Get rest curvature at these junctions
    s_junctions = np.linspace(DS, L-DS, N-1)
    k0 = kappa0_func(s_junctions)
    
    # Elastic Energy: Integral 1/2 EI (k - k0)^2 ds
    # We sum over the N-1 internal nodes
    e_bend = np.sum(0.5 * EI_0 * (kappa - k0)**2 * DS)
    
    # 2. Gravitational Potential Energy: Integral rho * g * y ds
    # We need height of each mass element. Let's use midpoint of segments.
    x_nodes, y_nodes = reconstruct_shape(thetas)
    y_mid = 0.5 * (y_nodes[:-1] + y_nodes[1:])
    
    e_grav = np.sum(RHO * G * y_mid * DS)
    
    return e_bend + e_grav

# --- Gene / Control Functions ---

def kappa0_passive(s):
    """No intrinsic curvature (Straight rod)"""
    return np.zeros_like(s)

def kappa0_antigravity(s):
    """
    A simple programmed curvature to resist gravity.
    For a cantilever, curvature needs to increase towards the base?
    Actually, to be 'upright', we might want an S-curve or just a simple curve.
    Let's try a constant curvature that essentially makes it a part of a circle 
    bending 'backwards' against gravity.
    """
    # Negative curvature bends "back" (if gravity is down -y and we start vertical)
    # Let's verify coordinates later.
    return 2.0 * np.ones_like(s) # Curve Up (Positive curvature) 

def kappa0_humanoid(s):
    """
    Approximation of Lordosis (lumbar) and Kyphosis (thoracic).
    s=0 is base (Sacrum). s=L is head.
    Low s -> Lumbar (Lordosis, extends back).
    High s -> Thoracic (Kyphosis, flexes forward).
    """
    # Normalize s
    sn = s / L 
    # Sinusoidal pattern: Negative (Lordosis) then Positive (Kyphosis)
    amplitude = 5.0
    return amplitude * np.sin(2 * np.pi * sn + np.pi) # Phase shift to start negative

# --- Simulation Logic ---

def solve_shape(kappa0_f, label):
    # Initial guess: Horizontal (theta = 0)
    x0 = np.zeros(N)
    
    # Constraint: Base segment is fixed vertical? 
    # Or purely energy minimization with penalties?
    # Let's fix the first segment to be vertical (theta[0] = pi/2)
    # Constraints dictionary for scipy.minimize is usually for strict equality
    
    cons = ({'type': 'eq', 'fun': lambda t: t[0]}) # Theta[0] = 0
    
    # Optimization
    res = minimize(total_energy, x0, args=(kappa0_f,), 
                   constraints=cons, method='SLSQP', options={'ftol': 1e-9})
    
    if not res.success:
        print(f"Warning: Optimization failed for {label}: {res.message}")
        
    return res.x

# --- Main Execution ---

if __name__ == "__main__":
    print("Running Biological Counter-Curvature Toy Model...")
    
    # 1. Passive Case (Dead Fish)
    theta_passive = solve_shape(kappa0_passive, "Passive")
    x_p, y_p = reconstruct_shape(theta_passive)
    
    # 2. Antigravity Case (Simple constant counter-torque)
    theta_anti = solve_shape(kappa0_antigravity, "Constant Counter")
    x_a, y_a = reconstruct_shape(theta_anti)
    
    # 3. Humanoid Case (S-Curve)
    theta_human = solve_shape(kappa0_humanoid, "Humanoid gene-field")
    x_h, y_h = reconstruct_shape(theta_human)

    # --- Plotting ---
    plt.figure(figsize=(10, 8))
    
    # Plot Passive
    plt.plot(x_p, y_p, 'r--', linewidth=2, label='Passive (Dead Genetics)')
    plt.scatter(x_p[-1], y_p[-1], color='red', s=50)
    
    # Plot Antigravity
    plt.plot(x_a, y_a, 'g-', linewidth=2, label='Simple Counter-Curvature')
    plt.scatter(x_a[-1], y_a[-1], color='green', s=50)
    
    # Plot Humanoid
    plt.plot(x_h, y_h, 'b-', linewidth=3, label='Humanoid (S-Curve Code)')
    plt.scatter(x_h[-1], y_h[-1], color='blue', s=50)
    
    # Reference Gravity Vector
    plt.arrow(0.2, 0.5, 0, -0.1, head_width=0.02, color='black')
    plt.text(0.22, 0.45, "g = 9.8 m/s²")
    
    plt.axhline(0, color='k', linestyle=':', label='Ground')
    plt.axvline(0, color='k', linestyle=':')
    
    plt.title("Biological Counter-Curvature: Horizontal Cantilever (Quadruped)")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.legend()
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    
    # Save
    output_path = "figures/toy_model_results.png"
    plt.savefig(output_path, dpi=150)
    print(f"Figure saved to {os.path.abspath(output_path)}")
    
    # Numerical validation output
    tip_height_p = y_p[-1]
    tip_height_a = y_a[-1]
    print(f"\n--- Metrics ---")
    print(f"Passive Tip Height: {tip_height_p:.3f} m")
    print(f"Antigravity Tip Height: {tip_height_a:.3f} m")
    
    if tip_height_a > tip_height_p:
        print("RESULT: Antigravity is EFFECTIVE (Maintains better height)")
    else:
        print("RESULT: Antigravity FAILED")
