"""Pure geometry for the extra rings of a traditional multi-wheel."""


def allocate_rings(max_radius, count):
    """Return (radix edge, zodiac edges, outer ring edges), inside to outside.

    All radii are measured from the same centre, so adding a ring never
    requires different drawing branches.
    """
    if not 1 <= count <= 3:
        raise ValueError('Multi-wheel needs 1, 2 or 3 outer charts')
    if max_radius <= 0:
        raise ValueError('Radius must be positive')
    core = max_radius * (0.62 - 0.06 * count)
    zodiac_outer = core + max_radius * 0.10
    band = (max_radius - zodiac_outer) / count
    rings = [(zodiac_outer + i * band, zodiac_outer + (i + 1) * band)
             for i in range(count)]
    return core, (core, zodiac_outer), rings


def spread_longitudes(longitudes, minimum=8.0):
    """Spread glyphs on a circle, preserving their cyclic zodiacal order.

    Return in the original object's order. Break at the largest unoccupied
    arc, so a cluster across 0 Aries is spread as one group.
    """
    n = len(longitudes)
    if n == 0:
        return []
    if minimum < 0 or minimum * n > 360.0:
        raise ValueError('Minimum separation cannot fit on a circle')
    if n == 1:
        return [longitudes[0] % 360.0]
    ordered = sorted(range(n), key=lambda i: (longitudes[i] % 360.0, i))
    gaps = [((longitudes[ordered[(i + 1) % n]] -
              longitudes[ordered[i]]) % 360.0) for i in range(n)]
    # Equal longitudes are still distinct: the last-to-first gap is 360,
    # not zero, when every glyph shares one longitude.
    if max(gaps) == 0.0:
        gaps[-1] = 360.0
    pivot = (max(range(n), key=lambda i: gaps[i]) + 1) % n
    indices = ordered[pivot:] + ordered[:pivot]
    raw = []
    for i in indices:
        v = longitudes[i] % 360.0
        if raw:
            while v < raw[-1]:
                v += 360.0
        raw.append(v)
    # Greedy minimum-gap projection, then enforce the closing 360-degree gap.
    pos = [raw[0]]
    for v in raw[1:]:
        pos.append(max(v, pos[-1] + minimum))
    limit = pos[0] + 360.0 - minimum
    if pos[-1] > limit:
        pos[-1] = limit
        for j in range(n - 2, 0, -1):
            pos[j] = min(pos[j], pos[j + 1] - minimum)
    # Recentre the glyph group, not the zodiac itself; exact ticks still use
    # the source longitudes.
    shift = sum(pos[j] - raw[j] for j in range(n)) / n
    result = [0.0] * n
    for i, lon in zip(indices, pos):
        result[i] = (lon - shift) % 360.0
    return result
