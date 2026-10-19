# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import astrology, chart, houses, planets, util

class Syzygy:
    LON = 0
    LAT = 1
    RA = 2
    DECL = 3
    MOON = 0
    ABOVEHOR = 1
    ABOVEHORNATAL = 2
    TOPICALDEFAULT = 0
    TOPICALCONIUNCTIO = 1
    TOPICALOPPOSITIO = 2
    TOPICALOPPOSITIORADIX = 3
    TOPICALMOON = 4

    def __init__(self, chrt):
        self.time = chrt.time
        self.lon = chrt.planets.planets[planets.Planets.MOON].data[planets.Planet.LON]
        self.flags = astrology.SEFLG_SPEED + astrology.SEFLG_SWIEPH
        self.lons = []
        if not chrt.time.bc:
            lonsun = chrt.planets.planets[planets.Planets.SUN].data[planets.Planet.LON]
            lonmoon = chrt.planets.planets[planets.Planets.MOON].data[planets.Planet.LON]
            d, m, s = util.decToDeg(lonsun)
            lonsun = d + m / 60.0 + s / 3600.0
            d, m, s = util.decToDeg(lonmoon)
            lonmoon = d + m / 60.0 + s / 3600.0
            diff = lonmoon - lonsun
            self.newmoon, self.ready = self.isNewMoon(diff)
            if not self.ready:
                ok, self.time, self.ready = self.getDateHour(self.time, chrt.place, self.newmoon)
                if not self.ready:
                    ok, self.time, self.ready = self.getDateMinute(self.time, chrt.place, self.newmoon)
                    if not self.ready:
                        ok, self.time, self.ready = self.getDateSecond(self.time, chrt.place, self.newmoon)
            self.time.calcPHs(chrt.place)
            hses = houses.Houses(self.time.jd, 0, chrt.place.lat, chrt.place.lon, chrt.options.hsys, chrt.obl[0], chrt.options.ayanamsha, chrt.ayanamsha)
            moon = planets.Planet(self.time.jd, planets.Planets.MOON, self.flags, chrt.place.lat, hses.ascmc2)
            if self.newmoon:
                self.lon = moon.data[planets.Planet.LON]
            elif chrt.options.syzmoon == Syzygy.MOON:
                self.lon = moon.data[planets.Planet.LON]
            elif chrt.options.syzmoon == Syzygy.ABOVEHOR:
                if moon.speculums[planets.Planet.PLACIDIAN].abovehorizon:
                    self.lon = moon.data[planets.Planet.LON]
                else:
                    sun = planets.Planet(self.time.jd, planets.Planets.SUN, self.flags)
                    self.lon = sun.data[planets.Planet.LON]
            else:
                moon = planets.Planet(self.time.jd, planets.Planets.MOON, self.flags, chrt.place.lat, chrt.houses.ascmc2)
                if moon.speculums[planets.Planet.PLACIDIAN].abovehorizon:
                    self.lon = moon.data[planets.Planet.LON]
                else:
                    sun = planets.Planet(self.time.jd, planets.Planets.SUN, self.flags)
                    self.lon = sun.data[planets.Planet.LON]
        ra, decl, dist = astrology.swe_cotrans(self.lon, 0.0, 1.0, -chrt.obl[0])
        self.speculum = [self.lon, 0.0, ra, decl]
        self.lon2 = chrt.planets.planets[planets.Planets.MOON].data[planets.Planet.LON]
        if not chrt.time.bc:
            self.time2 = self.time
            ok, self.time2, self.ready2 = self.getDateHour(self.time2, chrt.place, not self.newmoon)
            if not self.ready2:
                ok, self.time2, self.ready2 = self.getDateMinute(self.time2, chrt.place, not self.newmoon)
                if not self.ready2:
                    ok, self.time2, self.ready2 = self.getDateSecond(self.time2, chrt.place, not self.newmoon)
            self.time2.calcPHs(chrt.place)
            hses2 = houses.Houses(self.time2.jd, 0, chrt.place.lat, chrt.place.lon, chrt.options.hsys, chrt.obl[0], chrt.options.ayanamsha, chrt.ayanamsha)
            moon2 = planets.Planet(self.time2.jd, planets.Planets.MOON, self.flags, chrt.place.lat, hses2.ascmc2)
            if not self.newmoon:
                self.lon2 = moon2.data[planets.Planet.LON]
            elif chrt.options.syzmoon == Syzygy.MOON:
                self.lon2 = moon2.data[planets.Planet.LON]
            elif chrt.options.syzmoon == Syzygy.ABOVEHOR:
                if moon2.speculums[planets.Planet.PLACIDIAN].abovehorizon:
                    self.lon2 = moon2.data[planets.Planet.LON]
                else:
                    sun2 = planets.Planet(self.time2.jd, planets.Planets.SUN, self.flags)
                    self.lon2 = sun2.data[planets.Planet.LON]
            else:
                moon2 = planets.Planet(self.time2.jd, planets.Planets.MOON, self.flags, chrt.place.lat, chrt.houses.ascmc2)
                if moon2.speculums[planets.Planet.PLACIDIAN].abovehorizon:
                    self.lon2 = moon2.data[planets.Planet.LON]
                else:
                    sun2 = planets.Planet(self.time2.jd, planets.Planets.SUN, self.flags)
                    self.lon2 = sun2.data[planets.Planet.LON]
            ra2, decl2, dist2 = astrology.swe_cotrans(self.lon2, 0.0, 1.0, -chrt.obl[0])
            self.speculum2 = [self.lon2, 0.0, ra2, decl2]
            self.lons.append(self.lon)
            if self.newmoon:
                self.lons.append(self.lon)
            else:
                self.lons.append(self.lon2)
            hses = houses.Houses(self.time.jd, 0, chrt.place.lat, chrt.place.lon, chrt.options.hsys, chrt.obl[0], chrt.options.ayanamsha, chrt.ayanamsha)
            moonSyz = planets.Planet(self.time.jd, planets.Planets.MOON, self.flags, chrt.place.lat, hses.ascmc2)
            hses2 = houses.Houses(self.time2.jd, 0, chrt.place.lat, chrt.place.lon, chrt.options.hsys, chrt.obl[0], chrt.options.ayanamsha, chrt.ayanamsha)
            moonSyz2 = planets.Planet(self.time2.jd, planets.Planets.MOON, self.flags, chrt.place.lat, hses2.ascmc2)
            if not self.newmoon:
                if moonSyz.speculums[planets.Planet.PLACIDIAN].abovehorizon:
                    self.lons.append(moonSyz.data[planets.Planet.LON])
                else:
                    sun = planets.Planet(self.time.jd, planets.Planets.SUN, self.flags)
                    self.lons.append(sun.data[planets.Planet.LON])
            elif moonSyz2.speculums[planets.Planet.PLACIDIAN].abovehorizon:
                self.lons.append(moonSyz2.data[planets.Planet.LON])
            else:
                sun2 = planets.Planet(self.time2.jd, planets.Planets.SUN, self.flags)
                self.lons.append(sun2.data[planets.Planet.LON])
            if not self.newmoon:
                moon = planets.Planet(self.time.jd, planets.Planets.MOON, self.flags, chrt.place.lat, chrt.houses.ascmc2)
                if moon.speculums[planets.Planet.PLACIDIAN].abovehorizon:
                    self.lons.append(moon.data[planets.Planet.LON])
                else:
                    sun = planets.Planet(self.time.jd, planets.Planets.SUN, self.flags)
                    self.lons.append(sun.data[planets.Planet.LON])
            else:
                moon = planets.Planet(self.time2.jd, planets.Planets.MOON, self.flags, chrt.place.lat, chrt.houses.ascmc2)
                if moon.speculums[planets.Planet.PLACIDIAN].abovehorizon:
                    self.lons.append(moon.data[planets.Planet.LON])
                else:
                    sun = planets.Planet(self.time.jd, planets.Planets.SUN, self.flags)
                    self.lons.append(sun.data[planets.Planet.LON])
            if not self.newmoon:
                self.lons.append(moonSyz.data[planets.Planet.LON])
            else:
                self.lons.append(moonSyz2.data[planets.Planet.LON])

    def isNewMoon(self, diff):
        newmoon = True
        ready = False
        if diff == 0.0:
            newmoon = True
            ready = True
        elif diff == 180.0 or diff == -180.0:
            newmoon = False
            ready = True
        elif diff < 0.0:
            if diff < -180.0:
                newmoon = True
            else:
                newmoon = False
        elif diff > 0.0:
            if diff > 180.0:
                newmoon = False
            else:
                newmoon = True
        return (
         newmoon, ready)

    def getDateHour(self, tim, place, newmoonorig):
        while True:
            h, m, s = util.decToDeg(tim.time)
            y, mo, d = tim.year, tim.month, tim.day
            h -= 1
            if h < 0:
                h = 23
                y, mo, d = util.decrDay(y, mo, d)
                if y == 0:
                    y = 1
                    tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)
                    return (
                     True, tim, True)
            tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)
            sun = planets.Planet(tim.jd, planets.Planets.SUN, self.flags)
            moon = planets.Planet(tim.jd, planets.Planets.MOON, self.flags)
            lonsun = sun.data[planets.Planet.LON]
            lonmoon = moon.data[planets.Planet.LON]
            d, m, s = util.decToDeg(lonsun)
            lonsun = d + m / 60.0 + s / 3600.0
            d, m, s = util.decToDeg(lonmoon)
            lonmoon = d + m / 60.0 + s / 3600.0
            diff = lonmoon - lonsun
            newmoon, ready = self.isNewMoon(diff)
            if newmoon != newmoonorig or ready:
                return (True, tim, ready)

        return (
         False, tim)

    def getDateMinute(self, tim, place, newmoonorig):
        h, m, s = util.decToDeg(tim.time)
        y, mo, d = tim.year, tim.month, tim.day
        h += 1
        if h > 23:
            h = 0
            y, mo, d = util.incrDay(y, mo, d)
        tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)
        while True:
            h, m, s = util.decToDeg(tim.time)
            y, mo, d = tim.year, tim.month, tim.day
            y, mo, d, h, m = util.subtractMins(y, mo, d, h, m, 1)
            if y == 0:
                y = 1
                tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)
                return (
                 True, tim, True)
            tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)
            sun = planets.Planet(tim.jd, planets.Planets.SUN, self.flags)
            moon = planets.Planet(tim.jd, planets.Planets.MOON, self.flags)
            lonsun = sun.data[planets.Planet.LON]
            lonmoon = moon.data[planets.Planet.LON]
            d, m, s = util.decToDeg(lonsun)
            lonsun = d + m / 60.0 + s / 3600.0
            d, m, s = util.decToDeg(lonmoon)
            lonmoon = d + m / 60.0 + s / 3600.0
            diff = lonmoon - lonsun
            newmoon, ready = self.isNewMoon(diff)
            if newmoon != newmoonorig or ready:
                return (True, tim, ready)

        return (
         False, tim)

    def getDateSecond(self, tim, place, newmoonorig):
        h, m, s = util.decToDeg(tim.time)
        y, mo, d = tim.year, tim.month, tim.day
        y, mo, d, h, m = util.addMins(y, mo, d, h, m, 1)
        tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)
        while True:
            h, m, s = util.decToDeg(tim.time)
            y, mo, d = tim.year, tim.month, tim.day
            y, mo, d, h, m, s = util.subtractSecs(y, mo, d, h, m, s, 1)
            if y == 0:
                y = 1
                tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)
                return (
                 True, tim, True)
            tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)
            sun = planets.Planet(tim.jd, planets.Planets.SUN, self.flags)
            moon = planets.Planet(tim.jd, planets.Planets.MOON, self.flags)
            lonsun = sun.data[planets.Planet.LON]
            lonmoon = moon.data[planets.Planet.LON]
            d, m, s = util.decToDeg(lonsun)
            lonsun = d + m / 60.0 + s / 3600.0
            d, m, s = util.decToDeg(lonmoon)
            lonmoon = d + m / 60.0 + s / 3600.0
            diff = lonmoon - lonsun
            newmoon, ready = self.isNewMoon(diff)
            if newmoon != newmoonorig or ready:
                return (True, tim, ready)

        return (
         False, tim)

    def printSyzygy(self):
        signs = ('Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap',
                 'Aqu', 'Pis')
        print ''
        print 'Syzygy:'
        txt = 'Full Moon'
        if self.newmoon:
            txt = 'New Moon'
        ye, mo, da = self.time.year, self.time.month, self.time.day
        h, m, s = util.decToDeg(self.time.time)
        si = int(self.lon / chart.Chart.SIGN_DEG)
        d, mi, se = util.decToDeg(self.lon)
        print '%s %d.%02d.%02d %02d:%02d:%02d lon=%02d%s %02dm %02ds' % (txt, ye, mo, da, h, m, s, d, signs[si], mi, se)
        print ''
        print 'Syzygy2:'
        txt = 'New Moon'
        if self.newmoon:
            txt = 'Full Moon'
        ye, mo, da = self.time2.year, self.time2.month, self.time2.day
        h, m, s = util.decToDeg(self.time2.time)
        si = int(self.lon2 / chart.Chart.SIGN_DEG)
        d, mi, se = util.decToDeg(self.lon2)
        print '%s %d.%02d.%02d %02d:%02d:%02d lon=%02d%s %02dm %02ds' % (txt, ye, mo, da, h, m, s, d, signs[si], mi, se)