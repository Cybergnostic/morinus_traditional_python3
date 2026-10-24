# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math
import datetime
import astrology
import planets
import planetshelio
import houses
import fortune
import rtofsigns
import firdaria
import munfortune
import antiscia
import dodecatemoria
import zodpars
import midpoints
import riseset
import placspec
import fixedstars
import lots
import almutens
import hours
import syzygy
import userpd
import util
import traditional_aspects
import tradoptions

class Time:
    """Time of Birth"""
    GREGORIAN = 0
    JULIAN = 1
    ZONE, GREENWICH, LOCALMEAN, LOCALAPPARENT = list(range(0, 4))
    HOURSPERDAY = 24.0

    def __init__(self, year, month, day, hour, minute, second, bc, cal, zt, plus, zh, zm, daylightsaving, place, full=True):
        self.year = year
        self.month = month
        self.day = day
        self.origyear = year
        self.origmonth = month
        self.origday = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.bc = bc
        self.cal = cal
        self.zt = zt
        self.plus = plus
        self.zh = zh
        self.zm = zm
        self.daylightsaving = daylightsaving
        self.time = hour + minute / 60.0 + second / 3600.0
        self.dyear, self.dmonth, self.dday, self.dhour, self.dmin, self.dsec = (
         year, month, day, hour, minute, second)
        if self.daylightsaving:
            self.time -= 1.0
            self.dhour -= 1
        if self.time < 0.0:
            self.time += Time.HOURSPERDAY
            self.year, self.month, self.day = util.decrDay(self.year, self.month, self.day)
            self.dhour += int(Time.HOURSPERDAY)
            self.dyear, self.dmonth, self.dday = self.year, self.month, self.day
        if zt == Time.ZONE:
            ztime = zh + zm / 60.0
            if self.plus:
                self.time -= ztime
            else:
                self.time += ztime
        elif zt == Time.LOCALMEAN:
            t = (place.deglon + place.minlon / 60.0) * 4.0
            if place.east:
                self.time -= t / 60.0
            else:
                self.time += t / 60.0
        if bc:
            self.year = 1 - self.year
        if self.time >= Time.HOURSPERDAY:
            self.time -= Time.HOURSPERDAY
            self.year, self.month, self.day = util.incrDay(self.year, self.month, self.day)
        elif self.time < 0.0:
            self.time += Time.HOURSPERDAY
            self.year, self.month, self.day = util.decrDay(self.year, self.month, self.day)
        calflag = astrology.SE_GREG_CAL
        if self.cal == Time.JULIAN:
            calflag = astrology.SE_JUL_CAL
        self.jd = astrology.swe_julday(self.year, self.month, self.day, self.time, calflag)
        if zt == Time.LOCALAPPARENT:
            ret, te, serr = astrology.swe_time_equ(self.jd)
            self.jd += te
            self.year, self.month, self.day, self.time = astrology.swe_revjul(self.jd, calflag)
            t = (place.deglon + place.minlon / 60.0) * 4.0
            if place.east:
                self.time -= t / 60.0
            else:
                self.time += t / 60.0
            if self.time >= Time.HOURSPERDAY:
                self.time -= Time.HOURSPERDAY
                self.year, self.month, self.day = util.incrDay(self.year, self.month, self.day)
            elif self.time < 0.0:
                self.time += Time.HOURSPERDAY
                self.year, self.month, self.day = util.decrDay(self.year, self.month, self.day)
            self.jd = astrology.swe_julday(self.year, self.month, self.day, self.time, calflag)
        self.sidTime = astrology.swe_sidtime(self.jd)
        self.ph = None
        if full:
            self.calcPHs(place)
        return

    def localoffset(self):
        """Days from UT to the chart's own time, as entered (zone, LMT, ...)."""
        calflag = astrology.SE_GREG_CAL if self.cal == Time.GREGORIAN else astrology.SE_JUL_CAL
        year = 1 - self.origyear if self.bc else self.origyear
        return astrology.swe_julday(year, self.origmonth, self.origday, self.hour + self.minute / 60.0 + self.second / 3600.0, calflag) - self.jd

    def calcPHs(self, place):
        weekday = datetime.datetime(self.dyear, self.dmonth, self.dday, self.dhour, self.dmin, self.dsec).weekday()
        lon = place.deglon + place.minlon / 60.0
        if not place.east:
            lon *= -1
        lat = place.deglat + place.minlat / 60.0
        if not place.north:
            lat *= -1
        self.ph = hours.PlanetaryHours(lon, lat, place.altitude, weekday, self.jd)


class Place:
    """Place of Birth"""

    def __init__(self, placename, deglon, minlon, seclon, east, deglat, minlat, seclat, north, altitude):
        self.placename = placename
        self.deglon = deglon
        self.minlon = minlon
        self.seclon = seclon
        self.east = east
        self.deglat = deglat
        self.minlat = minlat
        self.seclat = seclat
        self.north = north
        self.altitude = altitude
        self.lon = deglon + minlon / 60.0 + seclon / 3600.0
        self.lat = deglat + minlat / 60.0 + seclat / 3600.0
        if not self.north:
            self.lat *= -1.0
        if not self.east:
            self.lon *= -1.0


