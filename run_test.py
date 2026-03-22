import sys
try:
    with open("docs/spine_submission_roadmap.md") as f:
        print("Roadmap exists")
except Exception as e:
    print(e)
