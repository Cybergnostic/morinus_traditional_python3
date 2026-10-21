# UI checkpoints

Baseline commit: 36cc569e1374bf54ea0523ad70aff901c2ef2019.
Checkpoint branch: checkpoint/ui-2026-10-21.
Integration branch: integration/morinus-ui-a1-b5 (PR #14). Original ui and main stay untouched.

## A1: Resizable sidebar

Draggable native divider for natal, transit, and return charts.
Preferred width is saved in the separate Opts/traditional.json file when settings are saved.
Spacing and headings are refined using system palette colors.
No astrological calculation or original .opt format changes.

Test with python -m unittest discover -s tests -p 'test_sidebar_width.py'
GUI review: sidebar dragging and minimum window sizes on Linux and Windows.
The GitHub integration cannot execute the GUI, so this remains subject to local review.

## A2: Command palette

- New toolbar-independent Ctrl+K command palette with a keyboard-navigable results list.
- Toolbar button opens the same palette; no popup/focus race or hidden-toolbar dependency.
- Search considers command name, menu path and help text, with name-first ranking.
- Search ranking is independent of wxPython and covered by tests/test_commandindex.py.
- The original menu-command handlers are reused unchanged.
- Feature branch: feature/ui-command-palette (stacked on A1 until CI review).

Run: python -m unittest discover -s tests -p 'test_commandindex.py'
GUI review: Ctrl+K with toolbar on/off, Escape, arrows, Enter, mouse double-click, checkable menu commands and settings dialogs.

## A3: Individual Settings search

- The left pane shows matching settings, not only matching category names.
- Results search labels, category, groups, descriptions and available choices.
- Clicking a result switches page and scrolls/focuses the existing setting; merely searching never changes values.
- Original dialogs, callbacks and .opt/traditional.json formats remain unchanged.
- Ctrl+K command palette links directly to individual traditional Settings fields.
- Regression tests: tests/test_settingsindex.py; GUI searches in tests/guismoke.py.
- Feature branch: feature/ui-settings-search (stacked on A2).

Review: search Egyptian terms, Regiomontanus, Years shown, GeoNames user name.
Also try Ctrl+K for Length of a year and Phasis within (days).

## A4: Optional high-quality rendering of the Morinus chart wheel

- New Chart look > Rendering choice: Standard (original) or High quality.
- High draws the entire natal/bi-wheel at twice the resolution (both wx lines and
  Pillow glyphs), then Lanczos-reduces to the original on-screen dimensions.
- Both pen widths and small/medium chart thresholds retain their original
  *display-space* interpretation; the wheel's identity and layout are retained.
- Every planet hit test converts display clicks back to internal raster
  coordinates, avoiding a regression in chart interaction.
- Extremely small or huge canvases fall back to standard for performance.
- The standard path remains the default until high-quality rendering has
  passed local visual/GUI validation (the setting is separate in traditional.json).
- This stage intentionally does not rewrite the separate primary-directions,
  square, or heliocentric chart renderers; those require separate regression work.

Tests: tests/test_chartquality.py (pure functions), and the chartQuality
step in tests/guismoke.py (bitmap dimensions, hit testing for both modes).
Manual review: switch both modes in Chart look on natal and transit
bi-wheels; compare symbols, circular ticks, exact click selection, resize
behavior and CPU/memory. Check large charts and Windows high-DPI scaling.
A4 branch: feature/ui-chart-quality, stacked on A3.

## A5: Bitmap table presentation and safer CSV extension points

- A5 begins at commit e74b9ed404a517c116a7a5f1fb29f16c36d5df39.
- Feature branch: feature/ui-tables, stacked on A4; previous branches unmodified.
- CommonWnd: zoom always resamples the original table using Lanczos with modest sharpening.
- Ctrl+wheel now keeps the point under the cursor; keyboard/menu zoom uses the viewport center.
- Zoom label in context menu and memory cap for extremely large tables.
- Header rows in two speculum views, mundane positions and Firdaria have a subtle OS-independent tint; monochrome remains unchanged.
- Miscellaneous CSV is an explicitly structured two-column export; other tables keep their legacy text-based fallback.
- No changed astrological values, speculum columns, original .opt files or base bitmap export size.
- Pure tests: tests/test_tablepresentation.py; GUI smoke: tablePresentation.
- See docs/A5-TABLES.md for manual regression checklist and known limitations.

## B1: Comprehensive Positions workspace

- Starting SHA: 3323baaf715fb4a5422534bda972b750c3b50a08.
- Feature branch: feature/ui-positions-workspace (stacked on A5).
- Added Tables > Positions workspace (Ctrl+Shift+P) with four pages:
  Zodiacal/speculum, Mundane, Motion, Chart data.
- Existing Tables > Positions, Mundane positions, Speeds, Miscellaneous are
  retained and now open the corresponding workspace page as compatibility aliases.
- "Open separately" from any workspace tab creates the corresponding original
  independent table window.
- Zodiacal selector chooses Placidian or Regiomontanian speculum, independent
  of the current primary-direction calculation method; retains the original
  Appearance II configured columns and precision.
- Original windows, functions, algorithms and exported table formatting are
  reused without editing the numeric calculations.
- If a speculum has zero selected columns, show a clear prompt and offer
  Configure columns rather than constructing a malformed table.
- Pure test: tests/test_positionscatalog.py. GUI smoke: positionsWorkspace.
- User Speculum remains a separate specialist feature for arbitrary points.
- Do not merge to ui-next or main until Linux and Windows GUI regression checks.

Manual review: open one chart, invoke each of the four legacy Table menu items,
check it selects the correct notebook page, switch both specula, and verify
all columns and values against original individual windows. Test B&W,
saving image/CSV for each available tab, resizing, and Open separately.

## B2: Fixed Stars workspace

- Starts from B1 `a308a61c299771d8ab09432aaf9fedc6d256501c`.
- New `feature/ui-fixed-stars-workspace` and native three-tab explorer:
  star catalogue; original fixed-star aspect matrix; angular events (stars on
  angles + paranatellonta in two sections).
- Legacy Tables menu names retained as aliases to the matching page.
- Separate independent windows remain available via Open separately.
- Reuses original fixedstarswnd, fixedstarsaspectswnd, fixedstaranglewnd,
  including their original orb calculations and Swiss Ephemeris calls.
- Distinguish angular proximity to birth (`fsa_minutes`) from planet/star
  simultaneity (`fsa_paranminutes`). Neither is changed.
- Lazy view construction avoids expensive paran calculations until selected.
- Shared lazy `legacytabworkspace.TableWorkspace` is reusable for B3.
- New unit tests in tests/test_fixedstarscatalog.py and GUI smoke test.
- Test selected vs empty star catalogues, three pages, original windows,
  B&W, export, scrolling, angular events and paranatellonta correctness.

## B3: Planetary hours and Rise/Set workspace

- New branch feature/ui-hours-riseset-workspace, stacked on B2.
- New Tables > Planetary hours and Rise/Set workspace, two native pages.
- Legacy Tables > Planetary hours and Tables > Rise and set actions now
  open the appropriate tab in the existing workspace instance.
- Each tab uses the original HoursWnd/RiseSetWnd calculation and drawing
  code, including local time handling and rising times of zodiacal signs.
- Open separately recreates the original standalone frames.
- Loading the second tab is deferred until used.
- Heliacal phenomena intentionally remain separate (different calculations).
- Unit test: tests/test_hourscatalog.py. GUI smoke: hoursRiseSetWorkspace.
- Verify daylight/nighttime charts, hours around sunrise, rise/set, high
  latitude edge cases, black and white, CSV, zoom, original standalone view.

## B4: Independent New/Full Moon navigator

- Based on B3, on separate feature/ui-lunation-navigator branch.
- Charts > New and Full Moon navigator opens a separate wxPython list view.
- Computes geocentric Sun–Moon ecliptic conjunctions and oppositions via
  Swiss Ephemeris UT, with bracketed bisection (does not invoke Syzygy()).
- Earlier, Later, Birth date navigate successive ~two-month windows.
- Open event chart generates a normal transit chart for selected event.
- Dates are formatted in the radix's entered local-time convention.
- Does NOT modify radix.syzygy, its prenatal selection, its time, or
  lots, almutens, or other traditional calculations.
- Original Charts > Syzygy chart and Syzygy chart 2 remain untouched.
- BC event-chart navigation disabled as in existing syzygy chart tools.
- Pure tests: tests/test_lunationnav.py. GUI smoke: lunationNavigator.
- Test chart date around a new/full Moon, earlier/later windows, zoom,
  event chart, ephemeris tolerance, and original prenatal syzygy stability.

## B5: Graphical and tabular ephemeris, stations and ingresses

- Starts at B4 commit 0883c9ef794d5b170be2d2976e5640fe0423bced.
- Branch feature/ui-ephemeris-workspace is independent and stacked on B4.
- Tools > Ephemeris now opens coordinated Graph / Daily positions /
  Stations & ingresses tabs, plus year navigation.
- A single Swiss Ephemeris geocentric data source drives the plot and tables.
  Daily positions are sampled at 00:00 UT, with true 365/366-day Gregorian
  years and all seven traditional visible planets (no outer planets).
- Existing Morinus graphical ephemeris drawing is reused. The original six
  planet view is the default; Show Moon adds the Moon. Graph click selects a
  day, and choosing a tabular day marks it in the graph.
- Ingress boundaries include direct, retrograde and the 0/360 Aries wrap.
  Station times are roots of longitude speed, refined within daily brackets
  to around one second; events have UTC timestamps and a chart-opening action.
- Zodiacal positions respect options.ayanamsha calculated for the actual date
  (rather than only 1 January); displayed station speeds are geocentric
  tropical speeds, the conventional sign-change criterion for station events.
- Structured daily CSV has date, numeric longitude columns and numeric
  speed columns; events CSV has date/time UT, planet, type and details.
- Open classic graph keeps the original stand-alone presentation.
- This does NOT alter the chart, lots, returns, fixed-star algorithms, the
  original ephemcalc module or stored settings.
- Unit tests: tests/test_ephemerisdata.py; GUI smoke: ephemerisWorkspace.
- Manual review: 2024 leap day, a station retrograde/direct pair, a retrograde
  sign ingress, Moon on/off, precise event charts, B&W, CSV, year navigation,
  sidereal day-of-date values and mouse selection. No claims of historical
  BC support; UI years are AD 1–5000.

## Comparison grid and concentric multi-wheels (Parts 1 and 2)

- Charts > Compare charts... opens two or four independent, unmodified
  single wheels. Cells select radix, an open transit/return/lunation or a
  saved .hor file, and display chart title and entered local date.
- Charts > Multi-wheel... renders the radix, houses and internal aspects
  inside the zodiac band, followed by 1-3 selectable planetary rings.
  Each ring has boundary circles, spread glyphs, true longitude ticks,
  degrees and retrograde symbols. Radix-to-one-ring aspects are optional,
  using the existing planetary orbs. Clicking a glyph fills the status
  line; PNG export and resizing are supported.
- Both commands are enabled only when a radix is open. The original single
  and transit bi-wheel drawing and all calculations remain unchanged.
- Tests: tests/test_multiwheel_layout.py for radius allocation and Aries
  wrap-around; tests/guismoke.py steps comparisonGrid and multiWheel for
  a 2x2 layout with transit, three ring counts, resize, click and image
  export. Screenshots are retained as smoke-test artifacts when possible.

### Part 3: presentation (not implemented)

Before implementation, decide whether presentation means full-screen,
printing or a report builder; the default titles, legends and annotations;
which page sizes, aspect tables, and PDF/SVG export formats are needed.

- Same-orientation toggle was intentionally omitted: GraphChart fixes each
  single wheel to its own Ascendant, and the brief prohibits changing it.

- Focused smoke option `--multiwheel-only` runs onLoad, comparisonGrid,
  multiWheel and onExit, alongside the complete GUI smoke in CI.
