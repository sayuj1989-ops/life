import os
from instella_client import instella_chat
from instella_tasks import read_text_file

outline_path = "TARGET_OUTLINE_BCC.md"
current_outline = read_text_file(outline_path)

system_prompt = (
    "You are a senior scientific editor and planner. Your goal is to refine a manuscript outline "
    "for a paper on Biological Counter-Curvature. Ensure logical flow, explicit equation slots, "
    "and clear figure-to-code mappings."
)

user_msg = {
    "role": "user",
    "content": (
        f"Refine the following outline. \n"
        f"1. Ensure sections follow: Intro, Theory, Methods, Results, Discussion, Conclusion.\n"
        f"2. Add explicit placeholders for Eq 1 (Metric), Eq 2 (Energy), Eq 3 (Cosserat), Eq 4 (Modes).\n"
        f"3. Ensure every figure has a placeholder and links to a script.\n"
        f"4. Keep the structure clean and markdown-formatted.\n\n"
        f"Current Outline:\n{current_outline}"
    )
}

print("Refining outline with Instella...")
refined_outline = instella_chat(system_prompt, [user_msg], max_new_tokens=4096, temperature=0.3)

print(refined_outline)
