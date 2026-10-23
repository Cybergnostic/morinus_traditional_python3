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


def allocate_traditional_rings(max_radius, count, show_terms=False, show_decans=False):
    """Allocate exactly one shared zodiac, terms and decans reference system.

    Order from the centre: radix, decans, terms, zodiac, outer charts.
    Optional bands are None when disabled; outer charts only contain their
    chart-specific information. Radii are continuous and never overlap.
    """
    if not 1 <= count <= 3:
        raise ValueError('Multi-wheel needs 1, 2 or 3 outer charts')
    if max_radius <= 0:
        raise ValueError('Radius must be positive')

    # A planetary label needs at least three radial rows.  The old bi-wheel
    # reserved 61.5% for the radix and left only 15.5% for its outer chart.
    # These allocations balance the available ink space across the charts.
    # When the available screen is smaller than a readable layout, the viewer
    # renders on a larger scrollable canvas instead of shrinking the text.
    core_factor = {1: .53, 2: .42, 3: .32}[count]
    core = max_radius * core_factor
    band_fraction = {1: .065, 2: .058, 3: .050}[count]
    band_width = max_radius * band_fraction
    zodiac_width = max_radius * {1: .09, 2: .085, 3: .08}[count]
    cursor = core
    decans = None
    if show_decans:
        decans = (cursor, cursor + band_width)
        cursor = decans[1]
    terms = None
    if show_terms:
        terms = (cursor, cursor + band_width)
        cursor = terms[1]
    zodiac = (cursor, cursor + zodiac_width)
    cursor = zodiac[1]
    weights = [1.0] * count
    if count > 1:
        weights[-1] = 1.12
    unit = (max_radius - cursor) / sum(weights)
    rings = []
    for weight in weights:
        next_edge = cursor + unit * weight
        rings.append((cursor, next_edge))
        cursor = next_edge
    return core, decans, terms, zodiac, rings


def zodiac_sign_lane(edges):
    """The sign glyphs sit between the tick-lane divider and the outer edge.

    The longest degree ticks end at 28% of the band, leaving clear space
    before the sign-lane circle at 38%.
    """
    inner, outer = edges
    if outer <= inner:
        raise ValueError('Zodiac band must have positive width')
    return inner + (outer - inner) * .38, outer


def shared_planet_font_sizes(max_radius, content_band_widths):
    """One measured font scale shared by radix and every outer chart.

    Use the narrowest *usable* content band after removing its degree dial
    and separator. The 12px minimum keeps glyphs legible in Fit mode;
    the viewer's zoom is available if the groups cannot physically fit.
    """
    if max_radius <= 0 or not content_band_widths or any(
            width <= 0 for width in content_band_widths):
        raise ValueError('Need a radius and positive planetary content widths')
    # The symbol is the primary information. Numeric annotations no longer
    # have to fit inside its bounding box, so they cannot shrink the glyph.
    glyph = max(17, int(min(max_radius * .060,
                            min(content_band_widths) * .75)))
    return {
        'glyph': glyph,
        'degree': max(9, int(glyph * .46)),
        'minute': max(9, int(glyph * .42)),
        'motion': max(9, int(glyph * .42)),
    }


def _polar_point(asc, longitude, radius):
    """Cartesian offset in Morinus's left-Ascendant orientation."""
    import math
    angle = math.pi + math.radians(asc - longitude)
    return math.cos(angle) * radius, math.sin(angle) * radius


def _radial_reach(box, angle):
    import math
    return (abs(math.cos(angle)) * box[0] +
            abs(math.sin(angle)) * box[1]) * .5


def _rect(point, box, margin=1.0):
    x, y = point
    return (x - box[0] / 2 - margin, y - box[1] / 2 - margin,
            x + box[0] / 2 + margin, y + box[1] / 2 + margin)


