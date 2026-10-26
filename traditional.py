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
        male=chrt.male)


def planet_orbs():
    """The planetary orbs of Tables > Aspects, for hor_tools as well.

    hor_tools ships its own orb values; the course orbs (or the Custom ones)
    must apply everywhere. It already uses the larger orb of two planets and
    the full planet orb towards Lots. Legacy Morinus has no say here: these
    analyses are traditional techniques, so they keep the course orbs.
    """
    return dict(zip(traditional_aspects.PLANETS,
                    traditional_aspects.doctrinal_orbs(tradoptions.values())))


def analyse(chrt):
    orbs = planet_orbs()
    # Updated in place: hor_tools modules hold this same dict object.
    hor_aspects.PLANET_ORBS.update(orbs)
    cached = getattr(chrt, '_traditional', None)
    if cached is not None and getattr(chrt, '_traditional_orbs', None) == orbs:
        return cached
    ci = chart_input(chrt)
    planets = astro_engine.compute_planets(ci)
    houses = astro_engine.compute_houses(ci)
    reports, relationships = build_reports(ci, planets, houses)
    technical = build_natal_technical_report(ci, planets, houses, reports, relationships)
    result = Analysis(ci, planets, houses, reports, relationships, technical)
    chrt._traditional = result
    chrt._traditional_orbs = orbs
    return result
