# Morinus Traditional (Python 3)

The traditional Morinus astrology program — version 6.2 as released for Windows
in March 2014 — ported to Python 3 and wxPython 4 so it runs natively on Linux,
with additional tools for traditional astrology.

Morinus was written by Robert Nagy and is free software under the GNU GPL v3.

This branch, `main`, is the program with the additions below. The
[`clean-port`](../../tree/clean-port) branch is the 2014 program ported as it
was, with nothing added (Swiss Ephemeris 1.76).

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
- **Tables → Zodiacal releasing from Fortune / Spirit** — Valens's periods of
  the signs: levels 1 and 2 for a lifetime with the loosing of the bond, the
  places from the lot (angles and the peak) and the present period; click a
  level 2 period for levels 3 and 4. The method follows shin10567's Morinus.
- **Tables → Decennials** — Valens's periods of 10 years 9 months from the sect
  light, with levels 2-4 (click a level 2 period), after shin10567's Morinus.
- **Tables → Circumambulation** — the Ascendant directed through the bounds
  (Options → Terms) under the oblique ascensions of the birth latitude, a year
  per degree: distributors and the participants' bodies and rays, by age and date.
- **Tables → Heliacal phenomena and phasis** — for each planet the morning
  and evening first and last appearances nearest the birth (Swiss Ephemeris
  visibility) and the stations, with phasis within 7 days of the birth.
- **Tables → Fixed stars on the angles** — the stars (Options → Fixed stars)
  rising, culminating, setting or anticulminating within 30 minutes of the
  birth, and the paranatellonta of the birth day: a planet and a star on
  angles within 4 minutes.
- **Tables → Dodecatemoria calculator** — the dodecatemorion of any degree.
- **Options for the added techniques** — Options → Zodiacal releasing,
  Decennials, Circumambulation, Heliacal phenomena, Fixed stars on the angles,
  Antiscia, Places and time zones, Windows and errors (kept in
  `Opts/traditional.json`); every option has a help text, and these and
  Morinus's own options dialogs have a **Defaults** button.
- **Copy as text** in the popup menu of every table, **arrow keys** to step
  return and transit charts, windows reopen at their last size and position,
  and unexpected errors are shown and written to `morinus-error.log`.
- **Tables → Temperament** — the temperament worksheet with every factor and
  its points.
- **Charts → Lunar returns of the year** — the lunar returns covering a solar
  year: the one in force at the solar return, every one beginning during the
  year, the last of which is in force at its end. Each row shows the return's
  Ascendant and its whole-sign house in the solar and natal charts;
  double-click opens the return.
- **Divisions (Valens)** — right-click a solar return chart and choose
  *Divisions (Valens)*. The seven fixed planetary periods start with the lord
  of the annual profection and follow the solar planets in secondary zodiacal
  order. The table shows UTC boundaries and each ruler's solar house; the last
  ruler covers the remaining fraction of the solar year. Solar directions are
  already available from the same popup under *Primary Directions*.
- **Monthly solar revolutions** — in the same solar-chart popup, open an
  optional list of twelve Sun returns (the annual return plus eleven monthly
  returns at the natal degree in successive signs). Double-click opens a chart.
  The current implementation supports tropical charts.
- **Repeated natal configurations** — right-click a solar return and open the
  optional *Repeated natal configurations* search. It finds the same named
  traditional planet pairs forming the same Ptolemaic aspects in both natal
  and solar charts; complete three-planet aspect patterns are listed on their
  own tab. An adjustable maximum deviation (default 5 degrees, separately
  enforced in both charts) controls how tight a repetition must be. You can
  also search repeated zodiac signs and whole-sign houses, or restrict results
  to the annual profection ruler. No extra aspect marks are drawn on the chart.
  This is a **geometric pattern search**, not a replacement for the existing
  aspect-orb settings or the planned traditional aspect engine; the current
  search does not assess sign-boundary exceptions, reception or application.
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
`Res/atlas.db`) and adds "Morinus" to the application menu.
Start it from the menu or with `./morinus`. Run `./install.sh` again after
updating; `./install.sh --update-atlas` also gets the latest atlas.

Morinus runs from its folder, which must be writable: settings are kept in
`Opts/`, charts in `Hors/`, and your place list in `Res/placedb.dat` (the
shipped list is `Res/placedb-default.dat`). None of these are tracked by git.

Positions come from Swiss Ephemeris 2.10 (JPL DE431 data, current ΔT); the
data files in `SWEP/Ephem/` give full precision from 5400 BC to 5400 AD.
Compared with Morinus 6.2 (Swiss Ephemeris 1.76), modern charts differ by less
than 0.2" for the planets and 2" for the angles; charts of earlier centuries by
up to about a minute of arc, from the newer ΔT. The `clean-port` branch keeps 1.76.
Fixed stars come from the 2.10 catalogue (`sefstars.txt`), each listed once and
with the names Morinus 6.2 used (Bungula, Gemma, Asellus Australis, ...).

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

