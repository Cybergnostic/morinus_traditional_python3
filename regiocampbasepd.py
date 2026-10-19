# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math
import astrology
import primdirs
import planets
import regiospec
import chart
import fixedstars
import fortune
import syzygy
import houses
import secmotion
import userpd
import util

class RegioCampBasePD(primdirs.PrimDirs):
    """Implements Regiomontanian/Campanian(common) Primary Directions"""

    def __init__(self, chrt, options, pdrange, direction, abort):
        primdirs.PrimDirs.__init__(self, chrt, options, pdrange, direction, abort)

    def calcInterPlanetary(self, mundane):
        """Calclucates mundane/zodiacal directions of the promissors to aspects of planets"""
        for p in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            lonprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
            latprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
            raprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RA]
            declprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.DECL]
            if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                latprom = 0.0
                raprom, declprom, distprom = astrology.swe_cotrans(plprom.data[planets.Planet.LON], 0.0, 1.0, -self.chart.obl[0])
            self.toPlanets(mundane, p, lonprom, latprom, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcCustomerPlanetary(self, mundane):
        """Calclucates mundane/zodiacal directions of the Cutomer-promissor to aspects of planets"""
        lonprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
        latprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
        raprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RA]
        declprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.DECL]
        if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
            latprom = 0.0
            raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        self.toPlanets(mundane, primdirs.PrimDir.USERPD, lonprom, latprom, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcPlanetary2Customer2(self, mundane):
        """Calclucates mundane/zodiacal directions of the promissors to the Customer2 point"""
        for p in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            lonprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
            latprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
            raprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RA]
            declprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.DECL]
            if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                latprom = 0.0
                raprom, declprom, distprom = astrology.swe_cotrans(plprom.data[planets.Planet.LON], 0.0, 1.0, -self.chart.obl[0])
            self.toCustomer2(mundane, p, primdirs.PrimDir.NONE, lonprom, latprom, raprom, declprom, chart.Chart.CONIUNCTIO, 0.0, True)

    def calcAntiscia2Planets(self, mundane):
        """Calclucates mundane/zodiacal directions of the Antiscia to aspects of planets"""
        self.calcAntiscia2PlanetsSub(mundane, self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcAntiscia2PlanetsSub(mundane, self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)
        if not mundane:
            if self.options.pdlof[0]:
                ant = self.chart.antiscia.lofant
                lonlofant = ant.lon
                latlofant = ant.lat
                ralofant = ant.ra
                decllofant = ant.decl
                self.toPlanets(mundane, primdirs.PrimDir.ANTISCIONLOF, lonlofant, latlofant, ralofant, decllofant, chart.Chart.CONIUNCTIO)
                cant = self.chart.antiscia.lofcontraant
                lonlofcant = cant.lon
                latlofcant = cant.lat
                ralofcant = cant.ra
                decllofcant = cant.decl
                self.toPlanets(mundane, primdirs.PrimDir.CONTRAANTLOF, lonlofcant, latlofcant, ralofcant, decllofcant, chart.Chart.CONIUNCTIO)
            for i in range(2):
                ant = self.chart.antiscia.ascmcant[i]
                lonant = ant.lon
                raant = ant.ra
                declant = ant.decl
                typ = primdirs.PrimDir.ANTISCIONASC
                if i > 0:
                    typ = primdirs.PrimDir.ANTISCIONMC
                self.toPlanets(mundane, typ, lonant, 0.0, raant, declant, chart.Chart.CONIUNCTIO)

            for i in range(2):
                cant = self.chart.antiscia.ascmccontraant[i]
                loncant = cant.lon
                racant = cant.ra
                declcant = cant.decl
                typ = primdirs.PrimDir.CONTRAANTASC
                if i > 0:
                    typ = primdirs.PrimDir.CONTRAANTMC
                self.toPlanets(mundane, typ, loncant, 0.0, racant, declcant, chart.Chart.CONIUNCTIO)

    def calcAntiscia2PlanetsSub(self, mundane, pls, offs):
        for p in range(len(pls)):
            if not self.options.promplanets[p]:
                continue
            plprom = pls[p]
            lonprom = plprom.lon
            latprom = plprom.lat
            raprom = plprom.ra
            declprom = plprom.decl
            if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                latprom = 0.0
                raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
            self.toPlanets(mundane, p + offs, lonprom, latprom, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcAntiscia2Customer2(self, mundane):
        """Calclucates mundane/zodiacal directions of the Antiscia to aspects of planets"""
        self.calcAntiscia2Customer2Sub(mundane, self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcAntiscia2Customer2Sub(mundane, self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)
        if not mundane:
            if self.options.pdlof[0]:
                ant = self.chart.antiscia.lofant
                lonlofant = ant.lon
                latlofant = ant.lat
                ralofant = ant.ra
                decllofant = ant.decl
                self.toCustomer2(mundane, primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, lonlofant, latlofant, ralofant, decllofant, chart.Chart.CONIUNCTIO)
                cant = self.chart.antiscia.lofcontraant
                lonlofcant = cant.lon
                latlofcant = cant.lat
                ralofcant = cant.ra
                decllofcant = cant.decl
                self.toCustomer2(mundane, primdirs.PrimDir.CONTRAANTLOF, primdirs.PrimDir.NONE, lonlofcant, latlofcant, ralofcant, decllofcant, chart.Chart.CONIUNCTIO)
            for i in range(2):
                ant = self.chart.antiscia.ascmcant[i]
                lonant = ant.lon
                raant = ant.ra
                declant = ant.decl
                typ = primdirs.PrimDir.ANTISCIONASC
                if i > 0:
                    typ = primdirs.PrimDir.ANTISCIONMC
                self.toCustomer2(mundane, typ, primdirs.PrimDir.NONE, lonant, 0.0, raant, declant, chart.Chart.CONIUNCTIO)

            for i in range(2):
                cant = self.chart.antiscia.ascmccontraant[i]
                loncant = cant.lon
                racant = cant.ra
                declcant = cant.decl
                typ = primdirs.PrimDir.CONTRAANTASC
                if i > 0:
                    typ = primdirs.PrimDir.CONTRAANTMC
                self.toCustomer2(mundane, typ, primdirs.PrimDir.NONE, loncant, 0.0, racant, declcant, chart.Chart.CONIUNCTIO)

    def calcAntiscia2Customer2Sub(self, mundane, pls, offs):
        for p in range(len(pls)):
            if not self.options.promplanets[p]:
                continue
            plprom = pls[p]
            lonprom = plprom.lon
            latprom = plprom.lat
            raprom = plprom.ra
            declprom = plprom.decl
            if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                latprom = 0.0
                raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
            self.toCustomer2(mundane, p + offs, primdirs.PrimDir.NONE, lonprom, latprom, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcZodPromAspsInterPlanetary(self):
        """Calclucates zodiacal directions of the aspects of promissors to significators"""
        SINISTER = 0
        DEXTER = 1
        for p in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            pllat = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
            for psidx in range(chart.Chart.CONIUNCTIO + 1, chart.Chart.OPPOSITIO + 1):
                if not self.options.pdaspects[psidx]:
                    continue
                for k in range(DEXTER + 1):
                    aspect = chart.Chart.Aspects[psidx]
                    if k == DEXTER:
                        if psidx == chart.Chart.OPPOSITIO:
                            break
                        aspect *= -1
                    lonprom = util.normalize(plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON] + aspect)
                    latprom, raprom, declprom = (0.0, 0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
                    else:
                        raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
                    for s in range(planets.Planets.BODIES_NUM):
                        if not self.options.sigplanets[s]:
                            continue
                        if self.abort.abort:
                            return
                        self.toPlanet(False, p, primdirs.PrimDir.NONE, lonprom, latprom, raprom, declprom, psidx, s, chart.Chart.CONIUNCTIO, True, aspect)

    def calcZodPromAsps2HCs(self):
        """Calclucates zodiacal directions of the aspects of promissors to intermediate housecusps"""
        SINISTER = 0
        DEXTER = 1
        for p in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            pllat = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
            for psidx in range(chart.Chart.CONIUNCTIO + 1, chart.Chart.OPPOSITIO + 1):
                if not self.options.pdaspects[psidx]:
                    continue
                for k in range(DEXTER + 1):
                    aspect = chart.Chart.Aspects[psidx]
                    if k == DEXTER:
                        if psidx == chart.Chart.OPPOSITIO:
                            break
                        aspect *= -1
                    lonprom = util.normalize(plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON] + aspect)
                    latprom, raprom, declprom = (0.0, 0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
                    else:
                        raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
                    self.toHCs(False, p, raprom, declprom, psidx, aspect)

    def calcZodPromAspsInterPlanetary2Customer2(self):
        """Calclucates zodiacal directions of the aspects of promissors to Customer2"""
        SINISTER = 0
        DEXTER = 1
        for p in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            pllat = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
            for psidx in range(chart.Chart.CONIUNCTIO + 1, chart.Chart.OPPOSITIO + 1):
                if not self.options.pdaspects[psidx]:
                    continue
                if self.abort.abort:
                    return
                for k in range(DEXTER + 1):
                    aspect = chart.Chart.Aspects[psidx]
                    if k == DEXTER:
                        if psidx == chart.Chart.OPPOSITIO:
                            break
                        aspect *= -1
                    lonprom = util.normalize(plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON] + aspect)
                    latprom, raprom, declprom = (0.0, 0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
                    else:
                        raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
                    self.toCustomer2(False, p, primdirs.PrimDir.NONE, lonprom, latprom, raprom, declprom, psidx, aspect, True)

    def calcZodPromAntisciaAspsInterPlanetary(self):
        """Calclucates zodiacal directions of the aspects of Antiscia to significators"""
        self.calcZodPromAntisciaAspsInterPlanetarySub(self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcZodPromAntisciaAspsInterPlanetarySub(self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)

    def calcZodPromAntisciaAspsInterPlanetarySub(self, pls, offs):
        NODES = 2
        SINISTER = 0
        DEXTER = 1
        numpls = len(pls)
        for p in range(numpls - NODES):
            if not self.options.promplanets[p]:
                continue
            plprom = pls[p]
            pllat = plprom.lat
            for psidx in range(chart.Chart.CONIUNCTIO + 1, chart.Chart.OPPOSITIO + 1):
                if not self.options.pdaspects[psidx]:
                    continue
                for k in range(DEXTER + 1):
                    aspect = chart.Chart.Aspects[psidx]
                    if k == DEXTER:
                        if psidx == chart.Chart.OPPOSITIO:
                            break
                        aspect *= -1
                    lonprom = util.normalize(plprom.lon + aspect)
                    latprom, raprom, declprom = (0.0, 0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
                    else:
                        raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
                    for s in range(planets.Planets.BODIES_NUM):
                        if not self.options.sigplanets[s]:
                            continue
                        if self.abort.abort:
                            return
                        self.toPlanet(False, p + offs, primdirs.PrimDir.NONE, lonprom, latprom, raprom, declprom, psidx, s, chart.Chart.CONIUNCTIO)

    def calcZodPromAntisciaAspsInterPlanetary2Customer2(self):
        """Calclucates zodiacal directions of the aspects of Antiscia to significators"""
        self.calcZodPromAntisciaAspsInterPlanetary2Customer2Sub(self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcZodPromAntisciaAspsInterPlanetary2Customer2Sub(self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)

    def calcZodPromAntisciaAspsInterPlanetary2Customer2Sub(self, pls, offs):
        NODES = 2
        SINISTER = 0
        DEXTER = 1
        numpls = len(pls)
        for p in range(numpls - NODES):
            if not self.options.promplanets[p]:
                continue
            plprom = pls[p]
            pllat = plprom.lat
            for psidx in range(chart.Chart.CONIUNCTIO + 1, chart.Chart.OPPOSITIO + 1):
                if not self.options.pdaspects[psidx]:
                    continue
                if self.abort.abort:
                    return
                for k in range(DEXTER + 1):
                    aspect = chart.Chart.Aspects[psidx]
                    if k == DEXTER:
                        if psidx == chart.Chart.OPPOSITIO:
                            break
                        aspect *= -1
                    lonprom = util.normalize(plprom.lon + aspect)
                    latprom, raprom, declprom = (0.0, 0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
                    else:
                        raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
                    self.toCustomer2(False, p + offs, primdirs.PrimDir.NONE, lonprom, latprom, raprom, declprom, psidx, aspect)

    def calc2HouseCusps(self, mundane):
        """Calculates directions of Promissors to intermediate house cusps"""
        for i in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[i]:
                continue
            if self.abort.abort:
                return
            plprom = self.chart.planets.planets[i]
            raprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RA]
            declprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.DECL]
            if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                raprom, declprom, distprom = astrology.swe_cotrans(plprom.data[planets.Planet.LON], 0.0, 1.0, -self.chart.obl[0])
            self.toHCs(mundane, i, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcCustomer2HouseCusps(self, mundane):
        """Calculates directions of Customer-Promissor to intermediate house cusps"""
        lonprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
        raprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RA]
        declprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.DECL]
        if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
            raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        self.toHCs(mundane, primdirs.PrimDir.USERPD, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcAntiscia2HouseCusps(self, mundane):
        """Calculates directions of Antiscia to intermediate house cusps"""
        self.calcAntiscia2HouseCuspsSub(mundane, self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcAntiscia2HouseCuspsSub(mundane, self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)

    def calcAntiscia2HouseCuspsSub(self, mundane, pls, offs):
        numpls = len(pls)
        for i in range(numpls):
            if not self.options.promplanets[i]:
                continue
            if self.abort.abort:
                return
            plprom = pls[i]
            raprom = plprom.ra
            declprom = plprom.decl
            if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                raprom, declprom, distprom = astrology.swe_cotrans(plprom.lon, 0.0, 1.0, -self.chart.obl[0])
            self.toHCs(mundane, i + offs, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcZodFixedStars2HouseCusps(self):
        """Calculates zodiacal directions of fixedstars to HCs"""
        OFFS = primdirs.PrimDir.FIXEDSTAR
        numfs = len(self.chart.fixedstars.data)
        for i in range(numfs):
            if not self.options.pdfixedstarssel[self.chart.fixedstars.mixed[i]]:
                continue
            if self.abort.abort:
                return
            star = self.chart.fixedstars.data[i]
            lonstar = star[fixedstars.FixedStars.LON]
            rastar = star[fixedstars.FixedStars.RA]
            declstar = star[fixedstars.FixedStars.DECL]
            if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                rastar, declstar, dist = astrology.swe_cotrans(lonstar, 0.0, 1.0, -self.chart.obl[0])
            self.toHCs(False, i + OFFS, rastar, declstar, chart.Chart.CONIUNCTIO)

    def calcZodLoF2HouseCusps(self):
        """Calculates zodiacal LoF to housecusps"""
        raprom = self.chart.fortune.fortune[fortune.Fortune.RA]
        declprom = self.chart.fortune.fortune[fortune.Fortune.DECL]
        self.toHCs(False, primdirs.PrimDir.LOF, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcZodLoF2Planets(self):
        """Calculates zodiacal LoF to Planets and their aspects"""
        lonprom = self.chart.fortune.fortune[fortune.Fortune.LON]
        latprom = self.chart.fortune.fortune[fortune.Fortune.LAT]
        raprom = self.chart.fortune.fortune[fortune.Fortune.RA]
        declprom = self.chart.fortune.fortune[fortune.Fortune.DECL]
        self.toPlanets(False, primdirs.PrimDir.LOF, lonprom, latprom, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcZodPlanets2LoF(self):
        """Calculates zodiacal Planets and their aspects to LoF"""
        SINISTER = 0
        DEXTER = 1
        for p in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            pllat = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
            for psidx in range(chart.Chart.OPPOSITIO + 1):
                if not self.options.pdaspects[psidx]:
                    continue
                if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONIUNCTIO:
                    continue
                if p >= planets.Planets.PLANETS_NUM and psidx > chart.Chart.CONIUNCTIO:
                    break
                for k in range(DEXTER + 1):
                    aspect = chart.Chart.Aspects[psidx]
                    if k == DEXTER:
                        if psidx == chart.Chart.CONIUNCTIO or psidx == chart.Chart.OPPOSITIO:
                            break
                        aspect *= -1
                    if self.abort.abort:
                        return
                    lonprom = util.normalize(plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON] + aspect)
                    latprom = 0.0
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                    self.toLoF(p, primdirs.PrimDir.NONE, lonprom, latprom, psidx, aspect, True)

    def calcZodPlanets2Syzygy(self):
        """Calculates zodiacal Planets and their aspects to Syzygy"""
        SINISTER = 0
        DEXTER = 1
        for p in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            pllat = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
            for psidx in range(chart.Chart.OPPOSITIO + 1):
                if not self.options.pdaspects[psidx]:
                    continue
                if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONIUNCTIO:
                    continue
                if p >= planets.Planets.PLANETS_NUM and psidx > chart.Chart.CONIUNCTIO:
                    break
                for k in range(DEXTER + 1):
                    aspect = chart.Chart.Aspects[psidx]
                    if k == DEXTER:
                        if psidx == chart.Chart.CONIUNCTIO or psidx == chart.Chart.OPPOSITIO:
                            break
                        aspect *= -1
                    if self.abort.abort:
                        return
                    lonprom = util.normalize(plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON] + aspect)
                    latprom = 0.0
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                    self.toSyzygy(p, primdirs.PrimDir.NONE, lonprom, latprom, psidx, aspect, True)

    def calcZodCustomer2LoF(self):
        """Calculates zodiacal Customer to LoF"""
        lonprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
        latprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
        if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
            latprom = 0.0
        self.toLoF(primdirs.PrimDir.USERPD, primdirs.PrimDir.NONE, lonprom, latprom, chart.Chart.CONIUNCTIO)

    def calcZodCustomer2Syzygy(self):
        """Calculates zodiacal Customer to Syzygy"""
        lonprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
        latprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
        if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
            latprom = 0.0
        self.toSyzygy(primdirs.PrimDir.USERPD, primdirs.PrimDir.NONE, lonprom, latprom, chart.Chart.CONIUNCTIO)

    def calcZodAntiscia2LoF(self):
        """Calculates zodiacal Antiscia and their aspects to LoF"""
        self.calcZodAntiscia2LoFSub(self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcZodAntiscia2LoFSub(self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)
        if self.options.pdlof[0]:
            ant = self.chart.antiscia.lofant
            lonlofant = ant.lon
            ralofant = ant.ra
            decllofant = ant.decl
            self.toLoF(primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, lonlofant, 0.0, chart.Chart.CONIUNCTIO)
            cant = self.chart.antiscia.lofcontraant
            lonlofcant = ant.lon
            ralofcant = ant.ra
            decllofcant = ant.decl
            self.toLoF(primdirs.PrimDir.CONTRAANTLOF, primdirs.PrimDir.NONE, lonlofcant, 0.0, chart.Chart.CONIUNCTIO)
        for i in range(2):
            ant = self.chart.antiscia.ascmcant[i]
            lonant = ant.lon
            raant = ant.ra
            declant = ant.decl
            typ = primdirs.PrimDir.ANTISCIONASC
            if i > 0:
                typ = primdirs.PrimDir.ANTISCIONMC
            self.toLoF(typ, primdirs.PrimDir.NONE, lonant, 0.0, chart.Chart.CONIUNCTIO)

        for i in range(2):
            cant = self.chart.antiscia.ascmccontraant[i]
            loncant = ant.lon
            racant = ant.ra
            declcant = ant.decl
            typ = primdirs.PrimDir.CONTRAANTASC
            if i > 0:
                typ = primdirs.PrimDir.CONTRAANTMC
            self.toLoF(typ, primdirs.PrimDir.NONE, loncant, 0.0, chart.Chart.CONIUNCTIO)

    def calcZodAntiscia2LoFSub(self, pls, offs):
        SINISTER = 0
        DEXTER = 1
        numpls = len(pls)
        for p in range(numpls):
            if not self.options.promplanets[p]:
                continue
            plprom = pls[p]
            pllat = plprom.lat
            for psidx in range(chart.Chart.OPPOSITIO + 1):
                if not self.options.pdaspects[psidx]:
                    continue
                if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONIUNCTIO:
                    continue
                if p >= planets.Planets.PLANETS_NUM and psidx > chart.Chart.CONIUNCTIO:
                    break
                for k in range(DEXTER + 1):
                    aspect = chart.Chart.Aspects[psidx]
                    if k == DEXTER:
                        if psidx == chart.Chart.CONIUNCTIO or psidx == chart.Chart.OPPOSITIO:
                            break
                        aspect *= -1
                    if self.abort.abort:
                        return
                    lonprom = util.normalize(plprom.lon + aspect)
                    latprom = 0.0
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                    self.toLoF(p + offs, primdirs.PrimDir.NONE, lonprom, latprom, psidx)

    def calcZodAntiscia2Syzygy(self):
        """Calculates zodiacal Antiscia and their aspects to Syzygy"""
        self.calcZodAntiscia2SyzygySub(self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcZodAntiscia2SyzygySub(self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)
        if self.options.pdlof[0]:
            ant = self.chart.antiscia.lofant
            lonlofant = ant.lon
            ralofant = ant.ra
            decllofant = ant.decl
            self.toSyzygy(primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, lonlofant, 0.0, chart.Chart.CONIUNCTIO)
            cant = self.chart.antiscia.lofcontraant
            lonlofcant = ant.lon
            ralofcant = ant.ra
            decllofcant = ant.decl
            self.toSyzygy(primdirs.PrimDir.CONTRAANTLOF, primdirs.PrimDir.NONE, lonlofcant, 0.0, chart.Chart.CONIUNCTIO)
        for i in range(2):
            ant = self.chart.antiscia.ascmcant[i]
            lonant = ant.lon
            raant = ant.ra
            declant = ant.decl
            typ = primdirs.PrimDir.ANTISCIONASC
            if i > 0:
                typ = primdirs.PrimDir.ANTISCIONMC
            self.toSyzygy(typ, primdirs.PrimDir.NONE, lonant, 0.0, chart.Chart.CONIUNCTIO)

        for i in range(2):
            cant = self.chart.antiscia.ascmccontraant[i]
            loncant = ant.lon
            racant = ant.ra
            declcant = ant.decl
            typ = primdirs.PrimDir.CONTRAANTASC
            if i > 0:
                typ = primdirs.PrimDir.CONTRAANTMC
            self.toSyzygy(typ, primdirs.PrimDir.NONE, loncant, 0.0, chart.Chart.CONIUNCTIO)

    def calcZodAntiscia2SyzygySub(self, pls, offs):
        SINISTER = 0
        DEXTER = 1
        numpls = len(pls)
        for p in range(numpls):
            if not self.options.promplanets[p]:
                continue
            plprom = pls[p]
            pllat = plprom.lat
            for psidx in range(chart.Chart.OPPOSITIO + 1):
                if not self.options.pdaspects[psidx]:
                    continue
                if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONIUNCTIO:
                    continue
                if p >= planets.Planets.PLANETS_NUM and psidx > chart.Chart.CONIUNCTIO:
                    break
                for k in range(DEXTER + 1):
                    aspect = chart.Chart.Aspects[psidx]
                    if k == DEXTER:
                        if psidx == chart.Chart.CONIUNCTIO or psidx == chart.Chart.OPPOSITIO:
                            break
                        aspect *= -1
                    if self.abort.abort:
                        return
                    lonprom = util.normalize(plprom.lon + aspect)
                    latprom = 0.0
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                    self.toSyzygy(p + offs, primdirs.PrimDir.NONE, lonprom, latprom, psidx)

    def calcZodTerms(self):
        """Calculates zodiacal terms to Planets, LoF"""
        num = len(self.options.terms[0])
        subnum = len(self.options.terms[0][0])
        for i in range(num):
            summa = 0
            for j in range(subnum):
                if self.abort.abort:
                    return
                lonprom = i * chart.Chart.SIGN_DEG + summa
                if self.options.ayanamsha != 0:
                    lonprom += self.chart.ayanamsha
                    lonprom = util.normalize(lonprom)
                raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
                for s in range(planets.Planets.BODIES_NUM):
                    if self.options.sigplanets[s]:
                        plsig = self.chart.planets.planets[s]
                        wprom, wsig = (0.0, 0.0)
                        if self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                            wsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.W]
                            ok, wprom, ppole, seastern, md, umd = self.getZodW(plsig, lonprom, 0.0, plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.POLE], plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern)
                            if not ok:
                                continue
                        else:
                            lonsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
                            ok, wsig, spole, seastern, md, umd = self.getZodW(plsig, lonsig, 0.0)
                            if not ok:
                                continue
                            ok, wprom, ppole, seastern, md, umd = self.getZodW(plsig, lonprom, 0.0, spole, seastern)
                            if not ok:
                                continue
                        arc = wprom - wsig
                        self.create(False, primdirs.PrimDir.TERM + i, self.options.terms[self.options.selterm][i][j][0], s, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, arc)

                if self.options.pdlof[1]:
                    self.toLoF(primdirs.PrimDir.TERM + i, self.options.terms[self.options.selterm][i][j][0], lonprom, 0.0, chart.Chart.CONIUNCTIO)
                if self.chart.htype == chart.Chart.RADIX:
                    if self.options.pdsyzygy:
                        self.toSyzygy(primdirs.PrimDir.TERM + i, self.options.terms[self.options.selterm][i][j][0], lonprom, 0.0, chart.Chart.CONIUNCTIO)
                    if self.options.pduser2 and self.chart.usersigpd != None:
                        self.toCustomer2(False, primdirs.PrimDir.TERM + i, self.options.terms[self.options.selterm][i][j][0], lonprom, 0.0, raprom, declprom, chart.Chart.CONIUNCTIO)
                summa += self.options.terms[self.options.selterm][i][j][1]

        return

    def calcZodFixedStars2Planets(self):
        """Calculates zodiacal directions of fixedstars to planets"""
        OFFS = primdirs.PrimDir.FIXEDSTAR
        numfs = len(self.chart.fixedstars.data)
        for i in range(numfs):
            if not self.options.pdfixedstarssel[self.chart.fixedstars.mixed[i]]:
                continue
            if self.abort.abort:
                return
            star = self.chart.fixedstars.data[i]
            lonstar = star[fixedstars.FixedStars.LON]
            latstar = star[fixedstars.FixedStars.LAT]
            rastar = star[fixedstars.FixedStars.RA]
            declstar = star[fixedstars.FixedStars.DECL]
            if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                latstar = 0.0
                rastar, declstar, dist = astrology.swe_cotrans(lonstar, 0.0, 1.0, -self.chart.obl[0])
            for s in range(planets.Planets.BODIES_NUM):
                if not self.options.sigplanets[s]:
                    continue
                if self.abort.abort:
                    return
                self.toPlanet(False, i + OFFS, primdirs.PrimDir.NONE, lonstar, latstar, rastar, declstar, chart.Chart.CONIUNCTIO, s, chart.Chart.CONIUNCTIO)

    def calcZodAsc2Planets(self):
        """Calculates zodiacal Asc and its aspects to Planets"""
        lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
        self.calcZodAscMC2Planets(primdirs.PrimDir.ASC, lonprom)

    def calcZodMC2Planets(self):
        """Calculates zodiacal MC and its aspects to Planets"""
        lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
        self.calcZodAscMC2Planets(primdirs.PrimDir.MC, lonprom)

    def calcZodAscMC2Planets(self, p, lonprom):
        SINISTER = 0
        DEXTER = 1
        beg = chart.Chart.CONIUNCTIO
        if self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS]:
            beg += 1
        for psidx in range(beg, chart.Chart.CONIUNCTIO + 1):
            if not self.options.pdaspects[psidx]:
                continue
            if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONIUNCTIO:
                break
            for k in range(DEXTER + 1):
                aspect = chart.Chart.Aspects[psidx]
                if k == DEXTER:
                    if psidx == chart.Chart.CONIUNCTIO or psidx == chart.Chart.OPPOSITIO:
                        break
                    aspect *= -1
                lon = util.normalize(lonprom + aspect)
                raprom, declprom, distprom = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                for s in range(planets.Planets.BODIES_NUM):
                    if not self.options.sigplanets[s]:
                        continue
                    if self.abort.abort:
                        return
                    self.toPlanet(False, p, primdirs.PrimDir.NONE, lon, 0.0, raprom, declprom, psidx, s, chart.Chart.CONIUNCTIO)

    def calcZodAsc2AspPlanets(self):
        """Calculates zodiacal Asc to Planets and their aspects"""
        lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
        raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        self.toPlanets(False, primdirs.PrimDir.ASC, lonprom, 0.0, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcZodAsc2ParallelPlanets(self):
        lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
        self.toParallels(primdirs.PrimDir.ASC, lonprom, 0.0)

    def calcZodMC2AspPlanets(self):
        """Calculates zodiacal MC to Planets and their aspects"""
        lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
        raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        self.toPlanets(False, primdirs.PrimDir.MC, lonprom, 0.0, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcZodMC2ParallelPlanets(self):
        lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
        self.toParallels(primdirs.PrimDir.MC, lonprom, 0.0)

    def calcZodAsc2HCs(self):
        """Calculates zodiacal Asc to housecusps"""
        raprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.RA]
        declprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.DECL]
        self.toHCs(False, primdirs.PrimDir.ASC, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcZodMC2HCs(self):
        """Calculates zodiacal MC to housecusps"""
        raprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.RA]
        declprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.DECL]
        self.toHCs(False, primdirs.PrimDir.MC, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcZodAsc2LoF(self):
        """Calculates zodiacal Asc to LoF"""
        lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
        self.calcZodAscMC2LoF(primdirs.PrimDir.ASC, lonprom)

    def calcZodMC2LoF(self):
        """Calculates zodiacal MC to LoF"""
        lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
        self.calcZodAscMC2LoF(primdirs.PrimDir.MC, lonprom)

    def calcZodAscMC2LoF(self, p, lonprom):
        SINISTER = 0
        DEXTER = 1
        for psidx in range(chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO + 1):
            if not self.options.pdaspects[psidx]:
                continue
            if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONIUNCTIO:
                break
            for k in range(DEXTER + 1):
                aspect = chart.Chart.Aspects[psidx]
                if k == DEXTER:
                    if psidx == chart.Chart.CONIUNCTIO or psidx == chart.Chart.OPPOSITIO:
                        break
                    aspect *= -1
                lon = util.normalize(lonprom + aspect)
                raprom, declprom, distprom = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                self.toLoF(p, primdirs.PrimDir.NONE, lon, 0.0, psidx)

    def calcZodAsc2Syzygy(self):
        """Calculates zodiacal Asc to Syzygy"""
        lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
        self.calcZodAscMC2Syzygy(primdirs.PrimDir.ASC, lonprom)

    def calcZodMC2Syzygy(self):
        """Calculates zodiacal MC to Syzygy"""
        lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
        self.calcZodAscMC2Syzygy(primdirs.PrimDir.MC, lonprom)

    def calcZodAscMC2Syzygy(self, p, lonprom):
        SINISTER = 0
        DEXTER = 1
        for psidx in range(chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO + 1):
            if not self.options.pdaspects[psidx]:
                continue
            if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONIUNCTIO:
                break
            for k in range(DEXTER + 1):
                aspect = chart.Chart.Aspects[psidx]
                if k == DEXTER:
                    if psidx == chart.Chart.CONIUNCTIO or psidx == chart.Chart.OPPOSITIO:
                        break
                    aspect *= -1
                lon = util.normalize(lonprom + aspect)
                raprom, declprom, distprom = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                self.toSyzygy(p, primdirs.PrimDir.NONE, lon, 0.0, psidx)

    def calcZodAsc2Customer2(self):
        """Calculates zodiacal Asc to Customer2"""
        lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
        self.calcZodAscMC2Customer2(primdirs.PrimDir.ASC, lonprom)

    def calcZodMC2Customer2(self):
        """Calculates zodiacal MC to Customer2"""
        lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
        self.calcZodAscMC2Customer2(primdirs.PrimDir.MC, lonprom)

    def calcZodAscMC2Customer2(self, p, lonprom):
        SINISTER = 0
        DEXTER = 1
        for psidx in range(chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO + 1):
            if not self.options.pdaspects[psidx]:
                continue
            if not self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS] and psidx > chart.Chart.CONIUNCTIO:
                break
            for k in range(DEXTER + 1):
                aspect = chart.Chart.Aspects[psidx]
                if k == DEXTER:
                    if psidx == chart.Chart.CONIUNCTIO or psidx == chart.Chart.OPPOSITIO:
                        break
                    aspect *= -1
                lon = util.normalize(lonprom + aspect)
                raprom, declprom, distprom = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                self.toCustomer2(False, p, primdirs.PrimDir.NONE, lon, 0.0, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcZodParallels(self):
        """Calculates zodiacal parallels"""
        if self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS]:
            for p in range(planets.Planets.BODIES_NUM):
                if not self.options.promplanets[p]:
                    continue
                plprom = self.chart.planets.planets[p]
                lonprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
                pllat = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
                latprom = 0.0
                if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                    latprom = pllat
                self.toParallels(p, lonprom, latprom)

            if self.options.pduser and self.chart.userprompd != None:
                lonprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
                pllat = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
                latprom = 0.0
                if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                    latprom = pllat
                self.toParallels(primdirs.PrimDir.USERPD, lonprom, latprom)
        if self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS]:
            for p in range(planets.Planets.PLANETS_NUM):
                if not self.options.promplanets[p]:
                    continue
                ok = self.chart.zodpars.pars[p].valid
                points = self.chart.zodpars.pars[p].pts
                if not ok:
                    continue
                for k in range(len(points)):
                    if points[k][0] == -1.0:
                        continue
                    raprom, declprom, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
                    for s in range(planets.Planets.BODIES_NUM):
                        if not self.options.sigplanets[s]:
                            continue
                        if self.abort.abort:
                            return
                        self.toPlanet(False, p, primdirs.PrimDir.NONE, points[k][0], 0.0, raprom, declprom, points[k][1], s, chart.Chart.CONIUNCTIO, False)

                    if self.options.pduser2 and self.chart.usersigpd != None:
                        self.toCustomer2(False, p, primdirs.PrimDir.NONE, points[k][0], 0.0, raprom, declprom, points[k][1])

        return

    def calcZodAntisciaParallels(self):
        """Calculates zodiacal parallels(Antiscia)"""
        self.calcZodAntisciaParallelsSub(self.chart.antiscia.plantiscia, self.chart.antzodpars.apars, primdirs.PrimDir.ANTISCION)
        self.calcZodAntisciaParallelsSub(self.chart.antiscia.plcontraant, self.chart.antzodpars.cpars, primdirs.PrimDir.CONTRAANT)

    def calcZodAntisciaParallelsSub(self, pls, pars, offs):
        numpls = len(pls)
        if self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS]:
            for p in range(numpls):
                if not self.options.promplanets[p]:
                    continue
                plprom = pls[p]
                lonprom = plprom.lon
                pllat = plprom.lat
                latprom = 0.0
                if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                    latprom = pllat
                self.toParallels(p + offs, lonprom, latprom)

            if self.options.pdlof[0]:
                ant = self.chart.antiscia.lofant
                lonlofant = ant.lon
                self.toParallels(primdirs.PrimDir.ANTISCIONLOF, lonlofant, 0.0)
                cant = self.chart.antiscia.lofcontraant
                lonlofcant = cant.lon
                self.toParallels(primdirs.PrimDir.CONTRAANTLOF, lonlofcant, 0.0)
            for i in range(2):
                ant = self.chart.antiscia.ascmcant[i]
                lonant = ant.lon
                typ = primdirs.PrimDir.ANTISCIONASC
                if i > 0:
                    typ = primdirs.PrimDir.ANTISCIONMC
                self.toParallels(typ, lonant, 0.0)

            for i in range(2):
                cant = self.chart.antiscia.ascmccontraant[i]
                loncant = cant.lon
                typ = primdirs.PrimDir.CONTRAANTASC
                if i > 0:
                    typ = primdirs.PrimDir.CONTRAANTMC
                self.toParallels(typ, loncant, 0.0)

        if self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS]:
            for p in range(numpls):
                if not self.options.promplanets[p]:
                    continue
                if self.abort.abort:
                    return
                ok = pars[i].valid
                points = pars[i].pts
                if not ok:
                    continue
                for k in range(len(points)):
                    if points[k][0] == -1.0:
                        continue
                    raprom, declprom, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
                    for s in range(planets.Planets.BODIES_NUM):
                        if not self.options.sigplanets[s]:
                            continue
                        if self.abort.abort:
                            return
                        self.toPlanet(False, p + offs, primdirs.PrimDir.NONE, points[k][0], 0.0, raprom, declprom, points[k][1], s, chart.Chart.CONIUNCTIO)

    def calcZodMidPoints(self):
        """Calclucates zodiacal midpoint directions"""
        mids = self.chart.midpoints.mids
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            mids = self.chart.midpoints.midslat
        for mid in mids:
            if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
                continue
            plprom = self.chart.planets.planets[mid.p1]
            for s in range(planets.Planets.BODIES_NUM):
                if not self.options.sigplanets[s]:
                    continue
                if self.abort.abort:
                    return
                plsig = self.chart.planets.planets[s]
                lonsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
                lonmid = mid.m
                if math.fabs(lonmid - lonsig) > 90.0:
                    lonmid += 180.0
                    if lonmid >= 360.0:
                        lonmid -= 360.0
                raprom, declprom, distprom = astrology.swe_cotrans(lonmid, mid.lat, 1.0, -self.chart.obl[0])
                self.toPlanet(False, mid.p1, mid.p2, lonmid, mid.lat, raprom, declprom, chart.Chart.MIDPOINT, s, chart.Chart.CONIUNCTIO)

    def calcZodMidPoints2LoF(self):
        """Calclucates zodiacal midpoint directions to LoF"""
        mids = self.chart.midpoints.mids
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            mids = self.chart.midpoints.midslat
        for mid in mids:
            if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
                continue
            if self.abort.abort:
                return
            lonmid = mid.m
            lonsig = self.chart.fortune.fortune[fortune.Fortune.LON]
            if math.fabs(lonmid - lonsig) > 90.0:
                lonmid += 180.0
                if lonmid >= 360.0:
                    lonmid -= 360.0
            self.toLoF(mid.p1, mid.p2, lonmid, mid.lat, chart.Chart.MIDPOINT)

    def calcZodMidPoints2Syzygy(self):
        """Calclucates zodiacal midpoint directions to Syzygy"""
        mids = self.chart.midpoints.mids
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            mids = self.chart.midpoints.midslat
        for mid in mids:
            if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
                continue
            if self.abort.abort:
                return
            lonmid = mid.m
            lonsig = self.chart.syzygy.speculum[syzygy.Syzygy.LON]
            if math.fabs(lonmid - lonsig) > 90.0:
                lonmid += 180.0
                if lonmid >= 360.0:
                    lonmid -= 360.0
            self.toSyzygy(mid.p1, mid.p2, lonmid, mid.lat, chart.Chart.MIDPOINT)

    def calcZodMidPoints2Customer2(self):
        """Calclucates zodiacal midpoint directions to Customer2"""
        lonsig = self.chart.usersigpd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
        mids = self.chart.midpoints.mids
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            mids = self.chart.midpoints.midslat
        for mid in mids:
            if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
                continue
            if self.abort.abort:
                return
            lonmid = mid.m
            if math.fabs(lonmid - lonsig) > 90.0:
                lonmid += 180.0
                if lonmid >= 360.0:
                    lonmid -= 360.0
            raprom, declprom, dist = astrology.swe_cotrans(lonmid, mid.lat, 1.0, -self.chart.obl[0])
            self.toCustomer2(False, mid.p1, mid.p2, lonmid, mid.lat, raprom, declprom, chart.Chart.MIDPOINT)

    def calcZodLoF2ZodParallels(self):
        """Calculates zodiacal LoF to zodiacal parallels"""
        lonprom = self.chart.fortune.fortune[fortune.Fortune.LON]
        self.toParallels(primdirs.PrimDir.LOF, lonprom, 0.0)

    def calcZodLoF2Syzygy(self):
        """Calculates zodiacal LoF to Syzygy"""
        lonprom = self.chart.fortune.fortune[fortune.Fortune.LON]
        latprom = 0.0
        self.toSyzygy(primdirs.PrimDir.LOF, primdirs.PrimDir.NONE, lonprom, latprom, chart.Chart.CONIUNCTIO)

    def calcZodLoF2Customer2(self):
        """Calculates zodiacal LoF to Customer2"""
        lonprom = self.chart.fortune.fortune[fortune.Fortune.LON]
        latprom = 0.0
        raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
        self.toCustomer2(False, primdirs.PrimDir.LOF, primdirs.PrimDir.NONE, lonprom, latprom, raprom, declprom, chart.Chart.CONIUNCTIO)

    def calcZodParallels2LoF(self):
        """Calculates zodiacal parallels to zodiacal LoF"""
        for p in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[p]:
                continue
            ok = self.chart.zodpars.pars[p].valid
            points = self.chart.zodpars.pars[p].pts
            if not ok:
                continue
            for k in range(len(points)):
                if points[k][0] == -1.0:
                    continue
                self.toLoF(p, primdirs.PrimDir.NONE, points[k][0], 0.0, points[k][1])

    def calcZodParallels2Syzygy(self):
        """Calculates zodiacal parallels to zodiacal Syzygy"""
        for p in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[p]:
                continue
            ok = self.chart.zodpars.pars[p].valid
            points = self.chart.zodpars.pars[p].pts
            if not ok:
                continue
            for k in range(len(points)):
                if points[k][0] == -1.0:
                    continue
                self.toSyzygy(p, primdirs.PrimDir.NONE, points[k][0], 0.0, points[k][1])

    def calcZodAntisciaParallels2LoF(self):
        """Calculates zodiacal parallels to zodiacal LoF"""
        self.calcZodAntisciaParallels2LoFSub(self.chart.antzodpars.apars, primdirs.PrimDir.ANTISCION)
        self.calcZodAntisciaParallels2LoFSub(self.chart.antzodpars.cpars, primdirs.PrimDir.CONTRAANT)

    def calcZodAntisciaParallels2LoFSub(self, pars, offs):
        for p in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[p]:
                continue
            if self.abort.abort:
                return
            ok = pars[i].valid
            points = pars[i].pts
            if not ok:
                continue
            for k in range(len(points)):
                if points[k][0] == -1.0:
                    continue
                self.toLoF(p + offs, primdirs.PrimDir.NONE, points[k][0], 0.0, points[k][1])

    def calcZodFixedStars2LoF(self):
        """Calclucates zodiacal Fixstars directions to LoF"""
        OFFS = primdirs.PrimDir.FIXEDSTAR
        numfs = len(self.chart.fixedstars.data)
        for i in range(numfs):
            if not self.options.pdfixedstarssel[self.chart.fixedstars.mixed[i]]:
                continue
            if self.abort.abort:
                return
            star = self.chart.fixedstars.data[i]
            lonstar = star[fixedstars.FixedStars.LON]
            latstar = star[fixedstars.FixedStars.LAT]
            rastar = star[fixedstars.FixedStars.RA]
            declstar = star[fixedstars.FixedStars.DECL]
            if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                latstar = 0.0
                rastar, declstar, dist = astrology.swe_cotrans(lonstar, 0.0, 1.0, -self.chart.obl[0])
            self.toLoF(i + OFFS, primdirs.PrimDir.NONE, lonstar, latstar, chart.Chart.CONIUNCTIO)

    def calcZodFixedStars2Syzygy(self):
        """Calclucates zodiacal Fixstars directions to Syzygy"""
        OFFS = primdirs.PrimDir.FIXEDSTAR
        numfs = len(self.chart.fixedstars.data)
        for i in range(numfs):
            if not self.options.pdfixedstarssel[self.chart.fixedstars.mixed[i]]:
                continue
            if self.abort.abort:
                return
            star = self.chart.fixedstars.data[i]
            lonstar = star[fixedstars.FixedStars.LON]
            latstar = star[fixedstars.FixedStars.LAT]
            rastar = star[fixedstars.FixedStars.RA]
            declstar = star[fixedstars.FixedStars.DECL]
            if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                latstar = 0.0
                rastar, declstar, dist = astrology.swe_cotrans(lonstar, 0.0, 1.0, -self.chart.obl[0])
            self.toSyzygy(i + OFFS, primdirs.PrimDir.NONE, lonstar, latstar, chart.Chart.CONIUNCTIO)

    def calcZodFixedStars2Customer2(self):
        """Calclucates zodiacal Fixstars directions to Customer2"""
        OFFS = primdirs.PrimDir.FIXEDSTAR
        numfs = len(self.chart.fixedstars.data)
        for i in range(numfs):
            if not self.options.pdfixedstarssel[self.chart.fixedstars.mixed[i]]:
                continue
            if self.abort.abort:
                return
            star = self.chart.fixedstars.data[i]
            lonstar = star[fixedstars.FixedStars.LON]
            latstar = star[fixedstars.FixedStars.LAT]
            rastar = star[fixedstars.FixedStars.RA]
            declstar = star[fixedstars.FixedStars.DECL]
            if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                latstar = 0.0
                rastar, declstar, dist = astrology.swe_cotrans(lonstar, 0.0, 1.0, -self.chart.obl[0])
            self.toCustomer2(False, i + OFFS, primdirs.PrimDir.NONE, lonstar, latstar, rastar, declstar, chart.Chart.CONIUNCTIO)

    def calcParallels(self):
        """Calculates mundo parallels"""
        PARALLEL = 0
        CONTRAPARALLEL = 1
        for p in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            raprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RA]
            declprom = plprom.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.DECL]
            for s in range(planets.Planets.BODIES_NUM):
                if not self.options.sigplanets[s]:
                    continue
                if p == planets.Planets.ANODE and s == planets.Planets.DNODE or p == planets.Planets.DNODE and s == planets.Planets.ANODE:
                    continue
                if self.abort.abort:
                    return
                plsig = self.chart.planets.planets[s]
                mdsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RMD]
                umdsig = True
                if mdsig < 0.0:
                    mdsig *= -1
                    umdsig = False
                wsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.W]
                polesig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.POLE]
                ra = self.ramc
                if not umdsig:
                    ra = self.raic
                for k in range(CONTRAPARALLEL + 1):
                    parallelaxis = primdirs.PrimDir.MC
                    aspsig = chart.Chart.PARALLEL
                    rapprom = 0.0
                    if k == PARALLEL:
                        parallelaxis = primdirs.PrimDir.MC
                        if not plsig.speculums[planets.Planet.REGIOMONTANIAN].abovehorizon:
                            parallelaxis = primdirs.PrimDir.IC
                        aspsig = chart.Chart.PARALLEL
                        wpprom = util.normalize(2 * ra) - wsig
                        wpprom = util.normalize(wpprom)
                        val = math.tan(math.radians(declprom)) * math.tan(math.radians(polesig))
                        if math.fabs(val) > 1.0:
                            continue
                        qpprom = math.degrees(math.asin(val))
                        if plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                            rapprom = wpprom - qpprom
                        else:
                            rapprom = wpprom + qpprom
                        rapprom = util.normalize(rapprom)
                    else:
                        parallelaxis = primdirs.PrimDir.ASC
                        if not plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                            parallelaxis = primdirs.PrimDir.DESC
                        aspsig = chart.Chart.CONTRAPARALLEL
                        wpprom = util.normalize(util.normalize(2 * ra) - wsig) + 180.0
                        wpprom = util.normalize(wpprom)
                        val = math.tan(math.radians(declprom)) * math.tan(math.radians(polesig))
                        if math.fabs(val) > 1.0:
                            continue
                        qpprom = math.degrees(math.asin(val))
                        if plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                            rapprom = wpprom + qpprom
                        else:
                            rapprom = wpprom - qpprom
                        rapprom = util.normalize(rapprom)
                    arc = raprom - rapprom
                    ok = True
                    if p == planets.Planets.MOON and self.options.pdsecmotion:
                        for itera in range(self.options.pdsecmotioniter + 1):
                            ok, arc = self.calcPArcWithSM(p, s, k, arc)
                            if not ok:
                                break

                    if ok:
                        self.create(True, p, primdirs.PrimDir.NONE, s, chart.Chart.CONIUNCTIO, aspsig, arc, parallelaxis)

    def calcAntiscia2Parallels(self):
        """Calculates antiscia to mundo parallels"""
        self.calcAntiscia2ParallelsSub(self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcAntiscia2ParallelsSub(self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)

    def calcAntiscia2ParallelsSub(self, pls, offs):
        PARALLEL = 0
        CONTRAPARALLEL = 1
        for p in range(len(pls)):
            if not self.options.promplanets[p]:
                continue
            plprom = pls[p]
            raprom = plprom.ra
            declprom = plprom.decl
            for s in range(planets.Planets.BODIES_NUM):
                if not self.options.sigplanets[s]:
                    continue
                if p == planets.Planets.ANODE and s == planets.Planets.DNODE or p == planets.Planets.DNODE and s == planets.Planets.ANODE:
                    continue
                if self.abort.abort:
                    return
                plsig = self.chart.planets.planets[s]
                mdsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RMD]
                umdsig = True
                if mdsig < 0.0:
                    mdsig *= -1
                    umdsig = False
                wsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.W]
                polesig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.POLE]
                ra = self.ramc
                if not umdsig:
                    ra = self.raic
                for k in range(CONTRAPARALLEL + 1):
                    parallelaxis = primdirs.PrimDir.MC
                    aspsig = chart.Chart.PARALLEL
                    rapprom = 0.0
                    if k == PARALLEL:
                        parallelaxis = primdirs.PrimDir.MC
                        if not plsig.speculums[planets.Planet.REGIOMONTANIAN].abovehorizon:
                            parallelaxis = primdirs.PrimDir.IC
                        aspsig = chart.Chart.PARALLEL
                        wpprom = util.normalize(2 * ra) - wsig
                        wpprom = util.normalize(wpprom)
                        val = math.tan(math.radians(declprom)) * math.tan(math.radians(polesig))
                        if math.fabs(val) > 1.0:
                            continue
                        qpprom = math.degrees(math.asin(val))
                        if plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                            rapprom = wpprom - qpprom
                        else:
                            rapprom = wpprom + qpprom
                        rapprom = util.normalize(rapprom)
                    else:
                        parallelaxis = primdirs.PrimDir.ASC
                        if not plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                            parallelaxis = primdirs.PrimDir.DESC
                        aspsig = chart.Chart.CONTRAPARALLEL
                        wpprom = util.normalize(util.normalize(2 * ra) - wsig) + 180.0
                        wpprom = util.normalize(wpprom)
                        val = math.tan(math.radians(declprom)) * math.tan(math.radians(polesig))
                        if math.fabs(val) > 1.0:
                            continue
                        qpprom = math.degrees(math.asin(val))
                        if plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                            rapprom = wpprom + qpprom
                        else:
                            rapprom = wpprom - qpprom
                        rapprom = util.normalize(rapprom)
                    arc = raprom - rapprom
                    self.create(True, p + offs, primdirs.PrimDir.NONE, s, chart.Chart.CONIUNCTIO, aspsig, arc, parallelaxis)

    def calcCustomer2Parallels(self):
        """Calculates mundo parallels of the Customer point"""
        PARALLEL = 0
        CONTRAPARALLEL = 1
        raprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RA]
        declprom = self.chart.userprompd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.DECL]
        for s in range(planets.Planets.BODIES_NUM):
            if not self.options.sigplanets[s]:
                continue
            if self.abort.abort:
                return
            plsig = self.chart.planets.planets[s]
            mdsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RMD]
            umdsig = True
            if mdsig < 0.0:
                mdsig *= -1
                umdsig = False
            wsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.W]
            polesig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.POLE]
            ra = self.ramc
            if not umdsig:
                ra = self.raic
            for k in range(CONTRAPARALLEL + 1):
                parallelaxis = primdirs.PrimDir.MC
                aspsig = chart.Chart.PARALLEL
                rapprom = 0.0
                if k == PARALLEL:
                    parallelaxis = primdirs.PrimDir.MC
                    if not plsig.speculums[planets.Planet.REGIOMONTANIAN].abovehorizon:
                        parallelaxis = primdirs.PrimDir.IC
                    aspsig = chart.Chart.PARALLEL
                    wpprom = util.normalize(2 * ra) - wsig
                    wpprom = util.normalize(wpprom)
                    val = math.tan(math.radians(declprom)) * math.tan(math.radians(polesig))
                    if math.fabs(val) > 1.0:
                        continue
                    qpprom = math.degrees(math.asin(val))
                    if plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                        rapprom = wpprom - qpprom
                    else:
                        rapprom = wpprom + qpprom
                    rapprom = util.normalize(rapprom)
                else:
                    parallelaxis = primdirs.PrimDir.ASC
                    if not plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                        parallelaxis = primdirs.PrimDir.DESC
                    aspsig = chart.Chart.CONTRAPARALLEL
                    wpprom = util.normalize(util.normalize(2 * ra) - wsig) + 180.0
                    wpprom = util.normalize(wpprom)
                    val = math.tan(math.radians(declprom)) * math.tan(math.radians(polesig))
                    if math.fabs(val) > 1.0:
                        continue
                    qpprom = math.degrees(math.asin(val))
                    if plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                        rapprom = wpprom + qpprom
                    else:
                        rapprom = wpprom - qpprom
                    rapprom = util.normalize(rapprom)
                arc = raprom - rapprom
                self.create(True, primdirs.PrimDir.USERPD, primdirs.PrimDir.NONE, s, chart.Chart.CONIUNCTIO, aspsig, arc, parallelaxis)

    def calcPlanets2MLoF(self):
        pass

    def calcCustomer2MLoF(self):
        pass

    def calcAntiscia2MLoF(self):
        pass

    def calcPlanets2MLoF(self):
        pass

    def calcAntiscia2MLoF(self):
        pass

    def toPlanets(self, mundane, idprom, lonprom, latprom, raprom, declprom, promasp):
        """Calclucates mundane/zodiacal directions of the promissor to aspects of planets"""
        for s in range(planets.Planets.BODIES_NUM):
            if not self.options.sigplanets[s]:
                continue
            if idprom == planets.Planets.ANODE and s == planets.Planets.DNODE or idprom == planets.Planets.DNODE and s == planets.Planets.ANODE:
                continue
            plsig = self.chart.planets.planets[s]
            if self.abort.abort:
                return
            for asidx in range(chart.Chart.OPPOSITIO + 1):
                if not self.options.pdaspects[asidx] or idprom == s and asidx == chart.Chart.CONIUNCTIO:
                    continue
                if not mundane and not self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS] and asidx > chart.Chart.CONIUNCTIO:
                    continue
                if s >= planets.Planets.PLANETS_NUM and asidx > chart.Chart.CONIUNCTIO:
                    break
                if self.abort.abort:
                    return
                self.toPlanet(mundane, idprom, primdirs.PrimDir.NONE, lonprom, latprom, raprom, declprom, promasp, s, asidx)

    def toLoF(self, idprom, idprom2, lonprom, latprom, promasp, aspect=0.0, calcsecmotion=False):
        lonsig = self.chart.fortune.fortune[fortune.Fortune.LON]
        pltmp = self.chart.planets.planets[0]
        ok, wsig, spole, seastern, md, umd = self.getZodW(pltmp, lonsig, 0.0)
        if not ok:
            return
        ok, wprom, ppole, seastern, md, umd = self.getZodW(pltmp, lonprom, latprom, spole, seastern)
        if not ok:
            return
        arc = wprom - wsig
        ok = True
        if calcsecmotion and idprom == planets.Planets.MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion:
            for itera in range(self.options.pdsecmotioniter + 1):
                ok, arc = self.calcArcWithSMLoF(idprom, promasp, aspect, arc)
                if not ok:
                    break

        if ok:
            self.create(False, idprom, idprom2, primdirs.PrimDir.LOF, promasp, chart.Chart.CONIUNCTIO, arc)

    def toCustomer2(self, mundane, idprom, idprom2, lonprom, latprom, raprom, declprom, promasp, aspect=0.0, calcsecmotion=False):
        wprom, wsig = (0.0, 0.0)
        if mundane or self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            wsig = self.chart.usersigpd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.W]
            polesig = self.chart.usersigpd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.POLE]
            val = math.tan(math.radians(declprom)) * math.tan(math.radians(polesig))
            if math.fabs(val) > 1.0:
                return
            qprom = math.degrees(math.asin(val))
            if self.chart.usersigpd.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                wprom = raprom - qprom
            else:
                wprom = raprom + qprom
            wprom = util.normalize(wprom)
        else:
            lonsig = self.chart.usersigpd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
            pltmp = self.chart.planets.planets[0]
            ok, wsig, spole, seastern, md, umd = self.getZodW(pltmp, lonsig, 0.0)
            if not ok:
                return
            ok, wprom, ppole, seastern, md, umd = self.getZodW(pltmp, lonprom, latprom, spole, seastern)
            if not ok:
                return
        arc = wprom - wsig
        ok = True
        if calcsecmotion and idprom == planets.Planets.MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion:
            for itera in range(self.options.pdsecmotioniter + 1):
                ok, arc = self.calcArcWithSMCustomer2(mundane, idprom, promasp, aspect, arc)
                if not ok:
                    break

        if ok:
            self.create(mundane, idprom, idprom2, primdirs.PrimDir.USERPD, promasp, chart.Chart.CONIUNCTIO, arc)

    def toSyzygy(self, idprom, idprom2, lonprom, latprom, promasp, aspect=0.0, calcsecmotion=False):
        lonsig = self.chart.syzygy.speculum[syzygy.Syzygy.LON]
        pltmp = self.chart.planets.planets[0]
        ok, wsig, spole, seastern, md, umd = self.getZodW(pltmp, lonsig, 0.0)
        if not ok:
            return
        ok, wprom, ppole, seastern, md, umd = self.getZodW(pltmp, lonprom, latprom, spole, seastern)
        if not ok:
            return
        arc = wprom - wsig
        ok = True
        if calcsecmotion and idprom == planets.Planets.MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion:
            for itera in range(self.options.pdsecmotioniter + 1):
                ok, arc = self.calcArcWithSMSyzygy(idprom, promasp, aspect, arc)
                if not ok:
                    break

        if ok:
            self.create(False, idprom, idprom2, primdirs.PrimDir.SYZ, promasp, chart.Chart.CONIUNCTIO, arc)

    def toParallels(self, idprom, lonprom, latprom):
        for s in range(planets.Planets.PLANETS_NUM):
            if not self.options.sigplanets[s]:
                continue
            plsig = self.chart.planets.planets[s]
            ok = self.chart.zodpars.pars[s].valid
            points = self.chart.zodpars.pars[s].pts
            if not ok:
                continue
            for k in range(len(points)):
                if points[k][0] == -1.0:
                    continue
                if self.abort.abort:
                    return
                ok, wsig, spole, seastern, md, umd = self.getZodW(plsig, points[k][0], 0.0)
                if not ok:
                    continue
                ok, wprom, ppole, seastern, md, umd = self.getZodW(plsig, lonprom, latprom, spole, seastern)
                if not ok:
                    continue
                arc = wprom - wsig
                self.create(False, idprom, primdirs.PrimDir.NONE, s, chart.Chart.CONIUNCTIO, points[k][1], arc)

    def getZodW(self, pl, lon, lat, spole=None, seastern=None):
        """Calculates W, pole of the zodiacal(Regiomontan) point"""
        ra, decl, dist = astrology.swe_cotrans(lon, lat, 1.0, -self.chart.obl[0])
        eastern = True
        if seastern == None:
            if self.ramc > self.raic:
                if ra > self.raic and ra < self.ramc:
                    eastern = False
            elif ra > self.raic and ra < 360.0 or ra < self.ramc and ra > 0.0:
                eastern = False
        else:
            eastern = seastern
        med = math.fabs(self.ramc - ra)
        if med > 180.0:
            med = 360.0 - med
        icd = math.fabs(self.raic - ra)
        if icd > 180.0:
            icd = 360.0 - icd
        md = med
        umd = True
        if icd < med:
            md = icd
            umd = False
        zd = pl.speculums[planets.Planet.REGIOMONTANIAN].getZD(md, self.chart.place.lat, decl, umd)
        val = math.sin(math.radians(self.chart.place.lat)) * math.sin(math.radians(zd))
        if math.fabs(val) > 1.0:
            return (False, 0.0, 0.0, 0.0, 0.0, 0.0)
        else:
            pole = math.degrees(math.asin(val))
            p = pole
            if spole != None:
                p = spole
            val = math.tan(math.radians(decl)) * math.tan(math.radians(p))
            if math.fabs(val) > 1.0:
                return (False, 0.0, 0.0, 0.0, 0.0, 0.0)
            Q = math.degrees(math.asin(val))
            W = 0.0
            if eastern:
                W = ra - Q
            else:
                W = ra + Q
            return (True, util.normalize(W), pole, eastern, md, umd)

    def calcArcWithSMLoF(self, idprom, psidx, aspect, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        pllon = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
        pllat = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
        lonprom = util.normalize(pllon + aspect)
        latprom = 0.0
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            if self.options.bianchini:
                val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                if math.fabs(val) > 1.0:
                    return (False, 0.0)
                latprom = math.degrees(math.asin(val))
            else:
                latprom = pllat
        lonsig = self.chart.fortune.fortune[fortune.Fortune.LON]
        pltmp = self.chart.planets.planets[0]
        ok, wsig, spole, seastern, md, umd = self.getZodW(pltmp, lonsig, 0.0)
        if not ok:
            return (False, 0.0)
        ok, wprom, ppole, seastern, md, umd = self.getZodW(pltmp, lonprom, latprom, spole, seastern)
        if not ok:
            return (False, 0.0)
        arc = wprom - wsig
        return (
         True, arc)

    def calcArcWithSMSyzygy(self, idprom, psidx, aspect, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        pllon = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
        pllat = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
        lonprom = util.normalize(pllon + aspect)
        latprom = 0.0
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            if self.options.bianchini:
                val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                if math.fabs(val) > 1.0:
                    return (False, 0.0)
                latprom = math.degrees(math.asin(val))
            else:
                latprom = pllat
        lonsig = self.chart.syzygy.speculum[syzygy.Syzygy.LON]
        pltmp = self.chart.planets.planets[0]
        ok, wsig, spole, seastern, md, umd = self.getZodW(pltmp, lonsig, 0.0)
        if not ok:
            return (False, 0.0)
        ok, wprom, ppole, seastern, md, umd = self.getZodW(pltmp, lonprom, latprom, spole, seastern)
        if not ok:
            return (False, 0.0)
        arc = wprom - wsig
        return (
         True, arc)

    def calcArcWithSM2(self, idprom, psidx, sig, paspect, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        lonprom = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
        pllat = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
        lonprom += paspect
        lonprom = util.normalize(lonprom)
        plsig = self.chart.planets.planets[sig]
        latprom, raprom, declprom = (0.0, 0.0, 0.0)
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            if self.options.bianchini:
                val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                if math.fabs(val) > 1.0:
                    return (False, 0.0)
                latprom = math.degrees(math.asin(val))
            else:
                latprom = pllat
            raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
        else:
            raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        wprom, wsig = (0.0, 0.0)
        if self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            wsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.W]
            val = math.tan(math.radians(declprom)) * math.tan(math.radians(plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.POLE]))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            qprom = math.degrees(math.asin(val))
            if plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                wprom = raprom - qprom
            else:
                wprom = raprom + qprom
            wprom = util.normalize(wprom)
        else:
            lonsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
            ok, wsig, spole, seastern, md, umd = self.getZodW(plsig, lonsig, 0.0)
            if not ok:
                return (False, 0.0)
            ok, wprom, ppole, seastern, md, umd = self.getZodW(plsig, lonprom, latprom, spole, seastern)
            if not ok:
                return (False, 0.0)
        arc = wprom - wsig
        return (True, arc)

    def calcArcWithSMCustomer2(self, mundane, idprom, psidx, paspect, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        lonprom = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
        pllat = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
        lonprom += paspect
        lonprom = util.normalize(lonprom)
        latprom, raprom, declprom = (0.0, 0.0, 0.0)
        if mundane or self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            if not mundane and self.options.bianchini:
                val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                if math.fabs(val) > 1.0:
                    return (False, 0.0)
                latprom = math.degrees(math.asin(val))
            else:
                latprom = pllat
            raprom, declprom, dist = astrology.swe_cotrans(lonprom, latprom, 1.0, -self.chart.obl[0])
        else:
            raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        wprom, wsig = (0.0, 0.0)
        if mundane or self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            wsig = self.chart.usersigpd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.W]
            polesig = self.chart.usersigpd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.POLE]
            val = math.tan(math.radians(declprom)) * math.tan(math.radians(polesig))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            qprom = math.degrees(math.asin(val))
            if self.chart.usersigpd.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                wprom = raprom - qprom
            else:
                wprom = raprom + qprom
            wprom = util.normalize(wprom)
        else:
            lonsig = self.chart.usersigpd.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
            pltmp = self.chart.planets.planets[0]
            ok, wsig, spole, seastern, md, umd = self.getZodW(pltmp, lonsig, 0.0)
            if not ok:
                return (False, 0.0)
            ok, wprom, ppole, seastern, md, umd = self.getZodW(pltmp, lonprom, latprom, spole, seastern)
            if not ok:
                return (False, 0.0)
        arc = wprom - wsig
        return (True, arc)

    def toPlanet(self, mundane, idprom, idprom2, lonprom, latprom, raprom, declprom, promasp, sig, sigasp, calcsecmotion=True, paspect=chart.Chart.NONE):
        plsig = self.chart.planets.planets[sig]
        aspect = chart.Chart.Aspects[sigasp]
        SINISTER = 0
        DEXTER = 1
        for k in range(DEXTER + 1):
            if k == DEXTER:
                if sigasp == chart.Chart.CONIUNCTIO or sigasp == chart.Chart.OPPOSITIO:
                    break
                aspect *= -1
            wprom, wsig = (0.0, 0.0)
            if mundane or self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                wsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.W]
                if sigasp == chart.Chart.CONIUNCTIO:
                    val = math.tan(math.radians(declprom)) * math.tan(math.radians(plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.POLE]))
                    if math.fabs(val) > 1.0:
                        continue
                    qprom = math.degrees(math.asin(val))
                    if plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                        wprom = raprom - qprom
                    else:
                        wprom = raprom + qprom
                    wprom = util.normalize(wprom)
                elif mundane:
                    wsig += aspect
                    wsig = util.normalize(wsig)
                    med = math.fabs(self.ramc - wsig)
                    if med > 180.0:
                        med = 360.0 - med
                    icd = math.fabs(self.raic - wsig)
                    if icd > 180.0:
                        icd = 360.0 - icd
                    mdsig = med
                    if icd < med:
                        mdsig = icd
                    val = math.tan(math.radians(declprom)) * math.tan(math.radians(self.chart.place.lat)) * math.sin(math.radians(mdsig))
                    if math.fabs(val) > 1.0:
                        continue
                    qprom = math.degrees(math.asin(val))
                    eastern = True
                    if self.ramc > self.raic:
                        if wsig > self.raic and wsig < self.ramc:
                            eastern = False
                    elif wsig > self.raic and wsig < 360.0 or wsig < self.ramc and wsig > 0.0:
                        eastern = False
                    if eastern:
                        wprom = raprom - qprom
                    else:
                        wprom = raprom + qprom
                    wprom = util.normalize(wprom)
                else:
                    lonsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON] + aspect
                    lonsig = util.normalize(lonsig)
                    latsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
                    if self.options.bianchini:
                        val = self.getBianchini(latsig, chart.Chart.Aspects[sigasp])
                        if math.fabs(val) > 1.0:
                            continue
                        latsig = math.degrees(math.asin(val))
                    ok, wsig, spole, seastern, md, umd = self.getZodW(plsig, lonsig, latsig)
                    if not ok:
                        continue
                    ok, wprom, ppole, seastern, md, umd = self.getZodW(plsig, lonprom, latprom, spole, seastern)
                    if not ok:
                        continue
            else:
                lonsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON] + aspect
                lonsig = util.normalize(lonsig)
                ok, wsig, spole, seastern, md, umd = self.getZodW(plsig, lonsig, 0.0)
                if not ok:
                    continue
                ok, wprom, ppole, seastern, md, umd = self.getZodW(plsig, lonprom, latprom, spole, seastern)
                if not ok:
                    continue
            arc = wprom - wsig
            ok = True
            if idprom == planets.Planets.MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion and calcsecmotion:
                if paspect == chart.Chart.NONE:
                    for itera in range(self.options.pdsecmotioniter + 1):
                        ok, arc = self.calcArcWithSM(mundane, idprom, latprom, sig, sigasp, aspect, arc)
                        if not ok:
                            break

                else:
                    for itera in range(self.options.pdsecmotioniter + 1):
                        ok, arc = self.calcArcWithSM2(idprom, promasp, sig, paspect, arc)
                        if not ok:
                            break

            if ok:
                self.create(mundane, idprom, idprom2, sig, promasp, sigasp, arc)

    def calcPArcWithSM(self, idprom, idsig, k, arc):
        PARALLEL = 0
        CONTRAPARALLEL = 1
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        raprom = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RA]
        declprom = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.DECL]
        plsig = self.chart.planets.planets[idsig]
        mdsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RMD]
        umdsig = True
        if mdsig < 0.0:
            mdsig *= -1
            umdsig = False
        wsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.W]
        polesig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.POLE]
        ra = self.ramc
        if not umdsig:
            ra = self.raic
        parallelaxis = primdirs.PrimDir.MC
        aspsig = chart.Chart.PARALLEL
        rapprom = 0.0
        if k == PARALLEL:
            parallelaxis = primdirs.PrimDir.MC
            if not plsig.speculums[planets.Planet.REGIOMONTANIAN].abovehorizon:
                parallelaxis = primdirs.PrimDir.IC
            aspsig = chart.Chart.PARALLEL
            wpprom = util.normalize(2 * ra) - wsig
            wpprom = util.normalize(wpprom)
            val = math.tan(math.radians(declprom)) * math.tan(math.radians(polesig))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            qpprom = math.degrees(math.asin(val))
            if plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                rapprom = wpprom - qpprom
            else:
                rapprom = wpprom + qpprom
            rapprom = util.normalize(rapprom)
        else:
            parallelaxis = primdirs.PrimDir.ASC
            if not plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                parallelaxis = primdirs.PrimDir.DESC
            aspsig = chart.Chart.CONTRAPARALLEL
            wpprom = util.normalize(util.normalize(2 * ra) - wsig) + 180.0
            wpprom = util.normalize(wpprom)
            val = math.tan(math.radians(declprom)) * math.tan(math.radians(polesig))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            qpprom = math.degrees(math.asin(val))
            if plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                rapprom = wpprom + qpprom
            else:
                rapprom = wpprom - qpprom
            rapprom = util.normalize(rapprom)
        arc = raprom - rapprom
        return (
         True, arc)

    def calcArcWithSM(self, mundane, idprom, latprom, sig, sigasp, aspect, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        lonprom = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
        raprom = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.RA]
        declprom = sm.planet.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.DECL]
        if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
            raprom, declprom, distprom = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        plsig = self.chart.planets.planets[sig]
        wprom, wsig = (0.0, 0.0)
        if mundane or self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            wsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.W]
            if sigasp == chart.Chart.CONIUNCTIO:
                val = math.tan(math.radians(declprom)) * math.tan(math.radians(plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.POLE]))
                if math.fabs(val) > 1.0:
                    return (False, 0.0)
                qprom = math.degrees(math.asin(val))
                if plsig.speculums[planets.Planet.REGIOMONTANIAN].eastern:
                    wprom = raprom - qprom
                else:
                    wprom = raprom + qprom
                wprom = util.normalize(wprom)
            elif mundane:
                wsig += aspect
                wsig = util.normalize(wsig)
                med = math.fabs(self.ramc - wsig)
                if med > 180.0:
                    med = 360.0 - med
                icd = math.fabs(self.raic - wsig)
                if icd > 180.0:
                    icd = 360.0 - icd
                mdsig = med
                if icd < med:
                    mdsig = icd
                val = math.tan(math.radians(declprom)) * math.tan(math.radians(self.chart.place.lat)) * math.sin(math.radians(mdsig))
                if math.fabs(val) > 1.0:
                    return (False, 0.0)
                qprom = math.degrees(math.asin(val))
                eastern = True
                if self.ramc > self.raic:
                    if wsig > self.raic and wsig < self.ramc:
                        eastern = False
                elif wsig > self.raic and wsig < 360.0 or wsig < self.ramc and wsig > 0.0:
                    eastern = False
                if eastern:
                    wprom = raprom - qprom
                else:
                    wprom = raprom + qprom
                wprom = util.normalize(wprom)
            else:
                lonsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON] + aspect
                lonsig = util.normalize(lonsig)
                latsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LAT]
                if self.options.bianchini:
                    val = self.getBianchini(latsig, chart.Chart.Aspects[sigasp])
                    if math.fabs(val) > 1.0:
                        return (False, 0.0)
                    latsig = math.degrees(math.asin(val))
                ok, wsig, spole, seastern, md, umd = self.getZodW(plsig, lonsig, latsig)
                if not ok:
                    return (False, 0.0)
                ok, wprom, ppole, seastern, md, umd = self.getZodW(plsig, lonprom, latprom, spole, seastern)
                if not ok:
                    return (False, 0.0)
        else:
            lonsig = plsig.speculums[planets.Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON] + aspect
            lonsig = util.normalize(lonsig)
            ok, wsig, spole, seastern, md, umd = self.getZodW(plsig, lonsig, 0.0)
            if not ok:
                return (False, 0.0)
            ok, wprom, ppole, seastern, md, umd = self.getZodW(plsig, lonprom, latprom, spole, seastern)
            if not ok:
                return (False, 0.0)
        arc = wprom - wsig
        return (
         True, arc)