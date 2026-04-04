import re

with open("scripts/spine_daily_update.py", "r") as f:
    content = f.read()

new_func = """
def update_roadmap(filepath, percent_complete, expected_date):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r') as f:
        content = f.read()

    # Update Percent Complete
    content = re.sub(
        r'\\*\\*Percent Complete:\\*\\* .*',
        f'**Percent Complete:** {percent_complete:.1f}%',
        content
    )

    # Update Expected Date if it exists, or add it below Percent Complete
    if '**Expected Completion:**' in content:
        content = re.sub(
            r'\\*\\*Expected Completion:\\*\\* .*',
            f'**Expected Completion:** {expected_date}',
            content
        )
    else:
        # Add after Percent Complete
        content = re.sub(
            r'(\\*\\*Percent Complete:\\*\\* .*\\n)',
            f'\\\\1**Expected Completion:** {expected_date}\\n',
            content
        )

    with open(filepath, 'w') as f:
        f.write(content)
"""

if "def update_roadmap" not in content:
    content = content.replace("def save_report", new_func + "\ndef save_report")

main_replace = """    if error:
        print(error)
        sys.exit(1)
    else:
        expected_date = calculate_projection(data)
        update_roadmap(roadmap_path, data['percent_complete'], expected_date)
        report = generate_report(data)"""

content = content.replace("""    if error:
        print(error)
        sys.exit(1)
    else:
        report = generate_report(data)""", main_replace)

with open("scripts/spine_daily_update.py", "w") as f:
    f.write(content)
