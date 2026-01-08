#!/bin/bash
# Script to move LM Studio to /Applications directory
# This fixes the macOS security restriction that prevents running apps from Downloads

set -e

APP_NAME="LM Studio"
APP_NAME_ALT="LM Studio.app"
APPLICATIONS_DIR="/Applications"
DOWNLOADS_DIR="$HOME/Downloads"
DESKTOP_DIR="$HOME/Desktop"

echo "🔍 Searching for LM Studio application..."

# Function to check if app exists and move it
move_app() {
    local app_path="$1"
    if [ -d "$app_path" ] && [ -f "$app_path/Contents/Info.plist" ]; then
        echo "✅ Found LM Studio at: $app_path"
        
        # Check if already in Applications
        if [ "$(dirname "$app_path")" = "$APPLICATIONS_DIR" ]; then
            echo "✅ LM Studio is already in /Applications!"
            exit 0
        fi
        
        # Check if app already exists in Applications
        if [ -d "$APPLICATIONS_DIR/$APP_NAME_ALT" ]; then
            echo "⚠️  LM Studio already exists in /Applications"
            read -p "Do you want to replace it? (y/n): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                echo "❌ Installation cancelled"
                exit 1
            fi
            echo "🗑️  Removing existing installation..."
            rm -rf "$APPLICATIONS_DIR/$APP_NAME_ALT"
        fi
        
        echo "📦 Moving LM Studio to /Applications..."
        sudo mv "$app_path" "$APPLICATIONS_DIR/$APP_NAME_ALT"
        
        # Fix permissions
        echo "🔧 Fixing permissions..."
        sudo chown -R "$USER:staff" "$APPLICATIONS_DIR/$APP_NAME_ALT"
        sudo chmod -R 755 "$APPLICATIONS_DIR/$APP_NAME_ALT"
        
        echo "✅ Successfully moved LM Studio to /Applications!"
        echo "🚀 You can now launch LM Studio from /Applications or Spotlight"
        exit 0
    fi
}

# Search common locations
echo "Checking Downloads folder..."
find "$DOWNLOADS_DIR" -maxdepth 3 -type d -name "$APP_NAME_ALT" 2>/dev/null | while read -r app; do
    move_app "$app"
done

echo "Checking Desktop folder..."
find "$DESKTOP_DIR" -maxdepth 2 -type d -name "$APP_NAME_ALT" 2>/dev/null | while read -r app; do
    move_app "$app"
done

# Check for mounted DMG files
echo "Checking for mounted disk images..."
for dmg_vol in /Volumes/*; do
    if [ -d "$dmg_vol/$APP_NAME_ALT" ]; then
        echo "✅ Found LM Studio in mounted disk image: $dmg_vol"
        move_app "$dmg_vol/$APP_NAME_ALT"
    fi
done

# If not found, provide manual instructions
echo ""
echo "❌ Could not automatically find LM Studio application"
echo ""
echo "📋 Manual installation steps:"
echo "   1. Open Finder"
echo "   2. Navigate to your Downloads folder (or wherever you downloaded LM Studio)"
echo "   3. If it's a .dmg file, double-click to mount it"
echo "   4. Find the 'LM Studio.app' file"
echo "   5. Drag and drop it into the /Applications folder"
echo "   6. If prompted, enter your password"
echo ""
echo "Alternatively, you can run:"
echo "   sudo mv '/path/to/LM Studio.app' /Applications/"
echo "   sudo chown -R \$USER:staff /Applications/LM\ Studio.app"

exit 1





