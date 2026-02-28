import re

with open("manuscript/references.bib", "r") as f:
    content = f.read()

keys = [
    "krishnan2025consciousness",
    "sato2025convective",
    "shao2025ros",
    "wuest2025vim",
    "steger2025gravity",
    "mader2026glymphatic",
    "gerwin2026proprioceptive"
]

for key in keys:
    # Use a regex to find the block @...{key, ... }
    # This matches from @ to the closing brace, handling nested braces up to a certain depth if needed,
    # but a simpler way is to find the start and then count braces.
    start_idx = content.find("{" + key + ",")
    if start_idx == -1:
        # try without space after comma or just {key,
        start_idx = content.find("{" + key)
        if start_idx != -1 and content[start_idx:start_idx+len(key)+2] not in ["{" + key + ",", "{" + key + "\n"]:
            start_idx = -1

    if start_idx != -1:
        # Find the preceding '@'
        at_idx = content.rfind("@", 0, start_idx)
        if at_idx != -1:
            # Count braces to find the end
            brace_count = 0
            end_idx = -1
            for i in range(at_idx, len(content)):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break
            if end_idx != -1:
                print(f"Removing {key} from index {at_idx} to {end_idx}")
                content = content[:at_idx] + content[end_idx:]

with open("manuscript/references.bib", "w") as f:
    f.write(content)