- A selected fixed star that the 2.10 catalogue no longer has (the solar apex,
  Barnard's star, kappa Ceti, kappa Coronae Borealis) is listed as not in the
  catalogue.
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
python3 tests/refcompare.py tests/reference/se210.json.gz /tmp/py3.json
python3 tests/check_arp_lots.py parts.arp                        # Solar Fire conversion
xvfb-run python3 tests/guismoke.py /path/to/copy /tmp/smoke [--variant 1|2|3]
```

`refdump.py` computes a set of charts and dumps every value; `refcompare.py`
compares them with a reference: `se210.json.gz` is this version's (Swiss
Ephemeris 2.10), `py2.json.gz` the recovered Python 2 program's, which the port
matched exactly with Swiss Ephemeris 1.76 (the `clean-port` branch). `guismoke.py` opens a chart and
triggers every menu command and popup-menu item (run it on a copy of the
folder, since it saves options).

## Traditional aspects: A3 planetary connections and event chronology

Use **Tables → Aspects** (F8). The **Connections** tab works in natal,
horary, electional, solar-return and other chart types. On opening the tab,
Morinus automatically scans a 90-day event horizon, including the seven
traditional planets' major aspects, stations and sign ingresses. It lists
only chronologically verified **translation of light** and **collection of
light**, with exact UT contact times. A messenger/feeder reaching another
contact, station or ingress first invalidates that candidate and suppresses
it from the table. An absence of a matching perfection within the selected
horizon also suppresses that candidate rather than claiming success.
Use **Search days** and **Analyze connections** to rescan 1–180 days.
No receptions are required by this initial geometric filter. The Classic
matrix remains available. Under Whole Sign or Equal houses, the Classic matrix hides
the six intermediary house-cusp aspect columns; quadrant-like systems keep them.
The Ascendant/MC and the original planetary matrix are unaffected.

Open **Horary perfection** to choose two planets as significators, set an
event horizon (1–180 days, 30 by default), and click **Analyze timeline**.
The Swiss Ephemeris scans the days **following the chart's date** (not the
current calendar date), refining actual aspect perfections, planetary stations
and sign ingresses. The timeline reports all such events involving either
selected significator. The Horary scan is independent of the Connections tab
and does not alter its selected time horizon. The horary scan starts when
**Analyze timeline** is clicked; Connections are computed on first opening
their tab or when **Analyze connections** is clicked.

**Interpretive boundary:** "Candidate" means a configuration at the chart's
date, "Chronologically supported" means no earlier listed planetary
contact/ingress/station for the moving planet, "Needs review" flags earlier
events, and "Unverified" means no matching perfection found within the
selected horizon. A preceding contact, ingress, or station is **not**
automatically a valid prohibition, frustration or refranation. The **Perfection and impediments** list now classifies the originally
applying contact between the selected significators. It separately shows:
**prohibition** when a faster third planet contacts both significators in
sequence before their own perfection, **frustration** when the slower
significator first conjoins another planet, and **refranation** when an
initially applying planet reverses and withdraws before the contact.
It also lists earlier contacts, stations, and sign changes; a single
early contact is not automatically labeled prohibition. Actual planetary
positions after a station are checked before refranation is asserted.

This is a **chronological and classical-pattern assessment**, not an
automatic yes/no judgment. Reception, accidental dignity, sign/house context,
and source disagreements remain for the astrologer to judge, including
whether an intervention delays, redirects, or denies the matter. Events
after an ingress may represent new circumstances. The initial application
must be present in Morinus's current aspect matrix, and contacts of a
different Ptolemaic type do not fulfill the original application.
Natal translations and collections should not be read as event predictions.
Only the seven visible planets participate.

Reference for the distinctions: William Lilly, *Christian Astrology*,
part I pp. 110–113, and the Graeme Tobyn review of earlier horary
perfection doctrines:
https://www.skyscript.co.uk/tobyn2.html

Additional tests:
`python3 -m unittest discover -s tests -p 'test_horary_impediments.py' -v`

Calculation-level tests:
`python3 -m unittest discover -s tests -p 'test_light_perfection.py' -v`

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
- Swiss Ephemeris 2.10 — Astrodienst AG, GNU AGPL v3 (`SWEP/src/LICENSE`,
  `SWEP/src/agpl-3.0.txt`); with it the program as distributed falls under the
  AGPL v3, which adds to the GPL that whoever offers it as a network service
  must offer its source too.
- hor-tools — Cybergnostic (`hor_tools/`).
- Atlas — [GeoNames](https://www.geonames.org), CC BY 4.0.
- Zodiacal releasing and decennials after [Morinus by shin10567](https://github.com/shin10567/Morinus-Source-Codes), GNU GPL v3.
