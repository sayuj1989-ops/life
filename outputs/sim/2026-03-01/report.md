# Weekly Simulation: Growth S-Shape Emergence

## What Changed
In this parameter sweep, we investigated whether an S-shaped spinal profile emerges under gravity-like loading in the presence of growth (`chi_kappa`) and anisotropic stiffness.
- We held gravity constant ($9.81$ m/s$^2$), pointing downwards.
- We maintained a high lateral stiffness anisotropy (`anisotropy_ratio = 3.0`) to constrain deformation primarily to the sagittal plane and prevent arbitrary lateral buckling initially.
- We swept the magnitude of the growth gradient (`chi_kappa`) from $0.0$ to $30.0$ over a sinusoidal information field.

## What Emergent Shapes Occurred
- **$chi\_kappa = 0$**: The spine forms a C-shape primarily dominated by gravity, with high sagittal range ($~0.93$ m) and $1$ curvature inflection point (base).
- **$chi\_kappa = 5$ to $20$**: An S-shaped curve emerges. The sagittal range is minimized at $chi\_kappa = 10$ ($~0.17$ m), representing an optimal counter-curvature response where the active growth moments efficiently balance the gravitational moments. Here, we observe $2$ stable curvature inflection points representing the typical thoracic and lumbar curves of a healthy spine.
- **$chi\_kappa \ge 25$**: The growth gradient becomes too strong relative to the stiffness, causing the rod to buckle significantly within the sagittal plane, leading to a large spike in curvature inflections ($10-12$) and chaotic planar folding. Note that lateral deviation remained $0.0$ strictly due to perfect planar symmetry and the lack of a torsional coupling or a tiny initial defect.

## How This Informs Scoliosis vs Normal S-Curve
These results suggest that a "normal S-curve" is the product of an optimal balance between growth-induced active moments and gravitational loading (around $chi\_kappa=10$). The S-shape efficiently reduces the sagittal range and moment arms compared to a C-shape.
If the growth gradient exceeds a critical threshold (e.g., $chi\_kappa \ge 25$), the spine loses its stable S-shape and undergoes chaotic buckling. While this run stayed planar, it highlights the 'Exploding Gradient' vulnerability. In a real 3D biological system with slight asymmetries, this excess energy would likely precipitate the torsional buckling pathognomonic of scoliosis.

## Next Sweep Suggestion
The next sweep should investigate the effect of a **small lateral defect** or **torsional coupling** combined with this excessive growth ($chi\_kappa = 25$). This will test whether the planar buckling observed here immediately resolves into a 3D scoliotic deformity when the symmetry is broken. We could name it `weekly-sim-torsion-excess-growth`.