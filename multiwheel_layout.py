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


def allocate_traditional_rings(max_radius, count, show_terms=False, show_decans=False,
                               reference_outside=False):
    """Allocate one shared zodiac and optional dignity bands.

    Normal:   radix -> decans -> terms -> zodiac -> outer charts
    Exterior: radix -> outer charts -> decans -> terms -> zodiac

    The core size, band widths and planetary space are identical between
    modes: only the radial ordering changes. This lets users compare the
    two without changing the scaling of symbols or ring thicknesses.
    """
    if not 1 <= count <= 3:
        raise ValueError('Multi-wheel needs 1, 2 or 3 outer charts')
    if max_radius <= 0:
        raise ValueError('Radius must be positive')

    core_factor = {1: .53, 2: .42, 3: .32}[count]
    core = max_radius * core_factor
    band_fraction = {1: .065, 2: .058, 3: .050}[count]
    band_width = max_radius * band_fraction
    zodiac_width = max_radius * {1: .09, 2: .085, 3: .08}[count]
    reference_total = ((int(bool(show_decans)) + int(bool(show_terms))) *
                       band_width + zodiac_width)
    available_planets = max_radius - core - reference_total
    # The last chart gets a little more room, regardless of which layout
    # is being previewed.
    weights = [1.0] * count
    if count > 1:
        weights[-1] = 1.12
    planet_unit = available_planets / sum(weights)

    cursor = core
    def allocate_reference(start):
        decans = terms = None
        position = start
        if show_decans:
            decans = (position, position + band_width)
            position = decans[1]
        if show_terms:
            terms = (position, position + band_width)
            position = terms[1]
        zodiac = (position, position + zodiac_width)
        return decans, terms, zodiac, zodiac[1]

    if not reference_outside:
        decans, terms, zodiac, cursor = allocate_reference(cursor)

    rings = []
    for weight in weights:
        following = cursor + planet_unit * weight
        rings.append((cursor, following))
        cursor = following

    if reference_outside:
        decans, terms, zodiac, cursor = allocate_reference(cursor)

    # Absorb floating-point accumulation into the very outer boundary.
    if reference_outside:
        zodiac = (zodiac[0], max_radius)
    else:
        rings[-1] = (rings[-1][0], max_radius)
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


def _rect_inside_annulus(rect, inner, outer):
    """Test the full ink rectangle, not just its centre or radial tangent."""
    import math
    x1, y1, x2, y2 = rect
    near_x = 0 if x1 <= 0 <= x2 else min(abs(x1), abs(x2))
    near_y = 0 if y1 <= 0 <= y2 else min(abs(y1), abs(y2))
    far = max(math.hypot(x, y) for x in (x1, x2) for y in (y1, y2))
    return math.hypot(near_x, near_y) >= inner and far <= outer


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


