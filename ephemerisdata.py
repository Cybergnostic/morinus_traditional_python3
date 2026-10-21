"""Shared geocentric ephemeris for Morinus's traditional visible planets.

All longitudes are ecliptic of date; 00:00 UT daily samples are used for
tables/plots, with ephemeris-sampled bisection for stations and ingresses.
The core is dependency-injected to allow precise tests without Swiss Ephemeris.
"""
import calendar
import datetime
import math
from collections import namedtuple

PLANETS = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon')
SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
Event = namedtuple('Event', 'jd planet kind detail')
YearData = namedtuple('YearData', 'year dates jds longitudes speeds events')


def year_days(year):
    """The graphical ephemeris has always used the Gregorian calendar."""
    if not 1 <= int(year) <= 5000:
        raise ValueError('Ephemeris year must be AD 1–5000')
    return 366 if calendar.isleap(int(year)) else 365


def delta(longitude_a, longitude_b):
    """Minimal signed displacement from a to b, crossing the Aries point."""
    return (longitude_b - longitude_a + 180.0) % 360.0 - 180.0


def station_crossing(a, b):
    """Strict signed-speed reversal, excluding ambiguous exact-zero endpoints."""
    return (a > 0.0 and b <= 0.0) or (a < 0.0 and b >= 0.0)


def ingress_crossing(a, b):
    """Next sign boundary crossed and motion direction, or None."""
    movement = delta(a, b)
    if not movement or abs(movement) > 30:
        return None
    if int((a % 360) // 30) == int((b % 360) // 30):
        return None
    if movement > 0:
        sign = int((b % 360) // 30)
        return sign, 1
    sign = int((a % 360) // 30)
    return sign, -1


def bisect(jd0, jd1, measure, iterations=25):
    """Refine a continuous zero bracket to approximately second precision."""
    y0 = measure(jd0)
    y1 = measure(jd1)
    if y0 == 0.0:
        return jd0
    if y1 == 0.0:
        return jd1
    if y0 * y1 > 0:
        raise ValueError('No event in ephemeris bracket')
    for _ in range(iterations):
        mid = (jd0 + jd1) / 2.0
        value = measure(mid)
        if value == 0.0:
            return mid
        if (y0 < 0) == (value < 0):
            jd0, y0 = mid, value
        else:
            jd1 = mid
    return (jd0 + jd1) / 2.0


def format_position(lon, speed):
    """Zodiacal longitude (degrees, minutes) and retrogradation indicator."""
    degrees_in_sign = (lon % 30.0)
    rounded_minutes = int(round(degrees_in_sign * 60))
    if rounded_minutes >= 1800:
        rounded_minutes = 0
        sign = (int(lon % 360 // 30) + 1) % 12
    else:
        sign = int(lon % 360 // 30)
    return '%02d°%02d\u2032 %s%s' % (
        rounded_minutes // 60, rounded_minutes % 60, SIGNS[sign][:3],
        ' R' if speed < 0 else '')


def calculate(year, start_jd, sampler):
    """Sample 7 planets at midnight UT each Gregorian day.

    sampler(jd, planet_index) returns (tropical or sidereal longitude, *tropical*
    geocentric longitude speed). Speed zero is the conventional station.
    """
    dates = [datetime.date(year, 1, 1) + datetime.timedelta(days=i)
             for i in range(year_days(year))]
    jds = [start_jd + i for i in range(len(dates))]
    longitudes = [[] for _ in PLANETS]
    speeds = [[] for _ in PLANETS]
    for jd in jds:
        for planet in range(len(PLANETS)):
            lon, speed = sampler(jd, planet)
            longitudes[planet].append(lon % 360)
            speeds[planet].append(speed)

    events = []
    # Includes the midnight of the following January to detect late-Dec
    # crossings; these will appear on the next year only.
    last_day = start_jd + len(dates)
    for planet in range(len(PLANETS)):
        sample = lambda jd, p=planet: sampler(jd, p)
        for day in range(len(jds)):
            jd0 = jds[day]
            jd1 = last_day if day == len(jds) - 1 else jds[day + 1]
            lon0, speed0 = longitudes[planet][day], speeds[planet][day]
            lon1, speed1 = sample(jd1)
            if station_crossing(speed0, speed1):
                t = bisect(jd0, jd1, lambda jd: sample(jd)[1])
                if start_jd <= t < last_day:
                    detail = 'Station direct' if speed1 > 0 else 'Station retrograde'
                    events.append(Event(t, planet, 'Station', detail))
            ingress = ingress_crossing(lon0, lon1)
            if ingress:
                sign, direction = ingress
                boundary = (sign if direction == 1 else (sign + 1) % 12) * 30.0
                t = bisect(jd0, jd1, lambda jd, target=boundary:
                           delta(target, sample(jd)[0]))
                if start_jd <= t < last_day:
                    label = ('Ingress ' if direction == 1 else 'Retrograde ingress ') + SIGNS[sign]
                    events.append(Event(t, planet, 'Ingress', label))
    return YearData(year, dates, jds, longitudes, speeds,
                    sorted(events, key=lambda e: (e.jd, e.planet, e.kind)))


def swiss_sampler(options):
    """Morinus Swiss Ephemeris bridge, using its Chaldean planet ordering."""
    import astrology
    import util
    flags = astrology.SEFLG_SWIEPH | astrology.SEFLG_SPEED
    sidereal = options.ayanamsha != 0
    if sidereal:
        astrology.swe_set_sid_mode(options.ayanamsha - 1, 0, 0)

    def sample(jd, planet):
        ret, data, error = astrology.swe_calc_ut(
            jd, util.mapChaldeanToModern(planet), flags)
        if ret < 0:
            raise RuntimeError('Swiss Ephemeris failed: ' + str(error))
        longitude = data[0]
        if sidereal:
            longitude -= astrology.swe_get_ayanamsa_ut(jd)
        return longitude % 360, data[3]
    return sample


def year_from_swiss(year, options):
    import astrology
    year_days(year)
    jd = astrology.swe_julday(year, 1, 1, 0.0, astrology.SE_GREG_CAL)
    return calculate(year, jd, swiss_sampler(options))
