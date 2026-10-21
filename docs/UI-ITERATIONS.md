# UI checkpoints

Baseline commit: 36cc569e1374bf54ea0523ad70aff901c2ef2019.
Checkpoint branch: checkpoint/ui-2026-10-21.
Integration branch: ui-next. Original ui and main stay untouched.

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
