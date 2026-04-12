with open('manuscript/nature_submission_v3.tex', 'r') as f:
    content = f.read()

# Fix broken cross-reference
content = content.replace("Table~\\ref{table:comprehensive_stats}", "Table~\\ref{tab:statistical_summary}")
content = content.replace("Supplementary Table S1", "Table~\\ref{tab:statistical_summary}")
content = content.replace("Supplementary Table~S1", "Table~\\ref{tab:statistical_summary}")

with open('manuscript/nature_submission_v3.tex', 'w') as f:
    f.write(content)

with open('manuscript/sections/results.tex', 'r') as f:
    results_content = f.read()

# Make sure the table matches references (replace Supplementary Table S1 with Table \ref{tab:statistical_summary} if needed)
results_content = results_content.replace("Supplementary Table S1", "Table~\\ref{tab:statistical_summary}")
with open('manuscript/sections/results.tex', 'w') as f:
    f.write(results_content)
