# Morinus Traditional (Python 3)

The traditional Morinus astrology program — version 6.2 as released for Windows
in March 2014 — ported to Python 3 and wxPython 4 so it runs natively on Linux,
with additional tools for traditional astrology.

Morinus was written by Robert Nagy and is free software under the GNU GPL v3.

## What's in it

Everything from the 2014 program: charts with clickable planets showing their
aspects and orbs, the seven traditional planets, tables (positions, almutens,
antiscia, aspects, fixed stars, lots, planetary hours, firdaria, profections,
primary directions…), revolutions, transits, syzygy charts, heliocentric
charts, elections, and its options.

Added in this version:

- **Tables → Planetary conditions** — sect by the Sun's true altitude,
  hayz/halb, synodic phase (combust, under the beams, cazimi), oriental /
  occidental, stations, motion, joys, latitude, Via Combusta, void-of-course
  Moon.
- **Tables → Antiscia** — two more columns show the planets standing on each
  antiscion and contraantiscion: in its sign, the whole degrees of the two
  adding up to 29 (10° Aries with 19° Virgo, or 19° Pisces).
- **Tables → Temperament** — the temperament worksheet with every factor and
  its points.
- **Charts → Lunar returns of the year** — the lunar returns covering a solar
  year: the one in force at the solar return, every one beginning during the
  year, the last of which is in force at its end. Each row shows the return's
  Ascendant and its whole-sign house in the solar and natal charts;
  double-click opens the return.
- **Steppers** (right-click in a chart window) — *Step solar/lunar returns*
  moves to the previous or next return; *Step time* moves transits over the
  natal chart by seconds up to years.
- **Duads on bi-wheels** — with dodecatemoria chosen in Options → Appearance I,
  return and transit charts show their duads in an outer ring.
- **Lots** — any number of lots (was 40) and names up to 40 characters; a
  Day/Night selector in Tables → Lots and in Options → Lots shows each lot as
  it applies to day or night charts (both open on the chart's sect).
  `tools/arp_lots.py` converts Solar Fire `.arp` Arabic-parts files, and
  `tools/merge_lots.py` merges them into your lots:

  ```sh
  python3 tools/merge_lots.py --arp parts.arp --dry-run
  ```

- **Automatic time zones** — a button in New Chart / Edit Data looks up the
  time zone and daylight saving for the birth date and place (offline);
  see [below](#automatic-time-zones-birth-data).
- **Offline atlas** — the place search (New Chart → Place → Search) looks up
  236,000 places worldwide without internet; see [below](#offline-atlas).

The planetary conditions and the temperament come from
[hor-tools](hor_tools/VENDORED.txt) (vendored in `hor_tools/`), run on
Morinus's own Swiss Ephemeris through `swe_compat.py`.

## Install

### Windows

Download `MorinusTraditional-…-setup.exe` from the
[latest release](https://github.com/Cybergnostic/morinus_traditional_python3/releases/latest)
and run it. It installs for the current user (no administrator rights needed)
into `%LOCALAPPDATA%\Programs\Morinus Traditional`, where your settings,
charts and places are kept; updating or uninstalling leaves them in place.
The `.zip` in the same release is the same program to run from any folder.

### Linux

You need Python 3.10 or newer, wxPython 4.2, Pillow, and a C compiler with the
Python headers for the Swiss Ephemeris module:

| Distribution    | Command |
|-----------------|---------|
| Debian / Ubuntu | `sudo apt install python3-wxgtk4.0 python3-pil python3-dev python3-setuptools python3-venv gcc` |
| Fedora          | `sudo dnf install python3-wxpython4 python3-pillow python3-devel python3-setuptools gcc` |
| Arch            | `sudo pacman -S python-wxpython python-pillow python-setuptools gcc` |

Then, in the Morinus folder:

```sh
./install.sh
```

This sets up a Python environment in `.venv/` inside the folder (it uses the
distribution's wxPython and Pillow and adds `timezonefinder` for automatic
time zones, so nothing is installed into the system Python), compiles the
Swiss Ephemeris module, downloads the offline atlas (about 14 MB, built into
`Res/atlas.db`) and adds "Morinus Traditional" to the application menu.
Start it from the menu or with `./morinus`. Run `./install.sh` again after
updating; `./install.sh --update-atlas` also gets the latest atlas.

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
revolution windows (a misspelt attribute stopped the calculation); the Lots
table showing the luminary of the time reversed; and uninitialised string
buffers in the Swiss Ephemeris module.

## Tests

```sh
python3 tests/refdump.py . /tmp/py3.json                         # with default settings (empty Opts/)
python3 tests/refcompare.py tests/reference/py2.json.gz /tmp/py3.json
python3 tests/check_arp_lots.py parts.arp                        # Solar Fire conversion
xvfb-run python3 tests/guismoke.py /path/to/copy /tmp/smoke [--variant 1|2|3]
```

`refdump.py` computes a set of charts and dumps every value; `refcompare.py`
compares them with the Python 2 reference. `guismoke.py` opens a chart and
triggers every menu command and popup-menu item (run it on a copy of the
folder, since it saves options).

## Automatic time zones (birth data)

The Windows build and `install.sh` include what this needs. In **New Chart**
or **Edit Data**, enter the civil birth date/time and select a location
(or enter longitude/latitude). Click **Auto time zone (date + location)**,
review the IANA zone, standard GMT offset and daylight-saving flag, and
confirm. This works offline: the zone comes from `timezonefinder`'s zone
borders, or without it from the nearest place in the offline atlas (within
30 km).

Morinus stores a standard GMT offset and a separate one-hour daylight-saving
flag. The automatic lookup deliberately splits those values to avoid
counting summer time twice. You can change the values manually afterward.
Existing charts are never automatically rewritten.

Dates before 1970 require independent historical verification. BC dates and
Julian-calendar input are not supported by the automatic lookup. Ambiguous
autumn clock-change times and nonexistent spring clock-change times are
rejected; enter researched settings manually. Daylight saving that does not
fit Morinus's one-hour checkbox (such as Irish winter time, which IANA counts
as negative DST) is entered as the total offset with DST unchecked. Offsets beyond
Morinus's 12-hour field must be entered manually. The lookup does not change
Morinus's underlying .hor file format.

Run the isolated time-zone tests with
`python3 -m unittest discover -s tests -p 'test_auto_timezone.py'`.

## Offline atlas

**Search** in the Places dialog (the **Place** button in New Chart / Edit
Data) looks in the offline atlas first: every place in the world with 500 or
more inhabitants (about 236,000), from [GeoNames](https://www.geonames.org).
Names can be typed without diacritics (*Nis* finds Niš) or in other spellings
and scripts (*Nisch*, *Ниш*); add a region or country after a comma to narrow
it down (*Springfield, Illinois*, *Nis, RS*). The results window searches again
as you type. Choosing a place fills its coordinates, altitude and present-day
standard time zone and adds it to your places list; for the birth date's own
offset and daylight saving, use **Auto time zone** in the chart data. A place
that is not in the atlas is looked up online as before.

Without `Res/atlas.db` the search is online only; build it with
`python3 tools/build_atlas.py` (or `./install.sh`).

## Credits and licences

- Morinus — Robert Nagy, GNU GPL v3 (`LICENSE`).
- Swiss Ephemeris 1.76 — Astrodienst AG (`SWEP/src/LICENSE`).
- hor-tools — Cybergnostic (`hor_tools/`).
- Atlas — [GeoNames](https://www.geonames.org), CC BY 4.0.
