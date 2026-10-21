# A5 table-display architecture

The bitmap-backed table windows share `commonwnd.CommonWnd`. The detailed
Placidian and Regiomontanian specula instead have two older, separate renderers
(`positionswnd.py` and `positionswnd2.py`); their columns, values and precision
are intentionally left untouched.

A5 includes a modest tinted header for the speculum and other selected tables
without changing their layout or contents. Monochrome rendering retains
the old white background.

In CommonWnd, bitmap zoom now uses Pillow Lanczos with restrained unsharp
filtering, rather than repeatedly interpolating an already zoomed bitmap.
The source `self.buffer` is untouched, so saving and copying images stay at
their original resolution. Ctrl+wheel preserves the source point under the
cursor; menu zoom keeps the viewport center. A maximum raster size avoids
massive transient allocations on long tables.

`tableRows()` is a typed CSV extension point. It defaults to the historical
text-collection mechanism. The Miscellaneous table now provides explicit
two-column rows from its original numeric calculations; other tables are not
yet claimed to be semantically structured. Their export remains compatible.

There is no change to the astrological calculations, original `.opt` files,
or default font-size setting.

Test:
`python -m unittest discover -s tests -p 'test_tablepresentation.py'`

GUI review: open Positions (Placidian and Regiomontanian), Mundane Positions,
Firdaria, Miscellaneous and Aspects. Check column headers and glyphs, narrow
and wide windows, zoom, anchor under Ctrl+wheel, monochrome mode, copy as
image and CSV from Miscellaneous. Long tables must scroll smoothly. Check
the values/column order against the A4 checkpoint.
