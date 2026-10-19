# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math, datetime, astrology, houses, chart, fortune, syzygy, planets, fixedstars, transits, secmotion, userpd, placspec, regiospec, mtexts, util

class AbortPD:

    def __init__(self):
        self.abort = False

    def aborting(self):
        self.abort = True


class PrimDir:
    """Represents a direction"""
    NONE = -1
    OFFSANGLES = planets.Planets.BODIES_NUM
    ASC = OFFSANGLES
    DESC = ASC + 1
    MC = DESC + 1
    IC = MC + 1
    HC2 = IC + 1
    HC3 = HC2 + 1
    HC5 = HC3 + 1
    HC6 = HC5 + 1
    HC8 = HC6 + 1
    HC9 = HC8 + 1
    HC11 = HC9 + 1
    HC12 = HC11 + 1
    LOF = HC12 + 1
    SYZ = LOF + 1
    USERPD = SYZ + 1
    ANTISCION = USERPD + 1
    ANTISCIONLOF = ANTISCION + 12 + 1
    ANTISCIONASC = ANTISCIONLOF + 1
    ANTISCIONMC = ANTISCIONASC + 1
    CONTRAANT = ANTISCIONMC + 1
    CONTRAANTLOF = CONTRAANT + 12 + 1
    CONTRAANTASC = CONTRAANTLOF + 1
    CONTRAANTMC = CONTRAANTASC + 1
    TERM = CONTRAANTMC + 1
    FIXEDSTAR = TERM + 12 + 1

    def __init__(self):
        self.mundane = False
        self.prom = PrimDir.NONE
        self.prom2 = PrimDir.NONE
        self.sig = PrimDir.NONE
        self.promasp = PrimDir.NONE
        self.sigasp = PrimDir.NONE
        self.arc = 0.0
        self.direct = True
        self.time = 0.0
        self.age = 0.0


