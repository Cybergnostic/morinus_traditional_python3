#!/bin/sh
# Sets Morinus up to run from this folder: a virtual environment in .venv
# that uses your distribution's wxPython and Pillow and adds timezonefinder,
# the Swiss Ephemeris module, the offline atlas (downloaded from GeoNames)
# and an entry in the application menu. Run it again after updating;
# ./install.sh --update-atlas also downloads the latest atlas.
# Nothing is installed outside this folder
# except the menu entry (remove it with: ./install-desktop.sh --uninstall).
set -e

cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
	python3 -m venv --system-site-packages .venv
fi
if ! .venv/bin/python -c "import wx, PIL" 2>/dev/null; then
	echo "wxPython or Pillow is missing: install them with your package manager (see README.md)." >&2
	exit 1
fi
.venv/bin/python -m pip install -q --disable-pip-version-check "timezonefinder>=6,<9"
PYTHON="$PWD/.venv/bin/python" ./build.sh
if [ ! -f Res/atlas.db ] || [ "$1" = "--update-atlas" ]; then
	.venv/bin/python tools/build_atlas.py ||
		echo "Could not get the atlas (the online search still works); try again with ./install.sh --update-atlas" >&2
fi
./install-desktop.sh
echo "Start Morinus from the application menu or with ./morinus"
