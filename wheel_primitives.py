"""Drawing geometry and position labels shared by Morinus chart renderers.

Keep astrology/calculation modules out of this file.  Both the standard
GraphChart wheel and the multi-wheel use the same degree/minute formatting.
The geometric helpers accept radii, rather than embedding per-wheel sizes.
"""
import math

import util


def polar_point(cx, cy, asc, longitude, radius):
    """Morinus orientation: the reference Ascendant is at the left."""
    # Exactly the same normalisation used by GraphChart.drawHouses.
    angle = math.pi + math.radians(util.normalize(asc - longitude))
    return cx + math.cos(angle) * radius, cy + math.sin(angle) * radius


def position_text(longitude, degree_symbol):
    """Morinus's unrounded, two-part position format (degree / minute)."""
    d, m, _ = util.decToDeg(util.normalize(longitude))
    return (str(d % 30).zfill(2) + degree_symbol,
            str(m).zfill(2) + "'")


def angle_longitudes(ascendant, mc):
    """Four ecliptic angle longitudes in ASC/DSC/MC/IC order."""
    return (ascendant % 360, (ascendant + 180) % 360,
            mc % 360, (mc + 180) % 360)


def house_spoke_segments(cusps, inner, outer, inset=1.25):
    """Return chart-local (longitude, inner, outer) house line segments.

    Cusp longitudes must come from the *current* chart, already converted
    to display longitude. Inset each end so anti-aliased strokes stop inside
    the field and cannot bleed into adjacent rings or the zodiac strip.
    """
    if len(cusps) != 12:
        raise ValueError('Expected twelve chart-specific house cusps')
    if inner < 0 or outer <= inner or inset < 0 or 2 * inset >= outer - inner:
        raise ValueError('Invalid house-line annulus')
    return tuple((float(lon) % 360.0, inner + inset, outer - inset)
                 for lon in cusps)



def zodiac_guide_longitudes(cusps=None, tolerance=.02):
    """Sign divisions not already represented by this chart's house cusps.

    A cusp is equivalent when its distance to a sign boundary is within
    tolerance in degrees, including the 0/360 wrap. In Whole Sign houses
    every boundary coincides, leaving only house lines to draw.
    When house lines are switched off, pass None to keep all sign guides.
    """
    if tolerance < 0 or tolerance >= 15:
        raise ValueError('Invalid zodiac division tolerance')
    if cusps is not None and len(cusps) != 12:
        raise ValueError('Expected twelve chart-local cusps')
    def distance(a, b):
        return abs((a - b + 180.0) % 360.0 - 180.0)
    return tuple(float(boundary) for boundary in range(0, 360, 30)
                 if cusps is None or all(distance(boundary, cusp) > tolerance
                                         for cusp in cusps))


def planet_band_radii(inner, outer):
    """Morinus order, from the centre: motion, minutes, degrees, glyph.

    Positions are relative to a selected planetary band, so every outer
    chart uses precisely the same notation as the radix.
    """
    if outer <= inner:
        raise ValueError('Planetary band must have positive width')
    band = outer - inner
    return {
        'motion': inner + band * .12,
        'minute': inner + band * .30,
        'degree': inner + band * .51,
        'glyph': inner + band * .79,
        'tick': outer - max(2.0, min(8.0, band * .12)),
    }


