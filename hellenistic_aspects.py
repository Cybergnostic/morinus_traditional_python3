"""A4 Hellenistic domicile witnessing and directed planetary rays.

Whole-sign witnessing is calculated for every planet against each of its
traditional domiciles. Rays are judged once per pair from the naturally
faster planet in Chaldean order, independent of present daily speed.
Close counter-rays use the selected Morinus aspect matrix and 3-degree
limit. Light-based mediation uses only verified A3 connections.
"""
from dataclasses import dataclass
from itertools import combinations

from traditional_aspects import PLANETS, angular_distance
from aspect_workspace import SIGNS
from light_perfection import individual_motion

# Source-aligned with hor_tools/analysis/dignity.py and relationships.py,
# but do not import hor_tools here: its package __init__ loads pyswisseph,
# which Morinus installations are not required to have installed.
SIGN_RULERS = ("Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
               "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter")
ASPECT_FOR_DOMINATION = {8: "trine", 9: "square", 10: "sextile"}


def antiscia_longitude(longitude):
    return (180.0 - longitude) % 360.0


def contra_antiscia_longitude(longitude):
    return (360.0 - longitude) % 360.0

# +2/+3/+4: sinister ray; -2/-3/-4: dexter ray.
SIGN_RAYS = {2: ("Sextile", 60.0, 1), 3: ("Square", 90.0, 2),
             4: ("Trine", 120.0, 3),
             8: ("Trine", 120.0, 3), 9: ("Square", 90.0, 2),
             10: ("Sextile", 60.0, 1)}
AVERSE_STEPS = {1, 5, 7, 11}
EPS = 1e-9


@dataclass(frozen=True)
class AversionRow:
    planet: str
    placement: str
    domicile: str
    witnessing: str
    status: str
    mitigations: tuple


@dataclass(frozen=True)
class RayRow:
    caster: str
    target: str
    caster_sign: str
    target_sign: str
    aspect: str
    direction: str
    overcoming: str
    degree_orb: float
    close_counter_ray: bool
    aktinobolia: bool
    in_orb: bool


