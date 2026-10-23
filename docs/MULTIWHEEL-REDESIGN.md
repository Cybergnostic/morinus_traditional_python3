# Multi-wheel redesign - visual specification and implementation plan

Status: implementation in progress on `feature/multiwheel-redesign-20261022`.
Scope: the multi-wheel viewer only. The single-wheel GraphChart and
side-by-side comparison grid must not change.

## Decisions

- The **radix stays inside** and 1, 2, or 3 selected charts are placed outside.
- **Only one zodiac** appears, with exactly one set of traditional reference
  information (degree ticks, terms and decans). Never repeat these strips
  for solar returns, lunar returns, transits, or additional horoscopes.
- Terms and decans use the existing Morinus selections and visibility options.
- Chart-specific data (planets, positions, retrogrades, house cusps, angles)
  may differ on every ring. There must be a clear visual distinction and
  a labelled selection control identifying each chart.
- Aspect lines can be completely hidden. Default to **None**; additionally
  support radix-only and radix-to-one-selected-ring modes.
- Do not silently substitute a different chart when a source is unavailable.
  Identify repeated charts instead of presenting duplicates as different data.
- Preserve all astrological calculations and the familiar single-wheel style.
- Preserve **Charts > Compare charts...** and all existing comparison-grid code.

## Geometry and presentation

- A pure layout function allocates a radial sequence:
  **radix -> optional decans -> optional terms -> zodiac -> outer planetary rings**.
- Future stages must measure text and glyph extents and require minimum
  readable sizes; don't shrink everything indefinitely to fit.
- Thin, muted ring backgrounds and matching ring numbers distinguish the
  chart layers while leaving planet glyph colours intact.
- At high density, prefer a larger zoomable canvas to overlapping symbols.
- Test 1-, 2-, and 3-ring scenarios, especially chart clusters around 0 Aries.
- Check grayscale/black-white exports and contrast.
- Labels and selected chart names should remain legible on Linux and Windows.

## Milestones

1. **Usability correction:** no-aspect mode, chart identification, visible
   distinction between outer rings and repeated-chart warnings.
2. **Shared reference bands:** central allocation function and a single
   set of Morinus terms, decans and zodiac degree ticks. This is a baseline
   implementation to be visually reviewed, not yet full GraphChart parity.
3. **Visual parity:** reproduce the ordinary Morinus wheel's details, houses,
   angles, planet positions, and configurable objects with legible typography.
4. **Adaptive tri-/quad-wheel:** collision avoidance, automatic band sizing,
   warning/zoom when needed, and layout regression tests.
5. **Chart-specific options:** configurable houses, angles and optional objects
   for outer charts; defaults keep outer rings readable. Do not repeat zodiac.
6. **User experience:** zoom, better chart selection, legends and high-resolution
   image export.
7. **Verification:** reference screenshots, full unit tests, GUI smoke tests
   and visual checks on Linux/Windows before merging.

Do not merge the redesign until the normal single-wheel appearance remains
unchanged and the bi-/tri-/quad-wheel results pass visual inspection.

## October 22: chart boundaries and source controls

- The **radix** draws its own house cusps and four angles only inside the
  radix. Every additional chart draws its own cusps and angles inside its
  planetary ring. Angle arrows remain inside their own ring.
- The single shared zodiac band contains zodiac references only: no house
  cusps or angle spokes from any chart pass through it.
- Sign divisions continue within each planetary ring, but stop at the
  shared zodiac and at the chart separator gaps.
- Chart boundaries are pairs of concentric circles with an explicitly erased,
  background-coloured annulus between them. The gap is reserved before
  laying out the planetary labels, and painted again last so that no strokes
  can cross it.
- Changing the main window's house system must preserve open multi-wheels
  and their transit/return sources, update their cusp sets and redraw them.
  Closing the base horoscope is *not* part of this exception.
- Each multi-wheel ring's **Create chart...** menu offers Solar Return,
  Lunar Return and Transits. These call the existing Morinus dialogs, attach
  the resulting chart to the selected ring, and do nothing on cancellation.
- Comparison grid's interface and rendering remain unchanged.


## October 22: true-longitude pointers, chart dials and identity labels

- Every planetary ring (including the radix) draws a **360-degree dial**.
  Degree ticks are local to the ring and do not duplicate the one zodiac.
  The radial dial is on the outside of the radix planetary band and the
  inside of the extra chart bands.
- Every planet's exact longitude is marked on its own dial and a visible
  leader joins that exact location to the displayed glyph/degree-minute
  cluster. The glyph can move angularly to avoid collisions without losing
  the true longitude reference.
