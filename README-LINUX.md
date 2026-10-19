# Morinus on Linux (Python 3)

This is Morinus 6 ported from Python 2 / wxPython 2.8 to Python 3 / wxPython 4,
so it runs natively on current Linux distributions.

## Requirements

- Python 3.10 or newer
- wxPython 4.2 and Pillow
- a C compiler and the Python headers, to build the Swiss Ephemeris module

Distribution packages are the easiest way to get wxPython:

| Distribution    | Command |
|-----------------|---------|
| Debian / Ubuntu | `sudo apt install python3-wxgtk4.0 python3-pil python3-dev python3-setuptools gcc` |
| Fedora          | `sudo dnf install python3-wxpython4 python3-pillow python3-devel python3-setuptools gcc` |
| Arch            | `sudo pacman -S python-wxpython python-pillow python-setuptools gcc` |

## Build and run

```sh
./build.sh            # compiles the sweastrology module next to morinus.py
python3 morinus.py
```

To add Morinus to your desktop's application menu (runs it from this folder):

```sh
./install-desktop.sh              # ./install-desktop.sh --uninstall to remove
```

Morinus keeps its settings in `Opts/` and looks for charts in `Hors/` inside
this folder, as the original did, so the folder must be writable.

## Compatibility with the original Morinus

- Existing `.hor` charts, option files and the place database open unchanged.
- Files saved by this version use a pickle format the original Python 2
  Morinus can still read, so charts can be exchanged with Windows users.

## Tests

`tests/` contains the checks used during the port:

- `refdump.py` / `refcompare.py` compute a set of charts headlessly and compare
  every value (positions, houses, almutens, primary directions, transits,
  revolutions, profections, ...) with `tests/reference/py2.json.gz`, which was
  produced by the original code under Python 2.7:

  ```sh
  python3 tests/refdump.py . /tmp/py3.json
  python3 tests/refcompare.py tests/reference/py2.json.gz /tmp/py3.json
  ```

- `guismoke.py` opens a chart and triggers every menu command and popup-menu
  item, recording any exception. Run it on a copy of the program folder, since
  it confirms the options dialogs (which save to `Opts/`):

  ```sh
  xvfb-run python3 tests/guismoke.py /path/to/copy /tmp/smoke [--variant 1|2|3]
  ```
