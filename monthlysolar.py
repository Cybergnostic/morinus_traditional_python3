"""Monthly solar-revolution targets and chronological event selection.

Following Natalna 27, each monthly return occurs when the Sun reaches the
same degree it occupied natally, successively in the twelve zodiacal signs.
The first is the annual solar return; eleven more follow before the next one.
"""

from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class MonthlySolarEvent:
    month: int
    target_longitude: float
    jd: float
    utc_tuple: tuple[int, int, int, int, int, int] | None


def target_longitudes(natal_sun_longitude: float) -> tuple[float, ...]:
    return tuple((natal_sun_longitude + 30.0 * i) % 360.0 for i in range(12))


def choose_events(
    start_jd: float,
    next_start_jd: float,
    natal_sun_longitude: float,
    crossings: Callable[[float, float], Iterable[tuple[float, tuple[int, int, int, int, int, int]]]],
) -> tuple[MonthlySolarEvent, ...]:
    """Select 11 exact monthly solar crossings inside the solar year.

    ``crossings(target_longitude, approximate_jd)`` returns candidate exact
    Sun crossings as (Julian day, UTC calendar tuple). The ephemeris search is
    injected so order, uniqueness and boundaries can be tested independently.
    """
    duration = next_start_jd - start_jd
    if not 365.0 <= duration < 366.0:
        raise ValueError("Expected two successive annual solar returns")
    targets = target_longitudes(natal_sun_longitude)
    events = [MonthlySolarEvent(1, targets[0], start_jd, None)]
    for k in range(1, 12):
        estimate = start_jd + duration * k / 12.0
        candidates = [
            (jd, utc) for jd, utc in crossings(targets[k], estimate)
            if start_jd < jd < next_start_jd and abs(jd - estimate) < 20.0
        ]
        if not candidates:
            raise ValueError("Missing monthly solar return %d" % (k + 1))
        jd, utc = min(candidates, key=lambda row: abs(row[0] - estimate))
        if jd <= events[-1].jd:
            raise ValueError("Monthly solar returns are not chronological")
        events.append(MonthlySolarEvent(k + 1, targets[k], jd, utc))
    return tuple(events)
