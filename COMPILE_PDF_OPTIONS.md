# PDF Compilation Options

## Problem
LaTeX installation requires sudo password. Cannot compile manuscript locally without authentication.

## RECOMMENDED SOLUTION: Overleaf (15 minutes, no installation)

### Steps:

1. **Prepare manuscript archive**:
   ```bash
   cd /home/sayuj/life
   zip -r manuscript_upload.zip manuscript/
   ```

2. **Go to Overleaf**: https://www.overleaf.com
   - Login or create free account

3. **Upload project**:
   - Click "New Project" → "Upload Project"
   - Select `manuscript_upload.zip`
   - Project will open automatically

4. **Compile**:
   - Click green "Recompile" button
   - Wait ~30 seconds
   - PDF appears in right panel

5. **Download PDF**:
   - Click "Download PDF" icon (top right)
   - Save as `submission_manuscript.pdf`
   - Move to `/home/sayuj/life/submission_package/`

6. **Compile cover letter** (same process):
   - New Project → Upload `submission_package/cover_letter_spine_deformity.tex`
   - Recompile → Download as `cover_letter_spine_deformity.pdf`

**Advantages**:
- No local installation needed
- Automatic dependency management
- Error highlighting
- Version history
- Free for basic use

---

## ALTERNATIVE 1: Docker LaTeX (20 minutes, no sudo)

### Prerequisites:
Docker installed (check: `docker --version`)

### Steps:

```bash
cd /home/sayuj/life/manuscript

# Pull LaTeX docker image (one-time, ~2GB)
docker pull texlive/texlive:latest

# Compile manuscript
docker run --rm -v $(pwd):/workspace -w /workspace texlive/texlive:latest \
  pdflatex -interaction=nonstopmode main.tex

# Run bibtex for references
docker run --rm -v $(pwd):/workspace -w /workspace texlive/texlive:latest \
  bibtex main

# Compile again (2x for references)
docker run --rm -v $(pwd):/workspace -w /workspace texlive/texlive:latest \
  pdflatex -interaction=nonstopmode main.tex

docker run --rm -v $(pwd):/workspace -w /workspace texlive/texlive:latest \
  pdflatex -interaction=nonstopmode main.tex

# Result: main.pdf
```

**Advantages**:
- No sudo needed (if Docker already configured)
- Reproducible build environment
- Can automate in CI/CD

**Disadvantages**:
- Requires Docker (may need configuration)
- Large download (~2GB)

---

## ALTERNATIVE 2: Local LaTeX Install (Manual, requires sudo)

### Option A: Essential packages only (~500MB)

```bash
# You need to enter sudo password when prompted
sudo apt-get update
sudo apt-get install -y texlive-latex-base texlive-latex-extra \
  texlive-fonts-recommended texlive-bibtex-extra

cd /home/sayuj/life/manuscript
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Option B: Full TeXLive (~4GB, all packages)

```bash
sudo apt-get install -y texlive-full

cd /home/sayuj/life/manuscript
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

**Advantages**:
- Fastest compilation after installation
- Offline capable
- Professional workflow

**Disadvantages**:
- Requires sudo password
- Large disk space (500MB-4GB)

---

## ALTERNATIVE 3: GitHub Actions (Automated, 30 min setup)

### Create workflow file:

```bash
mkdir -p .github/workflows
cat > .github/workflows/compile-latex.yml << 'EOF'
name: Compile LaTeX

on:
  push:
    branches: [ main ]
    paths:
      - 'manuscript/**'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Compile LaTeX
        uses: xu-cheng/latex-action@v2
        with:
          root_file: main.tex
          working_directory: manuscript
          
      - name: Upload PDF
        uses: actions/upload-artifact@v3
        with:
          name: submission_manuscript
          path: manuscript/main.pdf
EOF

git add .github/workflows/compile-latex.yml
git commit -m "Add LaTeX compilation workflow"
git push
```

Then go to GitHub Actions tab, download artifact.

**Advantages**:
- Fully automated
- No local resources used
- Version controlled

**Disadvantages**:
- Requires GitHub push
- Takes 2-3 minutes per compilation

---

## ALTERNATIVE 4: Online LaTeX Editors (Quick, no setup)

### Options:

1. **Overleaf** (recommended): https://www.overleaf.com
   - Free, widely used
   - Best for collaboration

2. **Papeeria**: https://papeeria.com
   - Free tier available
   - Clean interface

3. **Authorea**: https://www.authorea.com
   - Free for public projects
   - Git integration

All work similarly: upload project → compile → download PDF.

---

## RECOMMENDATION

**For immediate submission**: Use **Overleaf** (Option 1)
- Fastest (15 min)
- No installation
- No sudo needed
- Widely used by journals

**For long-term workflow**: Install **LaTeX locally** (Option 2A)
- One-time setup
- Professional workflow
- Offline capable

**For automation**: Use **GitHub Actions** (Option 3)
- Best for continuous delivery
- No manual compilation

---

## CURRENT STATUS

- ❌ Local LaTeX: Not installed (sudo required)
- ❌ Docker LaTeX: Not verified
- ✅ Overleaf: Available immediately
- ✅ GitHub Actions: Can be set up

**Next action**: Create ZIP for Overleaf upload.
