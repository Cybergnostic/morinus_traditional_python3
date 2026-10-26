"""A3 traditional light transfer and chronological perfection checks.

Pure calculation module. Uses only the seven visible planets and the aspects
already selected by Morinus's active Traditional/Legacy/Custom matrix.
Astrological configurations are distinguished from verified future events.
"""
from dataclasses import dataclass
from itertools import combinations

from traditional_aspects import (PLANETS, ASPECT_ANGLES, RATE_TOLERANCE,
                                 angular_distance, deviation_rate, motion_status)

ASPECTS = ('Conjunction', 'Sextile', 'Square', 'Trine', 'Opposition')


@dataclass(frozen=True)
class Connection:
    kind: str
    actor: str
    source: str
    target: str
    source_aspect: str
    target_aspect: str
    status: str = 'Candidate'
    detail: str = ''
    exact_times: tuple = ()


def individual_motion(moving_lon, fixed_lon, moving_speed, angle):
    """Does the *moving planet*, rather than the pair, approach its contact?"""
    deviation = abs(angular_distance(moving_lon, fixed_lon) - angle)
    if deviation < 1e-7:
        return 'Exact'
    if abs(moving_speed) < 1e-10:
        return 'Stationary'
    rate = deviation_rate(moving_lon, fixed_lon, moving_speed, 0.0, angle)
    if rate < -RATE_TOLERANCE:
        return 'Applying'
    if rate > RATE_TOLERANCE:
        return 'Separating'
    return 'Stationary'


def _positions(chart):
    return [(float(p.data[0]), float(p.data[3]))
            for p in chart.planets.planets[:7]]


def _contact(chart, i, j):
    c = chart.aspmatrix[max(i, j)][min(i, j)]
    return c.typ if c.typ in range(5) else None


def _connect_themselves(chart, pos, i, j):
    """Do these two planets apply to each other in the chart?

    Course doctrine: translation and collection matter only for planets that
    cannot connect themselves; if they apply to each other they will meet
    anyway, whatever a third planet does.
    """
    kind = _contact(chart, i, j)
    if kind is None:
        return False
    return motion_status(pos[i][0], pos[j][0], pos[i][1], pos[j][1],
                         ASPECT_ANGLES[kind]) in ('Applying', 'Double application')


def _future_status(events, movers, targets, aspect_indexes):
    """Require every feeder's NEXT chronological contact to be the intended one.

    Any earlier exact contact with a different planet, station, or sign ingress
    invalidates the initial translation/collection under these strict rules.
    No claim is made when the intended perfection lies outside the horizon.
    Returns exact times for accepted configurations and None otherwise.
    """
    exact_times = []
    for mover, target, angle_index in zip(movers, targets, aspect_indexes):
        matched = None
        for event in sorted(events, key=lambda e: e.jd):
            if event.kind in ('station', 'ingress') and mover == event.first:
                return None
            if event.kind != 'aspect' or mover not in (event.first, event.second):
                continue
            other = event.second if mover == event.first else event.first
            if other == target and event.aspect_index == angle_index:
                matched = event.jd
                break
            # This includes any earlier aspect to the same target of a
            # different type; it is not the pending original application.
            return None
        if matched is None:
            return None
        exact_times.append(matched)
    return tuple(exact_times)


def connections(chart, events=None):
    """Identify light translation/collection in every chart type.

    Translation: faster messenger individually separates from A, applies to B.
    Collection: both faster contributors individually apply to a slower collector.
    Both only join planets that do not apply to each other themselves.
    Intervening events are evaluated only when an actual ephemeris scan exists.
    """
    pos = _positions(chart)
    rows = []
    for messenger in range(7):
        for source, target in ((a, b) for a in range(7) for b in range(7)
                               if a != b and messenger not in (a, b)):
            past = _contact(chart, messenger, source)
            future = _contact(chart, messenger, target)
            if past is None or future is None:
                continue
            if abs(pos[messenger][1]) <= max(abs(pos[source][1]), abs(pos[target][1])):
                continue
            if _connect_themselves(chart, pos, source, target):
                continue
            if individual_motion(pos[messenger][0], pos[source][0],
                                 pos[messenger][1], ASPECT_ANGLES[past]) != 'Separating':
                continue
            if individual_motion(pos[messenger][0], pos[target][0],
                                 pos[messenger][1], ASPECT_ANGLES[future]) != 'Applying':
                continue
            times = ()
            if events is not None:
                times = _future_status(events, [PLANETS[messenger]],
                                       [PLANETS[target]], [future])
                if times is None:
                    continue
            rows.append(Connection('Translation', PLANETS[messenger],
                                   PLANETS[source], PLANETS[target],
                                   ASPECTS[past], ASPECTS[future],
                                   'Verified' if events is not None else 'Candidate',
                                   '', times))
    for collector in range(7):
        for first, second in combinations((i for i in range(7) if i != collector), 2):
            a = _contact(chart, first, collector)
            b = _contact(chart, second, collector)
            if a is None or b is None:
                continue
            if abs(pos[collector][1]) >= min(abs(pos[first][1]), abs(pos[second][1])):
                continue
            if _connect_themselves(chart, pos, first, second):
                continue
            if individual_motion(pos[first][0], pos[collector][0],
                                 pos[first][1], ASPECT_ANGLES[a]) != 'Applying':
                continue
            if individual_motion(pos[second][0], pos[collector][0],
                                 pos[second][1], ASPECT_ANGLES[b]) != 'Applying':
                continue
            times = ()
            if events is not None:
                times = _future_status(events,
                    [PLANETS[first], PLANETS[second]],
                    [PLANETS[collector], PLANETS[collector]], [a, b])
                if times is None:
                    continue
            rows.append(Connection('Collection', PLANETS[collector],
                                   PLANETS[first], PLANETS[second],
                                   ASPECTS[a], ASPECTS[b],
                                   'Verified' if events is not None else 'Candidate',
                                   '', times))
    return sorted(rows, key=lambda r: (r.kind, r.actor, r.source, r.target))


def horary_timeline(events, first, second, horizon_days):
    """Return factual contact chronology for two selected significators.

    Avoid automatically asserting prohibition/frustration/refranation: those
    judgments depend on role, reception and the precise horary doctrine.
    """
    significant = [e for e in events if first in (e.first, e.second)
                   or second in (e.first, e.second)]
    perfection = next((e for e in significant if e.kind == 'aspect'
                       and {e.first, e.second} == {first, second}), None)
    if perfection is None:
        return 'No exact contact in %d days' % horizon_days, significant
    obstacles = [e for e in significant if e.jd < perfection.jd - 1e-7
                 and (e.kind in ('station', 'ingress') or
                      (e.kind == 'aspect' and {e.first, e.second} != {first, second}))]
    if obstacles:
        return 'Contact after %d earlier event(s): review impediments' % len(obstacles), significant
    return 'Direct contact without earlier listed events', significant