class PrimDirs:
    """Implements the PDs that are common in all systems (directions to Asc-MC) and also implements the MidPoints"""
    PLACIDIANSEMIARC = 0
    PLACIDIANUNDERTHEPOLE = 1
    REGIOMONTAN = 2
    CAMPANIAN = 3
    MUNDANE = 0
    ZODIACAL = 1
    BOTH = 2
    SZNEITHER = 0
    SZPROMISSOR = 1
    SZSIGNIFICATOR = 2
    SZBOTH = 3
    ASPSPROMSTOSIGS = 0
    PROMSTOSIGASPS = 1
    TRUESOLAREQUATORIALARC = 0
    BIRTHDAYSOLAREQUATORIALARC = 1
    TRUESOLARECLIPTICALARC = 2
    BIRTHDAYSOLARECLIPTICALARC = 3
    NAIBOD = 0
    CARDAN = 1
    PTOLEMY = 2
    USER = 3
    DEG = 0
    MIN = 1
    SEC = 2
    COEFF = 3
    staticData = ((0, 59, 8, 1.01456164), (0, 59, 12, 1.0135135), (1, 0, 0, 1.0))
    DIRECT = 0
    CONVERSE = 1
    BOTHDC = 2
    RANGE25 = 0
    RANGE50 = 1
    RANGE75 = 2
    RANGE100 = 3
    RANGEALL = 4
    RANGEREV = 5
    LIMIT = 100.0
    REVOLUTIO = 360.0
    Ranges = (
     (0.0, 25.0), (25.0, 50.0), (50.0, 75.0), (75.0, 100.0), (0.0, LIMIT), (0.0, REVOLUTIO))
    LOW = 0
    HIGH = 1

    def __init__(self, chrt, options, pdrange, direction, abort):
        self.chart = chrt
        self.options = options
        self.pdrange = pdrange
        self.direction = direction
        self.abort = abort
        self.pds = []
        self.ramc = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.RA]
        self.raic = self.ramc + 180.0
        if self.raic >= 360.0:
            self.raic -= 360.0
        self.aoasc = self.ramc + 90.0
        if self.aoasc >= 360.0:
            self.aoasc -= 360.0
        self.dodesc = self.raic + 90.0
        if self.dodesc >= 360.0:
            self.dodesc -= 360.0
        self.calc()
        self.pds = self.qsort(self.pds)

    def calc(self):
        if self.options.subprimarydir == PrimDirs.MUNDANE:
            self.calcMunPDs()
        if self.options.subprimarydir == PrimDirs.ZODIACAL:
            self.calcZodPDs()
        if self.options.subprimarydir == PrimDirs.BOTH:
            self.calcMunPDs()
            self.calcZodPDs()

    def calcMunPDs(self):
        self.calcAscMC()
        if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
            self.calcAntiscia2AscMC()
            self.calcAntiscia2Planets(True)
        self.calcInterPlanetary(True)
        if self.chart.htype == chart.Chart.RADIX and self.options.pdparallels[0]:
            self.calcParallels()
            if self.options.pdantiscia:
                self.calcAntiscia2Parallels()
            if self.options.pduser and self.chart.userprompd != None:
                self.calcCustomer2Parallels()
        if self.options.primarydir == PrimDirs.PLACIDIANSEMIARC and self.options.pdparallels[1]:
            self.calcRaptParallels()
        if self.chart.htype == chart.Chart.RADIX and self.options.pdmidpoints:
            self.calcMidPoints()
        if self.options.sighouses:
            self.calc2HouseCusps(True)
            if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
                self.calcAntiscia2HouseCusps(True)
        if self.options.primarydir == PrimDirs.PLACIDIANSEMIARC and self.options.pdlof[1]:
            self.calcPlanets2MLoF()
            if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
                self.calcAntiscia2MLoF()
        if self.chart.htype == chart.Chart.RADIX and self.options.pduser and self.chart.userprompd != None:
            self.calcCustomer2AscMC(True)
            self.calcCustomerPlanetary(True)
            if self.options.primarydir == PrimDirs.PLACIDIANSEMIARC and self.options.pdlof[1]:
                self.calcCustomer2MLoF()
            if self.options.sighouses:
                self.calcCustomer2HouseCusps(True)
        if self.chart.htype == chart.Chart.RADIX and self.options.pduser2 and self.chart.usersigpd != None:
            self.calcPlanetary2Customer2(True)
            if self.options.pdantiscia:
                self.calcAntiscia2Customer2(True)
            if self.options.pdmidpoints:
                self.calcMidPoints2Customer2()
        return

    def calcZodPDs(self):
        self.calcZodAscMC()
        if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
            self.calcZodAntiscia2AscMC()
            self.calcAntiscia2Planets(False)
            if self.options.pduser2 and self.chart.usersigpd != None:
                self.calcAntiscia2Customer2(False)
        self.calcInterPlanetary(False)
        if self.chart.htype == chart.Chart.RADIX and self.options.pduser2 and self.chart.usersigpd != None:
            self.calcPlanetary2Customer2(False)
        if self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]:
            self.calcZodPromAspsInterPlanetary()
            if self.options.sighouses:
                self.calcZodPromAsps2HCs()
            if self.chart.htype == chart.Chart.RADIX and self.options.pduser2 and self.chart.usersigpd != None:
                self.calcZodPromAspsInterPlanetary2Customer2()
            if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
                self.calcZodPromAntisciaAspsInterPlanetary()
                if self.options.pduser2 and self.chart.usersigpd != None:
                    self.calcZodPromAntisciaAspsInterPlanetary2Customer2()
        if self.options.pdlof[0]:
            self.calcZodLoF2Planets()
            if self.chart.htype == chart.Chart.RADIX and self.options.pdsyzygy:
                self.calcZodLoF2Syzygy()
            if self.chart.htype == chart.Chart.RADIX and self.options.pduser2 and self.chart.usersigpd != None:
                self.calcZodLoF2Customer2()
        if self.options.pdlof[1]:
            self.calcZodPlanets2LoF()
            if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
                self.calcZodAntiscia2LoF()
        if self.chart.htype == chart.Chart.RADIX and self.options.pdsyzygy:
            self.calcZodPlanets2Syzygy()
            if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
                self.calcZodAntiscia2Syzygy()
        if self.chart.htype == chart.Chart.RADIX and self.options.pdparallels[0]:
            self.calcZodParallels()
            if self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]:
                self.calcZodParallelsAscMC()
                if self.options.pdlof[1]:
                    self.calcZodParallels2LoF()
                if self.options.pdsyzygy:
                    self.calcZodParallels2Syzygy()
            if self.options.zodpromsigasps[PrimDirs.PROMSTOSIGASPS]:
                if self.options.pdlof[0]:
                    self.calcZodLoF2ZodParallels()
        if self.chart.htype == chart.Chart.RADIX and self.options.pdmidpoints:
            self.calcZodMidPoints()
            self.calcZodMidPointsAscMC()
            if self.options.pdlof[1]:
                self.calcZodMidPoints2LoF()
            if self.options.pdsyzygy:
                self.calcZodMidPoints2Syzygy()
            if self.options.pduser2 and self.chart.usersigpd != None:
                self.calcZodMidPoints2Customer2()
        if self.options.sighouses:
            self.calc2HouseCusps(False)
            if self.options.pdlof[0]:
                self.calcZodLoF2HouseCusps()
            if self.chart.htype == chart.Chart.RADIX and self.options.pdantiscia:
                self.calcAntiscia2HouseCusps(False)
        if self.options.pdterms:
            self.calcZodTerms()
        if self.chart.htype == chart.Chart.RADIX and self.options.pdfixedstars:
            self.calcZodFixedStars2AscMC()
            self.calcZodFixedStars2Planets()
            if self.options.pdlof[1]:
                self.calcZodFixedStars2LoF()
            if self.options.pdsyzygy:
                self.calcZodFixedStars2Syzygy()
            if self.options.sighouses:
                self.calcZodFixedStars2HouseCusps()
            if self.options.pduser2 and self.chart.usersigpd != None:
                self.calcZodFixedStars2Customer2()
        if self.chart.htype == chart.Chart.RADIX and self.options.pduser and self.chart.userprompd != None:
            self.calcCustomer2AscMC(False)
            self.calcCustomerPlanetary(False)
            if self.options.pdlof[1]:
                self.calcZodCustomer2LoF()
            if self.options.pdsyzygy:
                self.calcZodCustomer2Syzygy()
            if self.options.sighouses:
                self.calcCustomer2HouseCusps(False)
        if self.options.ascmchcsasproms:
            if self.options.zodpromsigasps[PrimDirs.PROMSTOSIGASPS]:
                self.calcZodAsc2AspPlanets()
                if self.chart.htype == chart.Chart.RADIX and self.options.pdparallels[0]:
                    self.calcZodAsc2ParallelPlanets()
            self.calcZodAsc2Planets()
            if self.options.pdlof[1]:
                self.calcZodAsc2LoF()
            if self.chart.htype == chart.Chart.RADIX and self.options.pdsyzygy:
                self.calcZodAsc2Syzygy()
            if self.chart.htype == chart.Chart.RADIX and self.options.pduser2 and self.chart.usersigpd != None:
                self.calcZodAsc2Customer2()
            if self.options.sighouses:
                self.calcZodAsc2HCs()
            if self.options.sigascmc[1]:
                self.calcZodAsc2MC()
            if self.options.zodpromsigasps[PrimDirs.PROMSTOSIGASPS]:
                self.calcZodMC2AspPlanets()
                if self.chart.htype == chart.Chart.RADIX and self.options.pdparallels[0]:
                    self.calcZodMC2ParallelPlanets()
            self.calcZodMC2Planets()
            if self.options.pdlof[1]:
                self.calcZodMC2LoF()
            if self.chart.htype == chart.Chart.RADIX and self.options.pdsyzygy:
                self.calcZodMC2Syzygy()
            if self.chart.htype == chart.Chart.RADIX and self.options.pduser2 and self.chart.usersigpd != None:
                self.calcZodMC2Customer2()
            if self.options.sighouses:
                self.calcZodMC2HCs()
            if self.options.sigascmc[0]:
                self.calcZodMC2Asc()
        return

    def calcAscMC(self):
        """Calculates mundane directions to Asc-MC (mundane planets to Asc-MC)"""
        for i in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[i]:
                continue
            if self.abort.abort:
                return
            pl = self.chart.planets.planets[i]
            rapl = pl.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
            adlat = pl.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
            self.toAscMC(i, rapl, adlat)

    def calcAntiscia2AscMC(self):
        """Calculates mundane directions to Asc-MC (mundane antiscia to Asc-MC)"""
        for i in range(len(self.chart.antiscia.plantiscia)):
            if not self.options.promplanets[i]:
                continue
            if self.abort.abort:
                return
            ant = self.chart.antiscia.plantiscia[i]
            raant = ant.ra
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(ant.decl))
            if math.fabs(val) > 1.0:
                continue
            adlat = math.degrees(math.asin(val))
            self.toAscMC(PrimDir.ANTISCION + i, raant, adlat)

        for i in range(len(self.chart.antiscia.plcontraant)):
            if not self.options.promplanets[i]:
                continue
            if self.abort.abort:
                return
            ant = self.chart.antiscia.plcontraant[i]
            raant = ant.ra
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(ant.decl))
            if math.fabs(val) > 1.0:
                continue
            adlat = math.degrees(math.asin(val))
            self.toAscMC(PrimDir.CONTRAANT + i, raant, adlat)

    def toAscMC(self, idp, ra, adlat):
        if not self.options.pdaspects[chart.Chart.CONIUNCTIO]:
            return
        if self.options.sigascmc[1]:
            if idp == planets.Planets.MOON and self.options.pdsecmotion:
                for itera in range(self.options.pdsecmotioniter + 1):
                    ra, adlat = self.calcSM(idp, ra - self.ramc)

            self.create(True, idp, PrimDir.NONE, PrimDir.MC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, ra - self.ramc)
            if idp == planets.Planets.MOON and self.options.pdsecmotion:
                for itera in range(self.options.pdsecmotioniter + 1):
                    ra, adlat = self.calcSM(idp, ra - self.raic)

            self.create(True, idp, PrimDir.NONE, PrimDir.IC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, ra - self.raic)
        if self.options.sigascmc[0]:
            ao = ra - adlat
            if idp == planets.Planets.MOON and self.options.pdsecmotion:
                for itera in range(self.options.pdsecmotioniter + 1):
                    ra, adlat = self.calcSM(idp, ao - self.aoasc)
                    ao = ra - adlat

            self.create(True, idp, PrimDir.NONE, PrimDir.ASC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, ao - self.aoasc)
            do = ra + adlat
            if idp == planets.Planets.MOON and self.options.pdsecmotion:
                for itera in range(self.options.pdsecmotioniter + 1):
                    ra, adlat = self.calcSM(idp, do - self.dodesc)
                    do = ra + adlat

            self.create(True, idp, PrimDir.NONE, PrimDir.DESC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, do - self.dodesc)

    def calcCustomer2AscMC(self, mundane):
        lonpl = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        rapl = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
        adlat = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
        advalid = True
        if not mundane and self.options.subzodiacal != PrimDirs.SZPROMISSOR and self.options.subzodiacal != PrimDirs.SZBOTH:
            rapl, declpl, dist = astrology.swe_cotrans(lonpl, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declpl))
            if math.fabs(val) <= 1.0:
                adlat = math.degrees(math.asin(val))
            else:
                advalid = False
        if self.options.sigascmc[1]:
            self.create(mundane, PrimDir.USERPD, PrimDir.NONE, PrimDir.MC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, rapl - self.ramc)
            self.create(mundane, PrimDir.USERPD, PrimDir.NONE, PrimDir.IC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, rapl - self.raic)
        if self.options.sigascmc[0] and advalid:
            ao = rapl - adlat
            self.create(mundane, PrimDir.USERPD, PrimDir.NONE, PrimDir.ASC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, ao - self.aoasc)
            do = rapl + adlat
            self.create(mundane, PrimDir.USERPD, PrimDir.NONE, PrimDir.DESC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, do - self.dodesc)

    def calcSM(self, idp, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idp, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        ra = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
        adlat = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
        return (
         ra, adlat)

    def calcZodAscMC(self):
        """Calculates zodiacal directions to Asc-MC (zodiacal planets and their aspects to Asc-MC)"""
        SINISTER = 0
        DEXTER = 1
        for i in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[i]:
                continue
            pl = self.chart.planets.planets[i]
            self.toZodAscMC(pl.data[planets.Planet.LON], pl.data[planets.Planet.LAT], i, 0)

        if self.options.pdlof[0]:
            ralof = self.chart.fortune.fortune[fortune.Fortune.RA]
            decllof = self.chart.fortune.fortune[fortune.Fortune.DECL]
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllof))
            if self.options.sigascmc[1]:
                self.create(False, PrimDir.LOF, PrimDir.NONE, PrimDir.MC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, ralof - self.ramc)
                self.create(False, PrimDir.LOF, PrimDir.NONE, PrimDir.IC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, ralof - self.raic)
            if math.fabs(val) <= 1.0:
                adlat = math.degrees(math.asin(val))
                if self.options.sigascmc[0]:
                    aolof = ralof - adlat
                    self.create(False, PrimDir.LOF, PrimDir.NONE, PrimDir.ASC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, aolof - self.aoasc)
                    dolof = ralof + adlat
                    self.create(False, PrimDir.LOF, PrimDir.NONE, PrimDir.DESC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, dolof - self.dodesc)
        if self.options.pdterms:
            if self.options.sigascmc[0] or self.options.sigascmc[1]:
                num = len(self.options.terms[0])
                subnum = len(self.options.terms[0][0])
                for i in range(num):
                    summa = 0
                    for j in range(subnum):
                        self.options.terms[self.options.selterm][i][j][0]
                        lonterm = i * chart.Chart.SIGN_DEG + summa
                        if self.options.ayanamsha != 0:
                            lonterm += self.chart.ayanamsha
                            lonterm = util.normalize(lonterm)
                        raterm, declterm, dist = astrology.swe_cotrans(lonterm, 0.0, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declterm))
                        if math.fabs(val) > 1.0:
                            continue
                        adlat = math.degrees(math.asin(val))
                        if self.options.sigascmc[1]:
                            self.create(False, PrimDir.TERM + i, self.options.terms[self.options.selterm][i][j][0], PrimDir.MC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, raterm - self.ramc)
                        if self.options.sigascmc[0]:
                            aoterm = raterm - adlat
                            self.create(False, PrimDir.TERM + i, self.options.terms[self.options.selterm][i][j][0], PrimDir.ASC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, aoterm - self.aoasc)
                        summa += self.options.terms[self.options.selterm][i][j][1]

    def calcZodAntiscia2AscMC(self):
        """Calculates zodiacal directions to Asc-MC (zodiacal antiscia/contra and their aspects to Asc-MC)"""
        for i in range(len(self.chart.antiscia.plantiscia)):
            if not self.options.promplanets[i]:
                continue
            ant = self.chart.antiscia.plantiscia[i]
            lonant = ant.lon
            latant = ant.lat
            self.toZodAscMC(lonant, latant, i, PrimDir.ANTISCION)

        for i in range(len(self.chart.antiscia.plcontraant)):
            if not self.options.promplanets[i]:
                continue
            cant = self.chart.antiscia.plcontraant[i]
            loncant = cant.lon
            latcant = cant.lon
            self.toZodAscMC(loncant, latcant, i, PrimDir.CONTRAANT)

        if self.options.pdlof[0]:
            ant = self.chart.antiscia.lofant
            ralofant = ant.ra
            decllofant = ant.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllofant))
            if math.fabs(val) <= 1.0:
                adlat = math.degrees(math.asin(val))
                self.toZodAscMCSub(PrimDir.ANTISCIONLOF, ralofant, adlat)
            cant = self.chart.antiscia.lofcontraant
            ralofcant = ant.ra
            decllofcant = ant.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllofcant))
            if math.fabs(val) <= 1.0:
                adlat = math.degrees(math.asin(val))
                self.toZodAscMCSub(PrimDir.CONTRAANTLOF, ralofcant, adlat)
        for i in range(2):
            ant = self.chart.antiscia.ascmcant[i]
            raant = ant.ra
            declant = ant.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declant))
            if math.fabs(val) > 1.0:
                continue
            adlat = math.degrees(math.asin(val))
            typ = PrimDir.ANTISCIONASC
            if i > 0:
                typ = PrimDir.ANTISCIONMC
            self.toZodAscMCSub(typ, raant, adlat)

        for i in range(2):
            cant = self.chart.antiscia.ascmccontraant[i]
            racant = ant.ra
            declcant = ant.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declcant))
            if math.fabs(val) > 1.0:
                continue
            adlat = math.degrees(math.asin(val))
            typ = PrimDir.CONTRAANTASC
            if i > 0:
                typ = PrimDir.CONTRAANTMC
            self.toZodAscMCSub(typ, racant, adlat)

    def toZodAscMCSub(self, i, ra, adlat):
        if self.options.sigascmc[1]:
            self.create(False, i, PrimDir.NONE, PrimDir.MC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, ra - self.ramc)
            self.create(False, i, PrimDir.NONE, PrimDir.IC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, ra - self.raic)
        if self.options.sigascmc[0]:
            ao = ra - adlat
            self.create(False, i, PrimDir.NONE, PrimDir.ASC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, ao - self.aoasc)
            do = ra + adlat
            self.create(False, i, PrimDir.NONE, PrimDir.DESC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, do - self.dodesc)

    def toZodAscMC(self, pllon, pllat, i, ioffs):
        SINISTER = 0
        DEXTER = 1
        for j in range(chart.Chart.OPPOSITIO + 1):
            if not self.options.pdaspects[j]:
                continue
            if not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS] and j > chart.Chart.CONIUNCTIO:
                continue
            if i >= planets.Planets.PLANETS_NUM and j > chart.Chart.CONIUNCTIO:
                break
            if self.abort.abort:
                return
            aspectus = chart.Chart.Aspects[j]
            for k in range(DEXTER + 1):
                lon = 0.0
                if k == SINISTER:
                    lon = pllon + chart.Chart.Aspects[j]
                    if lon >= 360.0:
                        lon -= 360.0
                    aspectus = chart.Chart.Aspects[j]
                else:
                    if j == chart.Chart.CONIUNCTIO or j == chart.Chart.OPPOSITIO:
                        continue
                    lon = pllon - chart.Chart.Aspects[j]
                    if lon < 0.0:
                        lon += 360.0
                    aspectus = -chart.Chart.Aspects[j]
                rapl = 0.0
                adlat = 0.0
                if self.options.subzodiacal == PrimDirs.SZPROMISSOR or self.options.subzodiacal == PrimDirs.SZBOTH:
                    latprom = 0.0
                    if self.options.bianchini:
                        val = self.getBianchini(pllat, chart.Chart.Aspects[j])
                        if math.fabs(val) > 1.0:
                            continue
                        latprom = math.degrees(math.asin(val))
                    else:
                        latprom = pllat
                    rapl, declpl, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
                    val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declpl))
                    if math.fabs(val) > 1.0:
                        continue
                    adlat = math.degrees(math.asin(val))
                else:
                    rapl, declpl, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                    val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declpl))
                    if math.fabs(val) > 1.0:
                        continue
                    adlat = math.degrees(math.asin(val))
                if self.options.sigascmc[1]:
                    ok = True
                    if i == planets.Planets.MOON and ioffs == 0 and self.options.pdsecmotion:
                        for itera in range(self.options.pdsecmotioniter + 1):
                            ok, rapl, adlat = self.calcZodSM(i, j, aspectus, rapl - self.ramc)

                    if ok:
                        self.create(False, i + ioffs, PrimDir.NONE, PrimDir.MC, j, chart.Chart.CONIUNCTIO, rapl - self.ramc)
                    if (not self.options.pdaspects[chart.Chart.OPPOSITIO] or not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]) and j == chart.Chart.CONIUNCTIO:
                        ok = True
                        if i == planets.Planets.MOON and ioffs == 0 and self.options.pdsecmotion:
                            for itera in range(self.options.pdsecmotioniter + 1):
                                ok, rapl, adlat = self.calcZodSM(i, j, aspectus, rapl - self.raic)

                        if ok:
                            self.create(False, i + ioffs, PrimDir.NONE, PrimDir.IC, j, chart.Chart.CONIUNCTIO, rapl - self.raic)
                if self.options.sigascmc[0]:
                    aopl = rapl - adlat
                    ok = True
                    if i == planets.Planets.MOON and ioffs == 0 and self.options.pdsecmotion:
                        for itera in range(self.options.pdsecmotioniter + 1):
                            ok, rapl, adlat = self.calcZodSM(i, j, aspectus, aopl - self.aoasc)
                            aopl = rapl - adlat

                    if ok:
                        self.create(False, i + ioffs, PrimDir.NONE, PrimDir.ASC, j, chart.Chart.CONIUNCTIO, aopl - self.aoasc)
                    if (not self.options.pdaspects[chart.Chart.OPPOSITIO] or not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]) and j == chart.Chart.CONIUNCTIO:
                        dopl = rapl + adlat
                        ok = True
                        if i == planets.Planets.MOON and ioffs == 0 and self.options.pdsecmotion:
                            for itera in range(self.options.pdsecmotioniter + 1):
                                ok, rapl, adlat = self.calcZodSM(i, j, aspectus, dopl - self.dodesc)
                                dopl = rapl + adlat

                        if ok:
                            self.create(False, i + ioffs, PrimDir.NONE, PrimDir.DESC, j, chart.Chart.CONIUNCTIO, dopl - self.dodesc)

    def calcZodSM(self, idp, j, aspect, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idp, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        pllon = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        pllat = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LAT]
        lon = pllon + aspect
        lon = util.normalize(lon)
        rapl = 0.0
        adlat = 0.0
        if self.options.subzodiacal == PrimDirs.SZPROMISSOR or self.options.subzodiacal == PrimDirs.SZBOTH:
            latprom = 0.0
            if self.options.bianchini:
                val = self.getBianchini(pllat, chart.Chart.Aspects[j])
                if math.fabs(val) > 1.0:
                    return (False, 0.0, 0.0)
                latprom = math.degrees(math.asin(val))
            else:
                latprom = pllat
            rapl, declpl, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declpl))
            if math.fabs(val) > 1.0:
                return (False, 0.0, 0.0)
            adlat = math.degrees(math.asin(val))
        else:
            rapl, declpl, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declpl))
            if math.fabs(val) > 1.0:
                return (False, 0.0, 0.0)
            adlat = math.degrees(math.asin(val))
        return (True, rapl, adlat)

    def calcZodParallelsAscMC(self):
        NODES = 2
        for i in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[i]:
                continue
            ok = self.chart.zodpars.pars[i].valid
            points = self.chart.zodpars.pars[i].pts
            if not ok:
                continue
            for k in range(len(points)):
                if points[k][0] == -1.0:
                    continue
                if self.abort.abort:
                    return
                rapl, declpl, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declpl))
                if math.fabs(val) > 1.0:
                    continue
                adlat = math.degrees(math.asin(val))
                if self.options.sigascmc[1]:
                    self.create(False, i, PrimDir.NONE, PrimDir.MC, points[k][1], chart.Chart.CONIUNCTIO, rapl - self.ramc)
                if self.options.sigascmc[0]:
                    aopl = rapl - adlat
                    self.create(False, i, PrimDir.NONE, PrimDir.ASC, points[k][1], chart.Chart.CONIUNCTIO, aopl - self.aoasc)

    def calcZodAntisciaParallels2AscMC(self):
        self.calcZodAntisciaParallels2AscMCSub(self.chart.antzodpars.apars, PrimDir.ANTISCION)
        self.calcZodAntisciaParallels2AscMCSub(self.chart.antzodpars.cpars, PrimDir.CONTRAANT)

    def calcZodAntisciaParallels2AscMCSub(self, pars, ioffs):
        NODES = 2
        for i in range(len(pls) - NODES):
            if not self.options.promplanets[i]:
                continue
            ok = pars[i].valid
            points = pars[i].pts
            if not ok:
                continue
            for k in range(len(points)):
                if points[k][0] == -1.0:
                    continue
                if self.abort.abort:
                    return
                rapl, declpl, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declpl))
                if math.fabs(val) > 1.0:
                    continue
                adlat = math.degrees(math.asin(val))
                if self.options.sigascmc[1]:
                    self.create(False, i + ioffs, PrimDir.NONE, PrimDir.MC, points[k][1], chart.Chart.CONIUNCTIO, rapl - self.ramc)
                if self.options.sigascmc[0]:
                    aopl = rapl - adlat
                    self.create(False, i + ioffs, PrimDir.NONE, PrimDir.ASC, points[k][1], chart.Chart.CONIUNCTIO, aopl - self.aoasc)

    def calcZodMidPointsAscMC(self):
        """Calclucates zodiacal midpoint directions to Asc-MC"""
        mids = self.chart.midpoints.mids
        if self.options.subzodiacal == PrimDirs.SZPROMISSOR or self.options.subzodiacal == PrimDirs.SZBOTH:
            mids = self.chart.midpoints.midslat
        for mid in mids:
            if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
                continue
            if self.abort.abort:
                return
            raprom, declprom, dist = astrology.swe_cotrans(mid.m, mid.lat, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                continue
            adprom = math.degrees(math.asin(val))
            if self.options.sigascmc[1]:
                self.create(False, mid.p1, mid.p2, PrimDir.MC, chart.Chart.MIDPOINT, chart.Chart.CONIUNCTIO, raprom - self.ramc)
                self.create(False, mid.p1, mid.p2, PrimDir.IC, chart.Chart.MIDPOINT, chart.Chart.CONIUNCTIO, raprom - self.raic)
            if self.options.sigascmc[0]:
                aoprom = raprom - adprom
                self.create(False, mid.p1, mid.p2, PrimDir.ASC, chart.Chart.MIDPOINT, chart.Chart.CONIUNCTIO, aoprom - self.aoasc)
                doprom = raprom + adprom
                self.create(False, mid.p1, mid.p2, PrimDir.DESC, chart.Chart.MIDPOINT, chart.Chart.CONIUNCTIO, doprom - self.dodesc)

    def calcZodAsc2MC(self):
        lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
        SINISTER = 0
        DEXTER = 1
        for i in range(chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO + 1):
            if not self.options.pdaspects[i]:
                continue
            if not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS] and i > chart.Chart.CONIUNCTIO:
                break
            if self.abort.abort:
                return
            for k in range(DEXTER + 1):
                lon = 0.0
                if k == SINISTER:
                    lon = util.normalize(lonprom + chart.Chart.Aspects[i])
                else:
                    if i == chart.Chart.CONIUNCTIO or i == chart.Chart.OPPOSITIO:
                        continue
                    lon = util.normalize(lonprom - chart.Chart.Aspects[i])
                ra, decl, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                self.create(False, PrimDir.ASC, PrimDir.NONE, PrimDir.MC, i, chart.Chart.CONIUNCTIO, ra - self.ramc)
                if (not self.options.pdaspects[chart.Chart.OPPOSITIO] or not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]) and i == chart.Chart.CONIUNCTIO:
                    self.create(False, PrimDir.ASC, PrimDir.NONE, PrimDir.IC, i, chart.Chart.CONIUNCTIO, ra - self.raic)

    def calcZodParallelAsc2MCAsc(self):
        lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
        raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        ok, points = self.getEclPoints(lonprom, declprom, True)
        if not ok:
            return
        for k in range(len(points)):
            if points[k][0] == -1.0:
                continue
            if self.abort.abort:
                return
            rapl, declpl, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declpl))
            if math.fabs(val) > 1.0:
                continue
            adlat = math.degrees(math.asin(val))
            if self.options.sigascmc[1]:
                self.create(False, PrimDir.ASC, PrimDir.NONE, PrimDir.MC, points[k][1], chart.Chart.CONIUNCTIO, rapl - self.ramc)
            if self.options.sigascmc[0]:
                aopl = rapl - adlat
                self.create(False, PrimDir.ASC, PrimDir.NONE, PrimDir.ASC, points[k][1], chart.Chart.CONIUNCTIO, aopl - self.aoasc)

    def calcZodAspAsc2Asc(self):
        lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
        SINISTER = 0
        DEXTER = 1
        for i in range(chart.Chart.CONIUNCTIO + 1, chart.Chart.OPPOSITIO):
            if not self.options.pdaspects[i]:
                continue
            if self.abort.abort:
                return
            for k in range(DEXTER + 1):
                lon = 0.0
                if k == SINISTER:
                    lon = util.normalize(lonprom + chart.Chart.Aspects[i])
                else:
                    if i == chart.Chart.OPPOSITIO:
                        continue
                    lon = util.normalize(lonprom - chart.Chart.Aspects[i])
                ra, decl, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decl))
                if math.fabs(val) > 1.0:
                    continue
                adlat = math.degrees(math.asin(val))
                ao = ra - adlat
                self.create(False, PrimDir.ASC, PrimDir.NONE, PrimDir.ASC, i, chart.Chart.CONIUNCTIO, ao - self.aoasc)

    def calcZodMC2Asc(self):
        lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
        SINISTER = 0
        DEXTER = 1
        for i in range(chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO + 1):
            if not self.options.pdaspects[i]:
                continue
            if not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS] and i > chart.Chart.CONIUNCTIO:
                continue
            if self.abort.abort:
                return
            for k in range(DEXTER + 1):
                lon = 0.0
                if k == SINISTER:
                    lon = util.normalize(lonprom + chart.Chart.Aspects[i])
                else:
                    if i == chart.Chart.CONIUNCTIO or i == chart.Chart.OPPOSITIO:
                        continue
                    lon = util.normalize(lonprom - chart.Chart.Aspects[i])
                ra, decl, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decl))
                if math.fabs(val) > 1.0:
                    continue
                adlat = math.degrees(math.asin(val))
                aoprom = ra - adlat
                self.create(False, PrimDir.MC, PrimDir.NONE, PrimDir.ASC, i, chart.Chart.CONIUNCTIO, aoprom - self.aoasc)
                if (not self.options.pdaspects[chart.Chart.OPPOSITIO] or not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]) and i == chart.Chart.CONIUNCTIO:
                    doprom = ra + adlat
                    self.create(False, PrimDir.MC, PrimDir.NONE, PrimDir.DESC, i, chart.Chart.CONIUNCTIO, doprom - self.dodesc)

    def calcZodParallelMC2AscMC(self):
        lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
        raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        ok, points = self.getEclPoints(lonprom, declprom, True)
        if not ok:
            return
        for k in range(len(points)):
            if points[k][0] == -1.0:
                continue
            if self.abort.abort:
                return
            rapl, declpl, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declpl))
            if math.fabs(val) > 1.0:
                continue
            adlat = math.degrees(math.asin(val))
            if self.options.sigascmc[1]:
                self.create(False, PrimDir.MC, PrimDir.NONE, PrimDir.MC, points[k][1], chart.Chart.CONIUNCTIO, rapl - self.ramc)
            if self.options.sigascmc[0]:
                aopl = rapl - adlat
                self.create(False, PrimDir.MC, PrimDir.NONE, PrimDir.ASC, points[k][1], chart.Chart.CONIUNCTIO, aopl - self.aoasc)

    def calcZodAspMC2MC(self):
        lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
        SINISTER = 0
        DEXTER = 1
        for i in range(chart.Chart.CONIUNCTIO + 1, chart.Chart.OPPOSITIO):
            if not self.options.pdaspects[i]:
                continue
            if self.abort.abort:
                return
            for k in range(DEXTER + 1):
                lon = 0.0
                if k == SINISTER:
                    lon = util.normalize(lonprom + chart.Chart.Aspects[i])
                else:
                    if i == chart.Chart.OPPOSITIO:
                        continue
                    lon = util.normalize(lonprom - chart.Chart.Aspects[i])
                ra, decl, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                self.create(False, PrimDir.MC, PrimDir.NONE, PrimDir.MC, i, chart.Chart.CONIUNCTIO, ra - self.ramc)

    def calcZodFixedStars2AscMC(self):
        """Calculates zodiacal directions of fixedstars to Asc-MC"""
        OFFS = PrimDir.FIXEDSTAR
        for i in range(len(self.chart.fixedstars.data)):
            if not self.options.pdfixedstarssel[self.chart.fixedstars.mixed[i]]:
                continue
            if self.abort.abort:
                return
            star = self.chart.fixedstars.data[i]
            lonstar = star[fixedstars.FixedStars.LON]
            rastar = star[fixedstars.FixedStars.RA]
            declstar = star[fixedstars.FixedStars.DECL]
            if self.options.subzodiacal != PrimDirs.SZPROMISSOR and self.options.subzodiacal != PrimDirs.SZBOTH:
                rastar, declstar, dist = astrology.swe_cotrans(lonstar, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declstar))
            advalid = True
            adlat = 0.0
            if math.fabs(val) > 1.0:
                advalid = False
            else:
                adlat = math.degrees(math.asin(val))
            if self.options.sigascmc[1]:
                self.create(False, i + OFFS, PrimDir.NONE, PrimDir.MC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, rastar - self.ramc)
                self.create(False, i + OFFS, PrimDir.NONE, PrimDir.IC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, rastar - self.raic)
            if self.options.sigascmc[0] and advalid:
                aostar = rastar - adlat
                self.create(False, i + OFFS, PrimDir.NONE, PrimDir.ASC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, aostar - self.aoasc)
                dostar = rastar + adlat
                self.create(False, i + OFFS, PrimDir.NONE, PrimDir.DESC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, dostar - self.dodesc)

    def calcMidPoints(self):
        """Computes mundane midpoints to significators"""
        MP = placspec.PlacidianSpeculum.PMP
        SPECULUM = planets.Planet.PLACIDIAN
        RA = placspec.PlacidianSpeculum.RA
        DECL = placspec.PlacidianSpeculum.DECL
        if self.options.primarydir == PrimDirs.REGIOMONTAN:
            MP = regiospec.RegiomontanianSpeculum.W
            SPECULUM = planets.Planet.REGIOMONTANIAN
            RA = regiospec.RegiomontanianSpeculum.RA
            DECL = regiospec.RegiomontanianSpeculum.DECL
        if self.options.primarydir == PrimDirs.CAMPANIAN:
            MP = regiospec.RegiomontanianSpeculum.CMP
            SPECULUM = planets.Planet.REGIOMONTANIAN
            RA = regiospec.RegiomontanianSpeculum.RA
            DECL = regiospec.RegiomontanianSpeculum.DECL
        for p1 in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[p1]:
                continue
            plprom1 = self.chart.planets.planets[p1]
            raprom1 = plprom1.speculums[SPECULUM].speculum[RA]
            declprom1 = plprom1.speculums[SPECULUM].speculum[DECL]
            for p2 in range(p1 + 1, planets.Planets.BODIES_NUM):
                if not self.options.promplanets[p2]:
                    continue
                if p1 == planets.Planets.ANODE and p2 == planets.Planets.DNODE or p1 == planets.Planets.DNODE and p2 == planets.Planets.ANODE:
                    continue
                plprom2 = self.chart.planets.planets[p2]
                raprom2 = plprom2.speculums[SPECULUM].speculum[RA]
                declprom2 = plprom2.speculums[SPECULUM].speculum[DECL]
                ramid = util.normalize((raprom1 + raprom2) / 2.0)
                for s in range(planets.Planets.BODIES_NUM):
                    if not self.options.sigplanets[s]:
                        continue
                    if self.abort.abort:
                        return
                    plsig = self.chart.planets.planets[s]
                    rasig = plsig.speculums[SPECULUM].speculum[RA]
                    declsig = plsig.speculums[SPECULUM].speculum[DECL]
                    mpsig = plsig.speculums[SPECULUM].speculum[MP]
                    if math.fabs(ramid - rasig) > 90.0:
                        ramid += 180.0
                        if ramid >= 360.0:
                            ramid -= 360.0
                    arc = self.getDiff(ramid - rasig)
                    LIM = 30
                    x = 0
                    good = True
                    while x < LIM:
                        initarc = arc
                        ok, arc = self.iterate(raprom1, declprom1, raprom2, declprom2, mpsig, arc, plsig)
                        if not ok:
                            good = False
                            break
                        arc = self.getDiff(arc)
                        x += 1
                        if math.fabs(math.fabs(arc) - initarc) < 0.001:
                            break
                        if self.abort.abort:
                            return

                    if not good:
                        continue
                    if x == LIM:
                        arc = (arc + initarc) / 2.0
                    self.create(True, p1, p2, s, chart.Chart.MIDPOINT, chart.Chart.CONIUNCTIO, arc)

    def calcMidPoints2Customer2(self):
        """Computes mundane midpoints to Customer2"""
        NODES = 2
        MP = placspec.PlacidianSpeculum.PMP
        SPECULUM = planets.Planet.PLACIDIAN
        RA = placspec.PlacidianSpeculum.RA
        DECL = placspec.PlacidianSpeculum.DECL
        if self.options.primarydir == PrimDirs.REGIOMONTAN:
            MP = regiospec.RegiomontanianSpeculum.W
            SPECULUM = planets.Planet.REGIOMONTANIAN
            RA = regiospec.RegiomontanianSpeculum.RA
            DECL = regiospec.RegiomontanianSpeculum.DECL
        if self.options.primarydir == PrimDirs.CAMPANIAN:
            MP = regiospec.RegiomontanianSpeculum.CMP
            SPECULUM = planets.Planet.REGIOMONTANIAN
            RA = regiospec.RegiomontanianSpeculum.RA
            DECL = regiospec.RegiomontanianSpeculum.DECL
        for p1 in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[p1]:
                continue
            plprom1 = self.chart.planets.planets[p1]
            raprom1 = plprom1.speculums[SPECULUM].speculum[RA]
            declprom1 = plprom1.speculums[SPECULUM].speculum[DECL]
            for p2 in range(p1 + 1, planets.Planets.BODIES_NUM):
                if not self.options.promplanets[p2]:
                    continue
                if p1 == planets.Planets.ANODE and p2 == planets.Planets.DNODE or p1 == planets.Planets.DNODE and p2 == planets.Planets.ANODE:
                    continue
                plprom2 = self.chart.planets.planets[p2]
                raprom2 = plprom2.speculums[SPECULUM].speculum[RA]
                declprom2 = plprom2.speculums[SPECULUM].speculum[DECL]
                ramid = util.normalize((raprom1 + raprom2) / 2.0)
                if self.abort.abort:
                    return
                rasig = self.chart.usersigpd.speculums[SPECULUM].speculum[RA]
                declsig = self.chart.usersigpd.speculums[SPECULUM].speculum[DECL]
                mpsig = self.chart.usersigpd.speculums[SPECULUM].speculum[MP]
                if math.fabs(ramid - rasig) > 90.0:
                    ramid += 180.0
                    if ramid >= 360.0:
                        ramid -= 360.0
                arc = self.getDiff(ramid - rasig)
                LIM = 30
                x = 0
                good = True
                while x < LIM:
                    initarc = arc
                    ok, arc = self.iterate(raprom1, declprom1, raprom2, declprom2, mpsig, arc, plprom1)
                    if not ok:
                        good = False
                        break
                    arc = self.getDiff(arc)
                    x += 1
                    if math.fabs(math.fabs(arc) - initarc) < 0.001:
                        break
                    if self.abort.abort:
                        return

                if not good:
                    continue
                if x == LIM:
                    arc = (arc + initarc) / 2.0
                self.create(True, p1, p2, PrimDir.USERPD, chart.Chart.MIDPOINT, chart.Chart.CONIUNCTIO, arc)

    def iterate(self, raprom1, declprom1, raprom2, declprom2, mpsig, arc, pl):
        raprom1comma = util.normalize(raprom1 - arc)
        declprom1comma = declprom1
        raprom2comma = util.normalize(raprom2 - arc)
        declprom2comma = declprom2
        ok, mpp1comma = self.calcMP(raprom1comma, declprom1comma, pl)
        if not ok:
            return (False, 0.0)
        ok, mpp2comma = self.calcMP(raprom2comma, declprom2comma, pl)
        if not ok:
            return (False, 0.0)
        mppmidcomma = util.normalize((mpp1comma + mpp2comma) / 2.0)
        if math.fabs(mppmidcomma - mpsig) > 90.0:
            mppmidcomma += 180.0
            if mppmidcomma >= 360.0:
                mppmidcomma -= 360.0
        dmp = self.getDiff(mppmidcomma - mpsig)
        ok, mpp1 = self.calcMP(raprom1, declprom1, pl)
        if not ok:
            return (False, 0.0)
        darc = dmp * self.getDiff(raprom1 - raprom1comma) / self.getDiff(mpp1 - mpp1comma)
        return (
         True, arc + darc)

    def getEclPoints(self, lon, decl, onEcl):
        """Calculates points of the Ecliptic from declination"""
        PARALLEL = chart.Chart.PARALLEL
        CONTRAPARALLEL = chart.Chart.CONTRAPARALLEL
        origdecl = decl
        if decl < 0.0:
            decl *= -1
        if decl > self.chart.obl[0]:
            return (False, ((-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL)))
        if onEcl:
            if decl == self.chart.obl[0]:
                lon += 180.0
                lon = util.normalize(lon)
                return (
                 True, ((lon, CONTRAPARALLEL), (-1.0, PARALLEL)))
            else:
                lon1 = lon + 180.0
                lon1 = util.normalize(lon1)
                lon2 = 360.0 - lon1
                lon3 = util.normalize(lon2 + 180.0)
                return (True, ((lon1, CONTRAPARALLEL), (lon2, PARALLEL), (lon3, CONTRAPARALLEL)))

        elif decl == self.chart.obl[0]:
            val = math.sin(math.radians(origdecl)) / math.sin(math.radians(self.chart.obl[0]))
            if math.fabs(val) <= 1.0:
                lon1 = math.degrees(math.asin(val))
                lon1 = util.normalize(lon1)
                lon2 = util.normalize(lon1 + 180.0)
                return (
                 True, ((lon1, PARALLEL), (lon2, CONTRAPARALLEL)))
            return (False, ((-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL)))
        else:
            val = math.sin(math.radians(origdecl)) / math.sin(math.radians(self.chart.obl[0]))
            if math.fabs(val) <= 1.0:
                lon1 = math.degrees(math.asin(val))
                lon1 = util.normalize(lon1)
                lon2 = util.normalize(lon1 + 180.0)
                lon3 = 360.0 - lon2
                lon4 = util.normalize(lon3 + 180.0)
                return (
                 True, ((lon1, PARALLEL), (lon2, CONTRAPARALLEL), (lon3, PARALLEL), (lon4, CONTRAPARALLEL)))
            return (False, ((-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL)))
        return (False, ((-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL)))

    def getBianchini(self, lat, asp):
        return math.sin(math.radians(lat)) * math.cos(math.radians(asp))

    def create(self, mundane, prom, prom2, sig, promasp, sigasp, arc, parallelaxis=0):
        """Creates a direction and pushes it into the list of directions"""
        if self.chart.htype == chart.Chart.RADIX:
            if arc <= -360.0:
                arc += 360.0
            if arc >= 360.0:
                arc -= 360.0
            direct = True
            if arc < 0.0:
                arc *= -1
                direct = False
            if arc > 180.0:
                arc = 360.0 - arc
                direct = not direct
            lim = PrimDirs.LIMIT
        else:
            direct = True
            if arc < 0.0:
                arc *= -1
                direct = False
            if arc > 180.0:
                arc = 360.0 - arc
                direct = not direct
            lim = PrimDirs.REVOLUTIO
            if (arc < lim or arc > -lim) and self.direction == PrimDirs.DIRECT and direct or self.direction == PrimDirs.CONVERSE and not direct:
                time, age = self.calcTimeRev(arc)
                pd = PrimDir()
                pd.mundane = mundane
                pd.prom = prom
                pd.prom2 = prom2
                pd.sig = sig
                pd.promasp = promasp
                pd.sigasp = sigasp
                pd.arc = arc
                pd.direct = direct
                pd.parallelaxis = parallelaxis
                pd.time = time
                pd.age = age
                self.pds.append(pd)
            arc = 360.0 - arc
            direct = not direct
        if arc >= lim or arc <= -lim or self.direction == PrimDirs.DIRECT and not direct or self.direction == PrimDirs.CONVERSE and direct:
            return
        if self.chart.htype == chart.Chart.RADIX:
            time, age = self.calcTime(arc, direct)
        else:
            time, age = self.calcTimeRev(arc)
        if self.chart.htype == chart.Chart.RADIX and (age < PrimDirs.Ranges[self.pdrange][PrimDirs.LOW] or age >= PrimDirs.Ranges[self.pdrange][PrimDirs.HIGH]):
            return
        pd = PrimDir()
        pd.mundane = mundane
        pd.prom = prom
        pd.prom2 = prom2
        pd.sig = sig
        pd.promasp = promasp
        pd.sigasp = sigasp
        pd.arc = arc
        pd.direct = direct
        pd.parallelaxis = parallelaxis
        pd.time = time
        pd.age = age
        self.pds.append(pd)

    def calcTime(self, arc, direct):
        """Calculates time from arc according to the selected key (dynamic or static)"""
        ti = 0.0
        if self.options.pdkeydyn:
            if self.options.pdkeyd == PrimDirs.TRUESOLAREQUATORIALARC or self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
                if not direct and self.options.useregressive:
                    ti = self.calcTrueSolarArcRegressive(arc)
                else:
                    ti = self.calcTrueSolarArc(arc)
            else:
                ti = self.calcBirthSolarArc(arc)
        elif self.options.pdkeys == PrimDirs.USER:
            val = self.options.pdkeydeg + self.options.pdkeymin / 60.0 + self.options.pdkeysec / 3600.0
            if val != 0.0:
                coeff = 1.0 / val
                ti = arc * coeff
        else:
            ti = arc * PrimDirs.staticData[self.options.pdkeys][PrimDirs.COEFF]
        return (self.chart.time.jd + ti * 365.2421904, ti)

    def calcTrueSolarArc(self, arc):
        LIM = 120.0
        y = self.chart.time.year
        m = self.chart.time.month
        d = self.chart.time.day
        h, mi, s = util.decToDeg(self.chart.time.time)
        tt = 0.0
        prSunPos = self.chart.planets.planets[planets.Planets.SUN].dataEqu[planets.Planet.RAEQU]
        if self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
            prSunPos = self.chart.planets.planets[planets.Planets.SUN].data[planets.Planet.LON]
        prSunPosEnd = prSunPos + arc
        transition = False
        if prSunPosEnd >= 360.0:
            transition = True
        while prSunPos <= prSunPosEnd:
            y, m, d = util.incrDay(y, m, d)
            ti = chart.Time(y, m, d, 0, 0, 0, False, self.chart.time.cal, chart.Time.GREENWICH, True, 0, 0, False, self.chart.place, False)
            sun = planets.Planet(ti.jd, planets.Planets.SUN, astrology.SEFLG_SWIEPH)
            pos = sun.dataEqu[planets.Planet.RAEQU]
            if self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
                pos = sun.data[planets.Planet.LON]
            if transition and pos < LIM:
                pos += 360.0
            prSunPos = pos
            if self.abort.abort:
                return 0.0

        if prSunPos != prSunPosEnd:
            y, m, d = util.decrDay(y, m, d)
            if transition:
                prSunPosEnd -= 360.0
            trlon = 0.0
            if self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
                trlon = prSunPosEnd
            else:
                trlon = util.ra2ecl(prSunPosEnd, self.chart.obl[0])
            trans = transits.Transits()
            trans.day(y, m, d, self.chart, planets.Planets.SUN, trlon)
            if len(trans.transits) > 0:
                tt = trans.transits[0].time
        else:
            tt = 0.0
        d1 = datetime.datetime(self.chart.time.year, self.chart.time.month, self.chart.time.day, h, mi, s)
        th, tm, ts = util.decToDeg(tt)
        d2 = datetime.datetime(y, m, d, th, tm, ts)
        diff = d2 - d1
        ddays = diff.days
        dtime = diff.seconds / 3600.0
        dtimeindays = dtime / 24.0
        tt = ddays + dtimeindays
        return tt

    def calcTrueSolarArcRegressive(self, arc):
        LIM = 120.0
        y = self.chart.time.year
        m = self.chart.time.month
        d = self.chart.time.day
        h, mi, s = util.decToDeg(self.chart.time.time)
        tt = 0.0
        prSunPos = self.chart.planets.planets[planets.Planets.SUN].dataEqu[planets.Planet.RAEQU]
        if self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
            prSunPos = self.chart.planets.planets[planets.Planets.SUN].data[planets.Planet.LON]
        prSunPosEnd = prSunPos - arc
        transition = False
        if prSunPosEnd < 0.0:
            prSunPos += 360.0
            prSunPosEnd += 360.0
            transition = True
        while prSunPos >= prSunPosEnd:
            y, m, d = util.decrDay(y, m, d)
            ti = chart.Time(y, m, d, 0, 0, 0, False, self.chart.time.cal, chart.Time.GREENWICH, True, 0, 0, False, self.chart.place, False)
            sun = planets.Planet(ti.jd, planets.Planets.SUN, astrology.SEFLG_SWIEPH)
            pos = sun.dataEqu[planets.Planet.RAEQU]
            if self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
                pos = sun.data[planets.Planet.LON]
            if transition and pos < LIM:
                pos += 360.0
            prSunPos = pos
            if self.abort.abort:
                return 0.0

        if prSunPos != prSunPosEnd:
            if transition:
                prSunPosEnd -= 360.0
            trlon = 0.0
            if self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC:
                trlon = prSunPosEnd
            else:
                trlon = util.ra2ecl(prSunPosEnd, self.chart.obl[0])
            trans = transits.Transits()
            trans.day(y, m, d, self.chart, planets.Planets.SUN, trlon)
            if len(trans.transits) > 0:
                tt = trans.transits[0].time
        else:
            tt = 0.0
        th, tm, ts = util.decToDeg(tt)
        d1 = datetime.datetime(y, m, d, th, tm, ts)
        d2 = datetime.datetime(self.chart.time.year, self.chart.time.month, self.chart.time.day, h, mi, s)
        diff = d2 - d1
        ddays = diff.days
        dtime = diff.seconds / 3600.0
        dtimeindays = dtime / 24.0
        tt = ddays + dtimeindays
        return tt

    def calcBirthSolarArc(self, arc):
        y = self.chart.time.year
        m = self.chart.time.month
        d = self.chart.time.day
        yn, mn, dn = util.incrDay(y, m, d)
        ti1 = chart.Time(y, m, d, 0, 0, 0, False, self.chart.time.cal, chart.Time.LOCALMEAN, True, 0, 0, False, self.chart.place, False)
        ti2 = chart.Time(yn, mn, dn, 0, 0, 0, False, self.chart.time.cal, chart.Time.LOCALMEAN, True, 0, 0, False, self.chart.place, False)
        sun1 = planets.Planet(ti1.jd, planets.Planets.SUN, astrology.SEFLG_SWIEPH)
        sun2 = planets.Planet(ti2.jd, planets.Planets.SUN, astrology.SEFLG_SWIEPH)
        diff = 0.0
        if self.options.pdkeyd == PrimDirs.BIRTHDAYSOLAREQUATORIALARC:
            diff = sun2.dataEqu[planets.Planet.RAEQU] - sun1.dataEqu[planets.Planet.RAEQU]
        elif self.options.pdkeyd == PrimDirs.BIRTHDAYSOLARECLIPTICALARC:
            diff = sun2.data[planets.Planet.LON] - sun1.data[planets.Planet.LON]
        coeff = 0.0
        if diff != 0.0:
            coeff = 1.0 / diff
        return arc * coeff

    def calcTimeRev(self, arc):
        """Calculates time from arc in Revolutions (Solar, Lunar)"""
        if self.chart.htype == chart.Chart.SOLAR:
            ti = arc * PrimDirs.staticData[0][PrimDirs.COEFF] / 365.2421904
        else:
            ti = arc * 0.0758333 / 360.0
        return (self.chart.time.jd + ti * 365.2421904, ti)

    def sort(self):
        for j in range(len(self.pds)):
            for i in range(len(self.pds) - 1):
                if self.abort.abort:
                    return
                if self.pds[i].time > self.pds[(i + 1)].time:
                    tmp = self.pds[i]
                    self.pds[i] = self.pds[(i + 1)]
                    self.pds[i + 1] = tmp

    def qsort(self, L):
        if L == []:
            return []
        return self.qsort([ x for x in L[1:] if x.time < L[0].time ]) + L[0:1] + self.qsort([ x for x in L[1:] if x.time >= L[0].time ])

    def getDiff(self, diff):
        direct = True
        if diff < 0.0:
            diff *= -1
            direct = False
        if diff > 180.0:
            diff = 360.0 - diff
            direct = not direct
        if not direct:
            diff *= -1
        return diff

    def print2file(self, fname):
        bodies = (
         mtexts.txtscommon['Saturn'], mtexts.txtscommon['Jupiter'], mtexts.txtscommon['Mars'], mtexts.txtscommon['Sun'], mtexts.txtscommon['Venus'], mtexts.txtscommon['Mercury'], mtexts.txtscommon['Moon'], mtexts.txtscommon['ANode'], mtexts.txtscommon['DNode'], 'Asc', 'Desc', 'MC', 'IC', 'HC2', 'HC3', 'HC5', 'HC6', 'HC8', 'HC9', 'HC11', 'HC12', mtexts.txtscommon['LoF'], mtexts.txtscommon['Syzygy'], mtexts.txtscommon['User'])
        signs = ['(Aries)', '(Taurus)', '(Gemini)', '(Cancer)', '(Leo)', '(Virgo)', '(Libra)', '(Scorpio)', '(Sagittarius)', '(Capricornus)', '(Aquarius)', '(Pisces)']
        aspects = (mtexts.txtscommon['Conjunction'], mtexts.txtscommon['Sextile'], mtexts.txtscommon['Square'], mtexts.txtscommon['Trine'], mtexts.txtscommon['Opposition'], mtexts.txtscommon['Parallel'], mtexts.txtscommon['ContraParallel'], mtexts.txtscommon['MidPoint'])
        pdsystem = (
         mtexts.txtsprimdirsdlg['PlacidianSemiArc'], mtexts.txtsprimdirsdlg['PlacidianUnderThePole'], mtexts.txtsprimdirsdlg['Regiomontanian'])
        pdkeysdyn = (mtexts.txtsprimarykeysdlg['TrueSolarEquatorialArc'], mtexts.txtsprimarykeysdlg['BirthdaySolarEquatorialArc'], mtexts.txtsprimarykeysdlg['TrueSolarEclipticalArc'], mtexts.txtsprimarykeysdlg['BirthdaySolarEclipticalArc'])
        pdkeysstat = (mtexts.txtsprimarykeysdlg['Naibod'], mtexts.txtsprimarykeysdlg['Cardan'], mtexts.txtsprimarykeysdlg['Ptolemy'], mtexts.txtsprimarykeysdlg['User'])
        lines = []
        lines.append(pdsystem[self.options.primarydir])
        lines.append('\n')
        if self.options.pdkeydyn:
            lines.append(mtexts.txtscommon['DynamicKey'] + ':\n')
            lines.append(pdkeysdyn[self.options.pdkeyd])
            lines.append('\n')
        else:
            deg = self.options.pdkeydeg
            minu = self.options.pdkeymin
            sec = self.options.pdkeysec
            if self.options.pdkeys != PrimDirs.USER:
                deg = PrimDirs.staticData[self.options.pdkeys][PrimDirs.DEG]
                minu = PrimDirs.staticData[self.options.pdkeys][PrimDirs.MIN]
                sec = PrimDirs.staticData[self.options.pdkeys][PrimDirs.SEC]
            lines.append(mtexts.txtscommon['StaticKey'] + ':\n')
            txt = pdkeysstat[self.options.pdkeys] + ' ' + str(deg) + mtexts.txtscommon['DegPDList'] + ' ' + str(minu).zfill(2) + mtexts.txtscommon['MinPDList'] + ' ' + str(sec).zfill(2) + mtexts.txtscommon['SecPDList']
            lines.append(txt)
            lines.append('\n')
        for pd in self.pds:
            mtxt = mtexts.txtsprimdirslist['M']
            if not pd.mundane:
                mtxt = mtexts.txtsprimdirslist['Z']
            dirtxt = mtexts.txtsprimdirslist['D']
            if not pd.direct:
                dirtxt = mtexts.txtsprimdirslist['C']
            y, m, d, h = astrology.swe_revjul(pd.time, 1)
            formattxt = '%s '
            tuptxt = [mtxt]
            if pd.promasp == chart.Chart.MIDPOINT or pd.sigasp == chart.Chart.RAPTPAR or pd.sigasp == chart.Chart.RAPTCONTRAPAR:
                formattxt += '%s %s '
                tuptxt.append(bodies[pd.prom])
                tuptxt.append(bodies[pd.prom2])
            elif pd.prom >= PrimDir.ANTISCION and pd.prom < PrimDir.TERM:
                if pd.promasp != chart.Chart.CONIUNCTIO:
                    formattxt += '%s '
                    tuptxt.append(aspects[pd.promasp])
                anttxt = mtexts.txtscommon['Antiscion']
                if pd.prom >= PrimDir.CONTRAANT:
                    anttxt = mtexts.txtscommon['Contraantiscion']
                formattxt += '%s '
                tuptxt.append(anttxt)
                promtxt = ''
                antoffs = PrimDir.ANTISCION
                if pd.prom >= PrimDir.CONTRAANT:
                    antoffs = PrimDir.CONTRAANT
                if pd.prom == PrimDir.ANTISCIONLOF or pd.prom == PrimDir.CONTRAANTLOF:
                    promtxt = bodies[(pd.prom - antoffs)]
                elif pd.prom == PrimDir.ANTISCIONASC or pd.prom == PrimDir.CONTRAANTASC:
                    promtxt = mtexts.txtscommon['Asc']
                elif pd.prom == PrimDir.ANTISCIONMC or pd.prom == PrimDir.CONTRAANTMC:
                    promtxt = mtexts.txtscommon['MC']
                else:
                    promtxt = bodies[(pd.prom - antoffs)]
                formattxt += '%s '
                tuptxt.append(promtxt)
            elif pd.prom >= PrimDir.TERM and pd.prom < PrimDir.FIXEDSTAR:
                formattxt += '%s%s '
                tuptxt.append(signs[(pd.prom - PrimDir.TERM)])
                tuptxt.append(bodies[pd.prom2])
            elif pd.prom >= PrimDir.FIXEDSTAR:
                formattxt += '%s '
                promtxt = self.chart.fixedstars.data[(pd.prom - PrimDir.FIXEDSTAR)][fixedstars.FixedStars.NOMNAME]
                tradname = self.chart.fixedstars.data[(pd.prom - PrimDir.FIXEDSTAR)][fixedstars.FixedStars.NAME].strip()
                if tradname != '':
                    promtxt = tradname
                tuptxt.append(promtxt)
            elif pd.prom == PrimDir.LOF:
                formattxt += '%s '
                tuptxt.append(bodies[pd.prom])
            elif pd.prom == PrimDir.USERPD:
                formattxt += '%s '
                tuptxt.append(bodies[pd.prom])
            elif pd.prom == PrimDir.ASC or pd.prom == PrimDir.MC:
                if pd.promasp != chart.Chart.CONIUNCTIO:
                    formattxt += '%s '
                    tuptxt.append(aspects[pd.promasp])
                formattxt += '%s '
                atxt = mtexts.txtscommon['Asc']
                if pd.prom == PrimDir.MC:
                    atxt = mtexts.txtscommon['MC']
                tuptxt.append(atxt)
            elif pd.prom >= PrimDir.HC2 and pd.prom < PrimDir.LOF:
                formattxt += '%s '
                HCs = (mtexts.txtscommon['HC2'], mtexts.txtscommon['HC3'], mtexts.txtscommon['HC5'], mtexts.txtscommon['HC6'], mtexts.txtscommon['HC8'], mtexts.txtscommon['HC9'], mtexts.txtscommon['HC11'], mtexts.txtscommon['HC12'])
                htxt = HCs[(pd.sig - PrimDir.HC2)]
                tuptxt.append(htxt)
            else:
                if pd.promasp != chart.Chart.CONIUNCTIO:
                    formattxt += '%s '
                    tuptxt.append(aspects[pd.promasp])
                formattxt += '%s '
                tuptxt.append(bodies[pd.prom])
            formattxt += '%s %s '
            tuptxt.append(dirtxt)
            tuptxt.append('-->')
            if pd.sigasp == chart.Chart.PARALLEL or pd.sigasp == chart.Chart.CONTRAPARALLEL:
                formattxt += '%s %s '
                partxt = mtexts.txtscommon['Parallel']
                if pd.parallelaxis == 0 and pd.sigasp == chart.Chart.CONTRAPARALLEL:
                    partxt = mtexts.txtscommon['ContraParallel']
                tuptxt.append(partxt)
                tuptxt.append(bodies[pd.sig])
                if pd.parallelaxis != 0:
                    angles = (
                     '(' + mtexts.txtscommon['Asc'] + ')', '(' + mtexts.txtscommon['Dsc'] + ')', '(' + mtexts.txtscommon['MC'] + ')', '(' + mtexts.txtscommon['IC'] + ')')
                    formattxt += '%s '
                    tuptxt.append(angles[(pd.parallelaxis - PrimDir.OFFSANGLES)])
            elif pd.sigasp == chart.Chart.RAPTPAR or pd.sigasp == chart.Chart.RAPTCONTRAPAR:
                formattxt += '%s %s '
                tuptxt.append(mtexts.txtsprimdirslist['RaptParallel'])
                angles = ('(' + mtexts.txtscommon['Asc'] + ')', '(' + mtexts.txtscommon['Dsc'] + ')', '(' + mtexts.txtscommon['MC'] + ')', '(' + mtexts.txtscommon['IC'] + ')')
                tuptxt.append(angles[(pd.parallelaxis - PrimDir.OFFSANGLES)])
            elif pd.sig == PrimDir.LOF:
                if pd.mundane:
                    if pd.sigasp != chart.Chart.CONIUNCTIO:
                        formattxt += '%s '
                        tuptxt.append(aspects[pd.sigasp])
                formattxt += '%s '
                tuptxt.append(mtexts.txtscommon['LoF'])
            elif pd.sig == PrimDir.SYZ:
                formattxt += '%s '
                tuptxt.append(bodies[pd.sig])
            elif pd.sig == PrimDir.USERPD:
                formattxt += '%s '
                tuptxt.append(mtexts.txtscommon['User'])
            elif pd.sig >= PrimDir.OFFSANGLES and pd.sig < PrimDir.LOF:
                formattxt += '%s '
                stxt = ''
                if pd.sig <= PrimDir.IC:
                    angles = (
                     mtexts.txtscommon['Asc'], mtexts.txtscommon['Dsc'], mtexts.txtscommon['MC'], mtexts.txtscommon['IC'])
                    stxt = angles[(pd.sig - PrimDir.OFFSANGLES)]
                else:
                    HCs = (
                     mtexts.txtscommon['HC2'], mtexts.txtscommon['HC3'], mtexts.txtscommon['HC5'], mtexts.txtscommon['HC6'], mtexts.txtscommon['HC8'], mtexts.txtscommon['HC9'], mtexts.txtscommon['HC11'], mtexts.txtscommon['HC12'])
                    stxt = HCs[(pd.sig - PrimDir.HC2)]
                tuptxt.append(stxt)
            else:
                if pd.sigasp != chart.Chart.CONIUNCTIO:
                    formattxt += '%s '
                    tuptxt.append(aspects[pd.sigasp])
                formattxt += '%s '
                tuptxt.append(bodies[pd.sig])
            formattxt += '%f '
            tuptxt.append(pd.arc)
            formattxt += '%d.%02d.%02d'
            tuptxt.append(y)
            tuptxt.append(m)
            tuptxt.append(d)
            formattxt += '\n'
            lines.append(formattxt % tuple(tuptxt))

        f = open(fname, 'w')
        f.writelines(lines)
        f.close()