with open('manuscript/sections/figures.tex', 'r') as f:
    content = f.read()

old_caption = r"""\caption{\textbf{Counter-Curvature as Active Morphogenesis.} (A) \textbf{Passive Gravitational Prior}: In the absence of active correction, gravity dictates a low-energy, monotonic C-shaped sag (blue curve). (B) \textbf{Active Counter-Curvature Posterior}: Biological growth, guided by the ``Genetic Prior'' (HOX genes), generates an S-shaped ``Counter-Curvature'' (orange curve) that actively opposes the gravitational metric. This high-energy state is maintained by the continuous expenditure of metabolic work ($P_{\mathrm{counter}}$). (C) \textbf{The Energy Deficit Window}: During rapid adolescent growth, the thermodynamic cost of maintaining this active posterior (scaling as $L^3$) outpaces the diffusive nutrient supply ($L^2$). This triggers a ``Vector-Scalar Mismatch'' where high-cost Vector Sensors (Piezo2) fail, leading to a collapse into the passive, gravity-dominated scoliotic mode.}"""

new_caption = r"""\caption{\textbf{Counter-Curvature as Active Morphogenesis.} (A) \textbf{Passive Gravitational Prior}: In the absence of active correction, gravity dictates a low-energy, monotonic C-shaped sag (blue curve). (B) \textbf{Active Counter-Curvature Posterior}: Spinal morphogenesis, guided by the ``Genetic Prior'' (e.g., HOX genes) and the ``Matrix-Stiffness Code'', generates an S-shaped ``Counter-Curvature'' (orange curve) that actively opposes gravity through tensegrity-driven mechanotransduction. This high-energy state is maintained by the continuous expenditure of metabolic work. (C) \textbf{The Gravity Paradox}: During the pubertal growth spurt, the mechanical moment (Thermodynamic Tax) required to maintain the S-curve scales as $L^4$, outpacing the sublinear ($L^2$) diffusive nutrient supply. This creates a critical \textbf{Energy Deficit Window} that starves high-cost vector sensors (e.g., Piezo2), causing a ``Thermodynamic Buckling'' collapse into the passive, gravity-dominated scoliotic mode.}"""

content = content.replace(old_caption, new_caption)

with open('manuscript/sections/figures.tex', 'w') as f:
    f.write(content)
