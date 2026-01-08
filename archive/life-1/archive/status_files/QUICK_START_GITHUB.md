# 🚀 Quick Start: Push to GitHub

**Time:** 5 minutes  
**Current Status:** ✅ Repository initialized and committed locally

---

## Option 1: Automated Setup (Easiest)

Run the setup script that will guide you through the process:

```bash
cd /Users/dr.sayujkrishnan/LIFE
./setup_github.sh
```

Follow the prompts to:
1. Enter your GitHub username
2. Confirm repository creation
3. Push to GitHub

---

## Option 2: Manual Setup (Step by Step)

### Step 1: Create GitHub Repository (2 minutes)

1. Go to: **https://github.com/new**

2. Fill in:
   - **Repository name:** `spinalmodes-iec`
   - **Description:** `Information-Elasticity Coupling (IEC) model for spinal biomechanics research`
   - **Visibility:** Choose Public or Private
   - **⚠️ IMPORTANT:** Do NOT check any boxes (no README, .gitignore, or license)

3. Click **"Create repository"**

### Step 2: Push Your Code (2 minutes)

Replace `YOUR-USERNAME` with your actual GitHub username:

```bash
cd /Users/dr.sayujkrishnan/LIFE

# Add GitHub as remote
git remote add origin https://github.com/YOUR-USERNAME/spinalmodes-iec.git

# Push to GitHub
git push -u origin main
```

**Example:** If your username is `drsayujkrishnan`:
```bash
git remote add origin https://github.com/drsayujkrishnan/spinalmodes-iec.git
git push -u origin main
```

### Step 3: Enable GitHub Pages (1 minute)

1. Go to your repository: `https://github.com/YOUR-USERNAME/spinalmodes-iec`

2. Click **Settings** → **Pages** (in left sidebar)

3. Under "Build and deployment":
   - **Source:** Select "GitHub Actions"

4. Click **Save**

5. Wait ~2 minutes for deployment

6. Your docs will be at: `https://YOUR-USERNAME.github.io/spinalmodes-iec/`

---

## 🎯 What You'll Get

After completing the above:

### 1. GitHub Repository
```
https://github.com/YOUR-USERNAME/spinalmodes-iec
```
- Full source code
- Commit history
- Issue tracking
- Collaboration tools

### 2. Documentation Site (GitHub Pages)
```
https://YOUR-USERNAME.github.io/spinalmodes-iec/
```
- Beautiful MkDocs site
- Full manuscript online
- CLI reference
- Figure guides

### 3. Raw Manuscript
```
https://github.com/YOUR-USERNAME/spinalmodes-iec/blob/main/docs/manuscript/SpinalCountercurvature_IEC.md
```
- Readable on GitHub
- Formatted markdown
- Direct link for sharing

---

## 🔧 Troubleshooting

### Problem: "Authentication failed"

**Solution 1 - Personal Access Token:**
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: "spinalmodes-iec"
4. Check `repo` scope
5. Click "Generate token"
6. Copy the token
7. Use as password when pushing

**Solution 2 - GitHub CLI (Recommended):**
```bash
# Install GitHub CLI
brew install gh  # macOS

# Authenticate
gh auth login

# Push
git push -u origin main
```

### Problem: "remote origin already exists"

**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/spinalmodes-iec.git
git push -u origin main
```

### Problem: "Repository not found"

**Solution:**
- Make sure you created the repository on GitHub first
- Check your username is correct
- Verify repository name is exactly: `spinalmodes-iec`

---

## ✅ Verification Checklist

After pushing, verify:

- [ ] Repository visible at `https://github.com/YOUR-USERNAME/spinalmodes-iec`
- [ ] README displays correctly
- [ ] 27 files showing in repository
- [ ] CI badge (may be yellow initially, should turn green)
- [ ] GitHub Pages deploying (check Actions tab)
- [ ] Docs site accessible (after ~2 minutes)

---

## 📱 Share Your Work

Once pushed, share these links:

### For Manuscript Reviewers:
```
https://github.com/YOUR-USERNAME/spinalmodes-iec/blob/main/docs/manuscript/SpinalCountercurvature_IEC.md
```

### For Documentation Readers:
```
https://YOUR-USERNAME.github.io/spinalmodes-iec/
```

### For Developers:
```
git clone https://github.com/YOUR-USERNAME/spinalmodes-iec.git
```

---

## 🎨 Preview Options

### Local Preview (Instant)

No GitHub needed - preview docs locally:

```bash
cd /Users/dr.sayujkrishnan/LIFE
poetry install
poetry run mkdocs serve
```

Open: http://127.0.0.1:8000

### Netlify Drop (30 seconds, no account needed)

1. Build docs:
   ```bash
   poetry run mkdocs build
   ```

2. Go to: https://app.netlify.com/drop

3. Drag the `site/` folder

4. Get instant URL: `https://random-name.netlify.app`

---

## 📊 Repository Settings (Optional)

After pushing, enhance your repository:

### Add Topics:
- Go to repository main page
- Click gear icon next to "About"
- Add topics: `biomechanics`, `developmental-biology`, `python`, `spine`, `iec-model`

### Add Website:
- Same location as topics
- Add your GitHub Pages URL: `https://YOUR-USERNAME.github.io/spinalmodes-iec/`

### Enable Discussions:
- Settings → General → Features
- Check "Discussions"
- Great for Q&A with users

---

## 🌟 Next Steps

After successful push:

1. **Verify CI Passes:**
   - Go to "Actions" tab
   - Check that CI workflow completes successfully (green checkmark)

2. **Review GitHub Pages:**
   - Wait ~2 minutes for deployment
   - Visit your documentation site
   - Verify all pages load correctly

3. **Share with Team:**
   - Send repository link to collaborators
   - Add them as collaborators in Settings → Collaborators

4. **Create Release (Optional):**
   - Go to Releases
   - Click "Create a new release"
   - Tag: `v0.1.0`
   - Title: "Initial IEC Model Release"
   - Publish release

5. **Add DOI (Optional):**
   - Link repository to Zenodo
   - Get permanent DOI for citations

---

## 🆘 Need Help?

- **Detailed Guide:** See `GITHUB_SETUP.md`
- **Project Overview:** See `PROJECT_SUMMARY.md`
- **Technical Issues:** See `SETUP_AND_EXECUTION.md`

---

**Ready? Run `./setup_github.sh` to begin!** 🚀