- Each glyph and its combined degree-minute text form a **centrally balanced**
  two-tier cluster, not one pushed against the outside of its ring.
- Chart-local ASC, DSC, MC and IC axes end in distinct triangular arrowheads.
  No arrow crosses the shared zodiac or separator gap.
- The inner disk contains the radix identity and date/time. Each outer ring
  contains its own chart type, name, and date/time, printed into the chart
  image and PNG (not just the picker controls). Captions prefer fields far
  from planet glyphs.
- GUI regression covers one dial per wheel, each ring's identity field,
  and a four-angle rendering pass for each chart. Full screenshot review is
  still required before the draft pull request may be merged.


## October 22: correcting traditional-band parity with GraphChart

The original implementation wrongly treated the traditional bands as small
generic overlays. GraphChart's normal chart uses substantially wider bands,
its small Morinus glyph font and square-centred drawing conventions.

The normal GraphChart and multiwheel now use one shared pair of *pure*
longitude layout helpers, `traditional_term_markers` and
`traditional_decan_markers`, covering the exact unequal terms, 10-degree
decans, their rulers, and all division lines. GraphChart's existing
typography, radii and pens are preserved, while the multiwheel's bands
receive wheel-count-aware allocations (.065, .056, .047 radius respectively
for bi-, tri-, quad-wheels). The multiwheel ruler glyphs use GraphChart's
square-centred painting primitive and an approximate GraphChart small-symbol
scale bounded by the available band height.

This improves parity **without claiming the full multiwheel is yet
pixel-identical** to a single GraphChart. Houses, collision placement and
other chart-specific layers still need visual comparison and targeted reuse
rather than independent approximations.

## October 22: measured layouts, scrollable high-resolution viewer

The crowded bi-wheel screenshot exposed a structural mismatch: a large radix
core and narrowly allocated outer planetary band meant a dense chart could not
fit its labels. This stage corrects the **multiwheel renderer only**.

- Rebalanced the radius allocations: the bi-wheel now reserves more than 24%
  of the radius for the first outer chart even with terms and decans shown.
  Tri- and quad-wheel allocations likewise favour usable planetary labels.
- Replaced angular-only planet spreading in the multiwheel with actual
  glyph/degree/minute/retrograde rectangle measurements. Candidate positions
  vary both around the circle and along its radius, and remain in the
  planet's source zodiac sign. Exact degree-dial positions and leaders are
  still anchored to unchanged source longitude.
- Restored the normal Morinus three-tier glyph, degree, minute visual order.
  Reference rulers are smaller/lighter than the real planetary glyphs.
- When labels physically cannot fit, the viewer warns rather than claiming
  to have achieved a collision-free layout.
- Chart selection moved into a hideable left sidebar. The drawing has
  Fit, 100%, +/- controls and scrollable panning without bitmap magnification.
  A PNG is rendered at a separate 1600/2000/2400-pixel diameter depending on
  the number of chart rings.
- Extended pure geometry tests and the GUI smoke scenario to cover crowded
  positions, Aries and sign boundaries, zoom, sidebar, and viewport size.

**Still required before merging:** pass Linux/Windows CI and inspect actual
screenshots for all wheel counts. In particular, exact single-wheel visual
parity, optional chart-specific objects, and the remaining dense conjunction
cases are not yet guaranteed. Single-wheel GraphChart and comparison-grid
rendering have deliberately not been changed in this phase.

## October 23: chart-local axis markers and consistent planet glyph scale

- Radix and every outer chart now use the same marker vocabulary: ASC ends
  in a small unfilled circle (a fishing-hook-style beginning), DESC and MC
  have triangular outward arrowheads, and IC is a plain line.
- The hollow ASC centre is painted in the appropriate chart-field colour,
  so a house spoke does not appear inside the circle. Angle positions, chart
  boundaries and astrological calculations remain unchanged.
- Planet glyph, degree, minute and motion font sizes are computed **once**
  for the entire multiwheel using the narrowest usable planetary label band,
  excluding local degree dials and chart separator gaps.
- All radix and extra chart planetary glyphs therefore have identical font
  sizes. Terms/decans remain separate, smaller traditional ruler glyphs.
- GUI smoke now checks two triangle markers and one hollow ASC per chart,
  plus identical font settings across all planetary rings. Pure layout
  tests verify narrow-ring font selection and zoom behaviour.

Do not merge until the multiwheel screenshots have been checked.


## October 23: glyph-first visual hierarchy (current default)

