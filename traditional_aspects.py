"""Pure traditional planetary aspect geometry and motion for Morinus.

Only the seven visible planets. The five Ptolemaic aspects are distinguished
from whole-sign configurations.
Orbs follow the course: the larger orb of the two planets, never their sum
or half-orbs, and the three-degree rule across sign boundaries.
The legacy Morinus matrix remains available unchanged via Settings.
"""

from dataclasses import dataclass
from math import isfinite

PLANETS = ("Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon")
COURSE_ORBS = (9.0, 9.0, 8.0, 15.0, 7.0, 7.0, 12.0)
# The three-degree rule: across a sign boundary planets are configured only
# when no more than three degrees apart (from exactness), never more.
SIGN_BOUNDARY = 3.0
ASPECT_ANGLES = (0.0, 60.0, 90.0, 120.0, 180.0)
SIGN_ASPECTS = {0: 0, 2: 1, 3: 2, 4: 3, 6: 4,
                8: 3, 9: 2, 10: 1}


@dataclass(frozen=True)
class Contact:
    index: int
    angle: float
    deviation: float
    maximum_orb: float
    whole_sign_index: int | None
    out_of_sign: bool
    applying: bool
    separating: bool
    exact: bool
    double_applying: bool = False
    double_separating: bool = False


def angular_distance(a: float, b: float) -> float:
    """Shortest angular distance, in [0, 180]."""
    return abs(((float(b) - float(a) + 180.0) % 360.0) - 180.0)


def sign_configuration(a: float, b: float) -> int | None:
    """Ptolemaic relationship by signs alone, even far outside the orb."""
    difference = (int((b % 360.0) // 30.0) -
                  int((a % 360.0) // 30.0)) % 12
    return SIGN_ASPECTS.get(difference)



def motion_status(a: float, b: float, speed_a: float, speed_b: float,
                  angle: float) -> str:
    """Classify motion toward the current aspect's exact degree.

    A double application means each planet individually closes the deviation
    when the other is held fixed; double separation means both individually
    widen it. This includes opposite signed motions caused by retrogradation,
    is symmetric in the planet order and works across 0° Aries. Otherwise the
    ordinary label describes their *relative* motion. This is instantaneous,
    not a prediction of eventual perfection across an ingress or station.
    """
    current = abs(angular_distance(a, b) - angle)
    if current <= EXACT:
        return "Exact"

    rate_a = deviation_rate(a, b, speed_a, 0.0, angle)
    rate_b = deviation_rate(a, b, 0.0, speed_b, angle)
    if rate_a < -RATE_TOLERANCE and rate_b < -RATE_TOLERANCE:
        return "Double application"
    if rate_a > RATE_TOLERANCE and rate_b > RATE_TOLERANCE:
        return "Double separation"

    # The rate is linear in the two speeds: the pair's rate is the sum.
    rate_pair = rate_a + rate_b
    if rate_pair < -RATE_TOLERANCE:
        return "Applying"
    if rate_pair > RATE_TOLERANCE:
        return "Separating"
    return "Stationary"


EXACT = 1e-7
RATE_TOLERANCE = 1e-7  # degrees per day


def deviation_rate(a: float, b: float, speed_a: float, speed_b: float,
                   angle: float) -> float:
    """Instantaneous change (degrees/day) of the distance from exact aspect.

    Negative: approaching exactness; positive: moving away. Computed from the
    derivative rather than a finite time step, so a contact a few arc-seconds
    from perfection is not misread as separating because a step overshoots it.
    Returns 0.0 at exactness, where the direction is undefined.
    """
    signed = (float(b) - float(a) + 180.0) % 360.0 - 180.0  # b relative to a
    distance = abs(signed)
    offset = distance - angle
    if abs(offset) <= EXACT or distance == 0.0:
        return 0.0
    relative = float(speed_b) - float(speed_a)
    return (1.0 if offset > 0 else -1.0) * (1.0 if signed > 0 else -1.0) * relative


def combine_orbs(orb_a: float, orb_b: float) -> float:
    """The orb within which two planets are configured: the LARGER one.

    Course doctrine: the contact begins when the centre of one planet
    touches the orb of the other, and only the planet with the larger orb
    counts. Orbs are never added, and half-orbs (moieties) are not used.
    Venus (7) and the Moon (12) 10 degrees apart are configured, because
    10 is within the Moon's orb.
    """
    if not all(isfinite(float(x)) and float(x) >= 0 for x in (orb_a, orb_b)):
        raise ValueError("Planetary orbs must be finite non-negative numbers")
    return max(float(orb_a), float(orb_b))


def evaluate(a: float, b: float, speed_a: float, speed_b: float,
             orb_a: float, orb_b: float) -> Contact | None:
    """Calculate one planetary contact without ephemeris or GUI dependencies.

    A sign-based contact is accepted inside the larger planetary orb. Across
    a sign boundary a contact exists only when the planets are no more than
    SIGN_BOUNDARY (3) degrees from exactness, also inside the orb.
    Applying describes the immediate change in deviation from perfection,
    not a promise that perfection will occur before a station or ingress.
    """
    vals = (a, b, speed_a, speed_b)
    if not all(isfinite(float(x)) for x in vals):
        raise ValueError("Aspect inputs must be finite")
    allowed = combine_orbs(orb_a, orb_b)
    distance = angular_distance(a, b)
    sign_index = sign_configuration(a, b)
    chosen = None
    deviation = 0.0
    if sign_index is not None:
        candidate = abs(distance - ASPECT_ANGLES[sign_index])
        if candidate <= allowed + 1e-10:
            chosen, deviation = sign_index, candidate
    if chosen is None:
        idx = min(range(5), key=lambda i: abs(distance - ASPECT_ANGLES[i]))
        candidate = abs(distance - ASPECT_ANGLES[idx])
        if idx != sign_index and candidate <= min(allowed, SIGN_BOUNDARY) + 1e-10:
            chosen, deviation = idx, candidate
    if chosen is None:
        return None
    motion = motion_status(a, b, speed_a, speed_b, ASPECT_ANGLES[chosen])
    exact = motion == "Exact"
    applying = motion in ("Applying", "Double application")
    separating = motion in ("Separating", "Double separation")
    return Contact(chosen, ASPECT_ANGLES[chosen], deviation, allowed,
                   sign_index, chosen != sign_index,
                   applying, separating, exact,
                   motion == "Double application", motion == "Double separation")


def configured_orbs(values):
    """Traditional course preset or individually editable custom orbs."""
    preset = values.get("aspect_preset", "traditional")
    if preset == "traditional":
        return COURSE_ORBS
    if preset == "custom":
        orbs = tuple(float(values["aspect_custom_" + name.lower()]) for name in PLANETS)
        if not all(isfinite(x) and 0 <= x <= 20 for x in orbs):
            raise ValueError("Custom planet orbs must be between 0 and 20 degrees")
        return orbs
    raise ValueError("Legacy aspects must use Morinus's original algorithm")


def doctrinal_orbs(values):
    """Planet orbs for the traditional techniques (by name, Chaldean order).

    The Legacy preset only switches Morinus's own aspect matrix back to the
    original algorithm; techniques of the course keep the course orbs.
    """
    if values.get("aspect_preset", "traditional") == "legacy":
        return COURSE_ORBS
    return configured_orbs(values)
