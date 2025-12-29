# Instella Quick Start Guide

**For:** Antigravity agents & human researchers  
**Purpose:** Get Instella running on your BCC paper in 5 minutes  
**Model:** AMD Instella-3B-Long-Instruct (128k context)

---

## 🚀 5-Minute Quick Start

### Step 1: Activate Environment (30 seconds)

```bash
cd /Users/mac/LIFE
source .venv/bin/activate
```

**Check:** Terminal prompt should show `(.venv)` prefix

---

### Step 2: Verify Dependencies (1 minute)

```bash
pip list | grep -E "transformers|torch|accelerate|sentencepiece"
```

**Expected output:**
```
accelerate       0.XX.X
sentencepiece    0.XX.X
torch            2.XX.X
transformers     4.47.X (or higher)
```

**If missing, install:**
```bash
pip install --upgrade pip
pip install "transformers>=4.47.0" accelerate torch sentencepiece
```

---

### Step 3: Test Instella (2-3 minutes first time)

```bash
python -c "
from instella_client import instella_chat
print('🤖 Loading Instella...')
response = instella_chat(
    system='You are a helpful assistant.',
    messages=[{'role': 'user', 'content': 'Respond with exactly: Instella is ready!'}],
    max_new_tokens=20,
    temperature=0.3
)
print(f'✅ Response: {response}')
"
```

**First run:** Downloads ~6GB, takes 1-2 minutes  
**Subsequent runs:** Loads from cache, ~30 seconds

**Success:** You see `✅ Response: Instella is ready!` (or similar)

---

### Step 4: Run Your First Task (1 minute)

**Option A: Summarize a section**

```bash
python -c "
from instella_tasks import summarize_file
summary = summarize_file('draft_intro_BCC.md', goal='scientific')
print(summary)
" > intro_summary.txt

cat intro_summary.txt
```

**Option B: Rewrite a section**

```bash
python rewrite_driver.py draft_intro_BCC.md draft_intro_BCC_rewritten.md "Introduction" "Nature Communications"
```

**Option C: Get reviewer feedback**

```bash
python reviewer_pass_driver.py draft_intro_BCC.md REVIEW_NOTES_INSTELLA.md "Introduction"
cat REVIEW_NOTES_INSTELLA.md
```

---

## 🎯 Common Workflows

### Workflow 1: Summarize All Sections

```bash
python summarize_manuscript.py
```

**Outputs:** Summaries of all `draft_*_BCC.md` files

---

### Workflow 2: Rewrite All Sections (Batch)

```bash
for section in intro theory methods results discussion conclusion; do
    echo "🔄 Rewriting ${section}..."
    python rewrite_driver.py \
        draft_${section}_BCC.md \
        draft_${section}_BCC_rewritten.md \
        "${section}" \
        "Nature Communications"
done
```

**Outputs:** `draft_*_BCC_rewritten.md` files

---

### Workflow 3: Full Reviewer Pass (Batch)

```bash
# Clear old reviews
> REVIEW_NOTES_INSTELLA.md

for section in intro theory methods results discussion conclusion; do
    echo "🔍 Reviewing ${section}..."
    python reviewer_pass_driver.py \
        draft_${section}_BCC.md \
        REVIEW_NOTES_INSTELLA.md \
        "${section}"
done
```

**Output:** `REVIEW_NOTES_INSTELLA.md` with all feedback

---

### Workflow 4: Consistency Check

```bash
python consistency_check.py
```

**Output:** `CONSISTENCY_REPORT_INSTELLA.md`

---

## 🤖 For Antigravity Agents

**Mission file:** `INSTELLA_ANTIGRAVITY_MISSION.md`

**Quick execution:**

1. **Read the mission:**
   ```
   cat INSTELLA_ANTIGRAVITY_MISSION.md
   ```

2. **Execute phases sequentially:**
   - Phase 0: Test setup (see Step 3 above)
   - Phase 1: Run `python summarize_manuscript.py`
   - Phase 2: Run `python refine_outline.py`
   - Phase 3: Run batch rewrite (Workflow 2 above)
   - Phase 4: Run batch review (Workflow 3 above)
   - Phase 5: Run `python consistency_check.py`
   - Phase 6-7: Follow mission instructions for abstract/integration

3. **Track progress:**
   - Update `INSTELLA_STATUS.md` after each phase
   - Log any errors or issues immediately
   - Flag uncertainties with `[[VERIFY: ...]]` comments

---

## 🔧 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'transformers'"

