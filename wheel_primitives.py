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
