# Morinus 6.2 (2014 Windows build) on Linux

This is the Morinus version that shipped as `morinus.exe` in March 2014 —
with firdaria, lots, heliocentric charts, dodecatemoria, the user speculum,
default location and menu selection — ported to Python 3 and wxPython 4 so it
runs natively on Linux.

No public source exists for this build, so the code was recovered from the
executable (see *How the source was recovered* below).

## Requirements

- Python 3.10 or newer
- wxPython 4.2 and Pillow
- a C compiler and the Python headers, to build the Swiss Ephemeris module

| Distribution    | Command |
|-----------------|---------|
| Debian / Ubuntu | `sudo apt install python3-wxgtk4.0 python3-pil python3-dev python3-setuptools gcc` |
| Fedora          | `sudo dnf install python3-wxpython4 python3-pillow python3-devel python3-setuptools gcc` |
| Arch            | `sudo pacman -S python-wxpython python-pillow python-setuptools gcc` |

## Build and run

```sh
./build.sh            # compiles the sweastrology module next to morinus.py
python3 morinus.py
./install-desktop.sh  # optional: adds "Morinus 2014" to the application menu
```

Settings live in `Opts/` and charts in `Hors/` inside this folder (both kept
out of git). `.hor` charts and `.opt` settings files from the Windows program
load unchanged, and files saved here can be opened by the Windows program.

The full Swiss Ephemeris data files are in `SWEP/Ephem/` (from the Windows
installation), so positions are computed with full precision, 5400 BC–5400 AD.

## How the source was recovered

1. `morinus.exe` is a PyInstaller bundle of Python 2.7 bytecode. The 164
   Morinus modules were extracted and decompiled; `morinus.py` was stored as
   source in the bundle.
2. Every decompiled module was recompiled with Python 2.7 and compared with the
   original bytecode. 148 of 164 are byte-identical; the other 16 differ only
   in unreachable code, constant-table order or compiler optimisation details.
   18 functions where the decompiler had placed statements in the wrong block
   were corrected until their bytecode matched the original.
3. 13 modules unchanged since the public 2012 source use that source, with its
   original comments. Elsewhere comments could not be recovered.

The first commit on `main` is the recovered Python 2 code, before porting.

## Known issues from the original program

- Saving primary directions as text fails for the **Campanian** method: the
  list of method names used in the export has no entry for it. The same
  happens in the Windows build; it is left as is.

Fixed during the port: in transit/revolution windows, primary directions with
**Placidian under the pole** referred to a misspelt attribute, so the
calculation thread died and the progress dialog never closed.

## Tests

- `tests/refdump.py` / `tests/refcompare.py` compute a set of charts headlessly
  and compare every value with `tests/reference/py2.json.gz`, produced by the
  recovered code under Python 2.7:

  ```sh
  python3 tests/refdump.py . /tmp/py3.json
  python3 tests/refcompare.py tests/reference/py2.json.gz /tmp/py3.json
  ```

- `tests/guismoke.py` opens a chart and triggers every menu command and
  popup-menu item, recording any exception. Run it on a copy of this folder,
  since it confirms the options dialogs (which save to `Opts/`):

  ```sh
  xvfb-run python3 tests/guismoke.py /path/to/copy /tmp/smoke [--variant 1|2|3]
  ```
