#!/usr/bin/env bash
set -e

echo "=== Installing Dinoscreener for Linux ==="

INSTALL_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

mkdir -p "$INSTALL_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy binary
if [ -f "$SCRIPT_DIR/dinoscreener" ]; then
    cp "$SCRIPT_DIR/dinoscreener" "$INSTALL_DIR/dinoscreener"
    chmod +x "$INSTALL_DIR/dinoscreener"
    echo "✓ Installed binary to $INSTALL_DIR/dinoscreener"
elif [ -f "$SCRIPT_DIR/dinoscreener-linux-x86_64" ]; then
    cp "$SCRIPT_DIR/dinoscreener-linux-x86_64" "$INSTALL_DIR/dinoscreener"
    chmod +x "$INSTALL_DIR/dinoscreener"
    echo "✓ Installed binary to $INSTALL_DIR/dinoscreener"
fi

# Copy icon
if [ -f "$SCRIPT_DIR/app_icon.png" ]; then
    cp "$SCRIPT_DIR/app_icon.png" "$ICON_DIR/dinoscreener.png"
    echo "✓ Installed icon to $ICON_DIR/dinoscreener.png"
fi

# Copy desktop entry
if [ -f "$SCRIPT_DIR/dinoscreener.desktop" ]; then
    cp "$SCRIPT_DIR/dinoscreener.desktop" "$DESKTOP_DIR/dinoscreener.desktop"
    echo "✓ Installed desktop entry to $DESKTOP_DIR/dinoscreener.desktop"
fi

command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$DESKTOP_DIR" || true
command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" || true

echo "=== Installation Complete! ==="
echo "You can launch Dinoscreener from your Application Menu or run 'dinoscreener' in terminal."
echo "Ensure $HOME/.local/bin is in your PATH."
