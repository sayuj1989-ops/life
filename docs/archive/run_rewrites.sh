#!/bin/bash
source .venv/bin/activate

# Create drafts directory if not exists
mkdir -p life/manuscript/drafts_instella

# Define sections to rewrite
# Format: "input_file output_file title style"

python rewrite_driver.py \
    "life/manuscript/sections/introduction.tex" \
    "life/manuscript/drafts_instella/introduction.tex" \
    "Introduction: Biological Countercurvature" \
    "Nature Communications"

python rewrite_driver.py \
    "life/manuscript/sections/theory.tex" \
    "life/manuscript/drafts_instella/theory.tex" \
    "Theory: Information-Cosserat Framework" \
    "Physical Review E"

python rewrite_driver.py \
    "life/manuscript/sections/methods.tex" \
    "life/manuscript/drafts_instella/methods.tex" \
    "Methods: PyElastica Implementation" \
    "Nature Communications"

python rewrite_driver.py \
    "life/manuscript/sections/results.tex" \
    "life/manuscript/drafts_instella/results.tex" \
    "Results: Gravity-Selected Modes" \
    "Nature Communications"

python rewrite_driver.py \
    "life/manuscript/sections/discussion.tex" \
    "life/manuscript/drafts_instella/discussion.tex" \
    "Discussion: From Information to Deformity" \
    "Nature Communications"

python rewrite_driver.py \
    "life/manuscript/sections/conclusion.tex" \
    "life/manuscript/drafts_instella/conclusion.tex" \
    "Conclusion" \
    "Nature Communications"
