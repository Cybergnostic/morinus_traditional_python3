"""Traditional-astrology analysis of Morinus charts with the vendored hor_tools
package (its rules: Sun..Saturn, tropical, whole-sign houses).

analyse(chrt) returns the hor_tools results for a Morinus chart and caches
them on the chart, which never changes after it is created.
"""

import os
import datetime

import astrology
import chart
import swe_compat

swe_compat.install()

from hor_tools import astro_engine	# noqa: E402  (needs the swisseph module installed above)
from hor_tools.models import ChartInput	# noqa: E402
from hor_tools.analysis import build_reports	# noqa: E402
from hor_tools.analysis.technical import build_natal_technical_report	# noqa: E402

astro_engine.set_ephe_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SWEP', 'Ephem'))


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


def analyse(chrt):
    cached = getattr(chrt, '_traditional', None)
    if cached is not None:
        return cached
    ci = chart_input(chrt)
    planets = astro_engine.compute_planets(ci)
    houses = astro_engine.compute_houses(ci)
    reports, relationships = build_reports(ci, planets, houses)
    technical = build_natal_technical_report(ci, planets, houses, reports, relationships)
    result = Analysis(ci, planets, houses, reports, relationships, technical)
    chrt._traditional = result
    return result
