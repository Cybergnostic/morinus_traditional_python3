# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import astrology
import chart
import util

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
            # The planetary day begins at this sunrise: its ruler is the ruler of
            # the local date of the sunrise (the entered date can be another day).
            self.weekday = PlanetaryHours.localWeekday(self.risetime, self.weekday)
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
            # The night belongs to the day that ended with this sunset. (Morinus
            # 6.2 took the weekday of the entered date and went back a day after
            # local mean midnight, which was wrong when the zone time and the
            # local mean time fell on different dates.)
            if jd + offs > int(jd + offs) + 0.5:
                fallback = util.getPrevDay(self.weekday)
            else:
                fallback = self.weekday
            self.weekday = PlanetaryHours.localWeekday(self.settime, fallback)
            self.hrlen = (self.risetime - self.settime) / HOURSPERHALFDAY
            for i in range(int(HOURSPERHALFDAY)):
                if jd + offs < self.settime + self.hrlen * (i + 1):
                    hr = i + int(HOURSPERHALFDAY)
                    break

        self.planetaryhour = PlanetaryHours.PHs[self.weekday][hr]
        return

    @staticmethod
    def localWeekday(localjd, fallback):
        """Weekday (Monday 0, as datetime.weekday) of a Julian day already shifted
        to local mean time; fallback when the Sun did not rise or set (polar day
        or night) and the time is not valid."""
        # swe_rise_trans gives 0.0 when there is no rise or set; with the
        # longitude offset added it stays below 1.0
        if localjd is None or localjd < 1.0:
            return fallback
        return int(localjd + 0.5) % 7

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