"""
Managed Agent runner for scoliosis research work packages.

Usage:
    python run_research.py --wp 5   # Run WP5: Literature landscape
    python run_research.py --wp 6   # Run WP6: Fundable experiment
    python run_research.py --wp 7   # Run WP7: Editorial audit
"""
import argparse
import json
import os
import sys
import time

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

# Load .env
ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())

AGENT_ID = None
ENV_ID = None
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "agent_config.json")
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
        AGENT_ID = cfg.get("agent_id")
        ENV_ID = cfg.get("environment_id")


# ──────────────────────────────────────────────
# Work Package Prompts
# ──────────────────────────────────────────────

WP_PROMPTS = {}

WP_PROMPTS[5] = """
## WP5 — Literature Landscape: Competing and Complementary 2024–2026 Work

CONTEXT: You are working on a manuscript titled "The Allometric Trap" about Adolescent Idiopathic Scoliosis (AIS) as metabolic buckling. The manuscript models AIS via a Hopf bifurcation in a delayed proprioceptive control loop (the "Derivative Gain Trap"), with an L^4-vs-L^2 energy deficit during the adolescent growth spurt, and AlphaFold-derived Demand-Supply anisotropy gap (n=31, p=0.002).

Branch: claude/strengthen-manuscript-Avo07

TASKS:
1. Search for recent (2024–2026) theoretical/computational work on:
   - Scoliosis etiology (especially zebrafish urotensin/Reissner's fiber work, cilia models)
   - Scaling laws in vertebrate biomechanics
   - Active matter / active rods / morphogenesis under gravity
   - Delay-induced instabilities in biology
   - NAD+ and spinal deformity (Shi et al., Basse et al.)
   - Proprioceptive control and postural stability in adolescents

2. For each relevant paper, write 2–3 sentences: (a) what they found, (b) how it relates to the Allometric Trap, (c) whether it supports, complements, or competes.

3. Identify 3–5 citations to ADD to the Discussion section and 0–2 that require a DEFENSIVE response.

DELIVERABLES:
- Save a comprehensive report to: research/managed_agent/wp5_literature_landscape.md
- Include BibTeX entries for all new references
- Include a revised "Relation to existing models" paragraph ready for sections/discussion.tex

RULES:
- Cite real papers only — DOI or PubMed ID required for each. Do NOT fabricate references.
- Prefer primary sources over reviews.
- Report honestly if any paper directly contradicts the framework.
"""

WP_PROMPTS[6] = """
## WP6 — The Single Most Fundable Experiment

CONTEXT: The "Allometric Trap" manuscript proposes that AIS is caused by a transient derivative gain gap during adolescent growth (Hopf bifurcation in delayed PD postural control). Key model predictions:
- τ_c (critical neural delay) ~50-100ms triggers instability
- Growth velocity dL/dt (not height L) drives onset
- NAD+ depletion degrades proprioceptive axon integrity → increases τ
- Metabolic rescue (mitochondrial biogenesis, NAD+ precursors) should prevent/arrest curves
- Sex-specific vulnerability windows: girls 10.6-11.8 yr, boys 12.2-14.2 yr
- The AlphaFold Demand-Supply anisotropy gap (p=0.002): high-anisotropy mechanosensors fail first

Branch: claude/strengthen-manuscript-Avo07

TASK:
1. Propose ONE experiment that would decisively validate (or falsify) the Derivative Gain Gap hypothesis, feasible within a standard R01/Wellcome budget.

2. Criteria:
   - Directly tests a quantitative prediction (e.g., τ_c, dL/dt-dependence, NAD+ rescue)
   - Uses an existing model system (zebrafish ptk7, mouse Lbx1, ferret, or human cohort)
   - Produces binary go/no-go outcome within 18 months
   - Budget < $500K

3. Design sketch: experimental groups, N, primary endpoint, go/no-go criterion, statistical power calculation

4. Also briefly describe 2 runner-up experiments for a grant application's "Future Directions"

DELIVERABLES:
- Save to: research/managed_agent/wp6_fundable_experiment.md (2-3 pages, grant-ready language)
- Include a brief power analysis
- Identify the most suitable funding mechanism (NIH R21, R01, Wellcome Discovery, etc.)

RULES:
- The experiment must be feasible with current technology
- Cite existing model systems and their published phenotypes
- Be honest about what the experiment CAN and CANNOT distinguish
"""

WP_PROMPTS[7] = """
## WP7 — Editorial and Reference Audit

CONTEXT: The manuscript "The Allometric Trap" is on branch claude/strengthen-manuscript-Avo07. It targets eLife (primary) and Nature Communications (secondary).

Key files:
- Main manuscript: manuscript/spine_deformity_submission.tex (the Spine Deformity version)
- Theory: manuscript/sections/theory.tex
- References: manuscript/references.bib
- Cover letter: manuscript/cover_letter.tex
- Nature version: manuscript/nature_submission_manuscript.md

Branch: claude/strengthen-manuscript-Avo07

TASKS:
1. Run a full reference audit on manuscript/references.bib:
   - Every \\cite{} key in manuscript/sections/*.tex and manuscript/spine_deformity_submission.tex resolves
   - Every bib entry has a DOI or URL
   - Flag any Wikipedia, preprint-only, or predatory-journal sources
   - Missing or broken cross-references

2. Check every numerical claim in abstract, introduction, and results against its cited source:
   - AIS prevalence: 2-4%
   - Female ratio: 3:1 or 10:1 for curves >30°
   - PHV timing: girls ~11.5 yr, boys ~13.5 yr
   - Peterka (2002) controller gain ranges
   - Growth velocity values (8.3 cm/yr girls, 9.5 cm/yr boys)

3. Verify equation numbering, figure references, and table references are consistent

4. Check cover_letter.tex matches the current manuscript title and claims

5. Verify the manuscript compiles: read spine_deformity_submission.tex and check all \\cite keys exist in the bibliography

DELIVERABLES:
- Save audit report to: research/managed_agent/wp7_editorial_audit.md
- Include a red/yellow/green table for each citation
- List any undefined \\cite keys or missing references
- Recommend specific fixes

RULES:
- Do NOT modify the manuscript files — only audit and report
- Flag estimates and assumed parameters clearly
- Check DOIs are real by examining the URL format (do not need to visit each)
"""

