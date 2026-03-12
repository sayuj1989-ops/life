import os
import sys
import numpy as np
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    import elastica as ea
    from spinalmodes.countercurvature.pyelastica_bridge import (
        PYELASTICA_AVAILABLE,
        CounterCurvatureRodSystem,
        CounterCurvatureParams,
        InfoField1D
    )
except ImportError as e:
    print(f"Error importing simulation module: {e}")
    sys.exit(1)

if not PYELASTICA_AVAILABLE:
    print("PyElastica is not available. Exiting.")
    sys.exit(1)

def export_obj(filename, centerline, radius=0.015, num_segments=16):
    """
    Exports a 3D centerline to an OBJ file by generating a tube mesh around it.
    centerline: (N, 3) array of coordinates.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    N = centerline.shape[0]

    # Calculate tangents
    tangents = np.zeros_like(centerline)
    tangents[1:-1] = centerline[2:] - centerline[:-2]
    tangents[0] = centerline[1] - centerline[0]
    tangents[-1] = centerline[-1] - centerline[-2]

    # Normalize tangents
    norms = np.linalg.norm(tangents, axis=1)
    tangents = tangents / norms[:, np.newaxis]

    # Create an initial arbitrary normal vector
    up = np.array([0.0, 1.0, 0.0])
    if np.abs(np.dot(tangents[0], up)) > 0.99:
        up = np.array([1.0, 0.0, 0.0])

    n0 = np.cross(tangents[0], up)
    n0 = n0 / np.linalg.norm(n0)

    normals = np.zeros_like(centerline)
    normals[0] = n0

    # Parallel transport to get consistent normals
    for i in range(1, N):
        v = np.cross(tangents[i-1], tangents[i])
        if np.linalg.norm(v) < 1e-6:
            normals[i] = normals[i-1]
        else:
            angle = np.arccos(np.clip(np.dot(tangents[i-1], tangents[i]), -1.0, 1.0))
            # Rodrigues rotation formula around v
            k = v / np.linalg.norm(v)
            n_prev = normals[i-1]
            normals[i] = n_prev * np.cos(angle) + np.cross(k, n_prev) * np.sin(angle) + k * np.dot(k, n_prev) * (1 - np.cos(angle))
            normals[i] = normals[i] / np.linalg.norm(normals[i])

    binormals = np.cross(tangents, normals)

    # Generate vertices
    vertices = []
    for i in range(N):
        center = centerline[i]
        for j in range(num_segments):
            angle = 2.0 * np.pi * j / num_segments
            pos = center + radius * (np.cos(angle) * normals[i] + np.sin(angle) * binormals[i])
            vertices.append(pos)

    # Generate faces
    faces = []
    for i in range(N - 1):
        for j in range(num_segments):
            v1 = i * num_segments + j + 1
            v2 = i * num_segments + (j + 1) % num_segments + 1
            v3 = (i + 1) * num_segments + j + 1
            v4 = (i + 1) * num_segments + (j + 1) % num_segments + 1

            # Quads as two triangles
            faces.append((v1, v2, v3))
            faces.append((v2, v4, v3))

    with open(filename, 'w') as f:
        f.write(f"# Spine exported by Jules\n")
        f.write(f"o Spine\n")
        for v in vertices:
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        for face in faces:
            f.write(f"f {face[0]} {face[1]} {face[2]}\n")

    print(f"Exported {filename} with {len(vertices)} vertices and {len(faces)} faces.")


def run_simulation(active_curvature, anisotropy, gravity, initial_lateral_defect, length=0.4):
    n_elements = 60 # Higher resolution for smoother 3D objects
    dt = 1e-4
    duration = 2.0

    chi_kappa = active_curvature * 5.0

    s = np.linspace(0, length, n_elements + 1)
    info_center = 0.5 * length
    info_width = 0.1 * length
    I = 0.5 + 0.5 * np.exp(-0.5 * ((s - info_center) / info_width)**2)
    dIds = np.gradient(I, s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    params = CounterCurvatureParams(
        chi_kappa=chi_kappa,
        chi_tau=0.0,
        chi_E=0.0,
        chi_M=0.0,
        scale_length=length
    )

    kappa_gen = np.zeros((3, n_elements + 1))
    kappa_gen[1, :] = 2.5 # base kyphosis
    kappa_gen[0, :] = initial_lateral_defect

    rod_system = CounterCurvatureRodSystem.from_iec(
        info=info,
        params=params,
        length=length,
        n_elements=n_elements,
        kappa_gen=kappa_gen,
        stiffness_anisotropy=anisotropy,
        E0=1e6,
        radius=0.015, # Use same radius as export
        rho=1000.0,
    )

    class BasicSystem(ea.BaseSystemCollection, ea.Constraints, ea.Forcing, ea.Damping, ea.CallBacks):
        pass

    system = BasicSystem()
    system.append(rod_system.rod)

    # Base fixed (sacrum)
    system.constrain(rod_system.rod).using(
        ea.OneEndFixedBC,
        constrained_position_idx=(0,),
        constrained_director_idx=(0,)
    )

    # Gravity pointing "down" along the initial rod axis Z
    if gravity > 0.0:
        system.add_forcing_to(rod_system.rod).using(
            ea.GravityForces, acc_gravity=np.array([0.0, 0.0, -gravity])
        )

    system.dampen(rod_system.rod).using(ea.AnalyticalLinearDamper, damping_constant=0.5, time_step=dt)

    system.finalize()
    timestepper = ea.PositionVerlet()
    ea.integrate(timestepper, system, duration, int(duration/dt), progress_bar=False)

    return rod_system.rod.position_collection.copy().T


def run_experiments():
    out_dir = "outputs/3d_models"
    os.makedirs(out_dir, exist_ok=True)

    print("Running Healthy Spine (S-Curve) simulation...")
    centerline = run_simulation(active_curvature=2.5, anisotropy=3.0, gravity=9.81, initial_lateral_defect=0.0)
    export_obj(os.path.join(out_dir, "spine_healthy.obj"), centerline)

    print("\nRunning Scoliosis (Metabolic Buckling) simulation...")
    # Low anisotropy (energy deficit proxy), high active curvature driving instability
    centerline = run_simulation(active_curvature=4.0, anisotropy=1.5, gravity=9.81, initial_lateral_defect=0.1)
    export_obj(os.path.join(out_dir, "spine_scoliosis.obj"), centerline)

    print("\nRunning Microgravity (Spinal Jetlag) simulation...")
    # High active curvature, zero gravity
    centerline = run_simulation(active_curvature=2.5, anisotropy=3.0, gravity=0.0, initial_lateral_defect=0.0)
    export_obj(os.path.join(out_dir, "spine_microgravity.obj"), centerline)

if __name__ == "__main__":
    run_experiments()
