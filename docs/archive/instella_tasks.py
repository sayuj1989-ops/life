# instella_tasks.py
from pathlib import Path
from textwrap import shorten
from typing import List
from instella_client import instella_chat, summarize_text


def read_text_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="ignore")


def summarize_file(path: str, goal: str = "scientific") -> str:
    text = read_text_file(path)
    if len(text) > 120_000:  # chars, rough guard; token-level handled in client
        # crude chunking
        chunks: List[str] = []
        step = 40_000
        for i in range(0, len(text), step):
            chunk = text[i : i + step]
            chunks.append(chunk)

        summaries = []
        for idx, chunk in enumerate(chunks, start=1):
            partial = summarize_text(chunk, goal=goal)
            summaries.append(f"### Chunk {idx}\n{partial}")
        joined = "\n\n".join(summaries)
        return summarize_text(joined, goal=f"high-level {goal}")
    else:
        return summarize_text(text, goal=goal)


def rewrite_section(title: str, content: str, style: str = "Nature Communications") -> str:
    system = (
        "You are a co-author helping refine a theoretical biophysics/neuroscience "
        "manuscript on Biological Counter-Curvature and spinal modes. "
        f"Target style: {style}. Preserve all equations and technical meaning."
    )
    user = {
        "role": "user",
        "content": (
            f"Rewrite the following section titled '{title}' for clarity, logical flow, "
            "and scientific style. Keep all symbols, equations, and references.\n\n"
            f"{content}"
        ),
    }
    return instella_chat(system, [user], max_new_tokens=2048, temperature=0.35)


def reviewer_pass(section_title: str, content: str) -> str:
    system = (
        "You are a critical but constructive journal referee for a theoretical "
        "paper on information–elasticity coupling and spinal curvature."
    )
    user = {
        "role": "user",
        "content": (
            f"Act as Reviewer 2. Read this section '{section_title}' and give:\n"
            "1) Major issues\n2) Minor issues\n3) Missing references or checks\n"
            "4) Concrete rewrite suggestions (not full rewrite).\n\n"
            f"{content}"
        ),
    }
    return instella_chat(system, [user], max_new_tokens=2048, temperature=0.5)
