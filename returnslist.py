"""The lunar returns covering one solar year (birthday to birthday): the lunar
return in force when the solar return happens, every lunar return beginning
during the year, the last of which is in force when the year ends. Returns are
cast for the place of birth.
"""

import chart
import planets
import transits
import revolutions
import util

SOLAR_RETURN = 'Solar return'
IN_FORCE = 'in force at the start of the solar year'
AT_END = 'in force at the end of the solar year'


class Return:
    def __init__(self, kind, t, chrt, note=''):
        self.kind = kind	# 'Solar return' or 'Lunar return'
        self.t = t	# (year, month, day, hour, minute, second) UT
        self.chart = chrt
        self.note = note

    @property
    def jd(self):
        return self.chart.time.jd


def gmt_time(t, radix):
    return chart.Time(t[0], t[1], t[2], t[3], t[4], t[5], False, radix.time.cal, chart.Time.GREENWICH, True, 0, 0, False, radix.place, False)


def return_chart(t, radix, htype, place=None):
    place = place or radix.place
    time = chart.Time(t[0], t[1], t[2], t[3], t[4], t[5], False, radix.time.cal, chart.Time.GREENWICH, True, 0, 0, False, place)
    return chart.Chart(radix.name, radix.male, time, place, htype, '', radix.options, False)


# Set by the main window to its sidereal correction of solar returns
# (MFrame.calcPrecNutCorrectedSolar), so these returns match Charts > Revolutions.
sidereal_solar_correction = None


def solar_return(radix, year):
    """UT time tuple of the solar return in the given year, or None."""
    revs = revolutions.Revolutions()
    if not revs.compute(revolutions.Revolutions.SUN, year, radix.time.month, radix.time.day, radix):
        return None
    if radix.options.ayanamsha != 0 and sidereal_solar_correction is not None:
        return tuple(sidereal_solar_correction(revs))
    return tuple(revs.t)


def step_return(radix, current, forward):
    """The next (or previous) return of the same kind as the chart `current`,
    cast for the same place; None if it cannot be found."""
    if current.htype == chart.Chart.SOLAR:
        year = current.time.year+(1 if forward else -1)
        t = solar_return(radix, year)
        return return_chart(t, radix, chart.Chart.SOLAR, current.place) if t else None
    jd = current.time.jd
    y, m = current.time.year, current.time.month
    found = []
    for i in range(3):
        found += _month_returns(y, m, radix, planets.Planets.MOON)
        y, m = util.incrMonth(y, m) if forward else util.decrMonth(y, m)
    found.sort()
    if forward:
        later = [f for f in found if f[0] > jd+1.0]
        hit = later[0] if later else None
    else:
        earlier = [f for f in found if f[0] < jd-1.0]
        hit = earlier[-1] if earlier else None
    return return_chart(hit[1], radix, chart.Chart.LUNAR, current.place) if hit else None


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


def compute(radix, year):
    """The solar return in `year` and the lunar returns covering that solar year."""
    sr_t = solar_return(radix, year)
    next_t = solar_return(radix, year+1)
    if sr_t is None or next_t is None:
        return []
    sr = Return(SOLAR_RETURN, sr_t, return_chart(sr_t, radix, chart.Chart.SOLAR))
    next_jd = gmt_time(next_t, radix).jd
    rows = [sr]
    before, within = lunar_returns(radix, sr.jd, next_jd, sr_t)
    for jd, t in before:
        rows.append(Return('Lunar return', t, return_chart(t, radix, chart.Chart.LUNAR), IN_FORCE))
    for jd, t in within:
        rows.append(Return('Lunar return', t, return_chart(t, radix, chart.Chart.LUNAR)))
    if within:
        rows[-1].note = AT_END
    return rows


def sign_house(lon, asc):
    """Whole-sign house of a longitude counted from an Ascendant."""
    return (int(lon // 30)-int(asc // 30)) % 12+1
