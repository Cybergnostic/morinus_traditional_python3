# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math, astrology, chart, planets, mtexts, util

class RiseSet:
    """Computes Rise/Set times (for the birthday)"""
    RISE, MC, SET, IC = list(range(0, 4))
    Angles = [
     astrology.SE_CALC_RISE, astrology.SE_CALC_MTRANSIT, astrology.SE_CALC_SET, astrology.SE_CALC_ITRANSIT]

    def __init__(self, jd, cal, lon, lat, alt, pls):
        self.jd = jd
        self.cal = cal
        self.lon = lon
        self.lat = lat
        self.alt = alt
        self.calflag = astrology.SE_GREG_CAL
        if self.cal == chart.Time.JULIAN:
            self.calflag = astrology.SE_JUL_CAL
        self.times = []
        self.calcTimes()

    def calcTimes(self):
        oyear, omonth, oday, otim = astrology.swe_revjul(self.jd, self.calflag)
        for i in range(planets.Planets.PLANETS_NUM):
            ar = []
            ret, JDRise, serr = astrology.swe_rise_trans(self.jd, util.mapChaldeanToModern(i), '', astrology.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.RISE], self.lon, self.lat, self.alt, 0.0, 10.0)
            tyear, tmonth, tday, ttim = astrology.swe_revjul(JDRise, self.calflag)
            if oyear != tyear or omonth != tmonth or oday != tday:
                ret, JDRise, serr = astrology.swe_rise_trans(self.jd - 1.0, util.mapChaldeanToModern(i), '', astrology.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.RISE], self.lon, self.lat, self.alt, 0.0, 10.0)
            ret, JDMC, serr = astrology.swe_rise_trans(self.jd, util.mapChaldeanToModern(i), '', astrology.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.MC], self.lon, self.lat, self.alt, 0.0, 10.0)
            tyear, tmonth, tday, ttim = astrology.swe_revjul(JDMC, self.calflag)
            if oyear != tyear or omonth != tmonth or oday != tday:
                ret, JDMC, serr = astrology.swe_rise_trans(self.jd - 1.0, util.mapChaldeanToModern(i), '', astrology.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.MC], self.lon, self.lat, self.alt, 0.0, 10.0)
            ret, JDSet, serr = astrology.swe_rise_trans(self.jd, util.mapChaldeanToModern(i), '', astrology.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.SET], self.lon, self.lat, self.alt, 0.0, 10.0)
            tyear, tmonth, tday, ttim = astrology.swe_revjul(JDSet, self.calflag)
            if oyear != tyear or omonth != tmonth or oday != tday:
                ret, JDSet, serr = astrology.swe_rise_trans(self.jd - 1.0, util.mapChaldeanToModern(i), '', astrology.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.SET], self.lon, self.lat, self.alt, 0.0, 10.0)
            ret, JDIC, serr = astrology.swe_rise_trans(self.jd, util.mapChaldeanToModern(i), '', astrology.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.IC], self.lon, self.lat, self.alt, 0.0, 10.0)
            tyear, tmonth, tday, ttim = astrology.swe_revjul(JDIC, self.calflag)
            if oyear != tyear or omonth != tmonth or oday != tday:
                ret, JDIC, serr = astrology.swe_rise_trans(self.jd - 1.0, util.mapChaldeanToModern(i), '', astrology.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.IC], self.lon, self.lat, self.alt, 0.0, 10.0)
            year, month, day, hr = astrology.swe_revjul(JDRise, self.calflag)
            ar.append(hr)
            year, month, day, hr = astrology.swe_revjul(JDMC, self.calflag)
            ar.append(hr)
            year, month, day, hr = astrology.swe_revjul(JDSet, self.calflag)
            ar.append(hr)
            year, month, day, hr = astrology.swe_revjul(JDIC, self.calflag)
            ar.append(hr)
            self.times.append(ar)

    def printRiseSet(self, pls):
        numangles = len(RiseSet.Angles)
        txt = [mtexts.txtsriseset['Rise'], mtexts.txtsriseset['MC'], mtexts.txtsriseset['Set'], mtexts.txtsriseset['IC']]
        print('')
        print('Rise/Set times:')
        for i in range(planets.Planets.PLANETS_NUM):
            for angle in range(numangles):
                h, m, s = util.decToDeg(self.times[i][angle])
                print('%s: %s: %02d:%02d:%02d' % (pls.planets[i].name, txt[angle], h, m, s))