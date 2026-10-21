# Brief: comparison grid and multi-wheels (for an implementing agent)

Repository: Cybergnostic/morinus_traditional_python3. Work on branch
`feature/multiwheel` (it contains everything merged so far). Morinus is a
traditional-astrology program (Python 3, wxPython 4 / Phoenix, Pillow, a
bundled Swiss Ephemeris C extension `sweastrology` imported as `astrology`).
It must run on Linux (GTK3) and Windows.

## Goal, in three parts (do them in this order, one commit or more each)

1. **Comparison grid**: one window showing 2 or 4 chart wheels side by side
   (1x2 or 2x2), each an ordinary single wheel.
2. **Multi-wheel**: one wheel with the radix inside and 1, 2 or 3 further
   charts as rings outside it (bi-, tri-, quad-wheel).
3. **Presentation**: NOT specified yet. Do not implement; leave a note.

## Ground rules

- Do not change any astrological calculation or the existing single and
  bi-wheel drawing (`graphchart.GraphChart`). Existing windows must look
  exactly as before. Add new modules instead of growing `graphchart.py`.
- Match the style of the file you edit. Decompiled Morinus files (header
  "Recovered from morinus.exe") use 4 spaces; most new modules use tabs.
- No personal data: never add charts (`Hors/*.hor` other than the shipped
  `Morinus.hor`), `Opts/`, or `Res/placedb.dat` to the repository.
- One menu entry per feature (the user's rule: no two commands leading to
  the same place). Add both new commands to the **Charts** menu in
  `morin.py` `buildMenus()` with the `new(...)` helper, and add their ids to
  the list in `enableMenus()` (they need an open chart).
- Run before every commit:
  `python -m unittest discover -s tests -p 'test_*.py'` (all must pass).
  Before finishing, run the GUI smoke test (see "Testing").

## How charts are made and drawn (what to reuse)

- A chart: `chart.Chart(name, male, chart.Time(...), chart.Place(...), htype,
  notes, options, full)`. Secondary charts (transits, returns, ...) use
  `full=False`. Examples of making them: `morin.py` `onTransits`,
  `onRevolutions`; `transitsearch.py` `onOpen`; `lunationnavigator.py`
  `event_chart`. Loading a saved chart: `morin.py` `subLoad(fpath, dpath,
  dontclose=True)` returns a Chart from a `.hor` file.
- A wheel: `graphchart.GraphChart(chart, (w, h), options, bw, clickedPlanetId,
  chart2=None).drawChart()` returns a `wx.Bitmap`. With `chart2` it draws the
  existing bi-wheel (radix inside, chart2 outside). `onClick(pos)` returns the
  planet id at a mouse position. `transitwnd.TransitWnd` is a small window
  that wraps exactly this; copy its pattern (buffer bitmap, EVT_PAINT,
  redraw on EVT_SIZE).
- **Why multi-wheels need new code**: `GraphChart.__init__` hard-codes every
  radius (`self.r...` = fractions of `maxradius`) in separate branches for
  single/bi-wheel and for each outer-ring option (terms, decans, fixed stars,
  antiscia...). It cannot take a third ring without rewriting it.
- Planet glyphs are letters of the font `common.common.symbols`
  (`common.common.planets[i]`, signs `common.common.signs[i]`); text uses
  `common.common.abc`; fonts via `util.truetype(path, size)`. Planet indices:
  `planets.Planets.SATURN..MOON` = 0..6, nodes 7, 8. Longitude:
  `chart.planets.planets[i].data[planets.Planet.LON]`; speed `SPLON` (< 0 is
  retrograde). Sidereal charts: subtract `chart.ayanamsha` when
  `options.ayanamsha != 0` (see `tablewnd.TableWnd.position`).
- Colours: `options.clrplanets[i]`, `clrframe`, `clrsigns`, `clrbackground`,
  `clrtexts`; black and white when `bw`. Line weights by role:
  `chartstyle.frame_pen(options, bw, chartsize, role)`.
