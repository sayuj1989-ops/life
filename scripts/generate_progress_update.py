import datetime
import re

today = datetime.date.today().strftime('%Y-%m-%d')

with open('docs/spine_submission_roadmap.md', 'r') as f:
    roadmap = f.read()

total = len(re.findall(r'- \[[ x]\]', roadmap))
completed = len(re.findall(r'- \[x\]', roadmap))
percent = (completed / total * 100) if total else 0

current_state = ""
pending_work = ""
for line in roadmap.split('\n'):
    if line.strip().startswith('- [x]'):
        current_state += line + '\n'
    elif line.strip().startswith('- [ ]'):
        pending_work += line + '\n'

with open('docs/toy_models_plan.md', 'r') as f:
    toy_models = f.read()

toy_models_text = "## Toy Models Plan\n\n| Model | Owner | Effort | Status |\n| :--- | :--- | :--- | :--- |\n"
for line in toy_models.split('\n'):
    if line.startswith('| **Toy'):
        toy_models_text += line + '\n'

update_content = f"""# Research Progress Update: Biological Countercurvature

**Date:** {today}
**Role:** PI / Program Manager / Computational Scientist
**Target Journal:** Spine (IF: 3.30, Q1, H-index: 300)

Why: The highest prestige spine journal by H-index. Publishes basic science.
Fit score: 6/10 — High bar; will need experimental validation or strong clinical dataset comparison.
Strategy: Reframe as "A computational framework predicting adolescent scoliosis onset" with clinical validation against published cohort data.

## Executive Summary
Project is shifting toward clinical validation against published cohort data to target Spine. The daily metrics report {percent:.1f}% completion ({completed}/{total} tasks). Current focus is on extracting PHV/Sex ratios from literature for mapping against our computational Energy Deficit model instability window.

## A) Current State
**What's Done:**
{current_state}

## B) Pending Work
**What's In Progress/Pending:**
{pending_work}

## C) Timeline Estimate to Completion
**Target Submission Date:** 2026-04-06

**Critical Path:**
Cohort Data Extraction (PHV/Sex Ratios) -> Clinical Validation Experiments -> IMRaD Manuscript Reformatting -> Final Submission.

{toy_models_text}
"""

with open(f'docs/progress_update_{today}.md', 'w') as f:
    f.write(update_content)

print(f"Generated docs/progress_update_{today}.md")
