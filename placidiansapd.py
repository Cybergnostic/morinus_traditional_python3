# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math
import astrology
import primdirs
import placidiancommonpd
import planets
import houses
import chart
import fixedstars
import fortune
import syzygy
import secmotion
import userpd
import placspec
import util

class PlacidianSAPD(placidiancommonpd.PlacidianCommonPD):
    """Implements Placidian(Semiarc) Primary Directions"""

    def __init__(self, chrt, options, pdrange, direction, abort):
        placidiancommonpd.PlacidianCommonPD.__init__(self, chrt, options, pdrange, direction, abort)

    def calcInterPlanetary(self, mundane):
        """Calculates mundane/zodiacal directions of the promissors to aspects of significators"""
        for p in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[p]:
                continue
            if self.abort.abort:
                return
            plprom = self.chart.planets.planets[p]
            raprom = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
            adprom = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
            if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                raprom, declprom, dist = astrology.swe_cotrans(plprom.data[planets.Planet.LON], 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                if math.fabs(val) > 1.0:
                    continue
                adprom = math.degrees(math.asin(val))
            self.toPlanets(mundane, p, raprom, adprom)

    def calcCustomerPlanetary(self, mundane):
        """Calculates mundane/zodiacal directions of the Customer-promissor to aspects of significators"""
        lonprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        raprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
        adprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
        if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
            raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                return
            adprom = math.degrees(math.asin(val))
        self.toPlanets(mundane, primdirs.PrimDir.USERPD, raprom, adprom)

    def calcPlanetary2Customer2(self, mundane):
        """Calculates mundane/zodiacal directions of the promissors to the Customer2 point"""
        for p in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[p]:
                continue
            if self.abort.abort:
                return
            plprom = self.chart.planets.planets[p]
            raprom = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
            adprom = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
            if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                raprom, declprom, dist = astrology.swe_cotrans(plprom.data[planets.Planet.LON], 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                if math.fabs(val) > 1.0:
                    continue
                adprom = math.degrees(math.asin(val))
            self.toCustomer2(mundane, p, primdirs.PrimDir.NONE, raprom, adprom, chart.Chart.CONIUNCTIO, 0.0, True)

    def calcAntiscia2Planets(self, mundane):
        """Calculates mundane/zodiacal directions of the antiscia to aspects of significators"""
        self.calcAntiscia2PlanetsSub(mundane, self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcAntiscia2PlanetsSub(mundane, self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)
        if not mundane:
            if self.options.pdlof[0]:
                ant = self.chart.antiscia.lofant
                ralofant = ant.ra
                decllofant = ant.decl
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllofant))
                if math.fabs(val) <= 1.0:
                    adlat = math.degrees(math.asin(val))
                    self.toPlanets(mundane, primdirs.PrimDir.ANTISCIONLOF, ralofant, adlat)
                cant = self.chart.antiscia.lofcontraant
                ralofcant = cant.ra
                decllofcant = cant.decl
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllofcant))
                if math.fabs(val) <= 1.0:
                    adlat = math.degrees(math.asin(val))
                    self.toPlanets(mundane, primdirs.PrimDir.CONTRAANTLOF, ralofcant, adlat)
            for i in range(2):
                ant = self.chart.antiscia.ascmcant[i]
                raant = ant.ra
                declant = ant.decl
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declant))
                if math.fabs(val) > 1.0:
                    continue
                adlat = math.degrees(math.asin(val))
                typ = primdirs.PrimDir.ANTISCIONASC
                if i > 0:
                    typ = primdirs.PrimDir.ANTISCIONMC
                self.toPlanets(mundane, typ, raant, adlat)

            for i in range(2):
                cant = self.chart.antiscia.ascmccontraant[i]
                racant = cant.ra
                declcant = cant.decl
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declcant))
                if math.fabs(val) > 1.0:
                    continue
                adlat = math.degrees(math.asin(val))
                typ = primdirs.PrimDir.CONTRAANTASC
                if i > 0:
                    typ = primdirs.PrimDir.CONTRAANTMC
                self.toPlanets(mundane, typ, racant, adlat)

    def calcAntiscia2PlanetsSub(self, mundane, pls, offs):
        numpls = len(pls)
        for p in range(numpls):
            if not self.options.promplanets[p]:
                continue
            if self.abort.abort:
                return
            plprom = pls[p]
            lonprom = plprom.lon
            raprom = plprom.ra
            declprom = plprom.decl
            if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                continue
            adprom = math.degrees(math.asin(val))
            self.toPlanets(mundane, p + offs, raprom, adprom)

    def calcAntiscia2Customer2(self, mundane):
        """Calculates mundane/zodiacal directions of the antiscia to aspects of significators"""
        self.calcAntiscia2Customer2Sub(mundane, self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcAntiscia2Customer2Sub(mundane, self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)
        if not mundane:
            if self.options.pdlof[0]:
                ant = self.chart.antiscia.lofant
                ralofant = ant.ra
                decllofant = ant.decl
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllofant))
                if math.fabs(val) <= 1.0:
                    adlat = math.degrees(math.asin(val))
                    self.toCustomer2(mundane, primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, ralofant, adlat, chart.Chart.CONIUNCTIO)
                cant = self.chart.antiscia.lofcontraant
                ralofcant = cant.ra
                decllofcant = cant.decl
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllofcant))
                if math.fabs(val) <= 1.0:
                    adlat = math.degrees(math.asin(val))
                    self.toCustomer2(mundane, primdirs.PrimDir.CONTRAANTLOF, primdirs.PrimDir.NONE, ralofcant, adlat, chart.Chart.CONIUNCTIO)
            for i in range(2):
                ant = self.chart.antiscia.ascmcant[i]
                raant = ant.ra
                declant = ant.decl
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declant))
                if math.fabs(val) > 1.0:
                    continue
                adlat = math.degrees(math.asin(val))
                typ = primdirs.PrimDir.ANTISCIONASC
                if i > 0:
                    typ = primdirs.PrimDir.ANTISCIONMC
                self.toCustomer2(mundane, typ, primdirs.PrimDir.NONE, raant, adlat, chart.Chart.CONIUNCTIO)

            for i in range(2):
                cant = self.chart.antiscia.ascmccontraant[i]
                racant = cant.ra
                declcant = cant.decl
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declcant))
                if math.fabs(val) > 1.0:
                    continue
                adlat = math.degrees(math.asin(val))
                typ = primdirs.PrimDir.CONTRAANTASC
                if i > 0:
                    typ = primdirs.PrimDir.CONTRAANTMC
                self.toCustomer2(mundane, typ, primdirs.PrimDir.NONE, racant, adlat, chart.Chart.CONIUNCTIO)

    def calcAntiscia2Customer2Sub(self, mundane, pls, offs):
        numpls = len(pls)
        for p in range(numpls):
            if not self.options.promplanets[p]:
                continue
            if self.abort.abort:
                return
            plprom = pls[p]
            lonprom = plprom.lon
            raprom = plprom.ra
            declprom = plprom.decl
            if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                continue
            adprom = math.degrees(math.asin(val))
            self.toCustomer2(mundane, p + offs, primdirs.PrimDir.NONE, raprom, adprom, chart.Chart.CONIUNCTIO)

    def calcZodPromAspsInterPlanetary(self):
        """Calclucates zodiacal directions of the aspects of promissors to significators"""
        SINISTER = 0
        DEXTER = 1
        for p in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            pllat = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LAT]
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
                    lon = plprom.data[planets.Planet.LON] + aspect
                    lon = util.normalize(lon)
                    raprom, adprom = (0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        latprom = 0.0
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    else:
                        raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    for s in range(planets.Planets.BODIES_NUM):
                        if not self.options.sigplanets[s]:
                            continue
                        if self.abort.abort:
                            return
                        self.toPlanet(False, p, primdirs.PrimDir.NONE, raprom, adprom, psidx, s, chart.Chart.CONIUNCTIO, True, aspect)

    def calcZodPromAspsInterPlanetary2Customer2(self):
        """Calclucates zodiacal directions of the aspects of promissors to Customer2"""
        SINISTER = 0
        DEXTER = 1
        for p in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            pllat = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LAT]
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
                    lon = plprom.data[planets.Planet.LON] + aspect
                    lon = util.normalize(lon)
                    raprom, adprom = (0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        latprom = 0.0
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    else:
                        raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    self.toCustomer2(False, p, primdirs.PrimDir.NONE, raprom, adprom, psidx, aspect, True)

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
                if self.abort.abort:
                    return
                for k in range(DEXTER + 1):
                    aspect = chart.Chart.Aspects[psidx]
                    if k == DEXTER:
                        if psidx == chart.Chart.OPPOSITIO:
                            break
                        aspect *= -1
                    lon = plprom.lon + aspect
                    lon = util.normalize(lon)
                    raprom, adprom = (0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        latprom = 0.0
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    else:
                        raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    for s in range(planets.Planets.BODIES_NUM):
                        if not self.options.sigplanets[s]:
                            continue
                        if self.abort.abort:
                            return
                        self.toPlanet(False, p + offs, primdirs.PrimDir.NONE, raprom, adprom, psidx, s, chart.Chart.CONIUNCTIO)

    def calcZodPromAntisciaAspsInterPlanetary2Customer2(self):
        """Calclucates zodiacal directions of the aspects of Antiscia to Customer2"""
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
                    lon = plprom.lon + aspect
                    lon = util.normalize(lon)
                    raprom, adprom = (0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        latprom = 0.0
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    else:
                        raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    self.toCustomer2(False, p + offs, primdirs.PrimDir.NONE, raprom, adprom, psidx, aspect, True)

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
            if self.abort.abort:
                return
            for k in range(DEXTER + 1):
                aspect = chart.Chart.Aspects[psidx]
                if k == DEXTER:
                    if psidx == chart.Chart.CONIUNCTIO or psidx == chart.Chart.OPPOSITIO:
                        break
                    aspect *= -1
                lon = util.normalize(lonprom + aspect)
                raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                if math.fabs(val) > 1.0:
                    continue
                adprom = math.degrees(math.asin(val))
                for s in range(planets.Planets.BODIES_NUM):
                    if not self.options.sigplanets[s]:
                        continue
                    if self.abort.abort:
                        return
                    plsig = self.chart.planets.planets[s]
                    self.toPlanet(False, p, primdirs.PrimDir.NONE, raprom, adprom, psidx, s, chart.Chart.CONIUNCTIO)

    def calcZodAsc2AspPlanets(self):
        """Calculates zodiacal Asc to Planets and their aspects"""
        lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
        raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
        if math.fabs(val) > 1.0:
            return
        adprom = math.degrees(math.asin(val))
        self.toPlanets(False, primdirs.PrimDir.ASC, raprom, adprom)

    def calcZodAsc2ParallelPlanets(self):
        lonprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]
        raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
        if math.fabs(val) > 1.0:
            return
        adprom = math.degrees(math.asin(val))
        self.toZodParallels(primdirs.PrimDir.ASC, primdirs.PrimDir.NONE, raprom, adprom)

    def calcZodMC2AspPlanets(self):
        """Calculates zodiacal MC to Planets and their aspects"""
        lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
        raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
        if math.fabs(val) > 1.0:
            return
        adprom = math.degrees(math.asin(val))
        self.toPlanets(False, primdirs.PrimDir.MC, raprom, adprom)

    def calcZodMC2ParallelPlanets(self):
        lonprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]
        raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
        if math.fabs(val) > 1.0:
            return
        adprom = math.degrees(math.asin(val))
        self.toZodParallels(primdirs.PrimDir.MC, primdirs.PrimDir.NONE, raprom, adprom)

    def calcZodAsc2HCs(self):
        """Calculates zodiacal Asc to housecusps"""
        raprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.RA]
        declprom = self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.DECL]
        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
        if math.fabs(val) > 1.0:
            return
        adprom = math.degrees(math.asin(val))
        dsa = 90.0 + adprom
        nsa = 90.0 - adprom
        self.toHCs(False, primdirs.PrimDir.ASC, raprom, dsa, nsa, chart.Chart.CONIUNCTIO)

    def calcZodMC2HCs(self):
        """Calculates zodiacal MC to housecusps"""
        raprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.RA]
        declprom = self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.DECL]
        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
        if math.fabs(val) > 1.0:
            return
        adprom = math.degrees(math.asin(val))
        dsa = 90.0 + adprom
        nsa = 90.0 - adprom
        self.toHCs(False, primdirs.PrimDir.MC, raprom, dsa, nsa, chart.Chart.CONIUNCTIO)

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
            if self.abort.abort:
                return
            for k in range(DEXTER + 1):
                aspect = chart.Chart.Aspects[psidx]
                if k == DEXTER:
                    if psidx == chart.Chart.CONIUNCTIO or psidx == chart.Chart.OPPOSITIO:
                        break
                    aspect *= -1
                lon = util.normalize(lonprom + aspect)
                raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                if math.fabs(val) > 1.0:
                    continue
                adprom = math.degrees(math.asin(val))
                self.toLoF(p, primdirs.PrimDir.NONE, raprom, adprom, psidx)

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
            if self.abort.abort:
                return
            for k in range(DEXTER + 1):
                aspect = chart.Chart.Aspects[psidx]
                if k == DEXTER:
                    if psidx == chart.Chart.CONIUNCTIO or psidx == chart.Chart.OPPOSITIO:
                        break
                    aspect *= -1
                lon = util.normalize(lonprom + aspect)
                raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                if math.fabs(val) > 1.0:
                    continue
                adprom = math.degrees(math.asin(val))
                self.toCustomer2(False, p, primdirs.PrimDir.NONE, raprom, adprom, psidx, aspect)

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
            if self.abort.abort:
                return
            for k in range(DEXTER + 1):
                aspect = chart.Chart.Aspects[psidx]
                if k == DEXTER:
                    if psidx == chart.Chart.CONIUNCTIO or psidx == chart.Chart.OPPOSITIO:
                        break
                    aspect *= -1
                lon = util.normalize(lonprom + aspect)
                raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                if math.fabs(val) > 1.0:
                    continue
                adprom = math.degrees(math.asin(val))
                self.toSyzygy(p, primdirs.PrimDir.NONE, raprom, adprom, psidx)

    def calcZodLoF2Planets(self):
        """Calculates zodiacal LoF to Planets and their aspects"""
        raprom = self.chart.fortune.fortune[fortune.Fortune.RA]
        declprom = self.chart.fortune.fortune[fortune.Fortune.DECL]
        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
        if math.fabs(val) > 1.0:
            return
        adprom = math.degrees(math.asin(val))
        self.toPlanets(False, primdirs.PrimDir.LOF, raprom, adprom)

    def calcZodLoF2Customer2(self):
        """Calculates zodiacal LoF to Customer2"""
        raprom = self.chart.fortune.fortune[fortune.Fortune.RA]
        declprom = self.chart.fortune.fortune[fortune.Fortune.DECL]
        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
        if math.fabs(val) > 1.0:
            return
        adprom = math.degrees(math.asin(val))
        self.toCustomer2(False, primdirs.PrimDir.LOF, primdirs.PrimDir.NONE, raprom, adprom, chart.Chart.CONIUNCTIO)

    def calcZodPlanets2LoF(self):
        """Calculates zodiacal Planets and their aspects to LoF"""
        SINISTER = 0
        DEXTER = 1
        for p in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            pllat = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LAT]
            if self.abort.abort:
                return
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
                    lon = plprom.data[planets.Planet.LON] + aspect
                    lon = util.normalize(lon)
                    raprom, adprom = (0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        latprom = 0.0
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    else:
                        raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    if self.abort.abort:
                        return
                    self.toLoF(p, primdirs.PrimDir.NONE, raprom, adprom, psidx, aspect, True)

    def calcZodPlanets2Syzygy(self):
        """Calculates zodiacal Planets and their aspects to Syzygy"""
        SINISTER = 0
        DEXTER = 1
        for p in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            pllat = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LAT]
            if self.abort.abort:
                return
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
                    lon = plprom.data[planets.Planet.LON] + aspect
                    lon = util.normalize(lon)
                    raprom, adprom = (0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        latprom = 0.0
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    else:
                        raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    if self.abort.abort:
                        return
                    self.toSyzygy(p, primdirs.PrimDir.NONE, raprom, adprom, psidx, aspect, True)

    def calcZodCustomer2LoF(self):
        """Calculates zodiacal Customer to LoF"""
        lonprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        raprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
        adprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
        if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
            raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                return
            adprom = math.degrees(math.asin(val))
        self.toLoF(primdirs.PrimDir.USERPD, primdirs.PrimDir.NONE, raprom, adprom, chart.Chart.CONIUNCTIO)

    def calcZodCustomer2Syzygy(self):
        """Calculates zodiacal Customer to Syzygy"""
        lonprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        raprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
        adprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
        if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
            raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                return
            adprom = math.degrees(math.asin(val))
        self.toSyzygy(primdirs.PrimDir.USERPD, primdirs.PrimDir.NONE, raprom, adprom, chart.Chart.CONIUNCTIO)

    def calcZodAntiscia2LoF(self):
        """Calculates zodiacal Antiscia and their aspects to LoF"""
        self.calcZodAntiscia2LoFSub(self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcZodAntiscia2LoFSub(self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)
        if self.options.pdlof[0]:
            ant = self.chart.antiscia.lofant
            ralofant = ant.ra
            decllofant = ant.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllofant))
            if math.fabs(val) <= 1.0:
                adlat = math.degrees(math.asin(val))
                self.toLoF(primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, ralofant, adlat, chart.Chart.CONIUNCTIO)
            cant = self.chart.antiscia.lofcontraant
            ralofcant = ant.ra
            decllofcant = ant.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllofcant))
            if math.fabs(val) <= 1.0:
                adlat = math.degrees(math.asin(val))
                self.toLoF(primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, ralofcant, adlat, chart.Chart.CONIUNCTIO)
        for i in range(2):
            ant = self.chart.antiscia.ascmcant[i]
            raant = ant.ra
            declant = ant.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declant))
            if math.fabs(val) > 1.0:
                continue
            adlat = math.degrees(math.asin(val))
            typ = primdirs.PrimDir.ANTISCIONASC
            if i > 0:
                typ = primdirs.PrimDir.ANTISCIONMC
            self.toLoF(typ, primdirs.PrimDir.NONE, raant, adlat, chart.Chart.CONIUNCTIO)

        for i in range(2):
            cant = self.chart.antiscia.ascmccontraant[i]
            racant = ant.ra
            declcant = ant.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declcant))
            if math.fabs(val) > 1.0:
                continue
            adlat = math.degrees(math.asin(val))
            typ = primdirs.PrimDir.CONTRAANTASC
            if i > 0:
                typ = primdirs.PrimDir.CONTRAANTMC
            self.toLoF(typ, primdirs.PrimDir.NONE, racant, adlat, chart.Chart.CONIUNCTIO)

    def calcZodAntiscia2LoFSub(self, pls, offs):
        SINISTER = 0
        DEXTER = 1
        for p in range(len(pls)):
            if not self.options.promplanets[p]:
                continue
            plprom = pls[p]
            pllat = plprom.lat
            if self.abort.abort:
                return
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
                    lon = plprom.lon + aspect
                    lon = util.normalize(lon)
                    raprom, adprom = (0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        latprom = 0.0
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    else:
                        raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    if self.abort.abort:
                        return
                    self.toLoF(p + offs, primdirs.PrimDir.NONE, raprom, adprom, psidx)

    def calcZodAntiscia2Syzygy(self):
        """Calculates zodiacal Antiscia and their aspects to Syzygy"""
        self.calcZodAntiscia2SyzygySub(self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcZodAntiscia2SyzygySub(self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)
        if self.options.pdlof[0]:
            ant = self.chart.antiscia.lofant
            ralofant = ant.ra
            decllofant = ant.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllofant))
            if math.fabs(val) <= 1.0:
                adlat = math.degrees(math.asin(val))
                self.toSyzygy(primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, ralofant, adlat, chart.Chart.CONIUNCTIO)
            cant = self.chart.antiscia.lofcontraant
            ralofcant = ant.ra
            decllofcant = ant.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllofcant))
            if math.fabs(val) <= 1.0:
                adlat = math.degrees(math.asin(val))
                self.toSyzygy(primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, ralofcant, adlat, chart.Chart.CONIUNCTIO)
        for i in range(2):
            ant = self.chart.antiscia.ascmcant[i]
            raant = ant.ra
            declant = ant.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declant))
            if math.fabs(val) > 1.0:
                continue
            adlat = math.degrees(math.asin(val))
            typ = primdirs.PrimDir.ANTISCIONASC
            if i > 0:
                typ = primdirs.PrimDir.ANTISCIONMC
            self.toSyzygy(typ, primdirs.PrimDir.NONE, raant, adlat, chart.Chart.CONIUNCTIO)

        for i in range(2):
            cant = self.chart.antiscia.ascmccontraant[i]
            racant = ant.ra
            declcant = ant.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declcant))
            if math.fabs(val) > 1.0:
                continue
            adlat = math.degrees(math.asin(val))
            typ = primdirs.PrimDir.CONTRAANTASC
            if i > 0:
                typ = primdirs.PrimDir.CONTRAANTMC
            self.toSyzygy(typ, primdirs.PrimDir.NONE, racant, adlat, chart.Chart.CONIUNCTIO)

    def calcZodAntiscia2SyzygySub(self, pls, offs):
        SINISTER = 0
        DEXTER = 1
        numpls = len(pls)
        for p in range(numpls):
            if not self.options.promplanets[p]:
                continue
            plprom = pls[p]
            pllat = plprom.lat
            if self.abort.abort:
                return
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
                    lon = plprom.lon + aspect
                    lon = util.normalize(lon)
                    raprom, adprom = (0.0, 0.0)
                    if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                        latprom = 0.0
                        if self.options.bianchini:
                            val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                            if math.fabs(val) > 1.0:
                                continue
                            latprom = math.degrees(math.asin(val))
                        else:
                            latprom = pllat
                        raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    else:
                        raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
                        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                        if math.fabs(val) > 1.0:
                            continue
                        adprom = math.degrees(math.asin(val))
                    if self.abort.abort:
                        return
                    self.toSyzygy(p + offs, primdirs.PrimDir.NONE, raprom, adprom, psidx)

    def calcZodTerms(self):
        """Calculates zodiacal terms to Planets, LoF, Syzygy and Customer2"""
        num = len(self.options.terms[0])
        subnum = len(self.options.terms[0][0])
        for i in range(num):
            summa = 0
            for j in range(subnum):
                lonprom = i * chart.Chart.SIGN_DEG + summa
                if self.options.ayanamsha != 0:
                    lonprom += self.chart.ayanamsha
                    lonprom = util.normalize(lonprom)
                raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                if math.fabs(val) > 1.0:
                    continue
                adprom = math.degrees(math.asin(val))
                if self.abort.abort:
                    return
                for s in range(planets.Planets.BODIES_NUM):
                    if self.options.sigplanets[s]:
                        self.toPlanet(False, primdirs.PrimDir.TERM + i, self.options.terms[self.options.selterm][i][j][0], raprom, adprom, chart.Chart.CONIUNCTIO, s, chart.Chart.CONIUNCTIO)

                if self.options.pdlof[1]:
                    self.toLoF(primdirs.PrimDir.TERM + i, self.options.terms[self.options.selterm][i][j][0], raprom, adprom, chart.Chart.CONIUNCTIO)
                if self.chart.htype == chart.Chart.RADIX:
                    if self.options.pdsyzygy:
                        self.toSyzygy(primdirs.PrimDir.TERM + i, self.options.terms[self.options.selterm][i][j][0], raprom, adprom, chart.Chart.CONIUNCTIO)
                    if self.options.pduser2 and self.chart.usersigpd != None:
                        self.toCustomer2(False, primdirs.PrimDir.TERM + i, self.options.terms[self.options.selterm][i][j][0], raprom, adprom, chart.Chart.CONIUNCTIO)
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
            rastar = star[fixedstars.FixedStars.RA]
            declstar = star[fixedstars.FixedStars.DECL]
            if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                rastar, declstar, dist = astrology.swe_cotrans(lonstar, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declstar))
            if math.fabs(val) > 1.0:
                continue
            adstar = math.degrees(math.asin(val))
            for s in range(planets.Planets.BODIES_NUM):
                if not self.options.sigplanets[s]:
                    continue
                if self.abort.abort:
                    return
                self.toPlanet(False, i + OFFS, primdirs.PrimDir.NONE, rastar, adstar, chart.Chart.CONIUNCTIO, s, chart.Chart.CONIUNCTIO)

    def calcZodFixedStars2Customer2(self):
        """Calculates zodiacal directions of fixedstars to Customer2"""
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
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declstar))
            if math.fabs(val) > 1.0:
                continue
            adstar = math.degrees(math.asin(val))
            self.toCustomer2(False, i + OFFS, primdirs.PrimDir.NONE, rastar, adstar, chart.Chart.CONIUNCTIO)

    def calcParallels(self):
        """Calculates mundo parallels"""
        PARALLEL = 0
        CONTRAPARALLEL = 1
        for p in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[p]:
                continue
            plprom = self.chart.planets.planets[p]
            raprom = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
            adprom = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
            for s in range(planets.Planets.BODIES_NUM):
                if not self.options.sigplanets[s]:
                    continue
                if p == planets.Planets.ANODE and s == planets.Planets.DNODE or p == planets.Planets.DNODE and s == planets.Planets.ANODE:
                    continue
                if self.abort.abort:
                    return
                plsig = self.chart.planets.planets[s]
                for k in range(CONTRAPARALLEL + 1):
                    if self.abort.abort:
                        return
                    t, v, ra, mdpersasig = (0, 0, 0.0, 0.0)
                    parallelaxis = primdirs.PrimDir.MC
                    aspsig = chart.Chart.PARALLEL
                    mdsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
                    if mdsig < 0.0:
                        mdsig *= -1
                    sasig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.SA]
                    if sasig < 0.0:
                        sasig *= -1
                    mdpersasig = mdsig / sasig
                    if k == PARALLEL:
                        parallelaxis = primdirs.PrimDir.MC
                        if not plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon:
                            parallelaxis = primdirs.PrimDir.IC
                        aspsig = chart.Chart.PARALLEL
                        t, v, ra = self.getparvars(plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon, plsig.speculums[planets.Planet.PLACIDIAN].eastern)
                    else:
                        parallelaxis = primdirs.PrimDir.ASC
                        if not plsig.speculums[planets.Planet.PLACIDIAN].eastern:
                            parallelaxis = primdirs.PrimDir.DESC
                        aspsig = chart.Chart.CONTRAPARALLEL
                        t, v, ra = self.getcontraparvars(plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon, plsig.speculums[planets.Planet.PLACIDIAN].eastern)
                    arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
                    if p == planets.Planets.MOON and self.options.pdsecmotion:
                        for itera in range(self.options.pdsecmotioniter + 1):
                            arc = self.calcPArcWithSM(p, s, k, arc)

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
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                continue
            adprom = math.degrees(math.asin(val))
            for s in range(planets.Planets.BODIES_NUM):
                if not self.options.sigplanets[s]:
                    continue
                if p == planets.Planets.ANODE and s == planets.Planets.DNODE or p == planets.Planets.DNODE and s == planets.Planets.ANODE:
                    continue
                if self.abort.abort:
                    return
                plsig = self.chart.planets.planets[s]
                for k in range(CONTRAPARALLEL + 1):
                    if self.abort.abort:
                        return
                    t, v, ra, mdpersasig = (0, 0, 0.0, 0.0)
                    parallelaxis = primdirs.PrimDir.MC
                    aspsig = chart.Chart.PARALLEL
                    mdsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
                    if mdsig < 0.0:
                        mdsig *= -1
                    sasig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.SA]
                    if sasig < 0.0:
                        sasig *= -1
                    mdpersasig = mdsig / sasig
                    if k == PARALLEL:
                        parallelaxis = primdirs.PrimDir.MC
                        if not plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon:
                            parallelaxis = primdirs.PrimDir.IC
                        aspsig = chart.Chart.PARALLEL
                        t, v, ra = self.getparvars(plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon, plsig.speculums[planets.Planet.PLACIDIAN].eastern)
                    else:
                        parallelaxis = primdirs.PrimDir.ASC
                        if not plsig.speculums[planets.Planet.PLACIDIAN].eastern:
                            parallelaxis = primdirs.PrimDir.DESC
                        aspsig = chart.Chart.CONTRAPARALLEL
                        t, v, ra = self.getcontraparvars(plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon, plsig.speculums[planets.Planet.PLACIDIAN].eastern)
                    arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
                    self.create(True, p + offs, primdirs.PrimDir.NONE, s, chart.Chart.CONIUNCTIO, aspsig, arc, parallelaxis)

    def calcCustomer2Parallels(self):
        """Calculates mundo parallels of the Customer Point"""
        PARALLEL = 0
        CONTRAPARALLEL = 1
        lonprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        raprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
        adprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
        for s in range(planets.Planets.BODIES_NUM):
            if not self.options.sigplanets[s]:
                continue
            if self.abort.abort:
                return
            plsig = self.chart.planets.planets[s]
            for k in range(CONTRAPARALLEL + 1):
                if self.abort.abort:
                    return
                t, v, ra, mdpersasig = (0, 0, 0.0, 0.0)
                parallelaxis = primdirs.PrimDir.MC
                aspsig = chart.Chart.PARALLEL
                mdsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
                if mdsig < 0.0:
                    mdsig *= -1
                sasig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.SA]
                if sasig < 0.0:
                    sasig *= -1
                mdpersasig = mdsig / sasig
                if k == PARALLEL:
                    parallelaxis = primdirs.PrimDir.MC
                    if not plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon:
                        parallelaxis = primdirs.PrimDir.IC
                    aspsig = chart.Chart.PARALLEL
                    t, v, ra = self.getparvars(plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon, plsig.speculums[planets.Planet.PLACIDIAN].eastern)
                else:
                    parallelaxis = primdirs.PrimDir.ASC
                    if not plsig.speculums[planets.Planet.PLACIDIAN].eastern:
                        parallelaxis = primdirs.PrimDir.DESC
                    aspsig = chart.Chart.CONTRAPARALLEL
                    t, v, ra = self.getcontraparvars(plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon, plsig.speculums[planets.Planet.PLACIDIAN].eastern)
                arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
                self.create(True, primdirs.PrimDir.USERPD, primdirs.PrimDir.NONE, s, chart.Chart.CONIUNCTIO, aspsig, arc, parallelaxis)

    def calcZodParallels(self):
        """Calculates zodiacal parallels"""
        if self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS]:
            for p in range(planets.Planets.BODIES_NUM):
                if not self.options.promplanets[p]:
                    continue
                if self.abort.abort:
                    return
                plprom = self.chart.planets.planets[p]
                lonprom = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
                raprom, adprom = (0.0, 0.0)
                if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                    raprom = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
                    adprom = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
                else:
                    raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
                    val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                    if math.fabs(val) > 1.0:
                        continue
                    adprom = math.degrees(math.asin(val))
                self.toZodParallels(p, primdirs.PrimDir.NONE, raprom, adprom)

            if self.options.pduser and self.chart.userprompd != None:
                lonprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
                ok = True
                raprom, adprom = (0.0, 0.0)
                if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                    raprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
                    adprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
                else:
                    raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
                    val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                    if math.fabs(val) > 1.0:
                        ok = False
                    else:
                        adprom = math.degrees(math.asin(val))
                if ok:
                    self.toZodParallels(primdirs.PrimDir.USERPD, primdirs.PrimDir.NONE, raprom, adprom)
        if self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS]:
            for p in range(planets.Planets.PLANETS_NUM):
                if not self.options.promplanets[p]:
                    continue
                if self.abort.abort:
                    return
                ok = self.chart.zodpars.pars[p].valid
                points = self.chart.zodpars.pars[p].pts
                if not ok:
                    continue
                for k in range(len(points)):
                    if points[k][0] == -1.0:
                        continue
                    raprom, declprom, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
                    val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                    if math.fabs(val) > 1.0:
                        continue
                    adprom = math.degrees(math.asin(val))
                    for s in range(planets.Planets.BODIES_NUM):
                        if not self.options.sigplanets[s]:
                            continue
                        if self.abort.abort:
                            return
                        self.toPlanet(False, p, primdirs.PrimDir.NONE, raprom, adprom, points[k][1], s, chart.Chart.CONIUNCTIO, False)

                    if self.options.pduser2 and self.chart.usersigpd != None:
                        self.toCustomer2(False, p, primdirs.PrimDir.NONE, raprom, adprom, points[k][1])

        return

    def calcZodAntisciaParallels(self):
        """Calculates zodiacal parallels(Antiscia)"""
        self.calcZodAntisciaParallelsSub(self.chart.antiscia.plantiscia, self.chart.antzodpars.apars, primdirs.PrimDir.ANTISCION)
        self.calcZodAntisciaParallelsSub(self.chart.antiscia.plcontraant, self.chart.antzodpars.cpars, primdirs.PrimDir.CONTRAANT)

    def calcZodAntisciaParallelsSub(self, pls, pars, offs):
        if self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS]:
            numpls = len(pls)
            for p in range(numpls):
                if not self.options.promplanets[p]:
                    continue
                if self.abort.abort:
                    return
                plprom = pls[p]
                lonprom = plprom.lon
                pllat = plprom.lat
                raprom, adprom = (0.0, 0.0)
                if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                    raprom, declprom, dist = astrology.swe_cotrans(lon, pllat, 1.0, -self.chart.obl[0])
                    val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                    if math.fabs(val) > 1.0:
                        continue
                    adprom = math.degrees(math.asin(val))
                else:
                    raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
                    val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                    if math.fabs(val) > 1.0:
                        continue
                    adprom = math.degrees(math.asin(val))
                self.toZodParallels(p + offs, primdirs.PrimDir.NONE, raprom, adprom)

            if self.options.pdlof[0]:
                ant = self.chart.antiscia.lofant
                ralofant = ant.ra
                decllofant = ant.decl
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllofant))
                if math.fabs(val) <= 1.0:
                    adlat = math.degrees(math.asin(val))
                    self.toZodParallels(primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.NONE, ralofant, adlat)
                cant = self.chart.antiscia.lofcontraant
                ralofcant = cant.ra
                decllofcant = cant.decl
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decllofcant))
                if math.fabs(val) <= 1.0:
                    adlat = math.degrees(math.asin(val))
                    self.toZodParallels(primdirs.PrimDir.CONTRAANTLOF, primdirs.PrimDir.NONE, ralofcant, adlat)
            for i in range(2):
                ant = self.chart.antiscia.ascmcant[i]
                raant = ant.ra
                declant = ant.decl
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declant))
                if math.fabs(val) > 1.0:
                    continue
                adlat = math.degrees(math.asin(val))
                typ = primdirs.PrimDir.ANTISCIONASC
                if i > 0:
                    typ = primdirs.PrimDir.ANTISCIONMC
                self.toZodParallels(typ, primdirs.PrimDir.NONE, raant, adlat)

            for i in range(2):
                cant = self.chart.antiscia.ascmccontraant[i]
                racant = cant.ra
                declcant = cant.decl
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declcant))
                if math.fabs(val) > 1.0:
                    continue
                adlat = math.degrees(math.asin(val))
                typ = primdirs.PrimDir.CONTRAANTASC
                if i > 0:
                    typ = primdirs.PrimDir.CONTRAANTMC
                self.toZodParallels(typ, primdirs.PrimDir.NONE, racant, adlat)

        if self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS]:
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
                    raprom, declprom, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
                    val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                    if math.fabs(val) > 1.0:
                        continue
                    adprom = math.degrees(math.asin(val))
                    for s in range(planets.Planets.BODIES_NUM):
                        if not self.options.sigplanets[s]:
                            continue
                        if self.abort.abort:
                            return
                        self.toPlanet(False, p + offs, primdirs.PrimDir.NONE, raprom, adprom, points[k][1], s, chart.Chart.CONIUNCTIO)

    def calcZodLoF2ZodParallels(self):
        """Calculates zodiacal LoF to zodiacal parallels"""
        raprom = self.chart.fortune.fortune[fortune.Fortune.RA]
        declprom = self.chart.fortune.fortune[fortune.Fortune.DECL]
        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
        if math.fabs(val) > 1.0:
            return
        adprom = math.degrees(math.asin(val))
        self.toZodParallels(primdirs.PrimDir.LOF, primdirs.PrimDir.NONE, raprom, adprom)

    def calcZodLoF2Syzygy(self):
        """Calculates zodiacal LoF to Syzygy"""
        raprom = self.chart.fortune.fortune[fortune.Fortune.RA]
        declprom = self.chart.fortune.fortune[fortune.Fortune.DECL]
        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
        if math.fabs(val) > 1.0:
            return
        adprom = math.degrees(math.asin(val))
        self.toSyzygy(primdirs.PrimDir.LOF, primdirs.PrimDir.NONE, raprom, adprom, chart.Chart.CONIUNCTIO)

    def calcZodParallels2LoF(self):
        """Calculates zodiacal parallels to zodiacal LoF"""
        for p in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[p]:
                continue
            if self.abort.abort:
                return
            ok = self.chart.zodpars.pars[p].valid
            points = self.chart.zodpars.pars[p].pts
            if not ok:
                continue
            for k in range(len(points)):
                if points[k][0] == -1.0:
                    continue
                raprom, declprom, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                if math.fabs(val) > 1.0:
                    continue
                adprom = math.degrees(math.asin(val))
                self.toLoF(p, primdirs.PrimDir.NONE, raprom, adprom, points[k][1])

    def calcZodParallels2Syzygy(self):
        """Calculates zodiacal parallels to zodiacal Syzygy"""
        for p in range(planets.Planets.PLANETS_NUM):
            if not self.options.promplanets[p]:
                continue
            if self.abort.abort:
                return
            ok = self.chart.zodpars.pars[p].valid
            points = self.chart.zodpars.pars[p].pts
            if not ok:
                continue
            for k in range(len(points)):
                if points[k][0] == -1.0:
                    continue
                raprom, declprom, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                if math.fabs(val) > 1.0:
                    continue
                adprom = math.degrees(math.asin(val))
                self.toSyzygy(p, primdirs.PrimDir.NONE, raprom, adprom, points[k][1])

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
                raprom, declprom, dist = astrology.swe_cotrans(points[k][0], 0.0, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                if math.fabs(val) > 1.0:
                    continue
                adprom = math.degrees(math.asin(val))
                self.toLoF(p + offs, primdirs.PrimDir.NONE, raprom, adprom, points[k][1])

    def calcZodMidPoints(self):
        """Calclucates zodiacal midpoint directions"""
        mids = self.chart.midpoints.mids
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            mids = self.chart.midpoints.midslat
        for mid in mids:
            if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
                continue
            if self.abort.abort:
                return
            for s in range(planets.Planets.BODIES_NUM):
                if not self.options.sigplanets[s]:
                    continue
                if self.abort.abort:
                    return
                plsig = self.chart.planets.planets[s]
                lonsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
                lonmid = mid.m
                if math.fabs(lonmid - lonsig) > 90.0:
                    lonmid += 180.0
                    if lonmid >= 360.0:
                        lonmid -= 360.0
                raprom, declprom, dist = astrology.swe_cotrans(lonmid, mid.lat, 1.0, -self.chart.obl[0])
                val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
                if math.fabs(val) > 1.0:
                    continue
                adprom = math.degrees(math.asin(val))
                self.toPlanet(False, mid.p1, mid.p2, raprom, adprom, chart.Chart.MIDPOINT, s, chart.Chart.CONIUNCTIO)

    def calcZodMidPoints2LoF(self):
        """Calclucates zodiacal midpoint directions to LoF"""
        lonsig = self.chart.fortune.fortune[fortune.Fortune.LON]
        mids = self.chart.midpoints.mids
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            mids = self.chart.midpoints.midslat
        for mid in mids:
            if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
                continue
            lonmid = mid.m
            if self.abort.abort:
                return
            if math.fabs(lonmid - lonsig) > 90.0:
                lonmid += 180.0
                if lonmid >= 360.0:
                    lonmid -= 360.0
            raprom, declprom, dist = astrology.swe_cotrans(lonmid, mid.lat, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                continue
            adprom = math.degrees(math.asin(val))
            self.toLoF(mid.p1, mid.p2, raprom, adprom, chart.Chart.MIDPOINT)

    def calcZodMidPoints2Syzygy(self):
        """Calclucates zodiacal midpoint directions to Syzygy"""
        lonsig = self.chart.syzygy.speculum[syzygy.Syzygy.LON]
        mids = self.chart.midpoints.mids
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            mids = self.chart.midpoints.midslat
        for mid in mids:
            if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
                continue
            lonmid = mid.m
            if self.abort.abort:
                return
            if math.fabs(lonmid - lonsig) > 90.0:
                lonmid += 180.0
                if lonmid >= 360.0:
                    lonmid -= 360.0
            raprom, declprom, dist = astrology.swe_cotrans(lonmid, mid.lat, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                continue
            adprom = math.degrees(math.asin(val))
            self.toSyzygy(mid.p1, mid.p2, raprom, adprom, chart.Chart.MIDPOINT)

    def calcZodMidPoints2Customer2(self):
        """Calclucates zodiacal midpoint directions to Customer"""
        lonsig = self.chart.usersigpd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        mids = self.chart.midpoints.mids
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            mids = self.chart.midpoints.midslat
        for mid in mids:
            if not self.options.promplanets[mid.p1] or not self.options.promplanets[mid.p2]:
                continue
            lonmid = mid.m
            if self.abort.abort:
                return
            if math.fabs(lonmid - lonsig) > 90.0:
                lonmid += 180.0
                if lonmid >= 360.0:
                    lonmid -= 360.0
            raprom, declprom, dist = astrology.swe_cotrans(lonmid, mid.lat, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                continue
            adprom = math.degrees(math.asin(val))
            self.toCustomer2(False, mid.p1, mid.p2, raprom, adprom, chart.Chart.MIDPOINT)

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
            rastar = star[fixedstars.FixedStars.RA]
            declstar = star[fixedstars.FixedStars.DECL]
            if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                rastar, declstar, dist = astrology.swe_cotrans(lonstar, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declstar))
            if math.fabs(val) > 1.0:
                continue
            adstar = math.degrees(math.asin(val))
            self.toLoF(i + OFFS, primdirs.PrimDir.NONE, rastar, adstar, chart.Chart.CONIUNCTIO)

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
            rastar = star[fixedstars.FixedStars.RA]
            declstar = star[fixedstars.FixedStars.DECL]
            if self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
                rastar, declstar, dist = astrology.swe_cotrans(lonstar, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declstar))
            if math.fabs(val) > 1.0:
                continue
            adstar = math.degrees(math.asin(val))
            self.toSyzygy(i + OFFS, primdirs.PrimDir.NONE, rastar, adstar, chart.Chart.CONIUNCTIO)

    def calcPlanets2MLoF(self):
        for p in range(planets.Planets.BODIES_NUM):
            if not self.options.promplanets[p]:
                continue
            if self.abort.abort:
                return
            plprom = self.chart.planets.planets[p]
            raprom = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
            adprom = plprom.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
            self.toMundaneLoF(p, primdirs.PrimDir.NONE, raprom, adprom)

    def calcCustomer2MLoF(self):
        raprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
        adprom = self.chart.userprompd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
        self.toMundaneLoF(primdirs.PrimDir.USERPD, primdirs.PrimDir.NONE, raprom, adprom)

    def calcAntiscia2MLoF(self):
        self.calcAntiscia2MLoFSub(self.chart.antiscia.plantiscia, primdirs.PrimDir.ANTISCION)
        self.calcAntiscia2MLoFSub(self.chart.antiscia.plcontraant, primdirs.PrimDir.CONTRAANT)

    def calcAntiscia2MLoFSub(self, pls, offs):
        for p in range(len(pls)):
            if not self.options.promplanets[p]:
                continue
            if self.abort.abort:
                return
            plprom = pls[p]
            lonprom = plprom.lon
            raprom = plprom.ra
            declprom = plprom.decl
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                continue
            adprom = math.degrees(math.asin(val))
            self.toMundaneLoF(p + offs, primdirs.PrimDir.NONE, raprom, adprom, False)

    def calcRaptParallels(self):
        """Computes mundane Rapt Parallels (Roberto)"""
        MP = placspec.PlacidianSpeculum.PMP
        SPECULUM = planets.Planet.PLACIDIAN
        ordered = []
        mixed = []
        for i in range(planets.Planets.BODIES_NUM):
            ordered.append(self.chart.planets.planets[i])
            mixed.append(i)

        for j in range(planets.Planets.BODIES_NUM):
            for i in range(planets.Planets.BODIES_NUM - 1):
                if ordered[i].speculums[SPECULUM].speculum[MP] > ordered[(i + 1)].speculums[SPECULUM].speculum[MP]:
                    tmp = ordered[i]
                    ordered[i] = ordered[(i + 1)]
                    ordered[i + 1] = tmp
                    tmp = mixed[i]
                    mixed[i] = mixed[(i + 1)]
                    mixed[i + 1] = tmp

        num = len(ordered)
        for p1 in range(num):
            if not self.options.promplanets[mixed[p1]]:
                continue
            plprom1 = ordered[p1]
            raprom1 = plprom1.speculums[SPECULUM].speculum[placspec.PlacidianSpeculum.RA]
            pmpprom1 = plprom1.speculums[SPECULUM].speculum[placspec.PlacidianSpeculum.PMP]
            dsaprom1 = plprom1.speculums[SPECULUM].speculum[placspec.PlacidianSpeculum.SA]
            nsaprom1 = plprom1.speculums[SPECULUM].speculum[placspec.PlacidianSpeculum.SA]
            if dsaprom1 < 0.0:
                nsaprom1 = -dsaprom1
                dsaprom1 = 180.0 - nsaprom1
            else:
                nsaprom1 = 180.0 - dsaprom1
            umdprom1 = plprom1.speculums[SPECULUM].speculum[placspec.PlacidianSpeculum.MD]
            lmdprom1 = plprom1.speculums[SPECULUM].speculum[placspec.PlacidianSpeculum.MD]
            if umdprom1 < 0.0:
                lmdprom1 = -umdprom1
                umdprom1 = 180.0 - lmdprom1
            else:
                lmdprom1 = 180.0 - umdprom1
            for p2 in range(p1 + 1, num):
                if not self.options.promplanets[mixed[p2]]:
                    continue
                if mixed[p1] == planets.Planets.ANODE and mixed[p2] == planets.Planets.DNODE or mixed[p1] == planets.Planets.DNODE and mixed[p2] == planets.Planets.ANODE:
                    continue
                plprom2 = ordered[p2]
                raprom2 = plprom2.speculums[SPECULUM].speculum[placspec.PlacidianSpeculum.RA]
                pmpprom2 = plprom2.speculums[SPECULUM].speculum[placspec.PlacidianSpeculum.PMP]
                dsaprom2 = plprom2.speculums[SPECULUM].speculum[placspec.PlacidianSpeculum.SA]
                nsaprom2 = plprom2.speculums[SPECULUM].speculum[placspec.PlacidianSpeculum.SA]
                if dsaprom2 < 0.0:
                    nsaprom2 = -dsaprom2
                    dsaprom2 = 180.0 - nsaprom2
                else:
                    nsaprom2 = 180.0 - dsaprom2
                umdprom2 = plprom2.speculums[SPECULUM].speculum[placspec.PlacidianSpeculum.MD]
                lmdprom2 = plprom2.speculums[SPECULUM].speculum[placspec.PlacidianSpeculum.MD]
                if umdprom2 < 0.0:
                    lmdprom2 = -umdprom2
                    umdprom2 = 180.0 - lmdprom2
                else:
                    lmdprom2 = 180.0 - umdprom2
                switched = False
                diffRA = raprom2 - raprom1
                if diffRA < 0.0:
                    diffRA += 360.0
                if diffRA > 180.0:
                    diffRA = 360.0 - diffRA
                    tmp = p1
                    p1 = p2
                    p2 = tmp
                    tmpra = raprom1
                    tmppmp = pmpprom1
                    tmpdsa = dsaprom1
                    tmpnsa = nsaprom1
                    tmpumd = umdprom1
                    tmplmd = lmdprom1
                    raprom1 = raprom2
                    pmpprom1 = pmpprom2
                    dsaprom1 = dsaprom2
                    nsaprom1 = nsaprom2
                    umdprom1 = umdprom2
                    lmdprom1 = lmdprom2
                    raprom2 = tmpra
                    pmpprom2 = tmppmp
                    dsaprom2 = tmpdsa
                    nsaprom2 = tmpnsa
                    umdprom2 = tmpumd
                    lmdprom2 = tmplmd
                    switched = True
                puxASC = (180.0 - diffRA) / (dsaprom1 + nsaprom2) * dsaprom1
                plxIC = diffRA / (nsaprom1 + nsaprom2) * nsaprom1
                plxDSC = (180.0 - diffRA) / (nsaprom1 + dsaprom2) * nsaprom1
                puxMC = diffRA / (dsaprom1 + dsaprom2) * dsaprom1
                if self.options.sigascmc[0]:
                    if pmpprom1 >= 0.0 and pmpprom1 < 90.0 or pmpprom1 >= 270.0 and pmpprom1 < 360.0:
                        arc = umdprom1 - puxASC
                        mp1 = mixed[p1]
                        mp2 = mixed[p2]
                        if arc < 0.0:
                            mp1, mp2 = self.swap(mp1, mp2)
                        self.create(True, mp1, mp2, primdirs.PrimDir.ASC, chart.Chart.CONIUNCTIO, chart.Chart.RAPTPAR, arc, primdirs.PrimDir.ASC)
                    if pmpprom1 >= 90.0 and pmpprom1 < 270.0:
                        if puxASC >= lmdprom1:
                            arc = lmdprom1 + 180.0 - puxASC
                            mp1 = mixed[p1]
                            mp2 = mixed[p2]
                            if arc < 0.0:
                                mp1, mp2 = self.swap(mp1, mp2)
                            self.create(True, mp1, mp2, primdirs.PrimDir.ASC, chart.Chart.CONIUNCTIO, chart.Chart.RAPTPAR, arc, primdirs.PrimDir.ASC)
                        if puxASC < lmdprom1:
                            arc = -umdprom1 - puxASC
                            mp1 = mixed[p1]
                            mp2 = mixed[p2]
                            if arc < 0.0:
                                mp1, mp2 = self.swap(mp1, mp2)
                            self.create(True, mp1, mp2, primdirs.PrimDir.ASC, chart.Chart.CONIUNCTIO, chart.Chart.RAPTPAR, arc, primdirs.PrimDir.ASC)
                if self.options.sigascmc[1]:
                    if pmpprom1 >= 0.0 and pmpprom1 < 90.0 or pmpprom1 >= 270.0 and pmpprom1 < 360.0:
                        arc = plxIC - lmdprom1
                        mp1 = mixed[p1]
                        mp2 = mixed[p2]
                        if arc < 0.0:
                            mp1, mp2 = self.swap(mp1, mp2)
                        self.create(True, mp1, mp2, primdirs.PrimDir.IC, chart.Chart.CONIUNCTIO, chart.Chart.RAPTPAR, arc, primdirs.PrimDir.IC)
                    if pmpprom1 >= 90.0 and pmpprom1 < 270.0:
                        if plxIC < umdprom1:
                            arc = lmdprom1 + plxIC
                            mp1 = mixed[p1]
                            mp2 = mixed[p2]
                            if arc < 0.0:
                                mp1, mp2 = self.swap(mp1, mp2)
                            self.create(True, mp1, mp2, primdirs.PrimDir.IC, chart.Chart.CONIUNCTIO, chart.Chart.RAPTPAR, arc, primdirs.PrimDir.IC)
                        if plxIC >= umdprom1:
                            arc = -umdprom1 - (180.0 - plxIC)
                            mp1 = mixed[p1]
                            mp2 = mixed[p2]
                            if arc < 0.0:
                                mp1, mp2 = self.swap(mp1, mp2)
                            self.create(True, mp1, mp2, primdirs.PrimDir.IC, chart.Chart.CONIUNCTIO, chart.Chart.RAPTPAR, arc, primdirs.PrimDir.IC)
                if self.options.sigascmc[0]:
                    if pmpprom1 >= 0.0 and pmpprom1 < 90.0 or pmpprom1 >= 270.0 and pmpprom1 < 360.0:
                        if plxDSC >= umdprom1:
                            arc = umdprom1 + 180.0 - plxDSC
                            mp1 = mixed[p1]
                            mp2 = mixed[p2]
                            if arc < 0.0:
                                mp1, mp2 = self.swap(mp1, mp2)
                            self.create(True, mp1, mp2, primdirs.PrimDir.DESC, chart.Chart.CONIUNCTIO, chart.Chart.RAPTPAR, arc, primdirs.PrimDir.DESC)
                        if plxDSC < umdprom1:
                            arc = -lmdprom1 - plxDSC
                            mp1 = mixed[p1]
                            mp2 = mixed[p2]
                            if arc < 0.0:
                                mp1, mp2 = self.swap(mp1, mp2)
                            self.create(True, mp1, mp2, primdirs.PrimDir.DESC, chart.Chart.CONIUNCTIO, chart.Chart.RAPTPAR, arc, primdirs.PrimDir.DESC)
                    if pmpprom1 >= 90.0 and pmpprom1 < 270.0:
                        arc = lmdprom1 - plxDSC
                        mp1 = mixed[p1]
                        mp2 = mixed[p2]
                        if arc < 0.0:
                            mp1, mp2 = self.swap(mp1, mp2)
                        self.create(True, mp1, mp2, primdirs.PrimDir.DESC, chart.Chart.CONIUNCTIO, chart.Chart.RAPTPAR, arc, primdirs.PrimDir.DESC)
                if self.options.sigascmc[1]:
                    if pmpprom1 >= 0.0 and pmpprom1 < 90.0 or pmpprom1 >= 270.0 and pmpprom1 < 360.0:
                        if puxMC < lmdprom1:
                            arc = umdprom1 + puxMC
                            mp1 = mixed[p1]
                            mp2 = mixed[p2]
                            if arc < 0.0:
                                mp1, mp2 = self.swap(mp1, mp2)
                            self.create(True, mp1, mp2, primdirs.PrimDir.MC, chart.Chart.CONIUNCTIO, chart.Chart.RAPTPAR, arc, primdirs.PrimDir.MC)
                        if puxMC >= lmdprom1:
                            arc = -lmdprom1 - (180.0 - puxMC)
                            mp1 = mixed[p1]
                            mp2 = mixed[p2]
                            if arc < 0.0:
                                mp1, mp2 = self.swap(mp1, mp2)
                            self.create(True, mp1, mp2, primdirs.PrimDir.MC, chart.Chart.CONIUNCTIO, chart.Chart.RAPTPAR, arc, primdirs.PrimDir.MC)
                    if pmpprom1 >= 90.0 and pmpprom1 < 270.0:
                        arc = puxMC - umdprom1
                        mp1 = mixed[p1]
                        mp2 = mixed[p2]
                        if arc < 0.0:
                            mp1, mp2 = self.swap(mp1, mp2)
                        self.create(True, mp1, mp2, primdirs.PrimDir.MC, chart.Chart.CONIUNCTIO, chart.Chart.RAPTPAR, arc, primdirs.PrimDir.MC)
                if switched:
                    tmp = p1
                    p1 = p2
                    p2 = tmp
                    tmpra = raprom1
                    tmppmp = pmpprom1
                    tmpdsa = dsaprom1
                    tmpnsa = nsaprom1
                    tmpumd = umdprom1
                    tmplmd = lmdprom1
                    raprom1 = raprom2
                    pmpprom1 = pmpprom2
                    dsaprom1 = dsaprom2
                    nsaprom1 = nsaprom2
                    umdprom1 = umdprom2
                    lmdprom1 = lmdprom2
                    raprom2 = tmpra
                    pmpprom2 = tmppmp
                    dsaprom2 = tmpdsa
                    nsaprom2 = tmpnsa
                    umdprom2 = tmpumd
                    lmdprom2 = tmplmd

    def swap(self, x, y):
        return (
         y, x)

    def toPlanets(self, mundane, p, raprom, adprom):
        """Calculates the directions of the promissor to the planets and their aspects"""
        SINISTER = 0
        DEXTER = 1
        for s in range(planets.Planets.BODIES_NUM):
            if not self.options.sigplanets[s]:
                continue
            if self.abort.abort:
                return
            if p == planets.Planets.ANODE and s == planets.Planets.DNODE or p == planets.Planets.DNODE and s == planets.Planets.ANODE:
                continue
            for asidx in range(chart.Chart.OPPOSITIO + 1):
                if not self.options.pdaspects[asidx] or p == s and asidx == chart.Chart.CONIUNCTIO:
                    continue
                if not mundane and not self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS] and asidx > chart.Chart.CONIUNCTIO:
                    continue
                if self.abort.abort:
                    return
                if s >= planets.Planets.PLANETS_NUM and asidx > chart.Chart.CONIUNCTIO:
                    break
                self.toPlanet(mundane, p, primdirs.PrimDir.NONE, raprom, adprom, chart.Chart.CONIUNCTIO, s, asidx)

    def toPlanet(self, mundane, idprom, idprom2, raprom, adprom, promasp, sig, sigasp, calcsecmotion=True, paspect=chart.Chart.NONE):
        plsig = self.chart.planets.planets[sig]
        aspect = chart.Chart.Aspects[sigasp]
        SINISTER = 0
        DEXTER = 1
        for k in range(DEXTER + 1):
            if k == DEXTER:
                if sigasp == chart.Chart.CONIUNCTIO or sigasp == chart.Chart.OPPOSITIO:
                    break
                aspect *= -1
            t, v, ra, mdpersasig = (0, 0, 0.0, 0.0)
            if mundane or self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
                if sigasp == chart.Chart.CONIUNCTIO:
                    t, v, ra = self.getvars(plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon, plsig.speculums[planets.Planet.PLACIDIAN].eastern)
                    mdsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
                    if mdsig < 0.0:
                        mdsig *= -1
                    sasig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.SA]
                    if sasig < 0.0:
                        sasig *= -1
                    mdpersasig = mdsig / sasig
                elif mundane:
                    pmpsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP]
                    pmpap = pmpsig + aspect
                    pmpap = util.normalize(pmpap)
                    if pmpap >= 0.0 and pmpap < 90.0:
                        mdpersasig = 1.0 - pmpap / 90.0
                        t = 1.0
                        v = -1.0
                        ra = self.raic
                    elif pmpap >= 90.0 and pmpap < 180.0:
                        mdpersasig = pmpap / 90.0 - 1.0
                        t = -1.0
                        v = -1.0
                        ra = self.raic
                    elif pmpap >= 180.0 and pmpap < 270.0:
                        mdpersasig = 3.0 - pmpap / 90.0
                        t = 1.0
                        v = 1.0
                        ra = self.ramc
                    elif pmpap >= 270.0 and pmpap < 360.0:
                        mdpersasig = pmpap / 90.0 - 3.0
                        t = -1.0
                        v = 1.0
                        ra = self.ramc
                else:
                    lonsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON] + aspect
                    lonsig = util.normalize(lonsig)
                    latsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LAT]
                    if self.options.bianchini:
                        val = self.getBianchini(latsig, chart.Chart.Aspects[sigasp])
                        if math.fabs(val) > 1.0:
                            continue
                        latsig = math.degrees(math.asin(val))
                    ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig, latsig)
                    if not ok:
                        continue
                    t, v, ra = self.getvars(abovehorizon, eastern)
                    mdpersasig = mdsig / sasig
            else:
                lonsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON] + aspect
                lonsig = util.normalize(lonsig)
                ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig)
                if not ok:
                    continue
                t, v, ra = self.getvars(abovehorizon, eastern)
                mdpersasig = mdsig / sasig
            arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
            ok = True
            if idprom == planets.Planets.MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion and calcsecmotion:
                if paspect == chart.Chart.NONE:
                    for itera in range(self.options.pdsecmotioniter + 1):
                        ok, arc = self.calcArcWithSM(mundane, idprom, sig, sigasp, aspect, arc)
                        if not ok:
                            break

                else:
                    for itera in range(self.options.pdsecmotioniter + 1):
                        ok, arc = self.calcArcWithSM2(idprom, promasp, sig, paspect, arc)
                        if not ok:
                            break

            if ok:
                self.create(mundane, idprom, idprom2, sig, promasp, sigasp, arc)

    def toLoF(self, idprom, idprom2, raprom, adprom, promasp, aspect=0.0, calcsecmotion=False):
        lonsig = self.chart.fortune.fortune[fortune.Fortune.LON]
        ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig)
        if not ok:
            return
        t, v, ra = self.getvars(abovehorizon, eastern)
        mdpersasig = mdsig / sasig
        arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
        ok = True
        if calcsecmotion and idprom == planets.Planets.MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion:
            for itera in range(self.options.pdsecmotioniter + 1):
                ok, arc = self.calcArcWithSMLoF(idprom, promasp, aspect, arc)
                if not ok:
                    break

        if ok:
            self.create(False, idprom, idprom2, primdirs.PrimDir.LOF, promasp, chart.Chart.CONIUNCTIO, arc)

    def toCustomer2(self, mundane, idprom, idprom2, raprom, adprom, promasp, aspect=0.0, calcsecmotion=False):
        t, v, ra, mdsigpersasig = (0, 0, 0.0, 0.0)
        if mundane or self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            mdsig = self.chart.usersigpd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
            sasig = self.chart.usersigpd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.SA]
            if mdsig < 0.0:
                mdsig *= -1
            if sasig < 0.0:
                sasig *= -1
            mdsigpersasig = mdsig / sasig
            t, v, ra = self.getvars(self.chart.usersigpd.speculums[planets.Planet.PLACIDIAN].abovehorizon, self.chart.usersigpd.speculums[planets.Planet.PLACIDIAN].eastern)
        else:
            lonsig = self.chart.usersigpd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
            ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig)
            if not ok:
                return
            t, v, ra = self.getvars(abovehorizon, eastern)
            mdsigpersasig = mdsig / sasig
        arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdsigpersasig
        ok = True
        if calcsecmotion and idprom == planets.Planets.MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion:
            for itera in range(self.options.pdsecmotioniter + 1):
                ok, arc = self.calcArcWithSMCustomer2(mundane, idprom, promasp, aspect, arc)
                if not ok:
                    break

        if ok:
            self.create(mundane, idprom, idprom2, primdirs.PrimDir.USERPD, promasp, chart.Chart.CONIUNCTIO, arc)

    def toSyzygy(self, idprom, idprom2, raprom, adprom, promasp, aspect=0.0, calcsecmotion=False):
        lonsig = self.chart.syzygy.speculum[syzygy.Syzygy.LON]
        ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig)
        if not ok:
            return
        t, v, ra = self.getvars(abovehorizon, eastern)
        mdpersasig = mdsig / sasig
        arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
        ok = True
        if calcsecmotion and idprom == planets.Planets.MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion:
            for itera in range(self.options.pdsecmotioniter + 1):
                ok, arc = self.calcArcWithSMSyzygy(idprom, promasp, aspect, arc)
                if not ok:
                    break

        if ok:
            self.create(False, idprom, idprom2, primdirs.PrimDir.SYZ, promasp, chart.Chart.CONIUNCTIO, arc)

    def toMundaneLoF(self, idprom, idprom2, raprom, adprom, calcsecmotion=True):
        SINISTER = 0
        DEXTER = 1
        for sigasp in range(chart.Chart.OPPOSITIO + 1):
            if not self.options.pdaspects[sigasp]:
                continue
            if self.abort.abort:
                return
            aspect = chart.Chart.Aspects[sigasp]
            for k in range(DEXTER + 1):
                if k == DEXTER:
                    if sigasp == chart.Chart.CONIUNCTIO or sigasp == chart.Chart.OPPOSITIO:
                        break
                    aspect *= -1
                t, v, ra, mdpersasig = (0, 0, 0.0, 0.0)
                if sigasp == chart.Chart.CONIUNCTIO:
                    t, v, ra = self.getvars(self.chart.munfortune.speculum.abovehorizon, self.chart.munfortune.speculum.eastern)
                    mdsig = math.fabs(self.chart.munfortune.speculum.speculum[placspec.PlacidianSpeculum.MD])
                    sasig = math.fabs(self.chart.munfortune.speculum.speculum[placspec.PlacidianSpeculum.SA])
                    mdpersasig = mdsig / sasig
                else:
                    pmpsig = self.chart.munfortune.speculum.speculum[placspec.PlacidianSpeculum.PMP]
                    pmpap = pmpsig + aspect
                    pmpap = util.normalize(pmpap)
                    if pmpap >= 0.0 and pmpap < 90.0:
                        mdpersasig = 1.0 - pmpap / 90.0
                        t = 1.0
                        v = -1.0
                        ra = self.raic
                    elif pmpap >= 90.0 and pmpap < 180.0:
                        mdpersasig = pmpap / 90.0 - 1.0
                        t = -1.0
                        v = -1.0
                        ra = self.raic
                    elif pmpap >= 180.0 and pmpap < 270.0:
                        mdpersasig = 3.0 - pmpap / 90.0
                        t = 1.0
                        v = 1.0
                        ra = self.ramc
                    elif pmpap >= 270.0 and pmpap < 360.0:
                        mdpersasig = pmpap / 90.0 - 3.0
                        t = -1.0
                        v = 1.0
                        ra = self.ramc
                arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
                if calcsecmotion and idprom == planets.Planets.MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion:
                    for itera in range(self.options.pdsecmotioniter + 1):
                        arc = self.calcArcWithSMMLoF(idprom, sigasp, aspect, arc)

                self.create(True, idprom, idprom2, primdirs.PrimDir.LOF, chart.Chart.CONIUNCTIO, sigasp, arc)

    def toZodParallels(self, idprom, idprom2, raprom, adprom):
        """Calculates directions of the promissor to zodiacal parallels of the planets"""
        for s in range(planets.Planets.PLANETS_NUM):
            if not self.options.sigplanets[s]:
                continue
            if self.abort.abort:
                return
            ok = self.chart.zodpars.pars[s].valid
            points = self.chart.zodpars.pars[s].pts
            if not ok:
                continue
            for k in range(len(points)):
                if points[k][0] == -1.0:
                    continue
                if self.abort.abort:
                    return
                ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(points[k][0])
                if not ok:
                    continue
                t, v, ra = self.getvars(abovehorizon, eastern)
                arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdsig / sasig
                self.create(False, idprom, primdirs.PrimDir.NONE, s, chart.Chart.CONIUNCTIO, points[k][1], arc)

    def getZodMDSA(self, lon, lat=0.0):
        """Calculates md, sa of the zodiacal point"""
        ra, decl, dist = astrology.swe_cotrans(lon, lat, 1.0, -self.chart.obl[0])
        eastern = True
        if self.ramc > self.raic:
            if ra > self.raic and ra < self.ramc:
                eastern = False
        else:
            if ra > self.raic and ra < 360.0 or ra < self.ramc and ra > 0.0:
                eastern = False
        med = math.fabs(self.ramc - ra)
        if med > 180.0:
            med = 360.0 - med
        icd = math.fabs(self.raic - ra)
        if icd > 180.0:
            icd = 360.0 - icd
        md = med
        val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(decl))
        if math.fabs(val) > 1.0:
            return (False, 0.0, 0.0, 0.0, 0.0)
        adlat = math.degrees(math.asin(val))
        dsa = 90.0 + adlat
        nsa = 90.0 - adlat
        abovehorizon = True
        if med > dsa:
            abovehorizon = False
        sa = dsa
        if not abovehorizon:
            sa = nsa
            md = icd
        return (True, md, sa, abovehorizon, eastern)

    def getvars(self, abovehorizon, eastern):
        t = -1.0
        if eastern and not abovehorizon or not eastern and abovehorizon:
            t = 1.0
        v = 1.0
        ra = self.ramc
        if not abovehorizon:
            v = -1.0
            ra = self.raic
        return (t, v, ra)

    def getparvars(self, abovehorizon, eastern):
        t = 1.0
        if eastern and not abovehorizon or not eastern and abovehorizon:
            t = -1.0
        v = 1.0
        ra = self.ramc
        if not abovehorizon:
            v = -1.0
            ra = self.raic
        return (t, v, ra)

    def getcontraparvars(self, abovehorizon, eastern):
        t = 1.0
        if eastern and not abovehorizon or not eastern and abovehorizon:
            t = -1.0
        v = -1.0
        ra = self.raic
        if not abovehorizon:
            v = 1.0
            ra = self.ramc
        return (t, v, ra)

    def calcArcWithSM(self, mundane, idprom, sig, sigasp, aspect, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        lonprom = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        raprom = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
        adprom = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
        if not mundane and self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH:
            raprom, declprom, dist = astrology.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            adprom = math.degrees(math.asin(val))
        plsig = self.chart.planets.planets[sig]
        t, v, ra, mdpersasig = (0, 0, 0.0, 0.0)
        if mundane or self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            if sigasp == chart.Chart.CONIUNCTIO:
                t, v, ra = self.getvars(plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon, plsig.speculums[planets.Planet.PLACIDIAN].eastern)
                mdsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
                if mdsig < 0.0:
                    mdsig *= -1
                sasig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.SA]
                if sasig < 0.0:
                    sasig *= -1
                mdpersasig = mdsig / sasig
            elif mundane:
                pmpsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP]
                pmpap = pmpsig + aspect
                pmpap = util.normalize(pmpap)
                if pmpap >= 0.0 and pmpap < 90.0:
                    mdpersasig = 1.0 - pmpap / 90.0
                    t = 1.0
                    v = -1.0
                    ra = self.raic
                elif pmpap >= 90.0 and pmpap < 180.0:
                    mdpersasig = pmpap / 90.0 - 1.0
                    t = -1.0
                    v = -1.0
                    ra = self.raic
                elif pmpap >= 180.0 and pmpap < 270.0:
                    mdpersasig = 3.0 - pmpap / 90.0
                    t = 1.0
                    v = 1.0
                    ra = self.ramc
                elif pmpap >= 270.0 and pmpap < 360.0:
                    mdpersasig = pmpap / 90.0 - 3.0
                    t = -1.0
                    v = 1.0
                    ra = self.ramc
            else:
                lonsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON] + aspect
                lonsig = util.normalize(lonsig)
                latsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LAT]
                if self.options.bianchini:
                    val = self.getBianchini(latsig, chart.Chart.Aspects[sigasp])
                    if math.fabs(val) > 1.0:
                        return (False, 0.0)
                    latsig = math.degrees(math.asin(val))
                ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig, latsig)
                if not ok:
                    return (False, 0.0)
                t, v, ra = self.getvars(abovehorizon, eastern)
                mdpersasig = mdsig / sasig
        else:
            lonsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON] + aspect
            lonsig = util.normalize(lonsig)
            ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig)
            if not ok:
                return (False, 0.0)
            t, v, ra = self.getvars(abovehorizon, eastern)
            mdpersasig = mdsig / sasig
        arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
        return (
         True, arc)

    def calcArcWithSM2(self, idprom, psidx, sig, paspect, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        lonprom = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        pllat = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LAT]
        lon = lonprom + paspect
        lon = util.normalize(lon)
        raprom, adprom = (0.0, 0.0)
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            latprom = 0.0
            if self.options.bianchini:
                val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                if math.fabs(val) > 1.0:
                    return (False, 0.0)
                latprom = math.degrees(math.asin(val))
            else:
                latprom = pllat
            raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            adprom = math.degrees(math.asin(val))
        else:
            raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            adprom = math.degrees(math.asin(val))
        plsig = self.chart.planets.planets[sig]
        t, v, ra, mdpersasig = (0, 0, 0.0, 0.0)
        if self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            t, v, ra = self.getvars(plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon, plsig.speculums[planets.Planet.PLACIDIAN].eastern)
            mdsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
            if mdsig < 0.0:
                mdsig *= -1
            sasig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.SA]
            if sasig < 0.0:
                sasig *= -1
            mdpersasig = mdsig / sasig
        else:
            lonsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
            ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig)
            if not ok:
                return (False, 0.0)
            t, v, ra = self.getvars(abovehorizon, eastern)
            mdpersasig = mdsig / sasig
        arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
        return (
         True, arc)

    def calcPArcWithSM(self, idprom, idsig, k, arc):
        PARALLEL = 0
        CONTRAPARALLEL = 1
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        raprom = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
        adprom = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
        plsig = self.chart.planets.planets[idsig]
        t, v, ra, mdpersasig = (0, 0, 0.0, 0.0)
        parallelaxis = primdirs.PrimDir.MC
        aspsig = chart.Chart.PARALLEL
        mdsig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
        if mdsig < 0.0:
            mdsig *= -1
        sasig = plsig.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.SA]
        if sasig < 0.0:
            sasig *= -1
        mdpersasig = mdsig / sasig
        if k == PARALLEL:
            parallelaxis = primdirs.PrimDir.MC
            if not plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon:
                parallelaxis = primdirs.PrimDir.IC
            aspsig = chart.Chart.PARALLEL
            t, v, ra = self.getparvars(plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon, plsig.speculums[planets.Planet.PLACIDIAN].eastern)
        else:
            parallelaxis = primdirs.PrimDir.ASC
            if not plsig.speculums[planets.Planet.PLACIDIAN].eastern:
                parallelaxis = primdirs.PrimDir.DESC
            aspsig = chart.Chart.CONTRAPARALLEL
            t, v, ra = self.getcontraparvars(plsig.speculums[planets.Planet.PLACIDIAN].abovehorizon, plsig.speculums[planets.Planet.PLACIDIAN].eastern)
        arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
        return arc

    def calcArcWithSMMLoF(self, idprom, sigasp, aspect, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        raprom = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
        adprom = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADLAT]
        t, v, ra, mdpersasig = (0, 0, 0.0, 0.0)
        if sigasp == chart.Chart.CONIUNCTIO:
            t, v, ra = self.getvars(self.chart.munfortune.speculum.abovehorizon, self.chart.munfortune.speculum.eastern)
            mdsig = self.chart.munfortune.speculum.speculum[placspec.PlacidianSpeculum.MD]
            sasig = self.chart.munfortune.speculum.speculum[placspec.PlacidianSpeculum.SA]
            mdpersasig = mdsig / sasig
        else:
            pmpsig = self.chart.munfortune.speculum.speculum[placspec.PlacidianSpeculum.PMP]
            pmpap = pmpsig + aspect
            pmpap = util.normalize(pmpap)
            if pmpap >= 0.0 and pmpap < 90.0:
                mdpersasig = 1.0 - pmpap / 90.0
                t = 1.0
                v = -1.0
                ra = self.raic
            elif pmpap >= 90.0 and pmpap < 180.0:
                mdpersasig = pmpap / 90.0 - 1.0
                t = -1.0
                v = -1.0
                ra = self.raic
            elif pmpap >= 180.0 and pmpap < 270.0:
                mdpersasig = 3.0 - pmpap / 90.0
                t = 1.0
                v = 1.0
                ra = self.ramc
            elif pmpap >= 270.0 and pmpap < 360.0:
                mdpersasig = pmpap / 90.0 - 3.0
                t = -1.0
                v = 1.0
                ra = self.ramc
        arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
        return arc

    def calcArcWithSMLoF(self, idprom, psidx, aspect, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        pllon = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        pllat = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LAT]
        lon = pllon + aspect
        lon = util.normalize(lon)
        raprom, adprom = (0.0, 0.0)
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            latprom = 0.0
            if self.options.bianchini:
                val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                if math.fabs(val) > 1.0:
                    return (False, 0.0)
                latprom = math.degrees(math.asin(val))
            else:
                latprom = pllat
            raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            adprom = math.degrees(math.asin(val))
        else:
            raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            adprom = math.degrees(math.asin(val))
        lonsig = self.chart.fortune.fortune[fortune.Fortune.LON]
        ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig)
        if not ok:
            return (False, 0.0)
        t, v, ra = self.getvars(abovehorizon, eastern)
        mdpersasig = mdsig / sasig
        arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
        return (
         True, arc)

    def calcArcWithSMCustomer2(self, mundane, idprom, psidx, aspect, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        pllon = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        pllat = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LAT]
        lon = pllon + aspect
        lon = util.normalize(lon)
        raprom, adprom = (0.0, 0.0)
        if mundane or self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            latprom = 0.0
            if not mundane and self.options.bianchini:
                val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                if math.fabs(val) > 1.0:
                    return (False, 0.0)
                latprom = math.degrees(math.asin(val))
            else:
                latprom = pllat
            raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            adprom = math.degrees(math.asin(val))
        else:
            raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            adprom = math.degrees(math.asin(val))
        t, v, ra, mdsigpersasig = (0, 0, 0.0, 0.0)
        if mundane or self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            mdsig = self.chart.usersigpd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
            sasig = self.chart.usersigpd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.SA]
            if mdsig < 0.0:
                mdsig *= -1
            if sasig < 0.0:
                sasig *= -1
            mdsigpersasig = mdsig / sasig
            t, v, ra = self.getvars(self.chart.usersigpd.speculums[planets.Planet.PLACIDIAN].abovehorizon, self.chart.usersigpd.speculums[planets.Planet.PLACIDIAN].eastern)
        else:
            lonsig = self.chart.usersigpd.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
            ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig)
            if not ok:
                return (False, 0.0)
            t, v, ra = self.getvars(abovehorizon, eastern)
            mdsigpersasig = mdsig / sasig
        arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdsigpersasig
        return (
         True, arc)

    def calcArcWithSMSyzygy(self, idprom, psidx, aspect, arc):
        sm = secmotion.SecMotion(self.chart.time, self.chart.place, idprom, arc, self.chart.place.lat, self.chart.houses.ascmc2, self.options.topocentric)
        pllon = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        pllat = sm.planet.speculums[planets.Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LAT]
        lon = pllon + aspect
        lon = util.normalize(lon)
        raprom, adprom = (0.0, 0.0)
        if self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH:
            latprom = 0.0
            if self.options.bianchini:
                val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
                if math.fabs(val) > 1.0:
                    return (False, 0.0)
                latprom = math.degrees(math.asin(val))
            else:
                latprom = pllat
            raprom, declprom, dist = astrology.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            adprom = math.degrees(math.asin(val))
        else:
            raprom, declprom, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
            val = math.tan(math.radians(self.chart.place.lat)) * math.tan(math.radians(declprom))
            if math.fabs(val) > 1.0:
                return (False, 0.0)
            adprom = math.degrees(math.asin(val))
        lonsig = self.chart.syzygy.speculum[syzygy.Syzygy.LON]
        ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig)
        if not ok:
            return (False, 0.0)
        t, v, ra = self.getvars(abovehorizon, eastern)
        mdpersasig = mdsig / sasig
        arc = self.getDiff(raprom - ra) + t * (90 + v * adprom) * mdpersasig
        return (
         True, arc)