- The wheel is oriented with the radix Ascendant on the left: a longitude
  `lon` is at angle `math.pi + math.radians(asc - lon)` from the centre
  (see `GraphChart.onClick` and `drawPlanetLine`).
- Overlapping glyphs: `GraphChart.arrangeObjs/doArrange/doShift` spread
  objects that are too close. Reimplement the same idea for a ring (a small
  pure function: sorted longitudes in, display longitudes out, minimum
  separation in degrees) and unit-test it.

## Part 1: comparison grid

- New `comparegrid.py`: a `wx.Frame` "Compare charts" with a 1x2 / 2x2
  layout choice and, per cell, a chooser: the open radix, "Open chart
  file..." (via `subLoad`), or the transit/return/lunation charts currently
  open in other windows (`transitframe.TransitFrame` instances among
  `wx.GetTopLevelWindows()`, attribute `.chart`).
- Each cell draws `GraphChart(cell chart, cell size, ...)` (single wheel),
  with the chart's name and date above it. Redraw on resize (throttle like
  `morin.MFrame.onSidebarResize`).
- Optional, if simple: "Same orientation" check box: rotate every cell to
  the radix Ascendant. Only if it can be done without changing
  `GraphChart` (otherwise skip and note it).
- Menu: Charts > "Compare charts...".

## Part 2: multi-wheel

- New `multiwheel.py` with a renderer class `MultiWheel(radix, others,
  size, options, bw)` where `others` is a list of 1..3 charts, and a window
  `MultiWheelFrame`.
- Layout, from the centre outwards: the radix as an inner single wheel
  (houses, its planets, aspects among them), the zodiac band, then one ring
  per further chart (outermost = last chart). Each ring: two boundary
  circles, the chart's planet glyphs (spread, see above), degree and
  retrograde mark, and a short tick from the ring's inner edge to the exact
  longitude. Allocate radii by formula from the number of rings (no
  hard-coded per-count branches), so 1, 2 and 3 rings all fit.
- For the inner radix wheel, prefer drawing it yourself in `multiwheel.py`
  over compositing a scaled `GraphChart` bitmap (text would be blurred);
  reuse its fonts, colours and pens as described above.
- Aspects: by default only within the radix. A choice "Aspects between: radix
  / radix and ring N" may draw the aspects between the radix and one ring,
  using the orbs of `options` (look at `chart.Chart.calcPlsAspMatrix` for how
  orbs are read; do not modify it).
- Clicking a glyph shows that planet (chart and position) in a status line.
- Choosing the charts: like the grid's cell choosers (radix fixed inside).
- Menu: Charts > "Multi-wheel...". The existing bi-wheel ("Comparison" view
  of transit windows) stays as it is.
- Save as image (PNG) like `transitframe.TransitFrame.onSaveAsBitmap`.

## Testing

- Unit tests (new files `tests/test_multiwheel_layout.py` etc.): the radius
  allocation for 1..3 rings (strictly decreasing, no overlap, inside the
  window), and the glyph-spreading function (minimum separation kept, order
  kept, wrap-around at 0/360 Aries handled).
- GUI smoke test `tests/guismoke.py`: add steps (see the existing steps
  'transitSearch' or 'positionsWorkspace' and the HANDLERS list) that open
  the grid in 2x2 with the radix and a transit chart, and the multi-wheel
  with 3 rings; draw, resize, save an image, close. Run on Linux:
  `xvfb-run -a -s "-screen 0 1600x1000x24" python tests/guismoke.py <copy> <out> --exercise`
  then `python tests/check_smoke.py <out>/guismoke.json` (needs 0 errors and
  0 clipped controls). `<copy>` is a copy of the repository folder with the
  built extension (the test writes into it).
- Keep screenshots of 1-, 2- and 3-ring wheels and of the grid for review.

## Done means

- Both features in the Charts menu, enabled only with a chart open.
- Existing windows unchanged; all unit tests and the smoke test pass.
- A short note in `docs/UI-ITERATIONS.md` (what was added, what is left).
- Part 3 not started; list open questions about "presentation" there.
