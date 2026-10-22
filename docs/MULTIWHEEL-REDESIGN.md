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
