import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os
import sys

def parse_obj(filename):
    vertices = []
    faces = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == 'v':
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif parts[0] == 'f':
                # OBJ indices are 1-based
                faces.append([int(parts[1]) - 1, int(parts[2]) - 1, int(parts[3]) - 1])
    return vertices, faces

def plot_spine(ax, vertices, faces, title, color):
    # Convert lists to usable format
    mesh_faces = [[vertices[idx] for idx in face] for face in faces]

    # Create 3D polygon collection
    collection = Poly3DCollection(mesh_faces, facecolors=color, linewidths=0.1, edgecolors='k', alpha=0.9)
    ax.add_collection3d(collection)

    # Find bounding box
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]

    max_range = max(max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs)) / 2.0
    mid_x = (max(xs)+min(xs)) * 0.5
    mid_y = (max(ys)+min(ys)) * 0.5
    mid_z = (max(zs)+min(zs)) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    ax.set_title(title, pad=20)
    ax.set_xlabel('X (Lateral)')
    ax.set_ylabel('Y (A-P)')
    ax.set_zlabel('Z (Axial)')

    # View angle to best show the curves
    ax.view_init(elev=20, azim=45)

def main():
    out_dir = "outputs/3d_models"
    files = {
        "Healthy (S-Curve)": ("spine_healthy.obj", "skyblue"),
        "Scoliosis (Metabolic Buckling)": ("spine_scoliosis.obj", "salmon"),
        "Microgravity (Spinal Jetlag)": ("spine_microgravity.obj", "lightgreen")
    }

    fig = plt.figure(figsize=(15, 6))

    for i, (title, (filename, color)) in enumerate(files.items()):
        filepath = os.path.join(out_dir, filename)
        if not os.path.exists(filepath):
            print(f"Error: Could not find {filepath}. Have you run export script?")
            sys.exit(1)

        print(f"Parsing {filename}...")
        vertices, faces = parse_obj(filepath)

        ax = fig.add_subplot(1, 3, i + 1, projection='3d')
        print(f"Plotting {title}...")
        plot_spine(ax, vertices, faces, title, color)

    plt.tight_layout()
    output_png = os.path.join(out_dir, "spines_comparison_3d.png")
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    print(f"Saved visualization to {output_png}")

if __name__ == "__main__":
    main()
