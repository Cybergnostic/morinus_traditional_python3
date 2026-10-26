"""A5: cross-chart traditional contacts and directed receptions.

A and B are *different chart layers*, not planets moving at a single instant.
All 49 traditional-planet pairings are eligible, including Sun/Sun. A is
held fixed when assessing the instantaneous motion of B; this does not
promise future perfection. The selected traditional preset and Morinus's
user-defined essential-dignity tables are reused without mutating charts.
"""
from dataclasses import dataclass
from math import isfinite

import tradoptions
from traditional_aspects import (PLANETS, ASPECT_ANGLES, RATE_TOLERANCE,
                                 angular_distance, deviation_rate, evaluate,
                                 sign_configuration, configured_orbs)
from aspect_workspace import (ASPECT_NAMES, SIGNS, dignity_holds,
                              qualifies_for_reception)

@dataclass(frozen=True)
class CrossContact:
    first: str
    second: str
    aspect: str
    deviation: float
    out_of_sign: bool
    motion_b: str
    a_receives_b: tuple
    b_receives_a: tuple
    a_longitude: float
    b_longitude: float


def chart_positions(chrt, options):
    """Seven chart positions using each chart's own ayanamsha, if enabled."""
    shift = float(chrt.ayanamsha) if options.ayanamsha else 0.0
    return tuple(
        ((float(chrt.planets.planets[i].data[0]) - shift) % 360.0,
         float(chrt.planets.planets[i].data[3]))
        for i in range(7))


def _sect(chrt, options):
    day = bool(chrt.planets.planets[3].speculums[0].abovehorizon)
    if options.usedaynightorb:
        day = bool(chrt.abovehorizonwithorb)
    return day


def _legacy_contact(a, b, options, i, j):
    """Keep classic multiwheel legacy semantics for A5 legacy preset."""
    distance = angular_distance(a, b)
    orb = (float(options.orbs[i]) + float(options.orbs[j])) / 2.0
    candidates = [
        (abs(distance - angle), k)
        for k, angle in enumerate(ASPECT_ANGLES)
        if abs(distance - angle) <= orb + 1e-9]
    if not candidates:
        return None
    deviation, index = min(candidates)
    return index, deviation, sign_configuration(a, b) != index


def _b_motion(fixed_a, moving_b, b_speed, angle):
    """Motion of B alone relative to the fixed longitude from chart A."""
    current = abs(angular_distance(fixed_a, moving_b) - angle)
    if current <= 1e-7:
        return "Exact"
    if abs(b_speed) < 1e-10:
        return "Stationary"
    rate = deviation_rate(fixed_a, moving_b, 0.0, b_speed, angle)
    if rate < -RATE_TOLERANCE:
        return "Approaching A"
    if rate > RATE_TOLERANCE:
        return "Leaving A"
    return "Stationary"


def analyze(first_chart, second_chart, options=None, settings=None,
            only_first=None, only_second=None):
    """Compare A and B; return degree-qualified contacts, tightest first.

    The source chart is not silently substituted. Cross-chart reception is
    explicitly directional and uses each chart's own sect. Dignity systems
    come from the active options (selected term/face/triplicity tables).
    """
    if first_chart is second_chart:
        return ()
    options = options or first_chart.options
    settings = dict(settings if settings is not None else tradoptions.values())
    preset = settings.get("aspect_preset", "traditional")
    if preset == "legacy":
        orbs = None
    else:
        orbs = configured_orbs(settings)
    a_positions = chart_positions(first_chart, options)
    b_positions = chart_positions(second_chart, options)
    day_a = _sect(first_chart, options)
    day_b = _sect(second_chart, options)
    rows = []
    for i, name_a in enumerate(PLANETS):
        if only_first is not None and name_a != only_first:
            continue
        a, _speed_a = a_positions[i]
        for j, name_b in enumerate(PLANETS):
            if only_second is not None and name_b != only_second:
                continue
            b, speed_b = b_positions[j]
            if orbs is None:
                result = _legacy_contact(a, b, options, i, j)
                if result is None:
                    continue
                aspect_index, deviation, out_of_sign = result
            else:
                contact = evaluate(a, b, 0.0, speed_b, orbs[i], orbs[j])
                if contact is None:
                    continue
                aspect_index = contact.index
                deviation = contact.deviation
                out_of_sign = contact.out_of_sign
            holds_a = dignity_holds(options, i, b, day_a)
            holds_b = dignity_holds(options, j, a, day_b)
            rows.append(CrossContact(
                name_a, name_b, ASPECT_NAMES[aspect_index], deviation,
                out_of_sign,
                _b_motion(a, b, speed_b, ASPECT_ANGLES[aspect_index]),
                holds_a if qualifies_for_reception(holds_a) else (),
                holds_b if qualifies_for_reception(holds_b) else (),
                a, b))
    rows.sort(key=lambda item: (
        item.deviation, PLANETS.index(item.first), PLANETS.index(item.second)))
    return tuple(rows)
