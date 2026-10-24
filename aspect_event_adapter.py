"""Swiss Ephemeris adapter for the on-demand A3 event scanner."""

import astrology
from aspect_event_search import scan

IDS = (astrology.SE_SATURN, astrology.SE_JUPITER, astrology.SE_MARS,
       astrology.SE_SUN, astrology.SE_VENUS, astrology.SE_MERCURY,
       astrology.SE_MOON)


def position_provider(chart):
    """Return chart-consistent live ephemeris positions at any UT Julian day."""
    if chart.time.bc:
        raise ValueError('Event search is unavailable for BCE charts')
    options = chart.options
    flags = astrology.SEFLG_SWIEPH | astrology.SEFLG_SPEED
    if options.topocentric:
        astrology.swe_set_topo(chart.place.lon, chart.place.lat,
                               chart.place.altitude)
        flags |= astrology.SEFLG_TOPOCTR
    if options.ayanamsha != 0:
        astrology.swe_set_sid_mode(options.ayanamsha - 1, 0, 0)
    def positions(jd):
        # Apply a fresh ayanamsha for each step rather than holding the chart
        # epoch's offset constant. All seven planets share the same correction.
        shift = astrology.swe_get_ayanamsa_ut(jd) if options.ayanamsha != 0 else 0.0
        result = []
        for planet_id in IDS:
            _flag, data, _error = astrology.swe_calc_ut(jd, planet_id, flags)
            result.append(((data[0] - shift) % 360.0, data[3]))
        return result
    return positions


def search(chart, days):
    return scan(position_provider(chart), chart.time.jd, days)


def named_positions(chart):
    from traditional_aspects import PLANETS
    positions = position_provider(chart)
    return lambda jd: dict(zip(PLANETS, positions(jd)))