**Solution:**
```bash
source .venv/bin/activate  # Make sure venv is active
pip install "transformers>=4.47.0" accelerate torch sentencepiece
```

---

### Problem: "CUDA out of memory" or OOM errors

**Solution 1:** Reduce context limit in `instella_client.py`:
```python
MAX_CONTEXT_TOKENS = 60_000  # Lower from 120k
```

**Solution 2:** Use CPU instead of GPU (automatic fallback, just slower)

---

### Problem: Model loading is very slow

**Expected:** First load takes 1-2 minutes (downloading 6GB)  
**Subsequent loads:** 30 seconds from cache

**If still slow:** Check disk space and network connection

---

### Problem: Generated text is nonsensical or off-topic

**Solution:** Adjust temperature and prompts:
- Lower temperature (0.1-0.3) for factual tasks
- Higher temperature (0.5-0.7) for creative tasks
- Add more context in system prompt
- Specify "Preserve all equations and technical terms" in prompt

---

### Problem: Equations are mangled in output

**Solution:**
1. Check that input file has properly formatted LaTeX
2. Add to system prompt: "Do not modify any equation formatting. Preserve all LaTeX commands exactly."
3. Use temperature ≤ 0.3 for equation-heavy sections

---

## 📊 Performance Reference

**Typical timings on modern MacBook (CPU only):**

| Task | Input Size | Time |
|------|-----------|------|
| Model load (first time) | - | 1-2 min |
| Model load (cached) | - | 20-30 sec |
| Summarize (500 words) | ~500 tokens | 30-60 sec |
| Rewrite (2000 words) | ~2000 tokens | 2-4 min |
| Reviewer pass (2000 words) | ~2000 tokens | 2-4 min |
| Consistency check (10k words) | ~10k tokens | 8-12 min |

**On GPU (CUDA):** ~5-10x faster

---

## 🎓 Tips for Best Results

### For Summarization:
- Use `goal="scientific"` for papers
- Use `goal="high-level"` for quick overviews
- Use `goal="equations and methods"` for technical focus

### For Rewriting:
- Specify target journal explicitly: `"Nature Communications"`, `"Physical Review X"`, etc.
- Review rewrites carefully for preserved equations
- Compare word counts: original vs. rewritten

### For Reviewer Passes:
- Run on rewritten sections, not originals (better quality)
- Read feedback as constructive, not definitive
- Prioritize "Major issues" over "Minor issues"

### For Consistency Checks:
- Run after all sections are rewritten
- Focus on symbol definitions and narrative flow
- Use findings to refine abstract and conclusion

---

## 📁 Key Files Reference

| File | Purpose |
|------|---------|
| `instella_client.py` | Core Instella wrapper (don't modify) |
| `instella_tasks.py` | Helper functions (safe to extend) |
| `rewrite_driver.py` | CLI for rewrites |
| `reviewer_pass_driver.py` | CLI for reviews |
| `summarize_manuscript.py` | Batch summarization |
| `consistency_check.py` | Full manuscript analysis |
| `INSTELLA_ANTIGRAVITY_MISSION.md` | Full mission plan |
| `INSTELLA_STATUS.md` | Current status & diagnostics |
| `TARGET_OUTLINE_BCC.md` | Target structure |
| `MANUSCRIPT_PLAN_BCC_INSTELLA.md` | Project overview |

---

## 🆘 Need Help?

**Check these in order:**

1. **Status document:** `cat INSTELLA_STATUS.md`
2. **Mission document:** `cat INSTELLA_ANTIGRAVITY_MISSION.md`
3. **Model card:** https://huggingface.co/amd/Instella-3B-Long-Instruct
4. **Transformers docs:** https://huggingface.co/docs/transformers

**Run diagnostics:**

```bash
# Check Python/dependencies
python --version
pip list | grep -E "transformers|torch"

# Check PyTorch
python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"

# Check disk space
df -h .

# Test import
python -c "from instella_client import instella_chat; print('✅ Import successful')"
```

---

## 🎯 Success Checklist

After running this guide, you should have:

- ✅ Virtual environment activated
- ✅ All dependencies installed
- ✅ Instella model loaded and tested
- ✅ At least one task completed (summarize/rewrite/review)
- ✅ Understanding of available workflows
- ✅ `INSTELLA_STATUS.md` updated with test results

**Next step:** Proceed to Phase 1 of `INSTELLA_ANTIGRAVITY_MISSION.md`

---

**Quick Start Version:** 1.0  
**Last Updated:** 2025-11-27  
**Target Audience:** Both agents and humans  
**Estimated Time to Complete:** 5-10 minutes (including first model download)
