# GitHub Setup & Deployment Guide

This guide will help you push the IEC project to GitHub and set up documentation preview.

## ✅ What's Already Done

- ✅ Git repository initialized
- ✅ All files committed (27 files, 4513+ lines)
- ✅ Ready for GitHub push

---

## 📝 Step 1: Create GitHub Repository

### Option A: Via GitHub Web Interface (Recommended)

1. **Go to GitHub:**
   - Navigate to https://github.com/new
   - Or click your profile → "Your repositories" → "New"

2. **Repository Settings:**
   ```
   Repository name: spinalmodes-iec
   Description: Information-Elasticity Coupling (IEC) model for spinal biomechanics research
   Visibility: ○ Public  ○ Private  (choose based on preference)
   
   ⚠️ IMPORTANT: Do NOT initialize with:
   - ❌ README
   - ❌ .gitignore  
   - ❌ License
   (We already have all these files)
   ```

3. **Click "Create repository"**

### Option B: Via GitHub CLI (if installed)

```bash
gh repo create spinalmodes-iec --public --description "IEC model for spinal biomechanics" --source=. --remote=origin --push
```

---

## 🚀 Step 2: Push to GitHub

After creating the repository on GitHub, you'll see instructions. Use these commands:

### Commands to Run:

```bash
cd /Users/dr.sayujkrishnan/LIFE

# Add GitHub remote (replace YOUR-USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/spinalmodes-iec.git

# Verify remote was added
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### Example:
If your GitHub username is `drsayujkrishnan`, the command would be:
```bash
git remote add origin https://github.com/drsayujkrishnan/spinalmodes-iec.git
```

---

## 📖 Step 3: Set Up GitHub Pages (Documentation Preview)

### Enable GitHub Pages:

1. **Go to your repository on GitHub:**
   - https://github.com/YOUR-USERNAME/spinalmodes-iec

2. **Navigate to Settings:**
   - Click "Settings" tab (top right)

3. **Go to Pages:**
   - Click "Pages" in left sidebar (under "Code and automation")

4. **Configure Source:**
   ```
   Source: GitHub Actions
   ```
   (This will use the CI workflow to deploy docs)

### Add GitHub Pages Deployment to CI:

Add this to `.github/workflows/ci.yml` (after the test job):

```yaml
  deploy-docs:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    permissions:
      contents: read
      pages: write
      id-token: write
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
    
    - name: Install dependencies
      run: poetry install
    
    - name: Build MkDocs site
      run: poetry run mkdocs build
    
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v2
      with:
        path: ./site
    
    - name: Deploy to GitHub Pages
      uses: actions/deploy-pages@v2
```

---

## 🔗 Step 4: Access Your Sites

After setup, you'll have:

### 1. **Repository:**
```
https://github.com/YOUR-USERNAME/spinalmodes-iec
```

### 2. **GitHub Pages Documentation:**
```
https://YOUR-USERNAME.github.io/spinalmodes-iec/
```

### 3. **Raw Manuscript:**
```
https://github.com/YOUR-USERNAME/spinalmodes-iec/blob/main/docs/manuscript/SpinalCountercurvature_IEC.md
```

---

## 🎨 Quick Preview Option (No GitHub Pages)

If you want an immediate local preview before deploying:

```bash
cd /Users/dr.sayujkrishnan/LIFE

# Install dependencies
poetry install

# Serve documentation locally
poetry run mkdocs serve

# Open browser to: http://127.0.0.1:8000
```

This creates a live-reloading preview of your documentation site.

---

## 🔧 Alternative: Deploy to Netlify (Instant Preview)

For a quick public preview without GitHub Pages:

### Via Netlify CLI:

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Build docs:**
   ```bash
   cd /Users/dr.sayujkrishnan/LIFE
   poetry install
   poetry run mkdocs build
   ```

3. **Deploy:**
   ```bash
   netlify deploy --dir=site --prod
   ```

4. **Follow prompts:**
   - Authorize with Netlify
   - Choose "Create & configure a new site"
   - Get instant URL: `https://random-name.netlify.app`

### Via Netlify Web:

1. Go to https://app.netlify.com/drop
2. Build docs: `poetry run mkdocs build`
3. Drag the `site/` folder to the drop zone
4. Get instant preview URL

---

## 📋 Complete Setup Script

Save this as `setup_github.sh`:

