"""Horary A3: distinguish actual perfection events from traditional impediments.

Calculations accept the chart's seven (longitude, signed daily speed) pairs
and the chronological Swiss Ephemeris event sequence. Do not infer a firm
horary outcome from geometry alone: reception, houses, roles and doctrine
still require the astrologer's judgment.

Lilly-style distinctions:
- Frustration: the receiving/slower significator first conjoins a third.
- Prohibition: a swifter third body/ray reaches both significators in order.
- Refranation: an applying significator reverses, then moves away, before
  the originally intended exact aspect.
Events after an ingress/other station require fresh interpretation.
"""

from dataclasses import dataclass

from traditional_aspects import (PLANETS, ASPECT_ANGLES, RATE_TOLERANCE,
                                 motion_status, angular_distance, deviation_rate)

EPS = 1e-7
APPLYING = ("Applying", "Double application")


@dataclass(frozen=True)
class Finding:
    kind: str
    jd: float
    actor: str
    other: str
    detail: str


@dataclass(frozen=True)
class PerfectionReview:
    summary: str
    initial_motion: str
    intended_aspect: int | None
    target_jd: float | None
    findings: tuple


def _pair(event, first, second):
    return event.kind == "aspect" and {event.first, event.second} == {first, second}


def _other(event, who):
    if event.first == who:
        return event.second
    if event.second == who:
        return event.first
    return None


def _individual_applying(mover, other, angle):
    lon, speed = mover
    diff = abs(angular_distance(lon, other[0]) - angle)
    if diff <= EPS or abs(speed) < EPS:
        return False
    return deviation_rate(lon, other[0], speed, 0.0, angle) < -RATE_TOLERANCE


