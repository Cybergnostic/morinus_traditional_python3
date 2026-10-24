"""Traditional aspect and reception analysis, separate from the chart renderer.

Reads Morinus's selected dignity tables and the current chart aspect matrix.
No wxPython or ephemeris dependency: this module can be tested independently.
"""

from dataclasses import dataclass

from traditional_aspects import (ASPECT_ANGLES, PLANETS, angular_distance,
                                 motion_status, sign_configuration)

ASPECT_NAMES = ("Conjunction", "Sextile", "Square", "Trine", "Opposition")
SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")
# Morinus triplicity-table rows: fire, air, water, earth.
TRIP_ELEMENTS = (0, 3, 1, 2) * 3
MINOR_PAIRS = ({"triplicity", "term"}, {"triplicity", "face"}, {"term", "face"})


@dataclass(frozen=True)
class AspectRow:
    first: str
    second: str
    kind: str
    deviation: float
    motion: str
    out_of_sign: bool
    first_speed: float
    second_speed: float


@dataclass(frozen=True)
class ReceptionRow:
    host: str
    guest: str
    status: str
    dignities: tuple
    aspect: str
    mutual: bool
    guest_sign: str
    guest_degree: float


def angular_motion(a, b, speed_a, speed_b, angle):
    """Immediate applying/separating state from signed geocentric motions.

    This distinguishes double application/separation when both planets
    individually approach/recede from the same exact aspect, and ordinary
    applying/separating from their relative speed. Future perfection across
    stations, ingresses or intervening aspects is not guaranteed.
    """
    return motion_status(a, b, speed_a, speed_b, angle)


def dignity_holds(options, host_index, longitude, daytime):
    """Essential dignity components of host at guest's zodiacal longitude.

    Uses active Morinus domicile/exaltation, triplicity, term and decan
    selections. The Mercury-in-Virgo exaltation follows its existing switch.
    """
    sign = int((longitude % 360.0) // 30.0)
    degree = longitude % 30.0
    found = []
    if options.dignities[host_index][0][sign]:
        found.append("domicile")
    if options.dignities[host_index][1][sign] and (
            host_index != 5 or sign != 5 or options.useexaltationmercury):
        found.append("exaltation")
    trip = options.trips[options.seltrip][TRIP_ELEMENTS[sign]]
    if options.oneruler:
        lord = trip[0 if daytime else 1]
        if lord == host_index:
            found.append("triplicity")
    elif host_index in trip:
        found.append("triplicity")
    boundary = 0.0
    for lord, width in options.terms[options.selterm][sign]:
        boundary += width
        if degree < boundary:
            if lord == host_index:
                found.append("term")
            break
    face = options.decans[options.seldecan][sign][min(2, int(degree // 10))]
    if face == host_index:
        found.append("face")
    return tuple(found)


def qualifies_for_reception(held):
    held = set(held)
    return "domicile" in held or "exaltation" in held or any(
        pair <= held for pair in MINOR_PAIRS)


def _positions(chrt):
    return tuple(
        (float(chrt.planets.planets[i].data[0]),
         float(chrt.planets.planets[i].data[3]))
        for i in range(7))


def analyze(chrt):
    """Return (contact rows, directed reception/generosity rows) for 7 planets."""
    positions = _positions(chrt)
    aspects = []
    connections = {}
    for i in range(7):
        for j in range(i + 1, 7):
            cell = chrt.aspmatrix[j][i]
            aspect_id = cell.typ
            if aspect_id not in range(5):
                continue
            lon_a, speed_a = positions[i]
            lon_b, speed_b = positions[j]
            angle = ASPECT_ANGLES[aspect_id]
            separation = angular_distance(lon_a, lon_b)
            deviation = abs(separation - angle)
            out_of_sign = sign_configuration(lon_a, lon_b) != aspect_id
            aspects.append(AspectRow(
                PLANETS[i], PLANETS[j], ASPECT_NAMES[aspect_id], deviation,
                angular_motion(lon_a, lon_b, speed_a, speed_b, angle),
                out_of_sign, speed_a, speed_b))
            connections[(i, j)] = ASPECT_NAMES[aspect_id]
    aspects.sort(key=lambda a: (a.deviation, a.first, a.second))

    options = chrt.options
    day = bool(chrt.planets.planets[3].speculums[0].abovehorizon)
    if options.usedaynightorb:
        day = bool(chrt.abovehorizonwithorb)
    adjustment = chrt.ayanamsha if options.ayanamsha != 0 else 0.0
    potential = {}
    for host in range(7):
        for guest in range(7):
            if host == guest:
                continue
            place = (positions[guest][0] - adjustment) % 360.0
            dignity = dignity_holds(options, host, place, day)
            if qualifies_for_reception(dignity):
                potential[(host, guest)] = (dignity, place)
    receptions = []
    for (host, guest), (held, place) in potential.items():
        kind = connections.get((min(host, guest), max(host, guest)))
        mutual = (guest, host) in potential
        receptions.append(ReceptionRow(
            PLANETS[host], PLANETS[guest],
            "Reception" if kind else "Generosity",
            held, kind or "", mutual,
            SIGNS[int(place // 30.0)], place % 30.0))
    receptions.sort(key=lambda r: (
        0 if r.status == "Reception" else 1,
        0 if r.mutual else 1, r.host, r.guest))
    return aspects, receptions
