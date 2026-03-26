import datetime
import os
import re

def parse_roadmap(filepath):
    """
    Parses the roadmap markdown file to extract tasks and calculate progress.
    """
    if not os.path.exists(filepath):
        return None, "Roadmap file not found."

    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    total_tasks = 0
    completed_tasks = 0
    phases = {}
    current_phase = None
    next_milestones = []

    start_date_match = re.search(r'\*\*Start Date:\*\* (\d{4}-\d{2}-\d{2})', content)
    target_date_match = re.search(r'\*\*Target Submission Date:\*\* (\d{4}-\d{2}-\d{2})', content)

    start_date = datetime.datetime.strptime(start_date_match.group(1), '%Y-%m-%d').date() if start_date_match else None
    target_date = datetime.datetime.strptime(target_date_match.group(1), '%Y-%m-%d').date() if target_date_match else None

    for line in lines:
        if line.startswith('## Phase'):
            current_phase = line.strip().replace('## ', '')
            phases[current_phase] = {'total': 0, 'completed': 0}

        if line.strip().startswith('- ['):
            total_tasks += 1
            if current_phase:
                phases[current_phase]['total'] += 1

            if line.strip().startswith('- [x]'):
                completed_tasks += 1
                if current_phase:
                    phases[current_phase]['completed'] += 1
            else:
                # Extract task name for next milestones
                task_match = re.search(r'- \[ \] \*\*(.*?)\*\*', line)
                if task_match and len(next_milestones) < 3:
                    next_milestones.append(task_match.group(1))

    percent_complete = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'percent_complete': percent_complete,
        'phases': phases,
        'start_date': start_date,
        'target_date': target_date,
        'next_milestones': next_milestones
    }, None

def generate_report(data):
    """
    Generates a formatted daily update report.
    """
    today = datetime.date.today()

    # Calculate expected completion date based on task velocity
    expected_completion_str = "TBD"
    projected_completion = "TBD"

    if data['start_date'] and data['completed_tasks'] > 0:
        days_passed = (today - data['start_date']).days
        if days_passed > 0:
            velocity = data['completed_tasks'] / days_passed
            remaining_tasks = data['total_tasks'] - data['completed_tasks']
            if velocity > 0:
                days_remaining_proj = remaining_tasks / velocity
                proj_date = today + datetime.timedelta(days=int(days_remaining_proj))
                projected_completion = f"{proj_date.strftime('%Y-%m-%d')}"

    target_deadline_str = "TBD"
    if data['target_date']:
        target_deadline_str = f"{data['target_date'].strftime('%Y-%m-%d')}"

    report = f"""# Daily Update: Spine Submission

**Date:** {today}
**Target Journal:** Spine (IF: 3.30, Q1, H-index: 300)
**Why:** The highest prestige spine journal by H-index. Publishes basic science.
**Fit score:** 6/10 — High bar; will need experimental validation or strong clinical dataset comparison.
**Strategy:** Reframe as "A computational framework predicting adolescent scoliosis onset" with clinical validation against published cohort data.

## Status Overview
- **Percent Complete:** {data['percent_complete']:.1f}%
- **Tasks Completed:** {data['completed_tasks']} / {data['total_tasks']}
- **Projected Completion:** {projected_completion}
- **Target Deadline:** {target_deadline_str}

## Phase Breakdown
"""

    active_phase = "None"
    for phase, stats in data['phases'].items():
        phase_percent = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        status_icon = "✅" if phase_percent == 100 else "🔄" if phase_percent > 0 else "⚪"
        report += f"- {status_icon} **{phase}:** {phase_percent:.1f}% ({stats['completed']}/{stats['total']})\n"

        if phase_percent < 100 and active_phase == "None":
            active_phase = phase

    report += f"\n**Current Focus:** {active_phase}\n"

    report += "\n## Next Milestones\n"
    for i, milestone in enumerate(data['next_milestones']):
        report += f"{i+1}. {milestone}\n"

    report += "\nRun `python scripts/generate_spine_daily_update.py` to regenerate this report.\n"

    return report

if __name__ == "__main__":
    roadmap_path = "docs/spine_submission_roadmap.md"
    data, error = parse_roadmap(roadmap_path)

    if error:
        print(error)
    else:
        report_content = generate_report(data)
        os.makedirs("reports", exist_ok=True)
        with open("reports/daily_update_latest.md", "w") as f:
            f.write(report_content)
        print("Successfully generated reports/daily_update_latest.md")
