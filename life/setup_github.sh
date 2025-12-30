#!/bin/bash
set -e

echo "🚀 GitHub Setup for spinalmodes-iec"
echo "===================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Not in project root directory"
    echo "   Please cd to /Users/dr.sayujkrishnan/LIFE first"
    exit 1
fi

echo "✅ Project root verified"
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Error: GitHub username is required"
    exit 1
fi

REPO_NAME="spinalmodes-iec"
REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo ""
echo "📝 Configuration:"
echo "   GitHub username: $GITHUB_USERNAME"
echo "   Repository name: $REPO_NAME"
echo "   Repository URL:  $REPO_URL"
echo ""
echo "⚠️  IMPORTANT: Make sure you've created the repository on GitHub first!"
echo "   Go to: https://github.com/new"
echo "   Repository name: $REPO_NAME"
echo "   DO NOT initialize with README, .gitignore, or license"
echo ""
read -p "Have you created the repository on GitHub? (y/n): " REPO_CREATED

if [ "$REPO_CREATED" != "y" ]; then
    echo ""
    echo "📋 Steps to create repository:"
    echo "   1. Go to https://github.com/new"
    echo "   2. Repository name: $REPO_NAME"
    echo "   3. Description: Information-Elasticity Coupling (IEC) model for spinal biomechanics"
    echo "   4. Choose Public or Private"
    echo "   5. ❌ Do NOT check any boxes (no README, .gitignore, or license)"
    echo "   6. Click 'Create repository'"
    echo "   7. Run this script again"
    exit 0
fi

# Check if remote already exists
if git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  Remote 'origin' already exists"
    CURRENT_REMOTE=$(git remote get-url origin)
    echo "   Current URL: $CURRENT_REMOTE"
    echo ""
    read -p "Remove and re-add remote? (y/n): " REMOVE_REMOTE
    
    if [ "$REMOVE_REMOTE" = "y" ]; then
        echo "🔄 Removing existing remote..."
        git remote remove origin
    else
        echo "ℹ️  Keeping existing remote"
    fi
fi

# Add remote
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Adding GitHub remote..."
    git remote add origin "$REPO_URL"
    echo "✅ Remote added"
else
    echo "✅ Using existing remote"
fi

echo ""
echo "📍 Current remotes:"
git remote -v

# Check git status
echo ""
echo "📊 Git status:"
git status --short

# Push to GitHub
echo ""
read -p "Push to GitHub now? (y/n): " PUSH_NOW

if [ "$PUSH_NOW" = "y" ]; then
    echo ""
    echo "⬆️  Pushing to GitHub..."
    git branch -M main
    
    if git push -u origin main; then
        echo ""
        echo "🎉 Successfully pushed to GitHub!"
        echo ""
        echo "🔗 Your repository:"
        echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME"
        echo ""
        echo "📖 Setup GitHub Pages for documentation preview:"
        echo "   1. Go to: https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/pages"
        echo "   2. Under 'Build and deployment':"
        echo "      Source: Deploy from a branch"
        echo "      Branch: gh-pages (will be created automatically)"
        echo "   3. Or use GitHub Actions (recommended) - see GITHUB_SETUP.md"
        echo ""
        echo "📄 View manuscript:"
        echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME/blob/main/docs/manuscript/SpinalCountercurvature_IEC.md"
        echo ""
        echo "🌐 After enabling Pages, docs will be at:"
        echo "   https://$GITHUB_USERNAME.github.io/$REPO_NAME/"
        echo ""
        echo "📦 Clone command for collaborators:"
        echo "   git clone https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    else
        echo ""
        echo "❌ Push failed"
        echo ""
        echo "Common solutions:"
        echo "   1. Authentication issue:"
        echo "      Use Personal Access Token or GitHub CLI (gh auth login)"
        echo "   2. Repository not created:"
        echo "      Create at https://github.com/new"
        echo "   3. Check GITHUB_SETUP.md for detailed troubleshooting"
        exit 1
    fi
else
    echo ""
    echo "⏸️  Push skipped"
    echo ""
    echo "When ready to push, run:"
    echo "   git push -u origin main"
fi

echo ""
echo "✨ Next steps:"
echo "   1. Enable GitHub Pages (see above)"
echo "   2. Add topics in repository settings"
echo "   3. Review GITHUB_SETUP.md for full deployment guide"
echo "   4. Share repository link with collaborators"
echo ""
echo "🎯 Done!"