- The multiwheel opens in **Glyphs + degrees** mode. All planetary symbols
  are calculated at one shared, larger size; small degree labels (plus R/S)
  are laid out *after* the glyphs and never constrain their size or positions.
- A new label selector provides **Glyphs only**, **Glyphs + degrees** and
  **Full positions**. The last mode displays degrees and minutes wherever
  they can fit without covering planets. PNG export respects the selection.
- Glyphs prefer exact longitude and move radially before angular movement.
  Placement stays in the correct zodiac sign and the selected chart's own
  house, including wraparound at 0 Aries. Dial markers always show original
  longitudes even for displaced labels.
- An optional numeric annotation is omitted when no collision-free space is
  available; the planet itself is never omitted. Hover and click show the
  full degree/minute, sign, motion and chart identity regardless.
- New geometry tests cover house cusp transitions, independent annotation
  placement, impossible narrow labels and shared font scaling. GUI smoke
  covers default/optional modes in addition to previous angle-marker tests.
- The standard GraphChart and all astrology calculation modules are untouched.

Before merging, review fit and 100% screenshots for bi-, tri-, quad-wheels,
including tight conjunctions close to house cusps. The numeric annotation
suppression is intentional only when fit is mathematically impossible.

## October 23: numeric label loss in bi-wheel (follow-up)

Screenshots comparing Glyphs only / Glyphs + degrees / Full positions showed
all planetary glyphs present, but numeric labels disappeared in the latter
two modes. Root cause: the first independent-degree solver looked only in a
narrow radial strip and angular window, and rejected numbers near cusps as
if they were actual planet glyphs.

- Replaced that solver with measured candidates spread through the usable
  planetary annulus, testing both radial sides and a wider local angular
  window. Prioritizes close labels and scarce-space labels, tries to
  relocate an earlier label when one conflict prevents another.
- Sign/house requirements remain strict for **planetary glyphs**; numeric
  annotations may shift slightly across a nearby boundary if needed.
  They are visual metadata, not the displayed planetary position.
- Never paints numbers on top of real planetary glyphs or other degree
  labels. All exact degree/minute positions remain available on hover.
- Thin tinted connecting lines associate numeric annotations with their
  planets when the annotation must be moved significantly.
- Added nine-body degree and full-position collision regression tests.

Verify the actual chart screenshots again before merging. Exceptional
unplaceable labels are still reported rather than drawn over a glyph.

## October 23: chart-local house lines (latest)

- Initial fix removed the 30° zodiac spokes from the planetary rings
  because they were indistinguishable from house separators. The following
  revision restores these spokes in a much lighter style.
- Each planetary ring contains its own chart's house cusps and angles,
  plus independently styled zodiac sign guides when not coincident with
  those house cusps. All spokes remain confined to their respective fields.
- All house segments use their selected chart's cusp longitudes and an
  inward 1.25 px inset at both ring edges. This avoids antialias spill
  into the shared zodiac, separator gaps and neighbouring charts.
- Added pure geometry tests with different radix and outer cusps, and
  a GUI regression that deliberately offsets an outer chart's cusps,
  records each actual house stroke, and asserts the longitude/source and
  radial limits for both radix and outer chart.
- This affects multiwheel drawing only, not the traditional single
  chart, comparison grid or any astrology calculation code.

Note: if the user intentionally selects the same chart twice, both charts
will correctly have the same house longitudes, but each line will still
stop inside its own field rather than extending between the two charts.

## October 23: faint zodiac guides, Whole Sign cusp priority

- Keep zodiac divisions visible throughout planetary rings in a muted,
  thin, neutral-grey style mixed with the actual local ring background.
  These are **not** house cusps, which keep the stronger ring-specific
  colour and remain confined to their chart's boundaries.
- Zodiac guides never cross the chart's annulus or its empty separator
  gaps. The radix retains its inner house-number spokes; its faint zodiac
  references appear only in the planetary zone.
- Each chart independently compares its own displayed cusps to all 12
  sign boundaries. When a cusp matches a sign boundary within 0.02°,
  omit that zodiac guide; the house line already marks the division.
- In Whole Sign houses, all twelve sign guides are redundant and all are
  omitted. For other systems, non-coincident zodiac guides remain visible.
  If houses are hidden, all 12 zodiac guides are still drawn.
- Tests cover cusp/sign angular wrap, mixed coincidences, different
  house cusp arrays, and a GUI renderer check of non-coincident versus
  Whole Sign situations.
- This change affects only the multiwheel drawing and tests; the
  single-wheel GraphChart, calculations and comparison grid stay untouched.
