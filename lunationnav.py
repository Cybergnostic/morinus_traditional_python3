"""Swiss Ephemeris-driven New/Full Moon finder, independent of prenatal syzygy.

Never creates or mutates Syzygy or Chart objects; calculate ecliptic phase
crossings directly at UT Julian days. Pure phase helpers are testable without
Swiss Ephemeris, while production uses Morinus's astrology bridge.
"""

STEP_DAYS = 0.75
KINDS = ((0.0, 'New Moon'), (180.0, 'Full Moon'))


def phase_difference(moon_lon, sun_lon, target):
    """Signed separation in [-180, 180); a root represents target phase."""
    return ((moon_lon - sun_lon - target + 180.0) % 360.0) - 180.0


def crossing(left, right):
    """True at a forward-moving phase root, but not a 180-degree wrap."""
    return left <= 0.0 <= right and right - left < 40.0


def refine(jd0, jd1, target, sampler, iterations=27):
    """Bisect a bracket to better than a second using only the two luminaries."""
    for _ in range(iterations):
        mid = (jd0 + jd1) / 2.0
        sun, moon = sampler(mid)
        if phase_difference(moon, sun, target) < 0:
            jd0 = mid
        else:
            jd1 = mid
    return (jd0 + jd1) / 2.0


def find_events(center_jd, sampler, half_window=65):
    """Sorted (jd, kind, sun longitude, moon longitude) in UT window.

    The sample step is shorter than a day and crossing() rejects the false
    sign change at the discontinuity opposite the target. No natal object
    is passed to or modified by this function.
    """
    start, stop = center_jd - half_window, center_jd + half_window
    events = []
    last_t, last_sun, last_moon = start, *sampler(start)
    t = start + STEP_DAYS
    while last_t < stop:
        current_t = min(t, stop)
        sun, moon = sampler(current_t)
        for target, name in KINDS:
            a = phase_difference(last_moon, last_sun, target)
            b = phase_difference(moon, sun, target)
            if crossing(a, b):
                exact = refine(last_t, current_t, target, sampler)
                es, em = sampler(exact)
                events.append((exact, name, es, em))
        last_t, last_sun, last_moon = current_t, sun, moon
        t = current_t + STEP_DAYS
    return sorted(events)


def ephemeris_sampler():
    """Build a Swiss Ephemeris sampler; keep imports out of pure unit tests."""
    import astrology
    flags = astrology.SEFLG_SWIEPH | astrology.SEFLG_SPEED

    def sample(jd):
        sun_status, sun, sun_error = astrology.swe_calc_ut(
            jd, astrology.SE_SUN, flags)
        moon_status, moon, moon_error = astrology.swe_calc_ut(
            jd, astrology.SE_MOON, flags)
        if sun_status < 0 or moon_status < 0:
            raise RuntimeError('Swiss Ephemeris could not calculate a lunar phase: ' +
                               str(sun_error or moon_error))
        return sun[0], moon[0]
    return sample
