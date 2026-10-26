"""A4 Hellenistic domicile witnessing and directed planetary rays.

Course doctrine (aspects, receptions and degrees):

- Whole-sign witnessing of each planet's domiciles. A planet is NOT averse
  to its domicile when the two signs are joined by antiscia, contra-antiscia
  or a common ruler. Otherwise an aversion can be mitigated by a mediator: a
  planet seeing both the averse planet and its domicile by a Ptolemaic aspect
  (sextile, square, trine, opposition; not co-presence, not antiscia), and
  not cadent or combust. In a natal chart seeing is enough. Verified A3
  translation/collection of light also mitigates.
- Dexter and sinister are judged from the faster, applying planet: its
  actual speed in the chart, not the natural order of the planets.
- Overcoming: a planet in the 9th, 10th or 11th sign from another overcomes
  it (by trine, square, sextile), whether or not they are configured.
- Aktinobolia: the faster planet overcomes the slower within three degrees
  of the exact aspect, applying or separating (applying weighs more), and
  is struck by the overcome planet's ray.
"""
from dataclasses import dataclass
from itertools import combinations

from traditional_aspects import PLANETS, angular_distance, motion_status
from aspect_workspace import SIGNS

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
# Signs seen by a Ptolemaic aspect (not co-presence): sextile, square,
# trine and opposition on either side.
PTOLEMAIC_STEPS = {2, 3, 4, 6, 8, 9, 10}
CADENT_HOUSES = {3, 6, 9, 12}
# Combust between 0°17' and 7°30' from the Sun (cazimi is not combustion).
CAZIMI = 17.0 / 60.0
COMBUST = 7.5
AKTINOBOLIA_LIMIT = 3.0
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
    motion: str
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


def _connections(source_long, domicile):
    """Sign links that keep a planet from being averse to its domicile."""
    left = sign_of(source_long)
    links = []
    if SIGN_RULERS[left] == SIGN_RULERS[domicile]:
        links.append("Common domicile ruler: " + SIGN_RULERS[left])
    # A domicile is a whole sign: only sign-level mirrors, never degrees.
    links.extend(m for m in _reflections(source_long, domicile * 30.0 + 15.0)
                 if "(degree)" not in m)
    return links


def _house(chart, longitude, shift):
    houses = getattr(chart, "houses", None)
    if hasattr(houses, "getHousePos"):
        return houses.getHousePos(longitude, chart.options) + 1
    asc = (float(houses.ascmc[0]) - shift) % 360.0
    return (sign_of(longitude - shift) - sign_of(asc)) % 12 + 1


def _mediators(chart, planet, domicile, positions, shift):
    """Planets that see both an averse planet and its domicile sign.

    Ptolemaic aspects only, by sign; cadent and combust planets cannot help.
    """
    raw = {name: float(p.data[0]) for name, p in zip(PLANETS, chart.planets.planets[:7])}
    sun = positions["Sun"][0]
    source = sign_of(positions[planet][0])
    found = []
    for name in PLANETS:
        if name == planet:
            continue
        lon = positions[name][0]
        own = sign_of(lon)
        if (source - own) % 12 not in PTOLEMAIC_STEPS:
            continue
        if (domicile - own) % 12 not in PTOLEMAIC_STEPS:
            continue
        if _house(chart, raw[name], shift) in CADENT_HOUSES:
            continue
        if name != "Sun" and CAZIMI < angular_distance(lon, sun) <= COMBUST:
            continue
        found.append("Mediator: " + name)
    return found


def _light(source_name, domicile, positions, light_pairs):
    """Verified translation/collection with an occupant of the domicile."""
    methods = []
    for occupant, (lon, _speed) in positions.items():
        if occupant == source_name or sign_of(lon) != domicile:
            continue
        methods.extend(sorted(light_pairs.get(
            frozenset((source_name, occupant)), ())))
    return methods


def domicile_witnessing(source_sign, domicile_sign):
    """A sign-based testimony, not a claim of a close degree aspect."""
    step = (domicile_sign - source_sign) % 12
    return {0: "Co-presence", 2: "Sextile", 3: "Square",
            4: "Trine", 6: "Opposition", 8: "Trine",
            9: "Square", 10: "Sextile"}.get(step, "Averse")


def analyze_aversions(chart, light=()):
    """Show EACH planet's relation to EACH domicile it rules (12 rows).

    Status: Witnesses (whole-sign aspect or co-presence), Not averse (signs
    joined by antiscia, contra-antiscia or a common ruler), Mitigated (a
    mediator or verified light), or Averse. Planet-pair aversions and
    planet-to-Ascendant relations are not part of this table.
    """
    shift = _shift(chart)
    positions = {
        name: ((float(planet.data[0]) - shift) % 360.0,
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
            status = "Witnesses"
            if witnessing == "Averse":
                links = _connections(source_long, sign)
                if links:
                    status, methods = "Not averse", tuple(links)
                else:
                    methods = tuple(dict.fromkeys(
                        _mediators(chart, planet, sign, positions, shift) +
                        _light(planet, sign, positions, light_pairs)))
                    status = "Mitigated" if methods else "Averse"
            rows.append(AversionRow(
                planet, SIGNS[source_sign], SIGNS[sign], witnessing,
                status, methods))
    return rows


def _shift(chart):
    return float(chart.ayanamsha) if chart.options.ayanamsha else 0.0


def analyze_rays(chart):
    """Directional sign-based aspects, overcoming and aktinobolia.

    One row per pair in aspecting signs, cast by the faster planet (its
    actual speed; the natural order only breaks an exact tie), as the course
    judges dexter and sinister from the applying planet.
    """
    raw = {name: (float(p.data[0]), float(p.data[3]))
           for name, p in zip(PLANETS, chart.planets.planets[:7])}
    shift = _shift(chart)
    signs = {name: sign_of(lon - shift) for name, (lon, _) in raw.items()}
    rows = []
    for slower, faster in combinations(PLANETS, 2):
        # Chaldean order is slowest -> fastest: the tie-breaker only.
        if abs(raw[slower][1]) > abs(raw[faster][1]):
            slower, faster = faster, slower
        caster, target = faster, slower
        ray = directed_ray(signs[caster], signs[target])
        if ray is None:
            continue
        aspect, direction = ray
        step = (signs[target] - signs[caster]) % 12
        _name, angle, index = SIGN_RAYS[step]
        caster_lon, caster_speed = raw[caster]
        target_lon, target_speed = raw[target]
        deviation = abs(angular_distance(caster_lon, target_lon) - angle)
        i, j = PLANETS.index(caster), PLANETS.index(target)
        cell = chart.aspmatrix[max(i, j)][min(i, j)]
        in_orb = cell.typ == index
        superior = overcomes(signs[caster], signs[target])
        motion = motion_status(caster_lon, target_lon, caster_speed,
                               target_speed, angle) if in_orb else ""
        # In every sextile, square and trine one of the two planets is in the
        # 9th-11th sign from the other. Name it, whichever moves faster:
        # Saturn in the 10th from the Moon overcomes the Moon.
        rows.append(RayRow(
            caster, target, SIGNS[signs[caster]], SIGNS[signs[target]],
            aspect, direction, caster if superior else target,
            deviation, motion,
            superior and in_orb and deviation <= AKTINOBOLIA_LIMIT + EPS,
            in_orb))
    return sorted(rows, key=lambda r: (PLANETS.index(r.caster),
                                      PLANETS.index(r.target)))


def analyze(chart, verified_light=()):
    return analyze_aversions(chart, verified_light), analyze_rays(chart)