def assess(events, first, second, current_aspect, initial, positions_at=None,
           horizon_days=30):
    """Conservative doctrinal review of the originally applying aspect.

    current_aspect: 0..4 (or None), derived from the chart's existing matrix.
    initial: a mapping planet name -> (longitude, signed longitudinal speed).
    positions_at: optional function(JD) -> mapping name -> (lon, speed),
      used for confirming a *turn away* after an observed station.
    """
    if first == second or first not in PLANETS or second not in PLANETS:
        raise ValueError("Choose two different traditional planets")
    if current_aspect not in (None, 0, 1, 2, 3, 4):
        raise ValueError("Unknown current aspect")
    chron = sorted(events, key=lambda e: e.jd)
    if current_aspect is None:
        return PerfectionReview("No applying contact in the current chart",
                                "None", None, None, ())
    angle = ASPECT_ANGLES[current_aspect]
    lon_a, speed_a = initial[first]
    lon_b, speed_b = initial[second]
    state = motion_status(lon_a, lon_b, speed_a, speed_b, angle)
    if state not in APPLYING:
        return PerfectionReview("Current contact is not applying", state,
                                current_aspect, None, ())

    first_jd = chron[0].jd if chron else 0.0
    target = next((e for e in chron
                   if _pair(e, first, second)
                   and e.aspect_index == current_aspect), None)
    deadline = target.jd if target is not None else float("inf")
    ahead = [e for e in chron if e.jd < deadline - EPS]
    findings = []

    # The exact contacts may occur only after either party crosses a sign,
    # changes direction, or encounters another planet. These are displayed
    # chronologically rather than silently calling every ingress a denial.
    for e in ahead:
        if e.kind == "ingress" and e.first in (first, second):
            findings.append(Finding("Sign change", e.jd, e.first, "",
                                    "Significator enters another sign before the intended aspect"))

    # Lilly's refranation: a planet which was individually approaching the
    # intended aspect reverses and moves away. If no actual ephemeris position
    # callback is available, the station alone is not sufficient to assert it.
    for e in ahead:
        if e.kind != "station" or e.first not in (first, second):
            continue
        actor = e.first
        partner = second if actor == first else first
        if not _individual_applying(initial[actor], initial[partner], angle):
            findings.append(Finding("Station", e.jd, actor, partner,
                                    "A significator stations; inspect whether application changes"))
            continue
        if positions_at is None:
            findings.append(Finding("Possible refranation", e.jd, actor, partner,
                                    "An initially applying planet stations; later direction not verified"))
            continue
        after = positions_at(e.jd + .002)
        before = positions_at(e.jd - .002)
        prior = before[actor][1]
        later = after[actor][1]
        turn = prior * later < 0
        moves_away = not _individual_applying(after[actor], after[partner], angle)
        if turn and moves_away:
            findings.append(Finding("Refranation", e.jd, actor, partner,
                                    "Applying planet reversed and withdrew before intended perfection"))
        else:
            findings.append(Finding("Station", e.jd, actor, partner,
                                    "Observed station does not demonstrate withdrawal from the aspect"))

    # Frustration (Lilly's conjunction form): the slower/receiving partner
    # conjoins a third planet before the approaching significator arrives.
    slower = first if abs(speed_a) < abs(speed_b) else second
    faster = second if slower == first else first
    if abs(speed_a - speed_b) > EPS:
        for e in ahead:
            if e.kind != "aspect" or e.aspect_index != 0:
                continue
            third = _other(e, slower)
            if third in (None, faster):
                continue
            if third not in initial:
                continue
            if _individual_applying(initial[slower], initial[third], 0):
                findings.append(Finding("Frustration", e.jd, slower, third,
                    "The slower significator conjoins another planet before the faster reaches it; review reception"))

    # Lilly-style prohibition: swifter mediator first contacts the pursuing
    # significator, then the receiving significator ahead of direct perfection.
    # A lone third-planet contact is not sufficient for this classification.
    for third in PLANETS:
        if third in (first, second):
            continue
        if abs(initial[third][1]) <= max(abs(speed_a), abs(speed_b)) + EPS:
            continue
        contacts_first = [e for e in ahead if e.kind == "aspect"
                          and _other(e, first) == third]
        contacts_second = [e for e in ahead if e.kind == "aspect"
                           and _other(e, second) == third]
        matching = [(x, y) for x in contacts_first for y in contacts_second
                    if x.jd < y.jd - EPS]
        matching += [(x, y) for x in contacts_second for y in contacts_first
                     if x.jd < y.jd - EPS]
        if not matching:
            continue
        start, end = min(matching, key=lambda pair: pair[1].jd)
        # Earlier station/ingress of the mediator means this may be a new,
        # not the initially seen, third-party application.
        intervened = any(e.kind in ("station", "ingress") and e.first == third
                         and e.jd < end.jd - EPS for e in ahead)
        findings.append(Finding("Possible prohibition" if intervened else "Prohibition",
                                end.jd, third, first + " / " + second,
                                "Third planet perfects with both significators in sequence before their intended aspect; review reception"))

    # Other earlier contacts of the selected significators remain visible but
    # are not mislabeled as prohibition or frustration without the structure.
    classified = {(f.jd, f.actor) for f in findings
                  if f.kind in ("Frustration", "Prohibition", "Possible prohibition")}
    for e in ahead:
        if e.kind != "aspect":
            continue
        for actor in (first, second):
            other = _other(e, actor)
            if other and other not in (first, second) and (e.jd, actor) not in classified:
                findings.append(Finding("Earlier contact", e.jd, actor, other,
                                        "Another exact planetary aspect precedes the intended contact"))

    findings.sort(key=lambda f: (f.jd, f.kind, f.actor))
    if target is None:
        summary = "No direct perfection within %d days" % horizon_days
    elif any(f.kind in ("Prohibition", "Frustration", "Refranation")
             for f in findings):
        summary = "Perfection has identified impediment(s); interpret reception and context"
    elif findings:
        summary = "Perfection follows earlier events; review the timeline"
    else:
        summary = "Direct perfection: no intervening events detected"
    return PerfectionReview(summary, state, current_aspect,
                            target.jd if target is not None else None,
                            tuple(findings))
