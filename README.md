# Morinus 6.2 for Python 3

The traditional Morinus astrology program — version 6.2 as released for Windows
in March 2014 — ported to Python 3 and wxPython 4 so it runs natively on Linux.
Nothing is added: this is the program as it was, on a modern Python.

Morinus was written by Robert Nagy and is free software under the GNU GPL v3.

Additional traditional-astrology tools (planetary conditions, reception,
temperament, lunar returns of the solar year, steppers, duads on bi-wheels,
unlimited lots with a Day/Night selector, automatic time zones) are on the
[`traditional`](../../tree/traditional) branch.

## What's in it

Charts with clickable planets showing their aspects and orbs, the seven
traditional planets, tables (positions, almutens, antiscia, aspects, fixed
stars, lots, planetary hours, firdaria, profections, primary directions…),
revolutions, transits, syzygy charts, heliocentric charts, elections,
dodecatemoria, the user speculum, default location and menu selection.

## Install

You need Python 3.10 or newer, wxPython 4.2, Pillow, and a C compiler with the
Python headers for the Swiss Ephemeris module:

| Distribution    | Command |
|-----------------|---------|
| Debian / Ubuntu | `sudo apt install python3-wxgtk4.0 python3-pil python3-dev python3-setuptools gcc` |
| Fedora          | `sudo dnf install python3-wxpython4 python3-pillow python3-devel python3-setuptools gcc` |
| Arch            | `sudo pacman -S python-wxpython python-pillow python-setuptools gcc` |

Then:

```sh
./build.sh            # compiles the Swiss Ephemeris module (once)
python3 morinus.py
./install-desktop.sh  # optional: adds "Morinus 2014" to the application menu
```

Morinus runs from its folder, which must be writable: settings are kept in
`Opts/`, charts in `Hors/`, and your place list in `Res/placedb.dat` (the
shipped list is `Res/placedb-default.dat`). None of these are tracked by git.

The Swiss Ephemeris data files in `SWEP/Ephem/` give full precision from
5400 BC to 5400 AD.

### Coming from the Windows version

Copy your `.opt` files into `Opts/`, your charts into `Hors/` and your
`placedb.dat` into `Res/`. Charts, settings and the place list load unchanged,
and files saved here can still be opened by the Windows program.

## How this version was made

No source code was published for the 2014 Windows build, so it was recovered
from `morinus.exe`, a PyInstaller bundle of Python 2.7 bytecode:

1. The 164 Morinus modules were extracted and decompiled. Every module was
   recompiled with Python 2.7 and compared with the original bytecode:
   148 are byte-identical; the other 16 differ only in unreachable code,
   constant-table order or compiler optimisations. Eighteen functions in
   which the decompiler had misplaced statements were corrected until their
   bytecode matched the original. Thirteen modules unchanged since the public
   2012 source use that source with its comments; elsewhere the original
   comments could not be recovered.
2. The recovered program was run under Python 2.7 to produce reference results
   (`tests/reference/py2.json.gz`), then ported to Python 3, wxPython 4 and
   Pillow. The port reproduces every reference value; integer divisions whose
   meaning changed in Python 3 were found by tracing the program under
   Python 2's `-Qwarnall` and by instrumenting the GUI.

The first commit is the recovered Python 2 program.

## Known issues

- Saving primary directions as text fails for the Campanian method: the
  export has no name for it. This is in the original program and is left
  as is.
- On Linux the chart notes field has no length limit (GTK cannot enforce one).

Fixed from the original: Placidian under-the-pole directions from transit and
revolution windows (a misspelt attribute stopped the calculation), and
uninitialised string buffers in the Swiss Ephemeris module.

## Tests

```sh
python3 tests/refdump.py . /tmp/py3.json                         # with default settings (empty Opts/)
python3 tests/refcompare.py tests/reference/py2.json.gz /tmp/py3.json
xvfb-run python3 tests/guismoke.py /path/to/copy /tmp/smoke [--variant 1|2|3]
```

`refdump.py` computes a set of charts and dumps every value; `refcompare.py`
compares them with the Python 2 reference. `guismoke.py` opens a chart and
triggers every menu command and popup-menu item (run it on a copy of the
folder, since it saves options).

## Credits and licences

- Morinus — Robert Nagy, GNU GPL v3 (`LICENSE`).
- Swiss Ephemeris 1.76 — Astrodienst AG (`SWEP/src/LICENSE`).
