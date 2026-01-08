# Installing LaTeX Locally (macOS)

## ⚠️ Important: Large Download

**MacTeX Full:** ~4GB download, 30-60 minutes  
**BasicTeX:** ~100MB download, 5-10 minutes (may need additional packages)

---

## Option 1: MacTeX Full (Recommended if you'll use LaTeX often)

**Pros:**
- ✅ Complete installation (all packages)
- ✅ No missing package issues
- ✅ Includes GUI tools (TeXShop, etc.)

**Cons:**
- ❌ Large download (~4GB)
- ❌ Long installation time (30-60 min)

**Install:**
```bash
brew install --cask mactex
```

**After installation:**
- Add to PATH (usually automatic, but verify):
  ```bash
  export PATH="/usr/local/texlive/2024/bin/universal-darwin:$PATH"
  ```
- Or restart terminal

---

## Option 2: BasicTeX (Lighter, faster)

**Pros:**
- ✅ Small download (~100MB)
- ✅ Fast installation (5-10 min)

**Cons:**
- ❌ May need to install additional packages
- ❌ More manual setup

**Install:**
```bash
brew install --cask basictex
```

**After installation:**
```bash
# Update tlmgr (TeX Live Manager)
sudo tlmgr update --self

# Install common packages (if needed)
sudo tlmgr install collection-fontsrecommended collection-latexextra
```

---

## Option 3: Use Overleaf (No Installation)

**Pros:**
- ✅ No download
- ✅ Works immediately
- ✅ Cloud-based (access anywhere)

**Cons:**
- ❌ Requires internet
- ❌ No offline editing

**See:** `OVERLEAF_UPLOAD_GUIDE.md`

---

## Verification After Installation

```bash
# Check if pdflatex is available
which pdflatex

# Check version
pdflatex --version

# Check if bibtex is available
which bibtex
```

---

## Compile Manuscript

Once LaTeX is installed:

```bash
cd manuscript
pdflatex main_countercurvature.tex
bibtex main_countercurvature
pdflatex main_countercurvature.tex
pdflatex main_countercurvature.tex
```

**Expected output:**
- `main_countercurvature.pdf` - Your final PDF!

---

## Recommendation

**For one-time compilation:** Use Overleaf (5 minutes)  
**For regular LaTeX use:** Install MacTeX Full (one-time 30-60 min investment)

---

**Current Status:** LaTeX not installed. Choose an option above.

