"""Pure navigation rules for related solar and lunar return rings.

The calculations and chart objects belong to returnslist; these helpers only
choose an event and determine which ring relationships are unambiguous.
"""


# Return charts can differ by seconds if cast through different dialogs.
JD_TOLERANCE = .02


def solar_year_window(year):
    """Five directly selectable solar years, centred on the active year."""
    return tuple(value for value in range(year - 2, year + 3)
                 if 1 <= value <= 9998)


def nearest_inner_solar(lunar_index, assignments):
    """Closest inner solar ring derived from exactly the same natal object.

    assignments contains (kind, radix) for each ring, with kind 'solar',
    'lunar' or None and radix None if origin is unknown. Names, dates and
    chart contents are intentionally NOT used as evidence of common origin.
    """
    kind, radix = assignments[lunar_index]
    if kind != 'lunar' or radix is None:
        return None
    for index in range(lunar_index - 1, -1, -1):
        candidate_kind, candidate_radix = assignments[index]
        if candidate_kind == 'solar' and candidate_radix is radix:
            return index
    return None


def linked_lunar_indices(solar_index, assignments):
    if solar_index < 0 or solar_index >= len(assignments):
        return ()
    kind, radix = assignments[solar_index]
    if kind != 'solar' or radix is None:
        return ()
    return tuple(index for index in range(solar_index + 1, len(assignments))
                 if nearest_inner_solar(index, assignments) == solar_index)


def match_return_index(rows, jd, tolerance=JD_TOLERANCE):
    """Find the same lunar event in a fresh year's return list."""
    if not rows:
        return None
    index = min(range(len(rows)), key=lambda i: abs(rows[i].jd - jd))
    return index if abs(rows[index].jd - jd) <= tolerance else None


def corresponding_return(old_rows, old_jd, new_rows):
    """The new natal's lunar return in the same position of the solar year.

    old_rows/new_rows are the lunar returns of one solar year (the one in
    force at the solar return first). A lunar ring that showed the 5th lunar
    return of the year shows the 5th one of the new natal's year; if that is
    unknown or does not exist, the one in force at the solar return.
    """
    if not new_rows:
        return None
    index = match_return_index(old_rows, old_jd) if old_rows else None
    if index is None or index >= len(new_rows):
        index = 0
    return new_rows[index]


def rebased_place(old_place, previous_natal_place, natal_place):
    """Where a recast TRANSIT is cast for the new natal.

    A transit cast for the previous natal's birthplace follows the natal;
    one the user cast for another place (where one lives) keeps it. Returns
    never use this: the course casts them for the birthplace only.
    """
    def key(place):
        return (round(float(place.lon), 6), round(float(place.lat), 6))
    try:
        if old_place is None or key(old_place) == key(previous_natal_place):
            return natal_place
    except (AttributeError, TypeError, ValueError):
        return natal_place
    return old_place


def next_return_index(rows, jd, forward, tolerance=JD_TOLERANCE):
    """First event strictly after/before jd, never the current event again.

    Consecutive solar years share a boundary lunar return. Skipping the
    duplicate here ensures that a lunar arrow always makes actual progress.
    """
    if forward:
        return next((i for i, row in enumerate(rows)
                     if row.jd > jd + tolerance), None)
    return next((i for i in range(len(rows) - 1, -1, -1)
                 if rows[i].jd < jd - tolerance), None)