```bash
#!/bin/bash
set -e

echo "🚀 Setting up GitHub repository for spinalmodes-iec"
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Not in project root directory"
    exit 1
fi

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Error: GitHub username is required"
    exit 1
fi

echo ""
echo "📝 GitHub username: $GITHUB_USERNAME"
echo "📦 Repository name: spinalmodes-iec"
echo ""
read -p "Press Enter to continue, or Ctrl+C to cancel..."

# Add remote
echo "🔗 Adding GitHub remote..."
git remote add origin "https://github.com/$GITHUB_USERNAME/spinalmodes-iec.git" || echo "Remote already exists"

# Show remotes
echo ""
echo "📍 Current remotes:"
git remote -v

# Push to GitHub
echo ""
read -p "Push to GitHub now? (y/n): " PUSH_NOW

if [ "$PUSH_NOW" = "y" ]; then
    echo "⬆️  Pushing to GitHub..."
    git branch -M main
    git push -u origin main
    
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🔗 View your repository:"
    echo "   https://github.com/$GITHUB_USERNAME/spinalmodes-iec"
    echo ""
    echo "📖 Next steps:"
    echo "   1. Enable GitHub Pages in repository Settings → Pages"
    echo "   2. Set source to 'GitHub Actions'"
    echo "   3. Docs will be at: https://$GITHUB_USERNAME.github.io/spinalmodes-iec/"
else
    echo ""
    echo "⏸️  Skipping push. Run this when ready:"
    echo "   git push -u origin main"
fi

echo ""
echo "🎉 Setup complete!"
```

**Make executable and run:**
```bash
chmod +x setup_github.sh
./setup_github.sh
```

---

## 🐛 Troubleshooting

### Issue: "remote origin already exists"

**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/spinalmodes-iec.git
```

### Issue: Authentication failed

**Solution 1 - Use Personal Access Token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic) with `repo` scope
3. Use token as password when pushing

**Solution 2 - Use GitHub CLI:**
```bash
brew install gh  # macOS
gh auth login
git push -u origin main
```

### Issue: Push rejected (non-fast-forward)

**Solution:**
```bash
# If you're sure you want to overwrite
git push -u origin main --force

# Or fetch first and merge
git pull origin main --rebase
git push -u origin main
```

### Issue: Large files warning

**Solution:**
The project doesn't have large files, but if you add outputs:
```bash
# Add to .gitignore
echo "outputs/*.png" >> .gitignore
echo "outputs/*.csv" >> .gitignore
git rm --cached outputs/figs/*.png
git commit -m "chore: Remove generated outputs from git"
```

---

## 📊 Repository Settings Recommendations

After pushing, configure these in GitHub repository settings:

### General:
- ✅ Add topics: `biomechanics`, `developmental-biology`, `computational-biology`, `spine`, `python`
- ✅ Add website: Your GitHub Pages URL
- ✅ Enable Issues for bug reports
- ✅ Enable Discussions for Q&A

### Branches:
- ✅ Set `main` as default branch
- ✅ Enable branch protection for `main`:
  - Require PR reviews before merging
  - Require status checks (CI) to pass

### Actions:
- ✅ Allow all actions (for CI/CD)
- ✅ Enable workflow permissions:
  - Read and write permissions

### Pages:
- ✅ Source: GitHub Actions
- ✅ Custom domain (optional): Add if you have one

---

## 🎯 Quick Commands Reference

```bash
# View current remotes
git remote -v

# Add GitHub remote
git remote add origin https://github.com/USERNAME/spinalmodes-iec.git

# Push to GitHub
git push -u origin main

# View commit history
git log --oneline

# Check repository status
git status

# Create new branch for development
git checkout -b feature/new-analysis

# Generate local docs preview
poetry run mkdocs serve
```

---

## 📱 Sharing Your Work

Once pushed, share these links:

### For Collaborators:
- Repository: `https://github.com/YOUR-USERNAME/spinalmodes-iec`
- Clone command: `git clone https://github.com/YOUR-USERNAME/spinalmodes-iec.git`

### For Reviewers:
- Manuscript: `https://github.com/YOUR-USERNAME/spinalmodes-iec/blob/main/docs/manuscript/SpinalCountercurvature_IEC.md`
- Documentation: `https://YOUR-USERNAME.github.io/spinalmodes-iec/`

### For Users:
- Installation: Point to README:
  ```
  pip install git+https://github.com/YOUR-USERNAME/spinalmodes-iec.git
  ```
  (After publishing to PyPI, this becomes: `pip install spinalmodes`)

---

## 🌟 Making Repository Discoverable

### Add a DOI with Zenodo:

1. Go to https://zenodo.org/
2. Link your GitHub account
3. Enable the repository
4. Create a release on GitHub
5. Zenodo automatically archives and assigns DOI

### Add to PyPI (Python Package Index):

```bash
# Build package
poetry build

# Publish to PyPI
poetry publish

# Now users can install with:
# pip install spinalmodes
```

---

## ✅ Post-Push Checklist

After pushing to GitHub:

- [ ] Repository is public/private as intended
- [ ] README displays correctly
- [ ] CI workflow passes (green checkmark)
- [ ] GitHub Pages enabled and deploying
- [ ] Topics/tags added to repository
- [ ] Repository description is clear
- [ ] License file is visible
- [ ] Clone and test from fresh location:
  ```bash
  cd /tmp
  git clone https://github.com/YOUR-USERNAME/spinalmodes-iec.git
  cd spinalmodes-iec
  poetry install
  make green
  ```

---

**Questions?** See `DELIVERABLES_CHECKLIST.md` for full project overview.

**Next Steps:** After pushing, review `PROJECT_SUMMARY.md` for complete project details.

