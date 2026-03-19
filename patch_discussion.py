import os

filepath = "manuscript/sections/discussion.tex"

with open(filepath, "r") as f:
    content = f.read()

new_section = """
\\subsection{The Therapeutic Paradox: The Derivative Gain Trap}

While the primary mechanism of adolescent spinal instability is driven by a growth-induced loss of proprioceptive derivative gain (the ``Gap''), extended parameter sweeps of our delayed-feedback model reveal a secondary, non-monotonic dynamical phenomenon. In systems with elevated sensory delay ($\\tau$), increasing the derivative gain ($K_d$) improves stability only up to a critical threshold. Beyond this optimal window, further increasing the corrective velocity response paradoxically destabilizes the system, a phenomenon we term the Derivative Gain ``Trap''.

This finding has profound clinical implications. It suggests that aggressive corrective interventions---such as rapid bracing adjustments or high-intensity proprioceptive training that attempts to force a faster velocity response---may inadvertently worsen curve progression if the underlying neuromuscular delay remains elevated. The presence of this therapeutic trap implies that interventions should primarily target delay reduction (accelerating sensory adaptation) rather than solely focusing on aggressive gain augmentation.
"""

# Append it before the end of the file, or just at the end
if "The Therapeutic Paradox" not in content:
    content += new_section
    with open(filepath, "w") as f:
        f.write(content)
    print("Added section to discussion.tex")
else:
    print("Section already exists")
