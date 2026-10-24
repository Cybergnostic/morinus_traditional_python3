"""Course-based annual divisions (Valens) for a solar return.

The seven planetary periods use *fixed* day counts adding to 365 days.
The final ruler remains in force through the small remaining interval until
the following solar return; the nominal Valens duration is not rescaled.

The sequence begins with the lord of the annual whole-sign profection and
continues in secondary zodiacal order through the planets' solar longitudes.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Mapping


PLANETS = ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn")
VALENS_DAYS = {
    "Sun": 53,
    "Moon": 71,
    "Mercury": 57,
    "Venus": 23,
    "Mars": 42,
    "Jupiter": 34,
    "Saturn": 85,
}
SIGN_RULERS = (
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter",
)


@dataclass(frozen=True)
class DivisionPeriod:
    number: int
    ruler: str
    start: datetime
    end: datetime
    nominal_days: int
    solar_house: int


@dataclass(frozen=True)
class DivisionSchedule:
    profected_sign: int
    year_ruler: str
    periods: tuple[DivisionPeriod, ...]


def annual_sign(natal_asc: float, birth_year: int, solar_year: int) -> int:
    """Annual whole-sign profection, starting from the natal Ascendant."""
    if solar_year < birth_year:
        raise ValueError("Solar year cannot precede birth")
    return (int((natal_asc % 360.0) // 30.0) + solar_year - birth_year) % 12


def secondary_order(first: str, solar_longitudes: Mapping[str, float]) -> tuple[str, ...]:
    """Seven planets sorted by increasing zodiacal longitude from *first*.

    Equal positions use the standard planet order as a deterministic tie-breaker.
    """
    missing = set(PLANETS).difference(solar_longitudes)
    if missing:
        raise ValueError("Missing traditional planets: " + ", ".join(sorted(missing)))
    if first not in PLANETS:
        raise ValueError("First ruler must be a traditional planet")
    start = solar_longitudes[first] % 360.0
    others = (p for p in PLANETS if p != first)
    return (first,) + tuple(sorted(
        others, key=lambda p: ((solar_longitudes[p] - start) % 360.0, PLANETS.index(p))
    ))


def calculate_divisions(
    solar_start: datetime,
    next_solar_start: datetime,
    natal_asc: float,
    birth_year: int,
    solar_year: int,
    solar_asc: float,
    solar_longitudes: Mapping[str, float],
) -> DivisionSchedule:
    """Return the seven periods for one solar year using the course method.

    Dates must be timezone-aware and represent the two consecutive exact solar
    returns. The tiny difference between a 365-day Valens cycle and the actual
    solar year is assigned to the final period (not distributed among rulers).
    """
    if solar_start.tzinfo is None or next_solar_start.tzinfo is None:
        raise ValueError("Solar return dates must be timezone-aware")
    duration = next_solar_start - solar_start
    if not timedelta(days=365) <= duration < timedelta(days=366):
        raise ValueError("Expected consecutive solar returns about 365.24 days apart")

    sign = annual_sign(natal_asc, birth_year, solar_year)
    first = SIGN_RULERS[sign]
    order = secondary_order(first, solar_longitudes)
    cursor = solar_start
    periods = []
    for index, ruler in enumerate(order):
        nominal = VALENS_DAYS[ruler]
        end = next_solar_start if index == len(order) - 1 else cursor + timedelta(days=nominal)
        solar_house = (int((solar_longitudes[ruler] % 360.0) // 30.0) - int((solar_asc % 360.0) // 30.0)) % 12 + 1
        periods.append(DivisionPeriod(index + 1, ruler, cursor, end, nominal, solar_house))
        cursor = end
    return DivisionSchedule(sign, first, tuple(periods))
