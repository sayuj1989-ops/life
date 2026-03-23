import os
from datetime import datetime

progress_file = "paper3_progress.md"

date_str = datetime.now().strftime("%Y-%m-%d")
day_update = f"""## {date_str} - Phase 1, Day 1 Completed

**Key findings/decisions:**
- Initialized the `paper3_literature` directory.
- Built a query script to pull actual literature from EuropePMC APIs, fetching BibTeX entries via dynamic DOI resolution.
- Searched for literature covering ageing postural control, proprioceptive decline with age, vestibular degeneration, and cerebellar atrophy.
- Compiled abstracts and real DOIs into `paper3_literature/day1_postural_ageing.md`. Findings support that ageing drives multisensory deterioration (proprioceptive and vestibular) causing balance impairment, and cerebellar atrophy contributes to further cognitive and gross motor frailty.

**Issues/questions for Dr. Sayuj:**
- The EuropePMC API query terms returned several recent (some forecasted to 2025/2026 publication dates) and highly relevant papers. Please review `day1_postural_ageing.md` to confirm if these specific papers align with the narrative you want to build for the terminal derivative gain gap model.

**What the next session should do:**
- Proceed to Phase 1, Day 2: Search for papers on peripheral neuropathy and nerve conduction velocity changes with age. Quantify how τ increases with age and save to `paper3_literature/day2_neuropathy_delay.md`.
"""

if not os.path.exists(progress_file):
    content = f"# Paper 3 Progress Tracker\n\nThis file tracks the daily progress for Paper 3: 'The Terminal Derivative Gain Gap: A Control-Theoretic Model of Age-Related Postural Collapse'.\n\n{day_update}"
else:
    with open(progress_file, "r") as f:
        content = f.read()
    content += f"\n\n{day_update}"

with open(progress_file, "w") as f:
    f.write(content)

print(f"Updated {progress_file}")
