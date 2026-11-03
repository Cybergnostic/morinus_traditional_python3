"""Traditional-astrology analysis of Morinus charts with the vendored hor_tools
package (its rules: Sun..Saturn, tropical, whole-sign houses).

analyse(chrt) returns the hor_tools results for a Morinus chart and caches
them on the chart, which never changes after it is created (the analysis is
redone when the planetary orbs of Tables > Aspects change).
"""

import os
import sys
import datetime

import astrology
import chart
import swe_compat

swe_compat.install()

from hor_tools import astro_engine	# noqa: E402  (needs the swisseph module installed above)
from hor_tools.models import ChartInput	# noqa: E402
from hor_tools.analysis import build_reports	# noqa: E402
from hor_tools.analysis.technical import build_natal_technical_report	# noqa: E402
from hor_tools.analysis import aspects as hor_aspects	# noqa: E402
from hor_tools.analysis import dignity as hor_dignity	# noqa: E402
from hor_tools.analysis import temperament as hor_temperament	# noqa: E402
import tradoptions	# noqa: E402
import traditional_aspects	# noqa: E402

# the program folder (in a packaged Windows build, the folder of Morinus.exe)
PROGDIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
astro_engine.set_ephe_path(os.path.join(PROGDIR, 'SWEP', 'Ephem'))


class NotAvailable(Exception):
    """The chart is outside what the hor_tools calculations support (e.g. BC dates)."""


class Analysis:
    def __init__(self, chartinput, planets, houses, reports, relationships, technical):
        self.chart = chartinput
        self.planets = planets
        self.houses = houses
        self.reports = reports
        self.relationships = relationships
        self.technical = technical


def chart_input(chrt):
    """hor_tools ChartInput for a Morinus chart, using the same time rules as hor_tools' .hor parser."""
    t, p = chrt.time, chrt.place
    if t.bc:
        raise NotAvailable('BC charts')

    if t.zt == chart.Time.ZONE:
        offset = (t.zh+t.zm/60.0)*(1.0 if t.plus else -1.0)
    elif t.zt == chart.Time.GREENWICH:
        offset = 0.0
    else:
        # local mean time; local apparent time differs by the equation of time,
        # which only shifts the local midnight used for planetary hours
        offset = p.lon/15.0
    if t.daylightsaving:
        offset += 1.0

    if t.cal == chart.Time.GREGORIAN and t.zt != chart.Time.LOCALAPPARENT:
        local = datetime.datetime(t.origyear, t.origmonth, t.origday, t.hour, t.minute, t.second)
        utc = local-datetime.timedelta(hours=offset)
    else:
        y, m, d, h = astrology.swe_revjul(t.jd, astrology.SE_GREG_CAL)
        utc = datetime.datetime(y, m, d)+datetime.timedelta(seconds=round(h*3600.0))

    return ChartInput(
        name=chrt.name,
        datetime_utc=utc.replace(tzinfo=datetime.timezone.utc),
        tz_offset_hours=offset,
        latitude=p.lat,
        longitude=p.lon,
        house_system='W',
        zodiac='T',
        location_name=p.placename,
        altitude_m=float(p.altitude),
        male=chrt.male,
        sect='day' if chrt.isDaySect() else 'night')


def planet_orbs():
    """The planetary orbs of Tables > Aspects, for hor_tools as well.

    hor_tools ships its own orb values; the course orbs (or the Custom ones)
    must apply everywhere. It already uses the larger orb of two planets and
    the full planet orb towards Lots. Legacy Morinus has no say here: these
    analyses are traditional techniques, so they keep the course orbs.
    """
    return dict(zip(traditional_aspects.PLANETS,
                    traditional_aspects.doctrinal_orbs(tradoptions.values())))


# Mean daily motions for swift and slow (Options > Planetary conditions):
# the course slide (basic lesson 5, "PROSECNE BRZINE") or the astronomical
# mean motions hor_tools ships.
COURSE_SPEEDS = {'Sun': 59.0/60.0, 'Moon': 13.0+23.0/60.0, 'Mercury': 59.0/60.0, 'Venus': 59.0/60.0,
	'Mars': 31.0/60.0, 'Jupiter': 5.0/60.0, 'Saturn': 3.0/60.0}
ASTRONOMICAL_SPEEDS = dict(hor_dignity.MEAN_SPEED)


def mean_speeds():
    return COURSE_SPEEDS if tradoptions.get('speed_means') == 'course' else ASTRONOMICAL_SPEEDS


PLANETNAMES = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon')


def almuten_figuris(chrt):
    """Morinus's Almuten Figuris (Tables > Almutens, with its options) as a
    one-element tuple of the planet name, None when tied; None when the chart
    has no almutens (not a full chart)."""
    alm = getattr(chrt, 'almutens', None)
    if alm is None:
        return None
    pl, score, tie = alm.maxscore
    return (None if tie or pl < 0 else PLANETNAMES[pl],)


def analyse(chrt):
    orbs = planet_orbs()
    speeds = mean_speeds()
    almuten = almuten_figuris(chrt)
    settings = (orbs, chrt.isDaySect(), tuple(sorted(speeds.items())), tradoptions.get('temp_orb'),
                tradoptions.get('temp_moon_orb'), almuten)
    # Updated in place: hor_tools modules hold these same objects.
    hor_aspects.PLANET_ORBS.update(orbs)
    hor_dignity.MEAN_SPEED.update(speeds)
    hor_temperament.ASC_CONTACT_ORB = tradoptions.get('temp_orb')
    hor_temperament.MOON_CONTACT_ORB = tradoptions.get('temp_moon_orb')
    cached = getattr(chrt, '_traditional', None)
    if cached is not None and getattr(chrt, '_traditional_settings', None) == settings:
        return cached
    ci = chart_input(chrt)
    planets = astro_engine.compute_planets(ci)
    houses = astro_engine.compute_houses(ci)
    reports, relationships = build_reports(ci, planets, houses)
    technical = build_natal_technical_report(ci, planets, houses, reports, relationships, almuten)
    result = Analysis(ci, planets, houses, reports, relationships, technical)
    chrt._traditional = result
    chrt._traditional_settings = settings
    return result
