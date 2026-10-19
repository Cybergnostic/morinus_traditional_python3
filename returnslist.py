"""Returns within one solar year: the lunar returns (12 or 13, plus the one in
force when the solar year begins) or the monthly solar returns (the Sun on the
natal degree of each following sign), as they are used to narrow the
year down. Returns are cast for the place of birth.
"""

import chart
import planets
import transits
import revolutions
import util

LUNAR, MONTHLYSOLAR = list(range(2))

SOLAR_RETURN = 'Solar return'
IN_FORCE = 'in force at the solar return'


class Return:
    def __init__(self, kind, t, chrt, note=''):
        self.kind = kind	# 'Solar return', 'Lunar return' or 'Monthly solar return'
        self.t = t	# (year, month, day, hour, minute, second) UT
        self.chart = chrt
        self.note = note

    @property
    def jd(self):
        return self.chart.time.jd


def gmt_time(t, radix):
    return chart.Time(t[0], t[1], t[2], t[3], t[4], t[5], False, radix.time.cal, chart.Time.GREENWICH, True, 0, 0, False, radix.place, False)


def return_chart(t, radix, htype):
    time = chart.Time(t[0], t[1], t[2], t[3], t[4], t[5], False, radix.time.cal, chart.Time.GREENWICH, True, 0, 0, False, radix.place)
    return chart.Chart(radix.name, radix.male, time, radix.place, htype, '', radix.options, False)


def solar_return(radix, year):
    """UT time tuple of the solar return in the given year, or None."""
    revs = revolutions.Revolutions()
    if not revs.compute(revolutions.Revolutions.SUN, year, radix.time.month, radix.time.day, radix):
        return None
    return tuple(revs.t)


def _month_returns(year, month, radix, planet, pos=None):
    trans = transits.Transits()
    trans.month(year, month, radix, planet, pos)
    out = []
    for tr in trans.transits:
        h, m, s = util.decToDeg(tr.time)
        t = (year, month, tr.day, h, m, s)
        out.append((gmt_time(t, radix).jd, t))
    return out


def lunar_returns(radix, sr_jd, next_jd, sr_t):
    """The lunar return in force at sr_jd and all lunar returns before next_jd."""
    y, m = util.decrMonth(sr_t[0], sr_t[1])
    found = []
    for i in range(15):
        found += _month_returns(y, m, radix, planets.Planets.MOON)
        y, m = util.incrMonth(y, m)
    found.sort()
    before = [f for f in found if f[0] <= sr_jd]
    within = [f for f in found if sr_jd < f[0] < next_jd]
    return before[-1:], within


def monthly_solar_returns(radix, sr_t):
    """The Sun on the natal degree of each of the 11 signs after the solar return."""
    natal = radix.planets.planets[planets.Planets.SUN].data[planets.Planet.LON]
    out = []
    y, m = sr_t[0], sr_t[1]
    for k in range(1, 12):
        target = (natal+30.0*k) % 360.0
        for i in range(3):
            hits = _month_returns(y, m, radix, planets.Planets.SUN, target)
            if hits:
                out.append(hits[0])
                break
            y, m = util.incrMonth(y, m)
    return out


def compute(radix, year, kind):
    """Returns of the solar year beginning with the solar return in `year`."""
    sr_t = solar_return(radix, year)
    next_t = solar_return(radix, year+1)
    if sr_t is None or next_t is None:
        return []
    sr = Return(SOLAR_RETURN, sr_t, return_chart(sr_t, radix, chart.Chart.SOLAR))
    next_jd = gmt_time(next_t, radix).jd
    rows = [sr]
    if kind == LUNAR:
        before, within = lunar_returns(radix, sr.jd, next_jd, sr_t)
        for jd, t in before:
            rows.append(Return('Lunar return', t, return_chart(t, radix, chart.Chart.LUNAR), IN_FORCE))
        for jd, t in within:
            rows.append(Return('Lunar return', t, return_chart(t, radix, chart.Chart.LUNAR)))
    else:
        for jd, t in monthly_solar_returns(radix, sr_t):
            if jd < next_jd:
                rows.append(Return('Monthly solar return', t, return_chart(t, radix, chart.Chart.SOLAR)))
    return rows


def sign_house(lon, asc):
    """Whole-sign house of a longitude counted from an Ascendant."""
    return (int(lon // 30)-int(asc // 30)) % 12+1
