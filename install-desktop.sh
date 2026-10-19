#!/bin/sh
# Adds Morinus to the desktop application menu for the current user,
# running it from this folder. Remove with: install-desktop.sh --uninstall
set -e

DIR=$(cd "$(dirname "$0")" && pwd)
APPS=${XDG_DATA_HOME:-$HOME/.local/share}/applications
FILE=$APPS/morinus.desktop

if [ "$1" = "--uninstall" ]; then
	rm -f "$FILE"
	echo "Removed $FILE"
	exit 0
fi

mkdir -p "$APPS"
cat > "$FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Morinus
Comment=Astrology program
Exec=python3 "$DIR/morinus.py"
Path=$DIR
Icon=$DIR/Res/morinus-icon.png
Terminal=false
Categories=Education;Science;Astronomy;
EOF

command -v update-desktop-database >/dev/null && update-desktop-database "$APPS" 2>/dev/null || true
echo "Installed $FILE"
