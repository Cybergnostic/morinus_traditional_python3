"""Planet-to-point contacts shared by natal, cross-chart and multiwheel.

Asc/MC and Lots are targets, never planets: no reception, translation,
collection or double application. Course doctrine: points have no light and
no orb of their own and cannot aspect; they are aspected by planets, within
the PLANET's full orb (and the three-degree rule across sign boundaries).
For lots defined by whole signs, only the by-sign relation is meaningful.
"""
from dataclasses import dataclass
from math import isfinite

import tradoptions
from traditional_aspects import (PLANETS, ASPECT_ANGLES, configured_orbs,
                                 evaluate, sign_configuration)
from aspect_workspace import ASPECT_NAMES

ANGLE_NAMES = ("ASC", "MC")


@dataclass(frozen=True)
class Point:
    name: str
    longitude: float
    kind: str  # Angles or Lots
    degree_based: bool = True


@dataclass(frozen=True)
class PointContact:
    planet: str
    point: str
    aspect: str
    deviation: float | None
    out_of_sign: bool
    motion: str
    planet_longitude: float
    point_longitude: float
    degree_based: bool


@dataclass(frozen=True)
class CrossPointContact:
    chart_of_planet: str  # A or B
    planet: str
    chart_of_point: str
    point: str
    kind: str
    aspect: str
    deviation: float | None
    out_of_sign: bool
    planet_longitude: float
    point_longitude: float
    degree_based: bool


def _shift(chrt, options):
    return float(chrt.ayanamsha) if options.ayanamsha else 0.0


def angles(chrt, options):
    shift = _shift(chrt, options)
    return tuple(Point(name, (float(chrt.houses.ascmc[index]) - shift) % 360,
                       "Angles") for index, name in enumerate(ANGLE_NAMES))


def lots(chrt, options, visible_only=True):
    """Respect user's Lot names, visibility, chart sect and stored longitude.

    Lots.LON is at index 4 and Lots.NAME is at index 0. Unlike planetary and
    angle positions, calculated lot longitude has already had ayanamsha
    subtracted by lots.Lots when sidereal is enabled, so do NOT subtract it
    a second time. With lotsusehouses=True these are sign-only results.
    """
    found = getattr(getattr(chrt, "lots", None), "lots", None) or ()
    enabled = getattr(options, "lotsvisible", None)
    results = []
    for index, item in enumerate(found):
        if visible_only and enabled is not None and (
                index >= len(enabled) or not enabled[index]):
            continue
        if len(item) <= 4 or not isfinite(float(item[4])):
            continue
        results.append(Point(str(item[0]), float(item[4]) % 360,
                             "Lots", not bool(options.lotsusehouses)))
    return tuple(results)


def points(chrt, options, kind="Angles", visible_only=True):
    if kind == "Angles":
        return angles(chrt, options)
    if kind == "Lots":
        return lots(chrt, options, visible_only)
    raise ValueError("Unknown point category")


def _contact(planet_lon, speed, point, orb):
    if not point.degree_based:
        # A whole-sign lot is not a point with a reliable exact longitude.
        config = sign_configuration(planet_lon, point.longitude)
        if config is None:
            return None
        return config, None, False, "By sign"

    # The point has no orb: the planet's own orb is the limit, with the
    # standard A1 geometric aspect / out-of-sign rules.
    contact = evaluate(planet_lon, point.longitude, speed, 0.0, orb, 0.0)
    if contact is None:
        return None
    if contact.exact:
        motion = "Exact"
    elif abs(speed) < 1e-10:
        motion = "Stationary"
    else:
        from light_perfection import individual_motion
        motion = individual_motion(
            planet_lon, point.longitude, speed, contact.angle)
    return contact.index, contact.deviation, contact.out_of_sign, motion


def _orb_settings(options, settings):
    cfg = dict(settings if settings is not None else tradoptions.values())
    if cfg.get("aspect_preset", "traditional") == "legacy":
        # Morinus 6.2 has no planet-to-Lot aspects: its orb values are used
        # with the same rule (the planet's orb).
        return tuple(float(options.orbs[index]) for index in range(7))
    return configured_orbs(cfg)


def analyze_single(chrt, kind="Angles", options=None, settings=None,
                   planet_filter=None, point_filter=None):
    options = options or chrt.options
    orbs = _orb_settings(options, settings)
    targets = points(chrt, options, kind)
    shift = _shift(chrt, options)
    rows = []
    for index, planet in enumerate(PLANETS):
        if planet_filter is not None and planet != planet_filter:
            continue
        pl = chrt.planets.planets[index]
        lon = (float(pl.data[0]) - shift) % 360
        speed = float(pl.data[3])
        for target in targets:
            if point_filter is not None and target.name != point_filter:
                continue
            result = _contact(lon, speed, target, orbs[index])
            if result is None:
                continue
            kind_index, orb, outside, motion = result
            rows.append(PointContact(
                planet, target.name, ASPECT_NAMES[kind_index], orb, outside,
                motion, lon, target.longitude, target.degree_based))
    rows.sort(key=lambda row: (row.deviation is None,
                              row.deviation if row.deviation is not None else 0,
                              row.point, PLANETS.index(row.planet)))
    return tuple(rows)


def analyze_cross(first_chart, second_chart, kind="Angles", options=None,
                  settings=None, planet_filter=None, point_filter=None):
    """Compute BOTH directions: A planet -> B point and B planet -> A point."""
    if first_chart is second_chart:
        return ()
    options = options or first_chart.options
    orbs = _orb_settings(options, settings)
    rows = []
    for source_label, source, target_label, target in (
            ("A", first_chart, "B", second_chart),
            ("B", second_chart, "A", first_chart)):
        target_points = points(target, options, kind)
        shift = _shift(source, options)
        for index, planet in enumerate(PLANETS):
            if planet_filter is not None and planet != planet_filter:
                continue
            pl = source.planets.planets[index]
            lon = (float(pl.data[0]) - shift) % 360
            for target_point in target_points:
                if point_filter is not None and target_point.name != point_filter:
                    continue
                result = _contact(lon, float(pl.data[3]), target_point,
                                  orbs[index])
                if result is None:
                    continue
                kind_index, deviation, outside, _motion = result
                rows.append(CrossPointContact(
                    source_label, planet, target_label, target_point.name,
                    kind, ASPECT_NAMES[kind_index], deviation, outside,
                    lon, target_point.longitude, target_point.degree_based))
    rows.sort(key=lambda row: (row.deviation is None,
                              row.deviation if row.deviation is not None else 0,
                              row.chart_of_planet, row.planet, row.point))
    return tuple(rows)
