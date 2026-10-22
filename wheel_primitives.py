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
