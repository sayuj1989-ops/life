# Zenodo DOI Setup Instructions

## What Zenodo Provides
Permanent DOI (Digital Object Identifier) for code/data repository, required for Data Availability statement in manuscript.

## Steps to Complete

### 1. Push Changes to GitHub (Manual Authentication Required)
The publication-ready changes are committed locally with tag `v1.0.0-submission`. You need to push them:

```bash
cd /home/sayuj/life

# Configure git credentials if needed
git config --global credential.helper store

# Push commit and tag
git push origin main
git push origin v1.0.0-submission
```

If prompted for credentials, use your GitHub personal access token (not password).

### 2. Link Repository to Zenodo

1. **Go to Zenodo**: https://zenodo.org/
2. **Log in** with GitHub account
3. **Navigate to**: Settings → GitHub (or direct: https://zenodo.org/account/settings/github/)
4. **Find repository**: `sayujks0071/life` in the list
5. **Toggle ON** the slider next to the repository
6. **Refresh** if repository doesn't appear (may take a few minutes)

### 3. Create GitHub Release

1. **Go to repository**: https://github.com/sayujks0071/life
2. **Click**: "Releases" (right sidebar)
3. **Click**: "Draft a new release"
4. **Select tag**: `v1.0.0-submission` (should appear in dropdown)
5. **Release title**: "v1.0.0: Spine Deformity Journal Submission"
6. **Description**: Copy from tag message:

```
Manuscript: Biological Countercurvature of Spacetime: An Information-Cosserat Framework for Spinal Geometry

Key achievements:
- Publication-ready word count: ~5,550 words (target: ~5,000)
- Clinical accessibility: Abstract, figures, Theory/Methods condensed
- Quantitative predictions: L_crit=0.35m→ages 11-12, Cobb r=0.983
- Cross-species validation: 18 vertebrates, humans in Allometric Trap
- Validation test infrastructure: Fixed bugs, 21 simulations successful
- Required statements: Ethics, funding, competing interests complete

Targeting: Springer Spine Deformity / European Spine Journal
Submission date: 2026-05-05

This release enables Zenodo DOI generation for data availability statement.
```

7. **Click**: "Publish release"

### 4. Verify Zenodo Archive

1. **Wait ~5 minutes** after GitHub release
2. **Go to**: https://zenodo.org/account/settings/github/
3. **Find your release**: Should show under `sayujks0071/life`
4. **Click**: The Zenodo badge/link
5. **Copy the DOI**: Format will be `10.5281/zenodo.XXXXXXX`

### 5. Update Manuscript Data Availability Statement

Edit `manuscript/sections/availability.tex`:

**Current text:**
```latex
The release code and generated artifacts are tracked in this repository; the corresponding Zenodo archival DOI will be added once the deposition is finalized.
```

**Replace with:**
```latex
The release code and generated artifacts are tracked in this repository and permanently archived at Zenodo with DOI: \href{https://doi.org/10.5281/zenodo.XXXXXXX}{10.5281/zenodo.XXXXXXX}.
```

Replace `XXXXXXX` with your actual Zenodo DOI number.

### 6. Commit DOI Update

```bash
git add manuscript/sections/availability.tex
git commit -m "Add Zenodo DOI to data availability statement

DOI: 10.5281/zenodo.XXXXXXX

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
git push origin main
```

## Alternative: Manual Zenodo Upload (If GitHub Integration Fails)

1. **Go to**: https://zenodo.org/
2. **Click**: "New Upload"
3. **Upload**: Download GitHub repository as ZIP, upload to Zenodo
4. **Fill metadata**:
   - Title: "Biological Countercurvature of Spacetime: Code and Data"
   - Authors: Dr. Sayuj Krishnan S.
   - Description: "Code repository for manuscript submitted to Spine Deformity journal..."
   - Keywords: Scoliosis, Adolescent Idiopathic Scoliosis, Biomechanics, Computational Model
   - License: MIT
5. **Publish**: Zenodo will generate DOI immediately

## Troubleshooting

### Repository Not Appearing in Zenodo
- **Wait 10-15 minutes** after enabling the toggle
- **Ensure repository is public** on GitHub
- Try disabling and re-enabling the Zenodo integration

### Tag Not Creating Release
- Tags must be pushed: `git push origin --tags`
- Check tag exists: `git tag -l`
- Verify tag is on remote: `git ls-remote --tags origin`

### GitHub Authentication Issues
- Generate new Personal Access Token: GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
- Scopes needed: `repo` (full control)
- Use token as password when git prompts

## Why This Matters for Publication

Springer journals **require** permanent archival of code/data with a citable DOI. The Data Availability statement must include:
1. Where code is hosted (GitHub)
2. Permanent archive with DOI (Zenodo)
3. License information (MIT)

Without a DOI, the manuscript may be returned without review or receive a request for revision before acceptance.

## Current Status

- ✅ Changes committed locally with tag `v1.0.0-submission`
- ⏳ Push to GitHub (requires your authentication)
- ⏳ Link to Zenodo
- ⏳ Create GitHub release (triggers Zenodo archive)
- ⏳ Update manuscript with DOI

**Estimated time**: 15-20 minutes after you authenticate the git push.