def paint_glyph(draw, point, glyph, font, size, colour):
    """Original GraphChart glyph positioning (font-square centered)."""
    x, y = point
    draw.text((x - size // 2, y - size // 2), glyph, fill=colour, font=font)


def paint_position_text(draw, point, text, font, colour):
    """Original GraphChart degree/minute/motion text centering.

    Keep this distinct from Pillow's 'mm' anchor, which does not reproduce
    the decompiled Morinus wheel's text placement.
    """
    x, y = point
    width, height = draw.textbbox((0, 0), text, font=font)[2:]
    draw.text((x - width // 2, y - height // 2), text,
              fill=colour, font=font)


def optical_text_center(draw, point, text, font, colour):
    """Centre the *visible ink* of a glyph or position label on its point.

    PIL fonts can have different left/top bearings; the standard Morinus
    square-based symbol placement is preserved above for GraphChart, while
    densely packed multiwheel rings use consistent optical centring for
    all three label tiers.
    """
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    x, y = point
    draw.text((round(x - (left + right) / 2.0),
               round(y - (top + bottom) / 2.0)),
              text, fill=colour, font=font)


def radial_half_extent(size, angle):
    """Radial reach of a horizontal text bounding box at the given angle."""
    width, height = size
    return (abs(math.cos(angle)) * width +
            abs(math.sin(angle)) * height) / 2.0


def planet_cluster_radii(inner, outer, angle, glyph_box, degree_box,
                         minute_box, spacing=1.2):
    """Lay out one *centred* Morinus planet label group, outside to inside.

    The glyph, degree and minute share an angular position.  The gap between
    their visible boxes is computed from each label's true dimensions,
    rather than fixed percentages of the planetary band.  A retrograde or
    station mark belongs next to the minute label (tangentially), not on a
    fourth radial row.
    """
    if outer <= inner:
        raise ValueError('The planet band must have positive width')
    sizes = (glyph_box, degree_box, minute_box)
    reaches = [radial_half_extent(size, angle) for size in sizes]
    available = outer - inner - 4.0
    # Reduce inter-label whitespace before allowing labels to collide.
    free = available - 2.0 * sum(reaches)
    gap = min(spacing, max(0.0, free / 2.0))
    glyph = outer - 2.0 - reaches[0]
    degree = glyph - reaches[0] - reaches[1] - gap
    minute = degree - reaches[1] - reaches[2] - gap
    return {'glyph': glyph, 'degree': degree, 'minute': minute}


def compact_planet_radii(inner, outer, angle, glyph_box, position_box,
                        spacing=1.5):
    """Position a glyph over a single horizontal degree-minute label.

    The two rows share one longitude (the second row is closer to the
    centre). Use their actual font bounds to keep the visible ink together,
    without the variable gaps caused by percentage-based radii.
    """
    if outer <= inner:
        raise ValueError('The planet band must have positive width')
    glyph_reach = radial_half_extent(glyph_box, angle)
    position_reach = radial_half_extent(position_box, angle)
    free = outer - inner - 4.0 - 2.0 * (glyph_reach + position_reach)
    gap = min(spacing, max(0.0, free))
    # Centre the two-row group *in the available band*. Anchoring the
    # glyph to outer - 2 forced every planet to the rim of its chart.
    centre = (inner + outer) / 2.0
    # Opposite-row extents determine the two centres: both outside
    # edges are symmetric about the chosen band midpoint.
    glyph = centre + gap / 2.0 + position_reach
    position = centre - gap / 2.0 - glyph_reach
    return {'glyph': glyph, 'position': position}


def traditional_term_markers(terms):
    """Reproduce GraphChart's successive-bound approach to term geometry.

    Return (centre longitude, planet index, segment end longitude). The
    sign-specific rulers and unequal lengths come from Morinus's selected
    terms system; no independently estimated equal subdivisions.
    """
    for sign, divisions in enumerate(terms):
        cursor = float(sign * 30)
        for ruler, span in divisions:
            width = float(span)
            centre = cursor + width / 2.0
            cursor += width
            yield centre, ruler, cursor


def traditional_decan_markers(decans):
    """Return the precise 10-degree centres, rulers, and start lines.

    These are the same longitudes GraphChart.drawDecans uses (5, 15, 25
    degrees within each sign).
    """
    for sign, rulers in enumerate(decans):
        for part, ruler in enumerate(rulers):
            start = sign * 30 + part * 10
            yield start + 5.0, ruler, float(start)
