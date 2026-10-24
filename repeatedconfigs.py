"""Search for repeated natal configurations in a solar return.

This is a deliberately *on-demand* geometric comparison, not a replacement
for Morinus's aspect engine. The maximum distance from exactness is explicitly
set by the person searching. Future traditional aspect presets can be shared
with this search without changing its reporting/UI code.

Only the seven visible planets and five Ptolemaic aspects are considered.
Pairs must contain the SAME named planets and the SAME aspect in both charts.
Three-planet groups require every one of their three pairwise aspects to recur.
"""

from dataclasses import dataclass
from itertools import combinations
from math import isfinite
from typing import Mapping


PLANETS = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon')
ASPECTS = (('Conjunction', 0.0), ('Sextile', 60.0), ('Square', 90.0),
           ('Trine', 120.0), ('Opposition', 180.0))
SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')


@dataclass(frozen=True)
class RepeatedAspect:
    planets: tuple[str, str]
    aspect: str
    natal_orb: float
    solar_orb: float
    involves_year_lord: bool


@dataclass(frozen=True)
class RepeatedTriple:
    planets: tuple[str, str, str]
    relations: tuple[RepeatedAspect, RepeatedAspect, RepeatedAspect]
    involves_year_lord: bool


@dataclass(frozen=True)
class RepeatedPlacement:
    planet: str
    kind: str  # 'Sign' or 'Whole-sign house'
    index: int  # sign: 0..11; house: 1..12
    involves_year_lord: bool


@dataclass(frozen=True)
class SearchResults:
    aspects: tuple[RepeatedAspect, ...]
    triples: tuple[RepeatedTriple, ...]
    placements: tuple[RepeatedPlacement, ...]


def aspect_between(longitude_a: float, longitude_b: float, max_deviation: float):
    """Return (aspect name, actual orb) if within a geometric threshold."""
    distance = abs((longitude_b - longitude_a + 180.0) % 360.0 - 180.0)
    name, angle = min(ASPECTS, key=lambda a: abs(distance - a[1]))
    orb = abs(distance - angle)
    return (name, orb) if orb <= max_deviation else None


def _validate(longitudes, label):
    missing = set(PLANETS) - set(longitudes)
    if missing:
        raise ValueError('Missing %s planets: %s' % (label, ', '.join(sorted(missing))))
    if not all(isfinite(longitudes[name]) for name in PLANETS):
        raise ValueError('%s planet longitudes must be finite' % label)


def _sign(lon, shift=0.0):
    return int(((lon - shift) % 360.0) // 30.0)


def search(
    natal: Mapping[str, float], solar: Mapping[str, float],
    max_deviation: float = 5.0, year_lord: str | None = None,
    include_placements: bool = False, annual_only: bool = False,
    natal_asc: float | None = None, solar_asc: float | None = None,
    natal_ayanamsha: float = 0.0, solar_ayanamsha: float = 0.0,
) -> SearchResults:
    """Find repeated geometric aspects, complete triples and optional placements.

    Orb is the deviation from exact aspect in *each* chart separately; it is
    not the sum/average of planetary moieties. Neither applying/separating nor
    cross-chart aspects are inferred from this comparison.
    """
    _validate(natal, 'natal')
    _validate(solar, 'solar')
    if not isfinite(max_deviation) or not 0.0 < max_deviation <= 10.0:
        raise ValueError('Maximum deviation must be greater than 0 and at most 10 degrees')
    if year_lord is not None and year_lord not in PLANETS:
        raise ValueError('Unknown traditional ruler of the year')
    if annual_only and year_lord is None:
        raise ValueError('Ruler of the year is required for the annual-lord filter')

    # First gather every recurrence. Filter after assembling triples: a triple
    # with the annual lord still requires its other two planets' mutual aspect.
    repeated = {}
    for p, q in combinations(PLANETS, 2):
        na = aspect_between(natal[p], natal[q], max_deviation)
        sa = aspect_between(solar[p], solar[q], max_deviation)
        if na is not None and sa is not None and na[0] == sa[0]:
            repeated[(p, q)] = RepeatedAspect(
                (p, q), na[0], na[1], sa[1], year_lord in (p, q),
            )

    triples = []
    for p, q, r in combinations(PLANETS, 3):
        keys = ((p, q), (p, r), (q, r))
        if all(key in repeated for key in keys):
            has_lord = year_lord in (p, q, r)
            if not annual_only or has_lord:
                triples.append(RepeatedTriple(
                    (p, q, r), tuple(repeated[key] for key in keys), has_lord,
                ))

    aspects = [row for row in repeated.values()
               if not annual_only or row.involves_year_lord]
    aspects.sort(key=lambda a: (not a.involves_year_lord,
                                a.solar_orb + a.natal_orb, a.planets))
    triples.sort(key=lambda t: (not t.involves_year_lord,
                                sum(a.natal_orb + a.solar_orb for a in t.relations),
                                t.planets))

    placements = []
    if include_placements:
        if natal_asc is None or solar_asc is None:
            raise ValueError('Both Ascendants are required to compare houses')
        if not all(isfinite(value) for value in
                   (natal_asc, solar_asc, natal_ayanamsha, solar_ayanamsha)):
            raise ValueError('Ascendants and ayanamshas must be finite')
        nat_ascsign = _sign(natal_asc, natal_ayanamsha)
        sol_ascsign = _sign(solar_asc, solar_ayanamsha)
        for p in PLANETS:
            if annual_only and p != year_lord:
                continue
            ns = _sign(natal[p], natal_ayanamsha)
            ss = _sign(solar[p], solar_ayanamsha)
            # Solar-return Sun in its natal sign is automatic, not a finding.
            if p != 'Sun' and ns == ss:
                placements.append(RepeatedPlacement(
                    p, 'Sign', ns, p == year_lord,
                ))
            nh = (ns - nat_ascsign) % 12 + 1
            sh = (ss - sol_ascsign) % 12 + 1
            if nh == sh:
                placements.append(RepeatedPlacement(
                    p, 'Whole-sign house', nh, p == year_lord,
                ))
        placements.sort(key=lambda r: (not r.involves_year_lord, r.planet, r.kind))

    return SearchResults(tuple(aspects), tuple(triples), tuple(placements))
