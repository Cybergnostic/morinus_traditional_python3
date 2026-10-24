"""A3 precise contact, station, and sign-ingress event search.

A caller supplies positions(jd) -> seven (longitude, signed_speed) pairs in
Chaldean order. Swiss Ephemeris is used only in the optional GUI adapter.
Sampling locates crossings; bisection refines times from actual positions.
"""
from dataclasses import dataclass
from itertools import combinations

from traditional_aspects import PLANETS

# Directed relative longitudes cover both branches of the five major aspects.
RAYS = ((0, 0), (60, 1), (90, 2), (120, 3), (180, 4),
        (240, 3), (270, 2), (300, 1))


@dataclass(frozen=True)
class Event:
    jd: float
    kind: str
    first: str
    second: str = ''
    aspect_index: int = -1


def _delta(a, b):
    return (b - a + 180.0) % 360.0 - 180.0


def _bisect(left, right, f, target=0.0):
    fl = f(left) - target
    for _ in range(24):
        middle = (left + right) * 0.5
        fm = f(middle) - target
        if abs(fm) < 1e-7 or right - left < 1e-7:
            return middle
        if (fl <= 0 <= fm) or (fl >= 0 >= fm):
            right = middle
        else:
            left, fl = middle, fm
    return (left + right) * 0.5


def scan(positions, start_jd, days=30, step=0.25, sign_shift=0.0):
    """Search chronological events; angular roots refined below 0.01 minute.

    step <= 0.5 days ensures the Moon cannot skip an ordinary 30-degree sign
    ingress. Results are deliberately not horary judgments. Caller controls
    search horizon. sign_shift is the ayanamsha for sidereal sign boundaries.
    """
    if not (0 < days <= 365 and 0 < step <= 0.5):
        raise ValueError('Expected 0 < days <= 365 and 0 < step <= 0.5')
    cache = {}
    def at(t):
        key = round(t, 11)
        if key not in cache:
            data = tuple((float(lon) % 360.0, float(speed)) for lon, speed in positions(t))
            if len(data) != 7:
                raise ValueError('Expected exactly seven planetary positions')
            cache[key] = data
        return cache[key]
    events = []
    left = float(start_jd)
    old = at(left)
    limit = left + float(days)
    while left < limit - 1e-9:
        right = min(left + step, limit)
        new = at(right)
        for i in range(7):
            old_lon, old_speed = old[i]
            new_lon, new_speed = new[i]
            if old_speed * new_speed < 0 or (old_speed != 0 and new_speed == 0):
                root = _bisect(left, right, lambda t: at(t)[i][1])
                events.append(Event(root, 'station', PLANETS[i]))
            old_zod = (old_lon - sign_shift) % 360.0
            movement = _delta(old_lon, new_lon)
            unwrapped = old_zod + movement
            if movement > 0:
                boundaries = range(int(old_zod // 30) + 1,
                                   int(unwrapped // 30) + 1)
            elif movement < 0:
                boundaries = range(int(unwrapped // 30) + 1,
                                   int(old_zod // 30) + 1)
            else:
                boundaries = ()
            for bound in boundaries:
                target = bound * 30.0
                root = _bisect(left, right,
                    lambda t: old_zod + _delta(old_lon, at(t)[i][0]), target)
                events.append(Event(root, 'ingress', PLANETS[i]))
        for i, j in combinations(range(7), 2):
            old_difference = (old[i][0] - old[j][0]) % 360.0
            change = (_delta(old[i][0], new[i][0]) -
                      _delta(old[j][0], new[j][0]))
            end_difference = old_difference + change
            low, high = sorted((old_difference, end_difference))
            for ray, aspect_index in RAYS:
                for turn in (-1, 0, 1):
                    target = ray + 360.0 * turn
                    if low + 1e-8 < target <= high + 1e-8:
                        root = _bisect(left, right,
                            lambda t: old_difference +
                             _delta(old[i][0], at(t)[i][0]) -
                             _delta(old[j][0], at(t)[j][0]), target)
                        events.append(Event(root, 'aspect', PLANETS[i],
                                            PLANETS[j], aspect_index))
        left, old = right, new
    events.sort(key=lambda e: e.jd)
    unique = []
    for event in events:
        if not unique or event.kind != unique[-1].kind or \
                event.first != unique[-1].first or \
                event.second != unique[-1].second or \
                event.aspect_index != unique[-1].aspect_index or \
                abs(event.jd - unique[-1].jd) > 1e-4:
            unique.append(event)
    return unique
