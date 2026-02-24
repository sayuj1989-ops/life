# Spine Submission Workflow

This directory manages the submission process for the *Spine* journal.

## Key Files

*   `roadmap.md`: The central task list. Update this file manually as tasks are completed (mark `[x]`).
*   `../data/clinical_cohort_targets.csv`: Clinical data for validation.
*   `../../scripts/spine_daily_update.py`: Generates the daily status report.
*   `../../scripts/validate_clinical_data.py`: Validates simulation outputs against clinical data.

## Daily Routine

1.  **Check Roadmap**: Review `roadmap.md` for current tasks.
2.  **Run Validation**: If working on clinical validation, run:
    ```bash
    python scripts/validate_clinical_data.py
    ```
3.  **Update Roadmap**: Mark completed tasks in `roadmap.md`.
4.  **Generate Report**: Run the daily update script to see progress and ETA:
    ```bash
    python scripts/spine_daily_update.py
    ```

## Goal

Submit "A computational framework predicting adolescent scoliosis onset" to *Spine* (IF 3.30) by April 6, 2026.
