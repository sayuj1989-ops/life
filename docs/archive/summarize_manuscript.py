import os
from instella_tasks import summarize_file

sections = [
    "life/manuscript/sections/introduction.tex",
    "life/manuscript/sections/theory.tex",
    "life/manuscript/sections/methods.tex",
    "life/manuscript/sections/results.tex",
    "life/manuscript/sections/discussion.tex",
    "life/manuscript/sections/conclusion.tex"
]

print("# Manuscript Summary (Instella)\n")

for sec in sections:
    if os.path.exists(sec):
        print(f"## Section: {os.path.basename(sec)}\n")
        summary = summarize_file(sec)
        print(summary)
        print("\n")
    else:
        print(f"Warning: {sec} not found.\n")