def sign_of(longitude):
    return int((float(longitude) % 360.0) // 30.0)


def signs_averse(left, right):
    """Sign-based aversion includes 2nd, 6th, 8th and 12th sign."""
    return (right - left) % 12 in AVERSE_STEPS


def directed_ray(caster_sign, target_sign):
    """Return (aspect, dexter/sinister) from a NAMED casting planet."""
    step = (target_sign - caster_sign) % 12
    if step not in SIGN_RAYS:
        return None
    return (SIGN_RAYS[step][0], "Dexter" if step > 6 else "Sinister")


def overcomes(caster_sign, target_sign):
    """Caster in 9th, 10th or 11th sign from its target."""
    return (caster_sign - target_sign) % 12 in ASPECT_FOR_DOMINATION


def _reflections(source_lon, target_lon):
    """Keep sign-level and course whole-degree reflection evidence separate."""
    out = []
    target_sign = sign_of(target_lon)
    for name, mirror in (
            ("Antiscia", antiscia_longitude(source_lon)),
            ("Contra-antiscia", contra_antiscia_longitude(source_lon))):
        if sign_of(mirror) != target_sign:
            continue
        out.append(name + " (sign)")
        # Existing hor_tools reflection rule: corresponding integer degrees
        # within the sign add to 29. Minutes need not coincide.
        if int(source_lon % 30.0) + int(target_lon % 30.0) == 29:
            out.append(name + " (degree)")
    return out


def _verified_light_pairs(light):
    pairs = {}
    for link in light or ():
        if link.status != "Verified":
            continue
        if link.kind not in ("Translation", "Collection"):
            continue
        pair = frozenset((link.source, link.target))
        title = "%s via %s" % (link.kind, link.actor)
        pairs.setdefault(pair, set()).add(title)
    return pairs


def _methods(source_long, target_long, source_name, target_name,
             positions, light_pairs, target_is_sign=False):
    left, right = sign_of(source_long), sign_of(target_long)
    methods = []
    if SIGN_RULERS[left] == SIGN_RULERS[right]:
        methods.append("Common domicile ruler: " + SIGN_RULERS[left])
    reflections = _reflections(source_long, target_long)
    # Domicile rows represent the entire ruled sign, not a body at
    # its synthetic midpoint. Degree-level mirrors are meaningless there.
    if target_is_sign:
        reflections = [m for m in reflections if "(degree)" not in m]
    methods.extend(reflections)
    if target_name in positions and source_name in positions:
        methods.extend(sorted(light_pairs.get(
            frozenset((source_name, target_name)), ())))
    elif source_name in positions:
        # For an angle/domicile SIGN, translation/collection can connect
        # the source planet with an occupant of the otherwise averse sign.
        for occupant, (lon, _speed) in positions.items():
            if occupant == source_name or sign_of(lon) != right:
                continue
            methods.extend(sorted(light_pairs.get(
                frozenset((source_name, occupant)), ())))
    return tuple(dict.fromkeys(methods))


def domicile_witnessing(source_sign, domicile_sign):
    """A sign-based testimony, not a claim of a close degree aspect."""
    step = (domicile_sign - source_sign) % 12
    return {0: "Co-presence", 2: "Sextile", 3: "Square",
            4: "Trine", 6: "Opposition", 8: "Trine",
            9: "Square", 10: "Sextile"}.get(step, "Averse")


def analyze_aversions(chart, light=()):
    """Show EACH planet's relation to EACH domicile it rules (12 rows).

    Do not mix in planet-pair aversions or arbitrary planet-to-Ascendant
    relationships. For each domicile, report whole-sign witnessing; only
    averse signs need mitigating evidence. Co-rulership of two domiciles,
    mirror signs and verified light transfer can mitigate, but never
    erase, the underlying sign-based aversion.
    """
    positions = {
        name: ((float(planet.data[0]) - _shift(chart)) % 360.0,
               float(planet.data[3]))
        for name, planet in zip(PLANETS, chart.planets.planets[:7])
    }
    light_pairs = _verified_light_pairs(light)
    rows = []
    for planet in PLANETS:
        source_long = positions[planet][0]
        source_sign = sign_of(source_long)
        for sign, ruler in enumerate(SIGN_RULERS):
            if ruler != planet:
                continue
            witnessing = domicile_witnessing(source_sign, sign)
            methods = ()
            if witnessing == "Averse":
                # The domicile is a SIGN, not a physical planet located at
                # an arbitrary midpoint. Never manufacture degree contacts.
                methods = _methods(
                    source_long, sign * 30.0 + 15.0, planet,
                    SIGNS[sign] + " domicile", positions, light_pairs,
                    target_is_sign=True)
            rows.append(AversionRow(
                planet, SIGNS[source_sign], SIGNS[sign], witnessing,
                ("Mitigated" if methods else "Averse") if witnessing == "Averse"
                else "Witnesses", methods))
    return rows


def _shift(chart):
    return float(chart.ayanamsha) if chart.options.ayanamsha else 0.0


def analyze_rays(chart):
    """Directional sign-based aspects, overcoming and close counter-ray.

    The >3-degree aspects remain sign rays, NOT aktinobolia. Close
    counter-ray is the target's reciprocal ray striking the overcoming
    planet while the overcoming planet itself applies.
    """
    raw = {name: (float(p.data[0]), float(p.data[3]))
           for name, p in zip(PLANETS, chart.planets.planets[:7])}
    shift = _shift(chart)
    signs = {name: sign_of(lon - shift) for name, (lon, _) in raw.items()}
    rows = []
    # Chaldean order is slowest -> fastest. Each pair is evaluated ONCE
    # from its naturally faster body, regardless of current daily speed.
    for slower, faster in combinations(PLANETS, 2):
        caster, target = faster, slower
        ray = directed_ray(signs[caster], signs[target])
        if ray is None:
            continue
        aspect, direction = ray
        step = (signs[target] - signs[caster]) % 12
        _name, angle, index = SIGN_RAYS[step]
        caster_lon, caster_speed = raw[caster]
        target_lon, _ = raw[target]
        deviation = abs(angular_distance(caster_lon, target_lon) - angle)
        i, j = PLANETS.index(caster), PLANETS.index(target)
        cell = chart.aspmatrix[max(i, j)][min(i, j)]
        in_orb = cell.typ == index
        superior = overcomes(signs[caster], signs[target])
        # The victim's counter-ray is reciprocal at the same aspect
        # angle. It only qualifies within 3 degrees and when the
        # superior planet itself applies to the victim.
        counter = superior and in_orb and deviation <= 3.0 + EPS
        applying = (individual_motion(caster_lon, target_lon,
                                      caster_speed, angle) == "Applying")
        rows.append(RayRow(
            caster, target, SIGNS[signs[caster]], SIGNS[signs[target]],
            aspect, direction, "Yes" if superior else "No",
            deviation, counter, counter and applying, in_orb))
    return sorted(rows, key=lambda r: (PLANETS.index(r.caster),
                                      PLANETS.index(r.target)))


def analyze(chart, verified_light=()):
    return analyze_aversions(chart, verified_light), analyze_rays(chart)
