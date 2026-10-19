# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math, wx, astrology, chart, planets, rangechecker, findtimedlg, util

class FindTime:
    NONE = -1
    HOUR = 0
    MINUTE = 1
    SECOND = 2
    OVER = 3
    CIRCLE = 360.0
    OFFSET = 20.0
    YEAR, MONTH, DAY, TIME, JD = list(range(5))

    def __init__(self, bc, ftdata, ftdatause, ftdataascmc, ftdataapprox, abort, win):
        self.bc = bc
        self.ftdata = ftdata
        self.ftdatause = ftdatause
        self.ftdataascmc = ftdataascmc
        self.ftdataapprox = ftdataapprox
        self.abort = abort
        self.win = win
        self.flags = astrology.SEFLG_SPEED + astrology.SEFLG_SWIEPH

    def find(self):
        rnge = 3000
        checker = rangechecker.RangeChecker()
        if checker.isExtended():
            rnge = 5000
        y = 1973
        m = 3
        d = 21
        for i in range(int(self.ftdata[planets.Planets.SUN][findtimedlg.FindTimeDlg.LON])):
            y, m, d = util.incrDay(y, m, d)

        tim = chart.Time(y, m, d, 0, 0, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
        tmpSun = planets.Planet(tim.jd, planets.Planets.SUN, self.flags)
        lonSun = tmpSun.data[planets.Planet.LON]
        lontofind = self.ftdata[planets.Planets.SUN][findtimedlg.FindTimeDlg.LON]
        if lonSun > FindTime.CIRCLE - FindTime.OFFSET and lontofind < FindTime.OFFSET:
            lontofind += FindTime.CIRCLE
        if lontofind > FindTime.CIRCLE - FindTime.OFFSET and lonSun < FindTime.OFFSET:
            lonSun += FindTime.CIRCLE
        diff = int(math.fabs(int(lonSun) - int(lontofind)))
        if int(self.ftdata[planets.Planets.SUN][findtimedlg.FindTimeDlg.LON]) < int(lonSun):
            for i in range(diff):
                y, m, d = util.decrDay(y, m, d)

        else:
            for i in range(diff):
                y, m, d = util.incrDay(y, m, d)

        ybeg, mbeg, dbeg = y, m, d
        yend, mend, dend = y, m, d
        DATEOFFS = 7
        for i in range(DATEOFFS):
            ybeg, mbeg, dbeg = util.decrDay(ybeg, mbeg, dbeg)
            yend, mend, dend = util.incrDay(yend, mend, dend)

        tfnd = (1, 1, 1, 1.0, 1.0)
        y = 1
        m = mbeg
        d = dbeg
        while y < rnge:
            if self.abort.abort:
                return
            fnd = self.day(y, m, d, planets.Planets.SUN, self.ftdata[planets.Planets.SUN][findtimedlg.FindTimeDlg.LON])
            if fnd != None:
                found = True
                for i in range(planets.Planets.PLANETS_NUM):
                    if i != planets.Planets.SUN:
                        tfnd = self.day(y, m, d, i, self.ftdata[i][findtimedlg.FindTimeDlg.LON])
                        if tfnd == None:
                            found = False
                            break

                if found:
                    evt = findtimedlg.FTDataReadyEvent(attr1=tfnd)
                    wx.PostEvent(self.win, evt)
            yt = y
            if m == mend and d == dend:
                y += 1
                m = mbeg
                d = dbeg
            else:
                y, m, d = util.incrDay(y, m, d)
            if yt != y and yt % 50 == 0:
                evt = findtimedlg.FTYearEvent(attr1=yt)
                wx.PostEvent(self.win, evt)

        return

    def day(self, year, month, day, planet, pos):
        y, m, d = util.incrDay(year, month, day)
        time1 = chart.Time(year, month, day, 0, 0, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
        time2 = chart.Time(y, m, d, 0, 0, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
        return self.cycleplanet(time1, time2, planet, pos)

    def cycleplanet(self, time1, time2, planet, pos):
        planet1 = planets.Planet(time1.jd, planet, self.flags)
        planet2 = planets.Planet(time2.jd, planet, self.flags)
        if self.check(planet1, planet2, pos):
            return self.get(planet1, planet2, time1, pos, planet, FindTime.HOUR)
        return None

    def get(self, planet1, planet2, time1, lon, pl, unit):
        if self.check(planet1, planet2, lon):
            fr = 0
            to = 60
            if unit == FindTime.HOUR:
                fr = 0
                to = 24
            for val in range(fr, to):
                time = None
                if unit == FindTime.HOUR:
                    time1 = chart.Time(int(math.fabs(time1.year)), time1.month, time1.day, val, 0, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
                    time2 = None
                    if val + 1 < to:
                        time2 = chart.Time(int(math.fabs(time1.year)), time1.month, time1.day, val + 1, 0, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
                    else:
                        y, m, d = util.incrDay(int(math.fabs(time1.year)), time1.month, time1.day)
                        time2 = chart.Time(y, m, d, 0, 0, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
                elif unit == FindTime.MINUTE:
                    time1 = chart.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour, val, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
                    time2 = None
                    if val + 1 < to:
                        time2 = chart.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour, val + 1, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
                    elif time1.hour + 1 < 24:
                        time2 = chart.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour + 1, 0, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
                    else:
                        y, m, d = util.incrDay(int(math.fabs(time1.year)), time1.month, time1.day)
                        time2 = chart.Time(y, m, d, 0, 0, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
                elif unit == FindTime.SECOND:
                    time1 = chart.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour, time1.minute, val, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
                    time2 = None
                    if val + 1 < to:
                        time2 = chart.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour, time1.minute, val + 1, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
                    elif time1.minute + 1 < 60:
                        time2 = chart.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour, time1.minute + 1, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
                    elif time1.hour + 1 < 24:
                        time2 = chart.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour + 1, 0, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
                    else:
                        y, m, d = util.incrDay(int(math.fabs(time1.year)), time1.month, time1.day)
                        time2 = chart.Time(y, m, d, 0, 0, 0, self.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
                else:
                    return
                planet1 = planets.Planet(time1.jd, pl, self.flags)
                planet2 = planets.Planet(time2.jd, pl, self.flags)
                if self.check(planet1, planet2, lon):
                    un = FindTime.OVER
                    if unit == FindTime.HOUR:
                        un = FindTime.MINUTE
                    if unit == FindTime.MINUTE:
                        un = FindTime.SECOND
                    if un != FindTime.OVER:
                        return self.get(planet1, planet2, time1, lon, pl, un)
                    if self.ftdatause[findtimedlg.FindTimeDlg.RET]:
                        if planet1.data[planets.Planet.SPLON] <= 0.0 and self.ftdata[pl][findtimedlg.FindTimeDlg.RETR] or planet1.data[planets.Planet.SPLON] > 0.0 and not self.ftdata[pl][findtimedlg.FindTimeDlg.RETR]:
                            return (int(math.fabs(time1.year)), time1.month, time1.day, time1.time, time1.jd)
                        return
                    return (
                     int(math.fabs(time1.year)), time1.month, time1.day, time1.time, time1.jd)

        return

    def check(self, planet1, planet2, lon):
        y1, m1, s1 = util.decToDeg(planet1.data[planets.Planet.LON])
        y2, m2, s2 = util.decToDeg(planet2.data[planets.Planet.LON])
        if self.ftdataapprox[findtimedlg.FindTimeDlg.USEAPPROX] and (self.ftdataapprox[findtimedlg.FindTimeDlg.APPROXDEG] != 0 or self.ftdataapprox[findtimedlg.FindTimeDlg.APPROXMIN] != 0 or self.ftdataapprox[findtimedlg.FindTimeDlg.APPROXSEC] != 0):
            lon1 = float(y1) + float(m1) / 60.0 + float(s1) / 3600.0
            lon2 = float(y2) + float(m2) / 60.0 + float(s2) / 3600.0
            if lon2 < lon1:
                tlon = lon1
                lon1 = lon2
                lon2 = tlon
            approxval = self.ftdataapprox[findtimedlg.FindTimeDlg.APPROXDEG] + self.ftdataapprox[findtimedlg.FindTimeDlg.APPROXMIN] / 60.0 + self.ftdataapprox[findtimedlg.FindTimeDlg.APPROXSEC] / 3600.0
            lona = util.normalize(lon - approxval)
            lonb = util.normalize(lon + approxval)
            if lonb < lona:
                tlon = lona
                lona = lonb
                lonb = tlon
            if lon2 > FindTime.CIRCLE - FindTime.OFFSET and lon1 < FindTime.OFFSET and lonb > FindTime.CIRCLE - FindTime.OFFSET and lona < FindTime.OFFSET:
                return True
            if lon2 > FindTime.CIRCLE - FindTime.OFFSET and lon1 < FindTime.OFFSET and lonb > FindTime.CIRCLE - FindTime.OFFSET and lona > FindTime.CIRCLE - FindTime.OFFSET:
                if lon2 <= lona:
                    return True
                return False
            if lonb > FindTime.CIRCLE - FindTime.OFFSET and lona < FindTime.OFFSET and lon2 > FindTime.CIRCLE - FindTime.OFFSET and lon1 > FindTime.CIRCLE - FindTime.OFFSET:
                if lonb <= lon1:
                    return True
                return False
            if lonb < FindTime.OFFSET and lona < FindTime.OFFSET and lon2 > FindTime.CIRCLE - FindTime.OFFSET and lon1 < FindTime.OFFSET:
                if lonb <= lon1:
                    return True
                return False
            if lonb > FindTime.CIRCLE - FindTime.OFFSET and lona < FindTime.OFFSET and lon2 < FindTime.OFFSET and lon1 < FindTime.OFFSET:
                if lon2 <= lona:
                    return True
                return False
            if lonb > FindTime.CIRCLE - FindTime.OFFSET and lona < FindTime.OFFSET and lon2 > FindTime.OFFSET and lon2 < FindTime.CIRCLE - FindTime.OFFSET and lon1 > FindTime.OFFSET and lon1 < FindTime.CIRCLE - FindTime.OFFSET or lon2 > FindTime.CIRCLE - FindTime.OFFSET and lon1 < FindTime.OFFSET and lonb > FindTime.OFFSET and lonb < FindTime.CIRCLE - FindTime.OFFSET and lona > FindTime.OFFSET and lona < FindTime.CIRCLE - FindTime.OFFSET:
                return False
            if lon1 <= lona and lon2 >= lona or lona <= lon1 and lonb >= lon1:
                return True
        else:
            lon1 = lon2 = 0.0
            if self.ftdatause[findtimedlg.FindTimeDlg.MIN] and self.ftdatause[findtimedlg.FindTimeDlg.SEC]:
                lon1 = float(y1) + float(m1) / 60.0 + float(s1) / 3600.0
                lon2 = float(y2) + float(m2) / 60.0 + float(s2) / 3600.0
            else:
                if not self.ftdatause[findtimedlg.FindTimeDlg.SEC]:
                    lon1 = float(y1) + float(m1) / 60.0
                    lon2 = float(y2) + float(m2) / 60.0
                if not self.ftdatause[findtimedlg.FindTimeDlg.MIN]:
                    lon1 = float(y1)
                    lon2 = float(y2)
            if lon2 < lon1:
                tlon = lon1
                lon1 = lon2
                lon2 = tlon
            if lon2 > FindTime.CIRCLE - FindTime.OFFSET and lon1 < FindTime.OFFSET:
                if lon2 <= lon or lon1 > lon:
                    return True
                return False
            if lon1 <= lon and lon2 >= lon:
                return True
        return False