def _intersect_area(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(
        0, min(a[3], b[3]) - max(a[1], b[1]))


def _planet_candidate(exact, longitude, offset, asc, edges, boxes):
    """Place one measured glyph/degree/minute/optional-motion group."""
    import math
    inner, outer = edges
    glyph_box, degree_box, minute_box, motion_box = boxes
    theta = math.pi + math.radians(asc - longitude)
    reaches = [_radial_reach(b, theta)
               for b in (glyph_box, degree_box, minute_box)]
    width = outer - inner
    gap = min(2.4, max(0, (width - 4 - 2 * sum(reaches)) / 2))
    span = 2 * sum(reaches) + 2 * gap
    # Centre the full three-tier group in the band, not against its rim.
    r_glyph = (inner + outer + span) / 2 - reaches[0] + offset
    r_degree = r_glyph - reaches[0] - reaches[1] - gap
    r_minute = r_degree - reaches[1] - reaches[2] - gap
    radii = (r_glyph, r_degree, r_minute)
    points = [_polar_point(asc, longitude, radius) for radius in radii]
    points = tuple(points)
    labels = (glyph_box, degree_box, minute_box)
    rects = [_rect(point, box) for point, box in zip(points, labels)]
    motion_point = None
    if motion_box[0] > 0:
        # Keep the retrograde mark next to the minute, not as a fourth
        # circular row.  This uses the same tangent on every chart.
        tangential = lambda b: (abs(math.sin(theta)) * b[0] +
                                abs(math.cos(theta)) * b[1]) * .5
        distance = tangential(minute_box) + tangential(motion_box) + 2
        mx, my = points[2]
        motion_point = (mx - math.sin(theta) * distance,
                        my + math.cos(theta) * distance)
        rects.append(_rect(motion_point, motion_box))
    fits = (r_glyph + reaches[0] <= outer - 1 and
            r_minute - reaches[2] >= inner + 1)
    return {'longitude': longitude % 360, 'offset': offset,
            'glyph': points[0], 'degree': points[1],
            'minute': points[2], 'motion': motion_point,
            'rects': rects, 'fits': fits, 'exact': exact % 360}


def place_planet_clusters(longitudes, box_groups, edges, asc,
                          maximum_shift=8.0):
    """Measured 2-D planet placement, with sign-constrained angular shifts.

    Glyphs, degrees, minutes and retrograde signs are treated as one object.
    Test candidate angular and radial lanes against previously placed ink
    rectangles. Do not move a planet's label into another zodiac sign.
    Exact longitudes never change: callers draw leaders to the original
    point on the degree dial.

    Returns (placements in input order, indices with unresolved collisions).
    If no non-overlapping candidate exists we *report* it; the viewer should
    offer a larger canvas rather than silently misrepresenting the chart.
    """
    import math
    if len(longitudes) != len(box_groups):
        raise ValueError('Every planet requires a group of measured labels')
    if edges[1] <= edges[0]:
        raise ValueError('Planetary band must have positive width')
    if not longitudes:
        return [], []
    if maximum_shift < 0:
        raise ValueError('Maximum shift must be nonnegative')
    n = len(longitudes)
    longitudes = [lon % 360 for lon in longitudes]
    # Prioritise conjunctions, which have fewer unconstrained locations.
    neighbours = [min((abs((lon - other + 180) % 360 - 180)
                       for j, other in enumerate(longitudes) if j != i),
                      default=360) for i, lon in enumerate(longitudes)]
    order = sorted(range(n), key=lambda i: (neighbours[i], longitudes[i], i))
    placed = {}
    unresolved = []
    trials = (0, -1, 1, -2, 2, -3.5, 3.5, -5, 5, -6.5, 6.5, -8, 8)
    inner, outer = edges
    for i in order:
        lon = longitudes[i]
        group = box_groups[i]
        base = _planet_candidate(lon, lon, 0, asc, edges, group)
        # At steep angles the radial extent of a horizontal text label
        # changes. Compute a safe lane based on available radial slack.
        a = math.pi + math.radians(asc - lon)
        reach = sum(_radial_reach(b, a) for b in group[:3])
        slack = max(0, outer - inner - (2 * reach + 8))
        lane = min(11.0, slack * .36)
        offsets = (0, -lane, lane, -lane * 1.5, lane * 1.5)
        best = None
        best_score = float('inf')
        for delta in trials:
            if abs(delta) > maximum_shift + 1e-8:
                continue
            shifted = (lon + delta) % 360
            # Enforce sign membership using source longitude, not distance
            # to the closest sign border.
            if int(shifted // 30) != int(lon // 30):
                continue
            for off in offsets:
                candidate = _planet_candidate(
                    lon, shifted, off, asc, edges, group)
                collisions = sum(_intersect_area(a, b)
                                 for prior in placed.values()
                                 for a in candidate['rects']
                                 for b in prior['rects'])
                overflow = 0 if candidate['fits'] else 10000
                # Keeping the *centre* inside a sign is insufficient: the
                # horizontal text box can still straddle the division line.
                # Prefer candidates with enough tangent clearance for ink.
                theta = math.pi + math.radians(asc - shifted)
                tangent = max((abs(math.sin(theta)) * box[0] +
                               abs(math.cos(theta)) * box[1]) * .5
                              for box in group[:3])
                radius = max(1.0, (inner + outer) * .5)
                clearance = math.degrees(math.atan((tangent + 1.0) / radius))
                sign_degree = shifted % 30
                sign_penalty = (900 if sign_degree < clearance or
                                sign_degree > 30 - clearance else 0)
                score = (collisions * 100 + overflow + sign_penalty +
                         abs(delta) * 1.3 + abs(off) * .35)
                if score < best_score:
                    best, best_score = candidate, score
                if score == 0:
                    break
            if best_score == 0:
                break
        if best is None:
            best = base
        if not best['fits'] or any(
                _intersect_area(a, b) > 0
                for prior in placed.values()
                for a in best['rects'] for b in prior['rects']):
            unresolved.append(i)
        placed[i] = best
    return [placed[i] for i in range(n)], sorted(unresolved)


def house_sector(longitude, cusps):
    """Zero-based house containing a zodiac longitude; cusps in house order.

    Houses are chart-specific. At a cusp, the planet belongs to the house
    beginning there. Works across the Aries wrap (e.g. 350° to 18°).
    """
    if len(cusps) != 12:
        raise ValueError('House layout requires twelve ordered cusps')
    lon = longitude % 360.0
    for i, beginning in enumerate(cusps):
        span = (cusps[(i + 1) % 12] - beginning) % 360.0
        if span > 0 and (lon - beginning) % 360.0 < span:
            return i
    # Degenerate cusp sets (e.g. collapsed house systems near the poles):
    # use the most recent cusp in zodiacal longitude deterministically.
    return min(range(12), key=lambda i: (lon - cusps[i]) % 360.0)


def place_planet_glyphs(longitudes, glyph_boxes, edges, asc,
                        house_cusps=None, maximum_shift=7.5):
    """Lay out glyphs *without* considering degree/minute text.

    Exact longitude, sign and chart-local house are protected. Move the
    glyph radially before moving it around the zodiac. Return positions in
    source order plus unresolved indices (never silently hide a planet).
    """
    import math
    if len(longitudes) != len(glyph_boxes):
        raise ValueError('Each glyph requires a measured box')
    if edges[1] <= edges[0] or maximum_shift < 0:
        raise ValueError('Invalid glyph band or maximum shift')
    if house_cusps is not None and len(house_cusps) != 12:
        raise ValueError('Expected twelve chart-specific house cusps')
    if not longitudes:
        return [], []

    longitudes = [float(lon) % 360.0 for lon in longitudes]
    neighbours = [min((abs((lon - other + 180) % 360 - 180)
                       for j, other in enumerate(longitudes) if j != i),
                      default=360) for i, lon in enumerate(longitudes)]
    order = sorted(range(len(longitudes)),
                   key=lambda i: (neighbours[i], longitudes[i], i))
    placed = {}
    unresolved = []
    inner, outer = edges
    base_radius = (inner + outer) / 2.0
    angular_trials = (0, -0.5, 0.5, -1, 1, -2, 2, -3.5, 3.5,
                      -5, 5, -6.5, 6.5, -7.5, 7.5)
    for i in order:
        original = longitudes[i]
        original_sign = int(original // 30)
        original_house = (house_sector(original, house_cusps)
                          if house_cusps is not None else None)
        box = glyph_boxes[i]
        if box[0] <= 0 or box[1] <= 0:
            raise ValueError('Glyph box dimensions must be positive')
        best = None
        best_score = float('inf')
        for shift in angular_trials:
            if abs(shift) > maximum_shift:
                continue
            displayed = (original + shift) % 360
            if int(displayed // 30) != original_sign:
                continue
            if (original_house is not None and
                    house_sector(displayed, house_cusps) != original_house):
                continue
            theta = math.pi + math.radians(asc - displayed)
            reach = _radial_reach(box, theta)
            slack = max(0, (outer - inner) / 2 - reach - 2.0)
            radial_trials = (0, -slack * .33, slack * .33,
                             -slack * .66, slack * .66,
                             -slack, slack)
            for offset in radial_trials:
                radius = base_radius + offset
                point = _polar_point(asc, displayed, radius)
                box_rect = _rect(point, box, margin=1.2)
                fits = (radius - reach >= inner + 1 and
                        radius + reach <= outer - 1)
                overlap = sum(_intersect_area(box_rect, p['rect'])
                              for p in placed.values())
                score = ((0 if fits else 100000) + overlap * 1000 +
                         abs(shift) * 6.0 + abs(offset) * .28)
                if score < best_score:
                    best_score = score
                    best = {'longitude': displayed, 'exact': original,
                            'glyph': point, 'rect': box_rect, 'radius': radius,
                            'fits': fits, 'offset': offset}
        if best is None:
            raise ValueError('No valid glyph candidate')
        if not best['fits'] or any(
                _intersect_area(best['rect'], p['rect']) > 0
                for p in placed.values()):
            unresolved.append(i)
        placed[i] = best
    return [placed[i] for i in range(len(longitudes))], sorted(unresolved)


def place_degree_annotations(glyphs, longitudes, text_boxes, edges, asc,
                             direction, house_cusps=None):
    """Fit optional degree text around fixed glyphs, never move a glyph.

    Returns optional Cartesian label centres and hidden indices. Label
    collisions never affect the primary glyph positions. The centre of a
    numeric annotation stays in its planet's sign and house.
    """
    import math
    if not (len(glyphs) == len(longitudes) == len(text_boxes)):
        raise ValueError('Degree labels must match glyphs and longitudes')
    if edges[1] <= edges[0] or direction not in (-1, 1):
        raise ValueError('Invalid degree band or direction')
    if house_cusps is not None and len(house_cusps) != 12:
        raise ValueError('Expected twelve chart-specific house cusps')
    glyph_rects = [p['rect'] for p in glyphs]
    placed_rects = []
    points = []
    hidden = []
    for i, (glyph, source_lon, box) in enumerate(
            zip(glyphs, longitudes, text_boxes)):
        if box[0] <= 0 or box[1] <= 0:
            points.append(None)
            continue
        original_sign = int((source_lon % 360) // 30)
        original_house = (house_sector(source_lon, house_cusps)
                          if house_cusps is not None else None)
        base_longitude = glyph['longitude']
        theta = math.pi + math.radians(asc - base_longitude)
        glyph_w = glyph_rects[i][2] - glyph_rects[i][0] - 2.4
        glyph_h = glyph_rects[i][3] - glyph_rects[i][1] - 2.4
        glyph_reach = _radial_reach((glyph_w, glyph_h), theta)
        text_reach = _radial_reach(box, theta)
        ideal_radius = glyph['radius'] + direction * (
            glyph_reach + text_reach + 3.0)
        best = None
        best_score = float('inf')
        for shift in (0, -0.6, 0.6, -1.4, 1.4, -2.5, 2.5):
            label_lon = (base_longitude + shift) % 360.0
            if int(label_lon // 30) != original_sign:
                continue
            if (original_house is not None and
                    house_sector(label_lon, house_cusps) != original_house):
                continue
            label_theta = math.pi + math.radians(asc - label_lon)
            reach = _radial_reach(box, label_theta)
            for radial in (0, direction * 3, -direction * 3,
                           direction * 6, -direction * 6,
                           direction * 10, -direction * 10):
                r = ideal_radius + radial
                if r - reach < edges[0] + 2 or r + reach > edges[1] - 2:
                    continue
                point = _polar_point(asc, label_lon, r)
                rect = _rect(point, box, margin=.7)
                if any(_intersect_area(rect, other) > 0 for other in
                       glyph_rects + placed_rects):
                    continue
                score = abs(shift) * 6 + abs(radial)
                if score < best_score:
                    best = (point, rect)
                    best_score = score
        if best is None:
            points.append(None)
            hidden.append(i)
        else:
            points.append(best[0])
            placed_rects.append(best[1])
    return points, hidden