class Asp:

    def __init__(self):
        self.typ = Chart.NONE
        self.dif = 0.0
        self.aspdif = 0.0
        self.appl = False
        self.parallel = Chart.NONE
        self.exact = False


class Chart:
    """Represents a horoscope"""
    RADIX, SOLAR, LUNAR, REVOLUTION, TRANSIT, HORARY, PROFECTION, PDINCHART = list(range(0, 8))
    SIGN_NUM = 12
    SIGN_DEG = 30
    ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO, LIBRA, SCORPIO, SAGITTARIUS, CAPRICORNUS, AQUARIUS, PISCES = list(range(0, 12))
    NONE, CONIUNCTIO, SEXTIL, QUADRAT, TRIGON, OPPOSITIO, PARALLEL, CONTRAPARALLEL, RAPTPAR, RAPTCONTRAPAR, MIDPOINT = list(range(-1, 10))
    DOMICIL, EXAL, PEREGRIN, CASUS, EXIL = list(range(0, 5))
    Aspects = [
     0.0, 60.0, 90.0, 120.0, 180.0]
    ASPECT_NUM = len(Aspects)
    Signboundaries = (
     (0.0, 30.0), (30.0, 60.0), (60.0, 90.0), (90.0, 120.0), (120.0, 150.0), (150.0, 180.0), (180.0, 210.0), (210.0, 240.0), (240.0, 270.0), (270.0, 300.0), (300.0, 330.0), (330.0, 360.0))
    SHOWNONE, SHOWFIXEDSTARS, SHOWANTIS, SHOWLOTS, SHOWDODECATEMORIA = list(range(0, 5))

    def __init__(self, name, male, time, place, htype, notes, opts, full=True, nolat=False):
        self.name = name
        self.male = male
        self.time = time
        self.place = place
        self.htype = htype
        self.options = opts
        self.notes = notes
        self.full = full
        self.nolat = nolat
        d = astrology.swe_deltat(time.jd)
        rflag, self.obl, serr = astrology.swe_calc(time.jd + d, astrology.SE_ECL_NUT, 0)
        astrology.swe_set_topo(place.lon, place.lat, place.altitude)
        self.create()

    def create(self):
        pflag = astrology.SEFLG_SWIEPH + astrology.SEFLG_SPEED
        self.planetshelio = planetshelio.PlanetsHelio(self.time.jd, pflag)
        pflag = astrology.SEFLG_SWIEPH + astrology.SEFLG_SPEED
        astflag = astrology.SEFLG_SWIEPH
        self.ayanamsha = 0.0
        if self.options.ayanamsha != 0:
            astrology.swe_set_sid_mode(self.options.ayanamsha - 1, 0, 0)
            self.ayanamsha = astrology.swe_get_ayanamsa_ut(self.time.jd)
        if self.options.topocentric:
            pflag += astrology.SEFLG_TOPOCTR
        self.houses = houses.Houses(self.time.jd, 0, self.place.lat, self.place.lon, self.options.hsys, self.obl[0], self.options.ayanamsha, self.ayanamsha)
        self.planets = planets.Planets(self.time.jd, self.options.meannode, pflag, self.place.lat, self.houses.ascmc2, self.nolat, self.obl[0])
        self.abovehorizonwithorb = self.isAboveHorizonWithOrb()
        self.syzygy = None
        if self.full:
            self.syzygy = syzygy.Syzygy(self)
        abovehor = self.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].abovehorizon
        if self.options.usedaynightorb:
            abovehor = self.abovehorizonwithorb
        self.lots = lots.Lots(self.options.lots, self.houses.ascmc, self.planets, self.houses, self.houses.cusps, self.syzygy, self.time.ph.planetaryhour, self.options, abovehor, self.ayanamsha)
        self.fortune = fortune.Fortune(self.lots.lots[0][lots.Lots.LON], self.houses.ascmc2, self.obl[0], self.place.lat)
        self.risetimeofsigns = None
        self.firdaria = None
        self.munfortune = None
        self.antiscia = None
        self.dodecatemoria = None
        self.zodpars = None
        self.midpoints = None
        self.riseset = None
        self.fixedstars = None
        self.almutens = None
        self.userprompd = None
        self.usersigpd = None
        if self.full:
            self.risetimeofsigns = rtofsigns.RiseTimeOfSigns(self.place.lat, self.obl[0])
            self.firdaria = firdaria.Firdaria(self.time.origyear, self.time.origmonth, self.time.origday, self.options, self.abovehorizonwithorb)
            self.munfortune = munfortune.MundaneFortune(self.houses.ascmc2, self.planets, self.obl[0], self.place.lat)
            self.antiscia = antiscia.Antiscia(self.planets, self.houses.ascmc, self.fortune.fortune, self.obl[0])
            self.dodecatemoria = dodecatemoria.Dodecatemoria(self.planets, self.houses.ascmc, self.fortune.fortune, self.options.ayanamsha, self.ayanamsha)
            self.zodpars = zodpars.ZodPars(self.planets, self.obl[0])
            self.midpoints = midpoints.MidPoints(self.planets)
            self.riseset = riseset.RiseSet(self.time.jd, self.time.cal, self.place.lon, self.place.lat, self.place.altitude, self.planets)
            self.fixedstars = fixedstars.FixedStars(self.time.jd, 0, self.options.fixedstars, self.obl[0])
            self.almutens = almutens.Almutens(self)
            if self.options.pduser:
                self.userprompd = userpd.UserPD(self.options.pduserlon[0], self.options.pduserlon[1], self.options.pduserlon[2], self.options.pduserlat[0], self.options.pduserlat[1], self.options.pduserlat[2], self.options.pdusersouthern, self.place.lat, self.houses.ascmc2, self.obl[0])
            if self.options.pduser2:
                self.usersigpd = userpd.UserPD(self.options.pduser2lon[0], self.options.pduser2lon[1], self.options.pduser2lon[2], self.options.pduser2lat[0], self.options.pduser2lat[1], self.options.pduser2lat[2], self.options.pduser2southern, self.place.lat, self.houses.ascmc2, self.obl[0])
        astrology.swe_close()
        self.calcAspMatrices()
        if self.full:
            self.calcFixedStarAspMatrices()
        return

    def calcAspMatrices(self):
        self.calcPlsAspMatrix()
        self.calcAscMCAspMatrix()
        self.calcHcsAspMatrix()
        self.calcLoFAspMatrix()

    def calcFixedStarAspMatrices(self):
        self.calcPlsFixedStarAspMatrix()
        self.calcAscMCFixedStarAspMatrix()
        self.calcHCsFixedStarAspMatrix()
        self.calcLoFFixedStarAspMatrix()

    def setHouseSystem(self):
        self.houses = houses.Houses(self.time.jd, 0, self.place.lat, self.place.lon, self.options.hsys, self.obl[0], self.options.ayanamsha, self.ayanamsha)

    def setNodes(self):
        pflag = astrology.SEFLG_SWIEPH + astrology.SEFLG_SPEED
        self.planets = planets.Planets(self.time.jd, self.options.meannode, pflag, self.place.lat, self.houses.ascmc2)

    def calcPlsAspMatrix(self):
        self.calcSpeeds()
        self.aspmatrix = [
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()]]
        for i in range(planets.Planets.BODIES_NUM):
            for j in range(planets.Planets.BODIES_NUM):
                if i > planets.Planets.PLANETS_NUM - 1 and j > planets.Planets.PLANETS_NUM - 1:
                    break
                if i != j:
                    k = i
                    l = j
                    if j > i:
                        k = j
                        l = i
                    decl1 = self.planets.planets[i].dataEqu[1]
                    decl2 = self.planets.planets[j].dataEqu[1]
                    if decl1 > 0.0 and decl2 > 0.0 or decl1 < 0.0 and decl2 < 0.0:
                        if decl1 > 0.0 and decl1 + self.options.orbsplanetspar[i] + self.options.orbsplanetspar[j] > decl2 and decl1 - (self.options.orbsplanetspar[i] + self.options.orbsplanetspar[j]) < decl2 or decl1 < 0.0 and decl1 + self.options.orbsplanetspar[i] + self.options.orbsplanetspar[j] > decl2 and decl1 - (self.options.orbsplanetspar[i] + self.options.orbsplanetspar[j]) < decl2:
                            self.aspmatrix[k][l].parallel = Chart.PARALLEL
                    else:
                        if decl1 < 0.0:
                            decl1 *= -1.0
                        if decl2 < 0.0:
                            decl2 *= -1.0
                        if decl1 + self.options.orbsplanetspar[i] + self.options.orbsplanetspar[j] > decl2 and decl1 - (self.options.orbsplanetspar[i] + self.options.orbsplanetspar[j]) < decl2:
                            self.aspmatrix[k][l].parallel = Chart.CONTRAPARALLEL
                    val1 = util.normalize(self.planets.planets[j].data[planets.Planet.LON] - (self.options.orbs[j] / 2 + self.options.orbs[i] / 2))
                    val2 = util.normalize(self.planets.planets[j].data[planets.Planet.LON] + self.options.orbs[j] / 2 + self.options.orbs[i] / 2)
                    for a in range(Chart.ASPECT_NUM):
                        if (i > planets.Planets.PLANETS_NUM - 1 or j > planets.Planets.PLANETS_NUM - 1) and a > Chart.CONIUNCTIO:
                            break
                        plsign = int(self.planets.planets[j].data[planets.Planet.LON] / Chart.SIGN_DEG)
                        boundary1 = Chart.Signboundaries[plsign][0]
                        boundary2 = Chart.Signboundaries[plsign][1]
                        if val1 < boundary1:
                            val1 = boundary1
                        if val2 > boundary2:
                            val2 = boundary2
                        pllon = self.planets.planets[j].data[planets.Planet.LON]
                        asplon = util.normalize(self.planets.planets[i].data[planets.Planet.LON] + Chart.Aspects[a])
                        if asplon >= val1 and asplon < val2:
                            self.aspmatrix[k][l].typ = a
                            self.aspmatrix[k][l].aspdif = math.fabs(asplon - pllon)
                            self.aspmatrix[k][l].appl = self.isApplPlanets(asplon, i, j)
                            if int(pllon) == int(asplon):
                                self.aspmatrix[k][l].exact = True
                        dif = self.planets.planets[i].data[planets.Planet.LON] - self.planets.planets[j].data[planets.Planet.LON]
                        if self.planets.planets[j].data[planets.Planet.LON] > self.planets.planets[i].data[planets.Planet.LON]:
                            dif = self.planets.planets[j].data[planets.Planet.LON] - self.planets.planets[i].data[planets.Planet.LON]
                        if dif > 180.0:
                            dif = 360.0 - dif
                        self.aspmatrix[k][l].dif = dif

        self._apply_traditional_planet_aspects()

    def _apply_traditional_planet_aspects(self):
        """Replace only the seven planets' ecliptic aspects, never node or parallels.

        The original matrix calculation above is deliberately left unchanged
        for the Legacy preset and for all contacts outside these 21 pairs.
        """
        settings = tradoptions.values()
        if settings['aspect_preset'] == 'legacy':
            return
        orbs = traditional_aspects.configured_orbs(settings)
        for i in range(planets.Planets.PLANETS_NUM):
            for j in range(i):
                a = self.planets.planets[i]
                b = self.planets.planets[j]
                cell = self.aspmatrix[i][j]
                found = traditional_aspects.evaluate(
                    a.data[planets.Planet.LON], b.data[planets.Planet.LON],
                    a.data[planets.Planet.SPLON], b.data[planets.Planet.SPLON],
                    orbs[i], orbs[j], settings['aspect_combine'],
                    settings['aspect_boundary'])
                cell.dif = traditional_aspects.angular_distance(
                    a.data[planets.Planet.LON], b.data[planets.Planet.LON])
                cell.typ = found.index if found is not None else Chart.NONE
                cell.aspdif = found.deviation if found is not None else 0.0
                cell.appl = found.applying if found is not None else False
                cell.exact = found.exact if found is not None else False

    def calcAscMCAspMatrix(self):
        self.aspmatrixAscMC = [
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()]]
        ascmc = [
         self.houses.ascmc2[houses.Houses.ASC][houses.Houses.DECL], self.houses.ascmc2[houses.Houses.MC][houses.Houses.DECL]]
        for i in range(planets.Planets.BODIES_NUM):
            for j in range(2):
                val1 = self.houses.ascmc[j] - self.options.orbs[i] / 2
                val2 = self.houses.ascmc[j] + self.options.orbs[i] / 2
                for a in range(Chart.ASPECT_NUM):
                    if i > planets.Planets.PLANETS_NUM - 1 and a > Chart.CONIUNCTIO:
                        break
                    ascmcsign = int(self.houses.ascmc[j] / Chart.SIGN_DEG)
                    boundary1 = Chart.Signboundaries[ascmcsign][0]
                    boundary2 = Chart.Signboundaries[ascmcsign][1]
                    if val1 < boundary1:
                        val1 = boundary1
                    if val2 > boundary2:
                        val2 = boundary2
                    ascmclon = self.houses.ascmc[j]
                    asplon = util.normalize(self.planets.planets[i].data[planets.Planet.LON] + Chart.Aspects[a])
                    asplon2 = util.normalize(self.planets.planets[i].data[planets.Planet.LON] - Chart.Aspects[a])
                    if asplon >= val1 and asplon < val2:
                        self.aspmatrixAscMC[j][i].typ = a
                        self.aspmatrixAscMC[j][i].aspdif = math.fabs(asplon - ascmclon)
                        self.aspmatrixAscMC[j][i].appl = self.isApplH(asplon, ascmclon, i, True)
                        if int(ascmclon) == int(asplon):
                            self.aspmatrixAscMC[j][i].exact = True
                    elif asplon2 >= val1 and asplon2 < val2:
                        self.aspmatrixAscMC[j][i].typ = a
                        self.aspmatrixAscMC[j][i].aspdif = math.fabs(asplon2 - ascmclon)
                        self.aspmatrixAscMC[j][i].appl = self.isApplH(asplon2, ascmclon, i, False)
                        if int(ascmclon) == int(asplon2):
                            self.aspmatrixAscMC[j][i].exact = True
                    dif = self.planets.planets[i].data[planets.Planet.LON] - ascmclon
                    if ascmclon > self.planets.planets[i].data[planets.Planet.LON]:
                        dif = ascmclon - self.planets.planets[i].data[planets.Planet.LON]
                    if dif > 180.0:
                        dif = 360.0 - dif
                    self.aspmatrixAscMC[j][i].dif = dif

    def calcHcsAspMatrix(self):
        hidx = (1, 2, 3, 10, 11, 12)
        self.aspmatrixH = [
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()],
         [
          Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()]]
        for i in range(planets.Planets.PLANETS_NUM):
            for j in range(len(hidx)):
                val1 = self.houses.cusps[hidx[j]] - self.options.orbs[i] / 2
                val2 = self.houses.cusps[hidx[j]] + self.options.orbs[i] / 2
                for a in range(Chart.ASPECT_NUM):
                    hcsign = int(self.houses.cusps[hidx[j]] / Chart.SIGN_DEG)
                    boundary1 = Chart.Signboundaries[hcsign][0]
                    boundary2 = Chart.Signboundaries[hcsign][1]
                    if val1 < boundary1:
                        val1 = boundary1
                    if val2 > boundary2:
                        val2 = boundary2
                    hclon = self.houses.cusps[hidx[j]]
                    pllon = self.planets.planets[i].data[planets.Planet.LON]
                    if self.options.ayanamsha != 0 and self.houses.hsys == 5:
                        pllon = util.normalize(pllon - self.ayanamsha)
                    asplon = util.normalize(pllon + Chart.Aspects[a])
                    asplon2 = util.normalize(pllon - Chart.Aspects[a])
                    if asplon >= val1 and asplon < val2:
                        self.aspmatrixH[j][i].typ = a
                        self.aspmatrixH[j][i].aspdif = math.fabs(asplon - hclon)
                        self.aspmatrixH[j][i].appl = self.isApplH(asplon, hclon, i, True)
                        if int(hclon) == int(asplon):
                            self.aspmatrixH[j][i].exact = True
                    elif asplon2 >= val1 and asplon2 < val2:
                        self.aspmatrixH[j][i].typ = a
                        self.aspmatrixH[j][i].aspdif = math.fabs(asplon2 - hclon)
                        self.aspmatrixH[j][i].appl = self.isApplH(asplon, hclon, i, False)
                        if int(hclon) == int(asplon2):
                            self.aspmatrixH[j][i].exact = True
                    pllon = self.planets.planets[i].data[planets.Planet.LON]
                    if self.options.ayanamsha != 0 and self.houses.hsys == 5:
                        pllon = util.normalize(pllon - self.ayanamsha)
                    dif = pllon - hclon
                    if hclon > pllon:
                        dif = hclon - pllon
                    if dif > 180.0:
                        dif = 360.0 - dif
                    self.aspmatrixH[j][i].dif = dif

    def calcLoFAspMatrix(self):
        lonlof = self.fortune.fortune[fortune.Fortune.LON]
        self.aspmatrixLoF = [Asp(), Asp(), Asp(), Asp(), Asp(), Asp(), Asp()]
        for i in range(planets.Planets.PLANETS_NUM):
            for a in range(Chart.ASPECT_NUM):
                asplon = util.normalize(self.planets.planets[i].data[planets.Planet.LON] + Chart.Aspects[a])
                dif = math.fabs(asplon - lonlof)
                val1 = util.normalize(asplon - self.options.orbs[i] / 2)
                val2 = util.normalize(asplon + self.options.orbs[i] / 2)
                aspsign = int(asplon / Chart.SIGN_DEG)
                boundary1 = Chart.Signboundaries[aspsign][0]
                boundary2 = Chart.Signboundaries[aspsign][1]
                if val1 < boundary1:
                    val1 = boundary1
                if val2 > boundary2:
                    val2 = boundary2
                if lonlof >= val1 and lonlof < val2:
                    self.aspmatrixLoF[i].typ = a
                    self.aspmatrixLoF[i].aspdif = dif
                    self.aspmatrixLoF[i].appl = asplon < lonlof
                    if int(lonlof) == int(asplon):
                        self.aspmatrixLoF[i].exact = True
                else:
                    asplon = util.normalize(self.planets.planets[i].data[planets.Planet.LON] - Chart.Aspects[a])
                    dif = math.fabs(asplon - lonlof)
                    val1 = util.normalize(asplon - self.options.orbs[i] / 2)
                    val2 = util.normalize(asplon + self.options.orbs[i] / 2)
                    aspsign = int(asplon / Chart.SIGN_DEG)
                    boundary1 = Chart.Signboundaries[aspsign][0]
                    boundary2 = Chart.Signboundaries[aspsign][1]
                    if val1 < boundary1:
                        val1 = boundary1
                    if val2 > boundary2:
                        val2 = boundary2
                    if lonlof >= val1 and lonlof < val2:
                        self.aspmatrixLoF[i].typ = a
                        self.aspmatrixLoF[i].aspdif = dif
                        self.aspmatrixLoF[i].appl = asplon < lonlof
                        if int(lonlof) == int(asplon):
                            self.aspmatrixLoF[i].exact = True
                dif = self.planets.planets[i].data[planets.Planet.LON] - lonlof
                if lonlof > self.planets.planets[i].data[planets.Planet.LON]:
                    dif = lonlof - self.planets.planets[i].data[planets.Planet.LON]
                if dif > 180.0:
                    dif = 360.0 - dif
                self.aspmatrixLoF[i].dif = dif

    def calcPlsFixedStarAspMatrix(self):
        """Calculates conjunctions of fixedstars and planets"""
        self.fsaspmatrix = []
        num = len(self.fixedstars.data)
        for i in range(num):
            ar = []
            val1 = self.fixedstars.data[i][fixedstars.FixedStars.LON] - self.options.fixedstars[self.fixedstars.data[i][fixedstars.FixedStars.NOMNAME]] / 2
            val2 = self.fixedstars.data[i][fixedstars.FixedStars.LON] + self.options.fixedstars[self.fixedstars.data[i][fixedstars.FixedStars.NOMNAME]] / 2
            fssign = int(self.fixedstars.data[i][fixedstars.FixedStars.LON] / Chart.SIGN_DEG)
            boundary1 = Chart.Signboundaries[fssign][0]
            boundary2 = Chart.Signboundaries[fssign][1]
            if val1 < boundary1:
                val1 = boundary1
            if val2 > boundary2:
                val2 = boundary2
            for j in range(planets.Planets.BODIES_NUM):
                pllon = self.planets.planets[j].data[planets.Planet.LON]
                if pllon >= val1 and pllon < val2:
                    ar.append(j)

            if len(ar) != 0:
                fsar = (
                 i, ar)
                self.fsaspmatrix.append(fsar)

    def calcAscMCFixedStarAspMatrix(self):
        """Calculates conjuntions of the fixedstars and Asc/Desc, MC/IC (The angles)"""
        self.fsaspmatrixAngles = []
        ASC = self.houses.ascmc[houses.Houses.ASC]
        DESC = util.normalize(self.houses.ascmc[houses.Houses.ASC] + 180.0)
        MC = self.houses.ascmc[houses.Houses.MC]
        IC = util.normalize(self.houses.ascmc[houses.Houses.MC] + 180.0)
        ascmc = [ASC, DESC, MC, IC]
        lenascmc = len(ascmc)
        num = len(self.fixedstars.data)
        for i in range(num):
            ar = []
            val1 = self.fixedstars.data[i][fixedstars.FixedStars.LON] - self.options.fixedstars[self.fixedstars.data[i][fixedstars.FixedStars.NOMNAME]] / 2
            val2 = self.fixedstars.data[i][fixedstars.FixedStars.LON] + self.options.fixedstars[self.fixedstars.data[i][fixedstars.FixedStars.NOMNAME]] / 2
            fssign = int(self.fixedstars.data[i][fixedstars.FixedStars.LON] / Chart.SIGN_DEG)
            boundary1 = Chart.Signboundaries[fssign][0]
            boundary2 = Chart.Signboundaries[fssign][1]
            if val1 < boundary1:
                val1 = boundary1
            if val2 > boundary2:
                val2 = boundary2
            for j in range(lenascmc):
                if ascmc[j] >= val1 and ascmc[j] < val2:
                    ar.append(j)

            if len(ar) != 0:
                fsar = (
                 i, ar)
                self.fsaspmatrixAngles.append(fsar)

    def calcHCsFixedStarAspMatrix(self):
        """Calculates conjuntions of the fixedstars and intermediate housecusps"""
        self.fsaspmatrixHCs = []
        num = len(self.fixedstars.data)
        for i in range(num):
            ar = []
            val1 = self.fixedstars.data[i][fixedstars.FixedStars.LON] - self.options.fixedstars[self.fixedstars.data[i][fixedstars.FixedStars.NOMNAME]] / 2
            val2 = self.fixedstars.data[i][fixedstars.FixedStars.LON] + self.options.fixedstars[self.fixedstars.data[i][fixedstars.FixedStars.NOMNAME]] / 2
            for j in range(houses.Houses.HOUSE_NUM):
                if (j == 0 or j == 3 or j == 6 or j == 9) and (self.houses.hsys == 0 or self.houses.hsys == 1 or self.houses.hsys == 2 or self.houses.hsys == 3 or self.houses.hsys == 4 or self.houses.hsys == 9 or self.houses.hsys == 10 or self.houses.hsys == 11):
                    continue
                if self.houses.cusps[(j + 1)] >= val1 and self.houses.cusps[(j + 1)] < val2:
                    ar.append(j)

            if len(ar) != 0:
                fsar = (
                 i, ar)
                self.fsaspmatrixHCs.append(fsar)

    def calcLoFFixedStarAspMatrix(self):
        """Calculates conjuntions of the fixedstars and LoF"""
        self.fsaspmatrixLoF = []
        num = len(self.fixedstars.data)
        lonlof = self.fortune.fortune[fortune.Fortune.LON]
        for i in range(num):
            val1 = self.fixedstars.data[i][fixedstars.FixedStars.LON] - self.options.fixedstars[self.fixedstars.data[i][fixedstars.FixedStars.NOMNAME]] / 2
            val2 = self.fixedstars.data[i][fixedstars.FixedStars.LON] + self.options.fixedstars[self.fixedstars.data[i][fixedstars.FixedStars.NOMNAME]] / 2
            if lonlof >= val1 and lonlof < val2:
                self.fsaspmatrixLoF.append(i)

    def isApplPlanets(self, tmp, pl1, pl2):
        pl1speed = 0
        pl2speed = 0
        for i in range(planets.Planets.BODIES_NUM):
            if self.speeds[i] == pl1:
                pl1speed = i
            if self.speeds[i] == pl2:
                pl2speed = i

        pl1ret = self.planets.planets[pl1].data[planets.Planet.SPLON] < 0.0
        pl2ret = self.planets.planets[pl2].data[planets.Planet.SPLON] < 0.0
        if tmp < self.planets.planets[pl2].data[planets.Planet.LON]:
            if pl1speed > pl2speed:
                return not pl1ret
            else:
                return pl2ret

        else:
            if pl1speed > pl2speed:
                return pl1ret
            else:
                return not pl2ret

    def isApplH(self, asplon, hclon, plid, forwardasp):
        res = False
        if asplon < hclon:
            res = True
        else:
            res = False
        if self.planets.planets[plid].data[planets.Planet.SPLON] < 0.0:
            res = not res
        return res

    def calcSpeeds(self):
        self.speeds = [
         0, 1, 2, 3, 4, 5, 6, 7, 8]
        planetspds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(planets.Planets.BODIES_NUM):
            planetspds[i] = self.planets.planets[i].data[planets.Planet.SPLON]
            if planetspds[i] < 0.0:
                planetspds[i] *= -1.0

        swapped = True
        while swapped:
            swapped = False
            for i in range(planets.Planets.BODIES_NUM - 1):
                if planetspds[i] > planetspds[(i + 1)]:
                    tmp = planetspds[i]
                    planetspds[i] = planetspds[(i + 1)]
                    planetspds[i + 1] = tmp
                    a = self.speeds[i]
                    self.speeds[i] = self.speeds[(i + 1)]
                    self.speeds[i + 1] = a
                    swapped = True

    def dignity(self, pid):
        lona = self.planets.planets[pid].data[planets.Planet.LON]
        if self.options.ayanamsha != 0:
            lona -= self.ayanamsha
            lona = util.normalize(lona)
        sign = int(lona / Chart.SIGN_DEG)
        val = Chart.PEREGRIN
        if pid < planets.Planets.PLANETS_NUM:
            isdom = self.options.dignities[pid][0][sign]
            isexal = self.options.dignities[pid][1][sign]
            oppsign = sign + Chart.SIGN_NUM // 2
            if oppsign >= Chart.SIGN_NUM:
                oppsign -= Chart.SIGN_NUM
            isexil = self.options.dignities[pid][0][oppsign]
            iscasus = self.options.dignities[pid][1][oppsign]
            if isdom:
                val = Chart.DOMICIL
            elif isexil:
                val = Chart.EXIL
            elif isexal:
                val = Chart.EXAL
            elif iscasus:
                val = Chart.CASUS
        return val

    def recalc(self):
        del self.houses
        del self.planets
        del self.fortune
        del self.fixedstars
        del self.midpoints
        del self.riseset
        del self.zodpars
        del self.risetimeofsigns
        del self.firdaria
        del self.munfortune
        del self.antiscia
        del self.dodecatemoria
        del self.syzygy
        del self.lots
        del self.almutens
        del self.userprompd
        del self.usersigpd
        self.create()

    def calcAntiscia(self):
        del self.antiscia
        self.antiscia = antiscia.Antiscia(self.planets, self.houses.ascmc, self.fortune.fortune, self.obl[0])

    def calcFortune(self):
        del self.fortune
        self.fortune = fortune.Fortune(self.lots.lots[0][lots.Lots.LON], self.houses.ascmc2, self.obl[0], self.place.lat)
        self.calcLoFAspMatrix()
        self.calcLoFFixedStarAspMatrix()

    def calcSyzygy(self):
        del self.syzygy
        self.syzygy = syzygy.Syzygy(self)

    def calcFixedStars(self):
        del self.fixedstars
        self.fixedstars = fixedstars.FixedStars(self.time.jd, 0, self.options.fixedstars, self.obl[0])

    def calcLots(self):
        del self.lots
        self.abovehorizonwithorb = self.isAboveHorizonWithOrb()
        abovehor = self.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].abovehorizon
        if self.options.usedaynightorb:
            abovehor = self.abovehorizonwithorb
        self.lots = lots.Lots(self.options.lots, self.houses.ascmc, self.planets, self.houses, self.houses.cusps, self.syzygy, self.time.ph.planetaryhour, self.options, abovehor, self.ayanamsha)

    def calcAlmutens(self):
        del self.almutens
        self.almutens = almutens.Almutens(self)

    def setUserPromPD(self, upd):
        if self.userprompd != None:
            del self.userprompd
        self.userprompd = upd
        return

    def setUserSigPD(self, upd):
        if self.usersigpd != None:
            del self.usersigpd
        self.usersigpd = upd
        return

    def isAboveHorizonWithOrb(self):
        mdsun = self.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
        sasun = self.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.SA]
        abovehorizon = self.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].abovehorizon
        if not abovehorizon:
            if mdsun < 0.0:
                mdsun += 180.0
            if sasun < 0.0:
                sasun += 180.0
            orb = self.options.daynightorb
            if mdsun - orb < sasun:
                abovehorizon = True
        return abovehorizon

    def calcProfPos(self, prof):
        self.planets.calcProfPos(prof)
        self.houses.calcProfPos(prof)
        self.fortune.calcProfPos(prof)

    def printAspMatrices(self):
        partxt = ('none', 'parallel', 'contrap')
        print('')
        print('Aspects:')
        for i in range(planets.Planets.BODIES_NUM):
            for j in range(planets.Planets.BODIES_NUM):
                if j > i:
                    if self.aspmatrix[j][i].typ != Chart.NONE:
                        plel = 0
                        if self.aspmatrix[j][i].parallel == Chart.PARALLEL:
                            plel = 1
                        if self.aspmatrix[j][i].parallel == Chart.CONTRAPARALLEL:
                            plel = 2
                        extxt = ''
                        if self.aspmatrix[j][i].exact:
                            extxt = 'exact'
                        appltxt = 'sepa'
                        if self.aspmatrix[j][i].appl:
                            appltxt = 'appl'
                        print('%s - %s: type=%d diff=%f %s par=%s %s' % (self.planets.planets[i].name, self.planets.planets[j].name, self.aspmatrix[j][i].typ, self.aspmatrix[j][i].dif, appltxt, partxt[plel], extxt))

        print('')
        ascmcname = ('Asc', 'MC')
        num = len(self.aspmatrixAscMC)
        for i in range(planets.Planets.PLANETS_NUM):
            for j in range(num):
                if self.aspmatrixAscMC[j][i].typ != Chart.NONE:
                    extxt = ''
                    if self.aspmatrixAscMC[j][i].exact:
                        extxt = 'exact'
                    appltxt = 'sepa'
                    if self.aspmatrixAscMC[j][i].appl:
                        appltxt = 'appl'
                    print('%s - %s: type=%d %s diff=%f  %s' % (self.planets.planets[i].name, ascmcname[j], self.aspmatrixAscMC[j][i].typ, appltxt, self.aspmatrixAscMC[j][i].dif, extxt))

        print('')
        hname = ('1', '2', '3', '10', '11', '12')
        hnum = 6
        for i in range(planets.Planets.PLANETS_NUM):
            for j in range(hnum):
                if self.aspmatrixH[j][i].typ != Chart.NONE:
                    extxt = ''
                    if self.aspmatrixH[j][i].exact:
                        extxt = 'exact'
                    appltxt = 'sepa'
                    if self.aspmatrixH[j][i].appl:
                        appltxt = 'appl'
                    print('%s - %s: type=%d %s diff=%f  %s' % (self.planets.planets[i].name, hname[j], self.aspmatrixH[j][i].typ, appltxt, self.aspmatrixH[j][i].dif, extxt))

        print('')
        for i in range(planets.Planets.PLANETS_NUM):
            if self.aspmatrixLoF[i].typ != Chart.NONE:
                extxt = ''
                if self.aspmatrixLoF[i].exact:
                    extxt = 'exact'
                appltxt = 'sepa'
                if self.aspmatrixLoF[i].appl:
                    appltxt = 'appl'
                print('%s - %s: type=%d %s diff=%f  %s' % (self.planets.planets[i].name, 'LoF', self.aspmatrixLoF[i].typ, appltxt, self.aspmatrixLoF[i].dif, extxt))

    def printFixedStarAspMatrices(self):
        print('')
        print('FixedStars aspects:')
        leng = len(self.fsaspmatrix)
        for i in range(leng):
            subleng = len(self.fsaspmatrix[i][1])
            txt = ''
            for j in range(subleng):
                if j > 0:
                    txt += ' '
                txt += self.planets.planets[self.fsaspmatrix[i][1][j]].name

            print('%s %s' % (self.fixedstars.data[self.fsaspmatrix[i][0]][fixedstars.FixedStars.NAME], txt))

        print('')
        angles = ('Asc', 'Desc', 'MC', 'IC')
        leng = len(self.fsaspmatrixAngles)
        for i in range(leng):
            subleng = len(self.fsaspmatrixAngles[i][1])
            txt = ''
            for j in range(subleng):
                if j > 0:
                    txt += ' '
                txt += angles[self.fsaspmatrixAngles[i][1][j]]

            print('%s %s' % (self.fixedstars.data[self.fsaspmatrixAngles[i][0]][fixedstars.FixedStars.NAME], txt))

        print('')
        hcs = ('HC1', 'HC2', 'HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC9', 'HC10',
               'HC11', 'HC12')
        leng = len(self.fsaspmatrixHCs)
        for i in range(leng):
            subleng = len(self.fsaspmatrixHCs[i][1])
            txt = ''
            for j in range(subleng):
                if j > 0:
                    txt += ' '
                txt += hcs[self.fsaspmatrixHCs[i][1][j]]

            print('%s %s' % (self.fixedstars.data[self.fsaspmatrixHCs[i][0]][fixedstars.FixedStars.NAME], txt))

        print('')
        leng = len(self.fsaspmatrixLoF)
        txt = ''
        for i in range(leng):
            if i > 0:
                txt += ' '
            txt += self.fixedstars.data[i][fixedstars.FixedStars.NAME]

        print('%s %s' % ('LoF: ', txt))