WP_PROMPTS[8] = """
## WP8 — Active Inference Simulation (Paper 5, Day 14)

CONTEXT: You are working on "Paper 5" of the Allometric Trap scoliosis theory. Paper 5 reformulates the delayed PID postural control (from Paper 2) as an Active Inference (Free Energy Minimization) agent, building on Baltieri & Buckley (2019) who showed PID is active inference under linear Gaussian assumptions.
Our extension focuses on delayed observations (tau ~ 50-100ms) and time-varying plant parameters (growth spurt L(t)). 
Crucially, when the plant changes faster than the model updates, precision collapses. The variance of velocity prediction errors increases, leading to a dynamic reduction in sensory precision Pi_y,1 (which maps to effective derivative gain Kd). This transient drop in effective Kd triggers the Hopf bifurcation (Allometric Trap) in the adolescent spine.

Branch: claude/strengthen-manuscript-Avo07

TASKS:
1. Formulate the mathematical mapping from Free Energy Minimization to our delayed inverted pendulum system, showing how the precision parameter Pi_y,1 operates as an effective derivative feedback gain.
2. Outline the differential equations for the active inference agent (belief updating for generalized states and precision updating over time).
3. Write a self-contained, highly-documented Python script that simulates this framework. The script should:
   - Model an inverted pendulum with time-varying height L(t).
   - Implement an active inference controller (gradient descent on Free Energy) with delayed proprioception.
   - Implement dynamic precision updating: as prediction errors accumulate during the growth spurt, the effective precision Pi_y,1 dynamically decreases.
   - Run a simulation plotting true angle, belief state, and effective Kd over time, saving the plot to `active_inference_buckling.png`.

DELIVERABLES:
- Provide the mathematical derivation directly in your markdown response.
- Provide the full Python script enclosed in a ```python ... ``` code block so it can be extracted and run.
- Summarize the expected findings of the simulation.

RULES:
- The script must use standard libraries (numpy, scipy.integrate, matplotlib).
- Make sure the physics makes sense: buckling occurs when length L is high and effective Kd drops too low to stabilize the delay tau.
"""


# Best available model
MODEL = "claude-sonnet-4-6"


def run_wp(wp_number: int):
    """Run a work package via the Anthropic Messages API."""
    if wp_number not in WP_PROMPTS:
        print(f"ERROR: No prompt defined for WP{wp_number}")
        print(f"Available: {sorted(WP_PROMPTS.keys())}")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key or api_key.startswith("sk-ant-..."):
        print("ERROR: ANTHROPIC_API_KEY not set. Check .env file.")
        sys.exit(1)

    prompt = WP_PROMPTS[wp_number]

    print(f"{'='*70}")
    print(f"  MANAGED AGENT — WP{wp_number}")
    print(f"{'='*70}")
    print(f"  Model: {MODEL}")
    print(f"  Prompt length: {len(prompt)} chars")
    print(f"{'='*70}")
    print()

    client = anthropic.Anthropic(api_key=api_key)
    _run_direct(client, prompt, wp_number)


def _run_direct(client, prompt: str, wp_number: int):
    """Run via direct Messages API."""
    print(f"Sending WP{wp_number} to {MODEL}...\n")

    response = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        system="You are a senior computational biophysicist and scientific editor working on a scoliosis manuscript ('The Allometric Trap'). Execute the requested work package thoroughly. Cite real papers only (DOI/PMID). Show your work. Be honest if evidence contradicts the framework.",
        messages=[{"role": "user", "content": prompt}],
    )

    output_text = ""
    for block in response.content:
        if hasattr(block, 'text'):
            print(block.text)
            output_text += block.text

    # Save output
    out_path = os.path.join(
        os.path.dirname(__file__),
        f"wp{wp_number}_output.md"
    )
    with open(out_path, "w") as f:
        f.write(f"# WP{wp_number} — Managed Agent Output\n\n")
        f.write(output_text)
    print(f"\n✅ Output saved to {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Run managed agent work packages")
    parser.add_argument("--wp", type=int, required=True, help="Work package number (5, 6, or 7)")
    parser.add_argument("--list", action="store_true", help="List available WPs")
    args = parser.parse_args()

    if args.list:
        for n in sorted(WP_PROMPTS.keys()):
            print(f"  WP{n}: {WP_PROMPTS[n].split(chr(10))[1].strip()}")
        return

    run_wp(args.wp)


if __name__ == "__main__":
    main()
