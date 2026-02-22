
try:
    import elastica as ea
    import numpy as np
    print("Elastica imported successfully.")

    # Try to instantiate a rod to be sure
    rod = ea.CosseratRod.straight_rod(
        n_elements=10,
        start=np.array([0.0, 0.0, 0.0]),
        direction=np.array([0.0, 0.0, 1.0]),
        normal=np.array([0.0, 1.0, 0.0]),
        base_length=1.0,
        base_radius=0.01,
        density=1000,
        youngs_modulus=1e6,
    )
    print("Rod created successfully.")
except ImportError:
    print("Elastica not installed.")
except Exception as e:
    print(f"Error: {e}")