def place_planet_label_groups(longitudes, glyph_boxes, text_boxes, edges, asc,
                              direction, house_cusps=None, maximum_shift=7.5):
    """Place each glyph and its position as an inseparable two-part label.

    The text can sit beside the glyph in the tangential direction when the
    band is too narrow to stack it radially. Both move *together*, never in
    separate placement passes. A small beam search considers neighbours
    globally, and even in an impossible conjunction no position is hidden.
    The exact longitude remains available for a leader on the degree dial.
    """
    import math

    if not (len(longitudes) == len(glyph_boxes) == len(text_boxes)):
        raise ValueError('Each planet needs a glyph and position box')
    if edges[1] <= edges[0] or direction not in (-1, 1) or maximum_shift < 0:
        raise ValueError('Invalid planetary band, direction or shift')
    if house_cusps is not None and len(house_cusps) != 12:
        raise ValueError('Expected twelve chart-specific house cusps')
    if not longitudes:
        return [], []
    if any(min(*box) <= 0 for box in glyph_boxes + text_boxes):
        raise ValueError('Label box dimensions must be positive')

    inner, outer = edges
    sources = [float(lon) % 360 for lon in longitudes]
    trials = (0, -.5, .5, -1, 1, -2, 2, -3.5, 3.5,
              -5, 5, -6.5, 6.5, -7.5, 7.5)
    candidate_sets = []
    for i, original in enumerate(sources):
        original_sign = int(original // 30)
        original_house = (house_sector(original, house_cusps)
                          if house_cusps is not None else None)
        glyph_box, text_box = glyph_boxes[i], text_boxes[i]
        candidates = []
        for shift in trials:
            if abs(shift) > maximum_shift:
                continue
            displayed = (original + shift) % 360
            if int(displayed // 30) != original_sign:
                continue
            if (original_house is not None and
                    house_sector(displayed, house_cusps) != original_house):
                continue
            theta = math.pi + math.radians(asc - displayed)
            radial = (math.cos(theta), math.sin(theta))
            tangent = (-radial[1], radial[0])
            reach_g = _radial_reach(glyph_box, theta)
            reach_t = _radial_reach(text_box, theta)
            tangent_g = _radial_reach(glyph_box, theta + math.pi / 2)
            tangent_t = _radial_reach(text_box, theta + math.pi / 2)
            # Tangential pairs make good compact labels: the text remains
            # next to its glyph without consuming another radial row.
            side = 1 if tangent[1] >= 0 else -1
            tangential_distance = tangent_g + tangent_t + 2.5
            radial_distance = reach_g + reach_t + 2.5
            layouts = (
                # Like the normal Morinus chart, prefer degree text just
                # beneath the planet whenever the annulus accommodates it.
                ('below', 0.0, 0.0,
                 (glyph_box[1] + text_box[1]) / 2 + 2.5, 0.0),
                ('beside', side * tangential_distance, 0.0, 0.0, 2.0),
                ('beside', -side * tangential_distance, 0.0, 0.0, 5.0),
                ('stacked', 0.0, direction * radial_distance, 0.0, 5.5),
                ('stacked', 0.0, -direction * radial_distance, 0.0, 10.0),
            )
            for style, tangential_offset, radial_offset, downward, style_cost in layouts:
                # Offsets are relative to the glyph: the leader always
                # terminates at the glyph and never at a floating number.
                # Centre the combined pair, accounting for its two boxes.
                dx = (tangential_offset * tangent[0] +
                      radial_offset * radial[0])
                dy = (tangential_offset * tangent[1] +
                      radial_offset * radial[1] + downward)
                gx, gy = -dx / 2, -dy / 2
                tx, ty = dx / 2, dy / 2
                group_extent = max(_radial_reach(glyph_box, theta) +
                                   gx * radial[0] + gy * radial[1],
                                   _radial_reach(text_box, theta) +
                                   tx * radial[0] + ty * radial[1])
                group_inset = min(-_radial_reach(glyph_box, theta) +
                                  gx * radial[0] + gy * radial[1],
                                  -_radial_reach(text_box, theta) +
                                  tx * radial[0] + ty * radial[1])
                minimum = inner + 2.0 - group_inset
                maximum = outer - 2.0 - group_extent
                middle = (minimum + maximum) / 2.0
                if minimum <= maximum:
                    centres = (middle, minimum, maximum,
                               (2 * minimum + maximum) / 3,
                               (minimum + 2 * maximum) / 3)
                else:
                    # Still show every numeric label at the best possible
                    # centre when a narrow wheel cannot physically fit it.
                    centres = ((inner + outer - group_inset - group_extent) / 2,)
                for radius in centres:
                    cx, cy = _polar_point(asc, displayed, radius)
                    glyph = (cx + gx, cy + gy)
                    position = (cx + tx, cy + ty)
                    glyph_rect = _rect(glyph, glyph_box, margin=1.0)
                    text_rect = _rect(position, text_box, margin=1.0)
                    fits = (radius >= minimum - .01 and
                            radius <= maximum + .01 and
                            _rect_inside_annulus(glyph_rect, inner, outer) and
                            _rect_inside_annulus(text_rect, inner, outer))
                    # The *text*, not just the glyph, should remain inside
                    # the planet's sign whenever geometrically possible.
                    label_angle = (asc - math.degrees(math.atan2(
                        position[1], position[0])) + 180) % 360
                    wrong_sign = int(label_angle // 30) != original_sign
                    wrong_house = (original_house is not None and
                                   house_sector(label_angle, house_cusps) != original_house)
                    score = (abs(shift) * 6.0 + style_cost +
                             abs(radius - (inner + outer) / 2) * .15 +
                             (55 if wrong_sign else 0) +
                             (30 if wrong_house else 0) +
                             (12000 if not fits else 0))
                    candidates.append((score, {
                        'longitude': displayed, 'exact': original,
                        'glyph': glyph, 'position': position,
                        'rect': glyph_rect, 'rects': (glyph_rect, text_rect),
                        'radius': math.hypot(*glyph), 'fits': fits,
                        'style': style,
                    }))
        candidates.sort(key=lambda item: item[0])
        candidate_sets.append(candidates[:90])

    # Constrained bodies first; retaining several complete alternatives is
    # much better for conjunctions than a greedy placement one planet at a time.
    neighbours = [min((abs((lon - other + 180) % 360 - 180)
                       for j, other in enumerate(sources) if j != i),
                      default=360) for i, lon in enumerate(sources)]
    order = sorted(range(len(sources)), key=lambda i: (
        neighbours[i], len(candidate_sets[i]), i))
    beams = [(0.0, {})]
    for i in order:
        expanded = []
        for total, picked in beams:
            for own_score, candidate in candidate_sets[i]:
                overlap = sum(
                    _intersect_area(a, b)
                    for previous in picked.values()
                    for a in candidate['rects']
                    for b in previous['rects'])
                updated = picked.copy()
                updated[i] = candidate
                expanded.append((total + own_score + overlap * 1000, updated))
        expanded.sort(key=lambda item: item[0])
        beams = expanded[:24]
    selected = beams[0][1]
    unresolved = sorted(i for i, current in selected.items()
                        if not current['fits'] or any(
                            _intersect_area(a, b) > 0
                            for j, previous in selected.items() if j != i
                            for a in current['rects'] for b in previous['rects']))
    return [selected[i] for i in range(len(sources))], unresolved


def place_degree_annotations(glyphs, longitudes, text_boxes, edges, asc,
                             direction, house_cusps=None):
    """Fit numeric labels *around* fixed glyphs using the available annulus.

    Earlier versions tested only one narrow row on one side of a planet,
    then silently dropped most numbers in crowded signs. Labels are not
    planets: a number may sit to either side of its glyph and even cross a
    nearby cusp. The glyph and the exact-longitude dial remain in their
    correct house/sign. Prefer same-sector labels, but do not demand them.
    Returns label positions and genuinely unplaceable indices.
    """
    import math
    if not (len(glyphs) == len(longitudes) == len(text_boxes)):
        raise ValueError('Degree labels must match glyphs and longitudes')
    if edges[1] <= edges[0] or direction not in (-1, 1):
        raise ValueError('Invalid degree band or direction')
    if house_cusps is not None and len(house_cusps) != 12:
        raise ValueError('Expected twelve chart-specific house cusps')
    if not glyphs:
        return [], []

    occupied_glyphs = [p['rect'] for p in glyphs]
    inner, outer = edges
    # A numeric label can move into unused space of its chart band.
    # Use signed angular offsets in both directions and several radial
    # lanes. Labels nearest their planet are always favoured.
    angle_shifts = (0, -.5, .5, -1, 1, -1.75, 1.75, -2.5, 2.5,
                    -3.5, 3.5, -5, 5, -7, 7, -9, 9, -11, 11,
                    -13, 13, -16, 16)
    candidate_sets = []
    for i, (glyph, source_lon, box) in enumerate(
            zip(glyphs, longitudes, text_boxes)):
        if box[0] <= 0 or box[1] <= 0:
            candidate_sets.append([])
            continue
        glyph_pos = glyph['glyph']
        glyph_lon = glyph['longitude']
        glyph_radius = glyph['radius']
        sign = int((source_lon % 360) // 30)
        house = (house_sector(source_lon, house_cusps)
                 if house_cusps is not None else None)
        theta = math.pi + math.radians(asc - glyph_lon)
        glyph_width = glyph['rect'][2] - glyph['rect'][0] - 2.4
        glyph_height = glyph['rect'][3] - glyph['rect'][1] - 2.4
        preferred_radius = glyph_radius + direction * (
            _radial_reach((glyph_width, glyph_height), theta) +
            _radial_reach(box, theta) + 3.0)
        candidates = []
        for shift in angle_shifts:
            display_lon = (glyph_lon + shift) % 360
            display_theta = math.pi + math.radians(asc - display_lon)
            reach = _radial_reach(box, display_theta)
            min_radius = inner + reach + 2
            max_radius = outer - reach - 2
            if min_radius > max_radius:
                continue
            # Quantize radial positions to ~3px and include the preferred
            # radius, so tiny rings and wide outer ones both behave well.
            radii = [min_radius, max_radius,
                     max(min_radius, min(max_radius, preferred_radius))]
            step_count = max(1, int((max_radius - min_radius) / 3.0))
            radii.extend(min_radius + k * (max_radius - min_radius) /
                         step_count for k in range(step_count + 1))
            for radius in radii:
                point = _polar_point(asc, display_lon, radius)
                ink_rect = _rect(point, box, margin=.8)
                if any(_intersect_area(ink_rect, other) > 0
                       for other in occupied_glyphs):
                    continue
                distance = math.hypot(point[0] - glyph_pos[0],
                                      point[1] - glyph_pos[1])
                # Do not confuse planets by putting a number on the other
                # side of the chart. The limit scales with chart radius.
                if distance > max(40.0, min(65.0, glyph_radius * .18)):
                    continue
                sector_cost = 0
                if int(display_lon // 30) != sign:
                    sector_cost += 17
                if (house is not None and
                        house_sector(display_lon, house_cusps) != house):
                    sector_cost += 12
                opposite = (radius - glyph_radius) * direction < 0
                cost = (distance + abs(shift) * .30 +
                        abs(radius - preferred_radius) * .16 +
                        (6 if opposite else 0) + sector_cost)
                candidates.append((cost, point, ink_rect))
        # Deduplicate candidates with identical rounded coordinates.
        candidates.sort(key=lambda item: item[0])
        seen = set()
        unique = []
        for candidate in candidates:
            key = tuple(round(v, 1) for v in candidate[1])
            if key not in seen:
                unique.append(candidate)
                seen.add(key)
        candidate_sets.append(unique)

    # Constrained first: reserve the scarce nearby positions before less
    # crowded planets claim them. Every placement must avoid *all* glyphs.
    def close_count(index):
        candidates = candidate_sets[index]
        if not candidates:
            return 0
        best_cost = candidates[0][0]
        return sum(c[0] <= best_cost + 11 for c in candidates)

    order = sorted(range(len(glyphs)), key=lambda i: (
        close_count(i), len(candidate_sets[i]), i))
    selected = {}
    def fits(candidate, exclude=None):
        return all(_intersect_area(candidate[2], other[2]) == 0
                   for j, other in selected.items() if j != exclude)

    for i in order:
        for candidate in candidate_sets[i]:
            if fits(candidate):
                selected[i] = candidate
                break
        if i in selected:
            continue
        # Repair one earlier greedy placement before hiding the number.
        # This is cheap for the maximum nine planetary glyphs in a chart.
        for candidate in candidate_sets[i]:
            conflict = [j for j, other in selected.items()
                        if _intersect_area(candidate[2], other[2]) > 0]
            if len(conflict) != 1:
                continue
            victim = conflict[0]
            previous = selected.pop(victim)
            selected[i] = candidate
            replacement = next((alternative for alternative in
                                candidate_sets[victim] if fits(alternative)),
                               None)
            if replacement is not None:
                selected[victim] = replacement
                break
            selected.pop(i)
            selected[victim] = previous

    points = [selected[i][1] if i in selected else None
              for i in range(len(glyphs))]
    hidden = [i for i in range(len(glyphs)) if i not in selected]
    return points, hidden
