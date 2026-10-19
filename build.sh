#!/bin/sh
# Builds the Swiss Ephemeris extension (sweastrology) next to morinus.py.
# Needs a C compiler, the Python headers (python3-dev) and setuptools.
set -e

cd "$(dirname "$0")"
PYTHON=${PYTHON:-python3}
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

cd SWEP/src
# the bundled Swiss Ephemeris sources predate current compiler warnings
CFLAGS=${CFLAGS--w} "$PYTHON" setup.py -q build_ext --build-lib ../.. --build-temp "$TMP"
rm -rf sweastrology.egg-info
cd ../..

"$PYTHON" -c "import sweastrology; print('sweastrology built, Swiss Ephemeris', sweastrology.swe_version())"
