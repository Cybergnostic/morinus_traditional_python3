# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import astrology, chart, fortune, planets, util

class Transit:
    NONE = -1
    RETR = 0
    STAT = 1
    ASC = 0
    MC = 1
    ASCMC = 2
    PLANET = 3
    SIGN = 4
    ANTISCION = 5
    CONTRAANTISCION = 6
    LOF = 7

    def __init__(self):
        self.plt = chart.Chart.NONE
        self.pltretr = Transit.NONE
        self.obj = chart.Chart.NONE
        self.objretr = Transit.NONE
        self.objtype = chart.Chart.NONE
        self.aspect = chart.Chart.NONE
        self.house = chart.Chart.NONE
        self.day = chart.Chart.NONE
        self.time = 0.0


class Transits:
    NONE = -1
    HOUR = 0
    MINUTE = 1
    SECOND = 2
    OVER = 3
    CIRCLE = 360.0
    OFFSET = 20.0

    def __init__(self):
        self.transits = []
        self.flags = Transits.NONE

    def month(self, year, month, chrt, planet=-1, pos=None):
        self.flags = astrology.SEFLG_SPEED + astrology.SEFLG_SWIEPH
        if chrt.options.topocentric:
            self.flags += astrology.SEFLG_TOPOCTR
        lastday = 1
        for day in range(1, 31):
            valid = util.checkDate(year, month, day)
            if valid:
                lastday = day
                valid = util.checkDate(year, month, day + 1)
                if valid:
                    lastday = day + 1
                    self.day(year, month, day, chrt, planet, pos)
                else:
                    break
            else:
                break

        time1 = chart.Time(year, month, lastday, 0, 0, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
        year, month = util.incrMonth(year, month)
        time2 = chart.Time(year, month, 1, 0, 0, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
        cnt = len(self.transits)
        if planet == Transits.NONE:
            self.cycle(time1, chrt, time2)
        else:
            self.cycleplanet(time1, chrt, time2, planet, pos)
        self.order(cnt)

    def day(self, year, month, day, chrt, planet=-1, pos=None):
        if self.flags == Transits.NONE:
            self.flags = astrology.SEFLG_SPEED + astrology.SEFLG_SWIEPH
            if chrt.options.topocentric:
                self.flags += astrology.SEFLG_TOPOCTR
        time1 = chart.Time(year, month, day, 0, 0, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
        time2 = chart.Time(year, month, day + 1, 0, 0, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
        cnt = len(self.transits)
        if planet == Transits.NONE:
            self.cycle(time1, chrt, time2)
        else:
            self.cycleplanet(time1, chrt, time2, planet, pos)
        self.order(cnt)

    def order(self, cnt):
        if len(self.transits) > cnt + 1:
            beg = cnt
            for cyc in range(len(self.transits) - beg + 1):
                for i in range(beg, len(self.transits) - 1):
                    if self.transits[i].time > self.transits[(i + 1)].time:
                        tr = self.transits[i]
                        self.transits[i] = self.transits[(i + 1)]
                        self.transits[i + 1] = tr

    def cycle(self, time1, chrt, time2):
        for j in range(planets.Planets.PLANETS_NUM):
            if j == planets.Planets.MOON:
                continue
            planet1 = planets.Planet(time1.jd, j, self.flags)
            planet2 = planets.Planet(time2.jd, j, self.flags)
            for a in range(len(chart.Chart.Aspects)):
                for l in range(2):
                    if l == 1 and (a == chart.Chart.CONIUNCTIO or a == chart.Chart.OPPOSITIO):
                        continue
                    for k in range(planets.Planets.PLANETS_NUM):
                        lon = chrt.planets.planets[k].data[planets.Planet.LON]
                        if l == 0:
                            lon += chart.Chart.Aspects[a]
                            if lon > 360.0:
                                lon -= 360.0
                        else:
                            lon -= chart.Chart.Aspects[a]
                            if lon < 0.0:
                                lon += 360.0
                        tr = self.get(planet1, planet2, time1, chrt, lon, j, k, a, Transits.HOUR, Transit.PLANET)
                        if tr != None:
                            self.transits.append(tr)

                    for h in range(2):
                        lon = chrt.houses.ascmc[h]
                        if l == 0:
                            lon += chart.Chart.Aspects[a]
                            if lon > 360.0:
                                lon -= 360.0
                        else:
                            lon -= chart.Chart.Aspects[a]
                            if lon < 0.0:
                                lon += 360.0
                        tr = self.get(planet1, planet2, time1, chrt, lon, j, h, a, Transits.HOUR, Transit.ASCMC)
                        if tr != None:
                            self.transits.append(tr)

            signs = [
             0.0, 30.0, 60.0, 90.0, 120.0, 150.0, 180.0, 210.0, 240.0, 270.0, 300.0, 330.0]
            for s in range(len(signs)):
                lona = signs[s]
                if chrt.options.ayanamsha != 0:
                    lona += chrt.ayanamsha
                    lona = util.normalize(lona)
                tr = self.get(planet1, planet2, time1, chrt, lona, j, 0, 0, Transits.HOUR, Transit.SIGN)
                if tr != None:
                    self.transits.append(tr)

            for p in range(planets.Planets.PLANETS_NUM):
                lona = chrt.antiscia.plantiscia[p].lon
                tr = self.get(planet1, planet2, time1, chrt, lona, j, p, chart.Chart.CONIUNCTIO, Transits.HOUR, Transit.ANTISCION)
                if tr != None:
                    self.transits.append(tr)

            for p in range(planets.Planets.PLANETS_NUM):
                lona = chrt.antiscia.plcontraant[p].lon
                tr = self.get(planet1, planet2, time1, chrt, lona, j, p, chart.Chart.CONIUNCTIO, Transits.HOUR, Transit.CONTRAANTISCION)
                if tr != None:
                    self.transits.append(tr)

            tr = self.get(planet1, planet2, time1, chrt, chrt.fortune.fortune[fortune.Fortune.LON], j, 0, 0, Transits.HOUR, Transit.LOF)
            if tr != None:
                self.transits.append(tr)

        return

    def cycleplanet(self, time1, chrt, time2, planet, pos):
        planet1 = planets.Planet(time1.jd, planet, self.flags)
        planet2 = planets.Planet(time2.jd, planet, self.flags)
        lon = chrt.planets.planets[planet].data[planets.Planet.LON]
        if planet != Transits.NONE and pos != None:
            lon = pos
        tr = self.get(planet1, planet2, time1, chrt, lon, planet, planet, chart.Chart.CONIUNCTIO, Transits.HOUR, Transit.PLANET)
        if tr != None:
            self.transits.append(tr)
        return

    def get(self, planet1, planet2, time1, chrt, lon, j, k, a, unit, typ):
        if self.check(planet1, planet2, lon):
            fr = 0
            to = 60
            if unit == Transits.HOUR:
                fr = 0
                to = 24
            for val in range(fr, to):
                time = None
                if unit == Transits.HOUR:
                    time1 = chart.Time(time1.year, time1.month, time1.day, val, 0, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
                    time2 = None
                    if val + 1 < to:
                        time2 = chart.Time(time1.year, time1.month, time1.day, val + 1, 0, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
                    else:
                        y, m, d = util.incrDay(time1.year, time1.month, time1.day)
                        time2 = chart.Time(y, m, d, 0, 0, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
                elif unit == Transits.MINUTE:
                    time1 = chart.Time(time1.year, time1.month, time1.day, time1.hour, val, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
                    time2 = None
                    if val + 1 < to:
                        time2 = chart.Time(time1.year, time1.month, time1.day, time1.hour, val + 1, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
                    elif time1.hour + 1 < 24:
                        time2 = chart.Time(time1.year, time1.month, time1.day, time1.hour + 1, 0, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
                    else:
                        y, m, d = util.incrDay(time1.year, time1.month, time1.day)
                        time2 = chart.Time(y, m, d, 0, 0, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
                elif unit == Transits.SECOND:
                    time1 = chart.Time(time1.year, time1.month, time1.day, time1.hour, time1.minute, val, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
                    time2 = None
                    if val + 1 < to:
                        time2 = chart.Time(time1.year, time1.month, time1.day, time1.hour, time1.minute, val + 1, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
                    elif time1.minute + 1 < 60:
                        time2 = chart.Time(time1.year, time1.month, time1.day, time1.hour, time1.minute + 1, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
                    elif time1.hour + 1 < 24:
                        time2 = chart.Time(time1.year, time1.month, time1.day, time1.hour + 1, 0, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
                    else:
                        y, m, d = util.incrDay(time1.year, time1.month, time1.day)
                        time2 = chart.Time(y, m, d, 0, 0, 0, False, chrt.time.cal, chart.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
                else:
                    return
                planet1 = planets.Planet(time1.jd, j, self.flags)
                planet2 = planets.Planet(time2.jd, j, self.flags)
                if self.check(planet1, planet2, lon):
                    un = Transits.OVER
                    if unit == Transits.HOUR:
                        un = Transits.MINUTE
                    if unit == Transits.MINUTE:
                        un = Transits.SECOND
                    if un != Transits.OVER:
                        return self.get(planet1, planet2, time1, chrt, lon, j, k, a, un, typ)
                    tr = Transit()
                    tr.plt = j
                    tr.objtype = typ
                    if typ == Transit.SIGN:
                        tr.obj = int(lon / chart.Chart.SIGN_DEG)
                    else:
                        tr.obj = k
                    if planet1.data[planets.Planet.DIST] < 0.0:
                        tr.pltretr = Transit.RETR
                    elif planet1.data[planets.Planet.DIST] == 0.0:
                        tr.pltretr = Transit.STAT
                    if typ == Transit.PLANET:
                        if chrt.planets.planets[k].data[planets.Planet.SPLON] < 0.0:
                            tr.objretr = Transit.RETR
                        elif chrt.planets.planets[k].data[planets.Planet.SPLON] == 0.0:
                            tr.objretr = Transit.STAT
                    if typ != Transit.SIGN:
                        tr.aspect = a
                    tr.house = chrt.houses.getHousePos(planet1.data[planets.Planet.LON], chrt.options)
                    tr.day = time1.day
                    tr.time = time1.time
                    return tr

        return

    def check(self, planet1, planet2, lon):
        if planet1.data[planets.Planet.LON] > Transits.CIRCLE - Transits.OFFSET and planet2.data[planets.Planet.LON] < Transits.OFFSET or planet2.data[planets.Planet.LON] > Transits.CIRCLE - Transits.OFFSET and planet1.data[planets.Planet.LON] < Transits.OFFSET:
            if planet1.data[planets.Planet.LON] > Transits.CIRCLE - Transits.OFFSET and planet2.data[planets.Planet.LON] < Transits.OFFSET:
                if planet1.data[planets.Planet.LON] <= lon or planet2.data[planets.Planet.LON] > lon:
                    return True
            if planet2.data[planets.Planet.LON] > Transits.CIRCLE - Transits.OFFSET and planet1.data[planets.Planet.LON] < Transits.OFFSET:
                if planet2.data[planets.Planet.LON] <= lon or planet1.data[planets.Planet.LON] > lon:
                    return True
            return False
        if planet1.data[planets.Planet.LON] <= lon and planet2.data[planets.Planet.LON] > lon or planet2.data[planets.Planet.LON] <= lon and planet1.data[planets.Planet.LON] > lon:
            return True
        return False

    def printTransits(self, ls):
        planets = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon',
                   'ANode', 'DNode')
        asps = ['conjunctio', 'sextil', 'quadrat', 'trigon', 'oppositio']
        signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricornus', 'Aquarius', 'Pisces']
        ascmc = ['Asc', 'MC']
        for tr in ls:
            d, m, s = util.decToDeg(tr.time)
            if tr.objtype == Transit.PLANET:
                print('day %d: %s %s %s house:%d %d:%02d:%02d' % (tr.day, planets[tr.plt], asps[tr.aspect], planets[tr.obj], tr.house + 1, d, m, s))
            elif tr.objtype == Transit.ASCMC:
                print('day %d: %s %s %s house:%d %d:%02d:%02d' % (tr.day, planets[tr.plt], asps[tr.aspect], ascmc[tr.obj], tr.house + 1, d, m, s))
            else:
                print('day %d: %s %s house:%d %d:%02d:%02d' % (tr.day, planets[tr.plt], signs[tr.obj], tr.house + 1, d, m, s))