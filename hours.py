# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import astrology, chart, util

class PlanetaryHours:
    PHs = (
     (6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1),
     (2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4),
     (5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0),
     (1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3),
     (4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6),
     (0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2),
     (3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5))

    def __init__(self, lon, lat, altitude, weekday, jd):
        self.risetime = None
        self.settime = None
        self.hrlen = None
        self.daytime = None
        self.weekday = weekday
        ret, risetime, serr = astrology.swe_rise_trans(jd, astrology.SE_SUN, '', astrology.SEFLG_SWIEPH, astrology.SE_CALC_RISE, lon, lat, float(altitude), 0.0, 10.0)
        ret, settime, serr = astrology.swe_rise_trans(jd, astrology.SE_SUN, '', astrology.SEFLG_SWIEPH, astrology.SE_CALC_SET, lon, lat, float(altitude), 0.0, 10.0)
        offs = lon * 4.0 / 1440.0
        hr = 0
        HOURSPERHALFDAY = 12.0
        if risetime > settime:
            self.daytime = True
            ret, self.risetime, serr = astrology.swe_rise_trans(jd - 1.0, astrology.SE_SUN, '', astrology.SEFLG_SWIEPH, astrology.SE_CALC_RISE, lon, lat, float(altitude), 0.0, 10.0)
            ret, self.settime, serr = astrology.swe_rise_trans(jd, astrology.SE_SUN, '', astrology.SEFLG_SWIEPH, astrology.SE_CALC_SET, lon, lat, float(altitude), 0.0, 10.0)
            self.risetime += offs
            self.settime += offs
            self.hrlen = (self.settime - self.risetime) / HOURSPERHALFDAY
            for i in range(int(HOURSPERHALFDAY)):
                if jd + offs < self.risetime + self.hrlen * (i + 1):
                    hr = i
                    break

        else:
            self.daytime = False
            ret, self.risetime, serr = astrology.swe_rise_trans(jd, astrology.SE_SUN, '', astrology.SEFLG_SWIEPH, astrology.SE_CALC_RISE, lon, lat, float(altitude), 0.0, 10.0)
            ret, self.settime, serr = astrology.swe_rise_trans(jd - 1.0, astrology.SE_SUN, '', astrology.SEFLG_SWIEPH, astrology.SE_CALC_SET, lon, lat, float(altitude), 0.0, 10.0)
            self.risetime += offs
            self.settime += offs
            if jd + offs > int(jd + offs) + 0.5:
                self.weekday = util.getPrevDay(self.weekday)
            self.hrlen = (self.risetime - self.settime) / HOURSPERHALFDAY
            for i in range(int(HOURSPERHALFDAY)):
                if jd + offs < self.settime + self.hrlen * (i + 1):
                    hr = i + int(HOURSPERHALFDAY)
                    break

        self.planetaryhour = PlanetaryHours.PHs[self.weekday][hr]
        return

    def revTime(self, tjd, cal):
        calflag = astrology.SE_GREG_CAL
        if cal == chart.Time.JULIAN:
            calflag = astrology.SE_JUL_CAL
        jy, jm, jd, jh = astrology.swe_revjul(tjd, calflag)
        d, m, s = util.decToDeg(jh)
        return (d, m, s)

    def logCalc(self, tjd):
        jy, jm, jd, jh = astrology.swe_revjul(tjd, 1)
        d, m, s = util.decToDeg(jh)
        print('GMT: %d.%d.%d %d:%d:%d' % (jy, jm, jd, d, m, s))

    def printDayHour(self):
        pls = ('Saturnus', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon')
        print('')
        print('Planetary Day and Hour:')
        print('Day: %s Hour: %s' % (pls[PlanetaryHours.PHs[self.weekday][0]], pls[self.planetaryhour]))