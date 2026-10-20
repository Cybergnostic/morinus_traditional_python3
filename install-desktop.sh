#!/bin/sh
# Adds Morinus to the desktop application menu for the current user,
# running it from this folder (with the environment set up by install.sh).
# Remove with: install-desktop.sh --uninstall
set -e

DIR=$(cd "$(dirname "$0")" && pwd)
APPS=${XDG_DATA_HOME:-$HOME/.local/share}/applications
FILE=$APPS/morinus.desktop
OLD=$APPS/morinus-traditional.desktop	# the name of earlier versions

if [ "$1" = "--uninstall" ]; then
	rm -f "$FILE" "$OLD"
	echo "Removed $FILE"
	exit 0
fi

mkdir -p "$APPS"
rm -f "$OLD"
cat > "$FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Morinus
Comment=Traditional astrology (Morinus 6.2 with added traditional tools)
Exec="$DIR/morinus"
Path=$DIR
Icon=$DIR/Res/morinus-icon.png
Terminal=false
Categories=Education;Science;Astronomy;
EOF

command -v update-desktop-database >/dev/null && update-desktop-database "$APPS" 2>/dev/null || true
echo "Installed $FILE"
