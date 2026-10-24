"""Pure traditional planetary aspect geometry and motion for Morinus.

Only the seven visible planets. The five Ptolemaic aspects are distinguished
from whole-sign configurations and from the <=3 degree close-contact label.
The legacy Morinus matrix remains available unchanged via Settings.
"""

from dataclasses import dataclass
from math import isfinite

PLANETS = ("Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon")
COURSE_ORBS = (9.0, 9.0, 8.0, 15.0, 7.0, 7.0, 12.0)
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
    close_contact: bool
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
    if current <= 1e-7:
        return "Exact"

    dt = 0.001
    tolerance = 1e-10
    delta_a = abs(angular_distance(a + speed_a * dt, b) - angle) - current
    delta_b = abs(angular_distance(a, b + speed_b * dt) - angle) - current
    if delta_a < -tolerance and delta_b < -tolerance:
        return "Double application"
    if delta_a > tolerance and delta_b > tolerance:
        return "Double separation"

    delta_pair = abs(angular_distance(a + speed_a * dt,
                                      b + speed_b * dt) - angle) - current
    if delta_pair < -tolerance:
        return "Applying"
    if delta_pair > tolerance:
        return "Separating"
    return "Stationary"


def combine_orbs(orb_a: float, orb_b: float, method: str = "larger") -> float:
    if not all(isfinite(float(x)) and float(x) >= 0 for x in (orb_a, orb_b)):
        raise ValueError("Planetary orbs must be finite non-negative numbers")
    if method == "larger":
        return max(float(orb_a), float(orb_b))
    if method == "average":
        return (float(orb_a) + float(orb_b)) / 2.0
    raise ValueError("Unknown planetary orb combination method")


def evaluate(a: float, b: float, speed_a: float, speed_b: float,
             orb_a: float, orb_b: float, method: str = "larger",
             boundary_allowance: float = 3.0) -> Contact | None:
    """Calculate one planetary contact without ephemeris or GUI dependencies.

    A sign-based contact is accepted inside its planetary orb. A different
    geometrical aspect across the sign boundary is accepted only when no more
    than boundary_allowance degrees from exactness (0 = strict signs).
    Applying describes the immediate change in deviation from perfection,
    not a promise that perfection will occur before a station or ingress.
    """
    vals = (a, b, speed_a, speed_b, boundary_allowance)
    if not all(isfinite(float(x)) for x in vals):
        raise ValueError("Aspect inputs must be finite")
    if boundary_allowance < 0 or boundary_allowance > 10:
        raise ValueError("Out-of-sign allowance must lie between 0 and 10 degrees")
    allowed = combine_orbs(orb_a, orb_b, method)
    distance = angular_distance(a, b)
    sign_index = sign_configuration(a, b)
    chosen = None
    deviation = 0.0
    if sign_index is not None:
        candidate = abs(distance - ASPECT_ANGLES[sign_index])
        if candidate <= allowed + 1e-10:
            chosen, deviation = sign_index, candidate
    if chosen is None and boundary_allowance > 0:
        idx = min(range(5), key=lambda i: abs(distance - ASPECT_ANGLES[i]))
        candidate = abs(distance - ASPECT_ANGLES[idx])
        if idx != sign_index and candidate <= min(allowed, boundary_allowance) + 1e-10:
            chosen, deviation = idx, candidate
    if chosen is None:
        return None
    motion = motion_status(a, b, speed_a, speed_b, ASPECT_ANGLES[chosen])
    exact = motion == "Exact"
    applying = motion in ("Applying", "Double application")
    separating = motion in ("Separating", "Double separation")
    return Contact(chosen, ASPECT_ANGLES[chosen], deviation, allowed,
                   sign_index, chosen != sign_index, deviation <= 3.0,
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
