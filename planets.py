# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math, astrology, houses, placspec, regiospec, util

class Planet:
    """Data of a Planet"""
    LON, LAT, DIST, SPLON, SPLAT, SPDIST = range(0, 6)
    RAEQU, DECLEQU, DISTEQU, SPRAEQU, SPDECLEQU, SPDISTEQU = range(0, 6)
    PLACIDIAN = 0
    REGIOMONTANIAN = 1

    def __init__(self, tjd_ut, pId, flag, placelat=None, ascmc2=None, ecl=None, equ=None, nolat=False, obl=0.0):
        if pId < 7:
            pId = util.mapChaldeanToModern(pId)
        self.pId = pId
        self.speculums = None
        if ecl == None:
            rflag, self.data, serr = astrology.swe_calc_ut(tjd_ut, pId, flag)
            rflag, self.dataEqu, serr = astrology.swe_calc_ut(tjd_ut, pId, flag + astrology.SEFLG_EQUATORIAL)
            self.name = astrology.swe_get_planet_name(pId)
        else:
            self.data = tuple(ecl)
            self.dataEqu = tuple(equ)
            self.name = 'DescNode'
        if nolat:
            self.data = (
             self.data[Planet.LON], 0.0, self.data[Planet.DIST], self.data[Planet.SPLON], self.data[Planet.SPLAT], self.data[Planet.SPDIST])
            ra, decl, dist = astrology.swe_cotrans(self.data[Planet.LON], 0.0, 1.0, -obl)
            self.dataEqu = (ra, decl, self.dataEqu[Planet.DISTEQU], self.dataEqu[Planet.SPRAEQU], self.dataEqu[Planet.SPDECLEQU], self.dataEqu[Planet.SPDISTEQU])
        if placelat != None:
            self.speculums = []
            self.speculums.append(placspec.PlacidianSpeculum(placelat, ascmc2, self.data[Planet.LON], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU]))
            self.speculums.append(regiospec.RegiomontanianSpeculum(placelat, ascmc2, self.data[Planet.LON], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU]))
        return

    def calcProfPos(self, prof):
        self.data = (util.normalize(self.data[Planet.LON] + prof.offs), self.data[Planet.LAT], self.data[Planet.DIST], self.data[Planet.SPLON], self.data[Planet.SPLAT], self.data[Planet.SPDIST])
        spec = placspec.PlacidianSpeculum
        self.speculums[0].speculum = (self.data[spec.LON], self.data[spec.LAT], self.dataEqu[spec.RA], self.dataEqu[spec.DECL], self.speculums[0].speculum[spec.ADLAT], self.speculums[0].speculum[spec.SA], self.speculums[0].speculum[spec.MD], self.speculums[0].speculum[spec.HD], self.speculums[0].speculum[spec.TH], self.speculums[0].speculum[spec.HOD], self.speculums[0].speculum[spec.PMP], self.speculums[0].speculum[spec.ADPH], self.speculums[0].speculum[spec.POH], self.speculums[0].speculum[spec.AODO])
        spec = regiospec.RegiomontanianSpeculum
        self.speculums[1].speculum = (self.data[spec.LON], self.data[spec.LAT], self.dataEqu[spec.RA], self.dataEqu[spec.DECL], self.speculums[1].speculum[spec.RMD], self.speculums[1].speculum[spec.RHD], self.speculums[1].speculum[spec.ZD], self.speculums[1].speculum[spec.POLE], self.speculums[1].speculum[spec.Q], self.speculums[1].speculum[spec.W], self.speculums[1].speculum[spec.CMP])

    def calcMundaneProfPos(self, ascmc2, pl, placelat, obl):
        ramc = ascmc2[houses.Houses.MC][houses.Houses.RA]
        raic = ramc + 180.0
        if raic > 360.0:
            raic -= 360.0
        md = pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
        if md < 0.0:
            md *= -1
        ra = pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
        if pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] < 90.0:
            ra = raic - md
        elif pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] >= 90.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] < 180.0:
            ra = raic + md
        elif pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] >= 180.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] < 270.0:
            ra = ramc - md
        elif pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] >= 270.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] < 360.0:
            ra = ramc + md
        ra = util.normalize(ra)
        ao = do = 0.0
        adph = math.fabs(pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.ADPH])
        if placelat == 0.0 or pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.DECL] == 0.0:
            ao = do = ra
        if placelat > 0.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.DECL] > 0.0 or placelat < 0.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.DECL] < 0.0:
            ao = ra - adph
            do = ra + adph
        if placelat > 0.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.DECL] < 0.0 or placelat < 0.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.DECL] > 0.0:
            ao = ra + adph
            do = ra - adph
        ao = util.normalize(ao)
        do = util.normalize(do)
        poh = pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.POH]
        rao = math.radians(ao)
        rdo = math.radians(do)
        robl = math.radians(obl)
        rpoh = math.radians(poh)
        lon = pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.LON]
        okGa, okGd, lon = self.iterate(pl, rao, rdo, robl, rpoh, lon)
        if not okGa:
            rao1 = rao + math.radians(0.5)
            lon1 = self.iterate(pl, rao1, rdo, robl, rpoh, lon)
            rao2 = rao - math.radians(0.5)
            lon2 = self.iterate(pl, rao2, rdo, robl, rpoh, lon)
            lon = (lon1 + lon2) / 2
            okGa, okGd, lon = util.normalize(lon)
        elif not okGd:
            rdo1 = rdo + math.radians(0.5)
            lon1 = self.iterate(pl, rao, rdo1, robl, rpoh, lon)
            rdo2 = rdo - math.radians(0.5)
            lon2 = self.iterate(pl, rao, rdo2, robl, rpoh, lon)
            lon = (lon1 + lon2) / 2
            okGa, okGd, lon = util.normalize(lon)
        self.data = (lon, self.data[Planet.LAT], self.data[Planet.DIST], self.data[Planet.SPLON], self.data[Planet.SPLAT], self.data[Planet.SPDIST])
        self.dataEqu = (ra, self.dataEqu[Planet.DECLEQU], self.dataEqu[Planet.DISTEQU], self.dataEqu[Planet.SPRAEQU], self.dataEqu[Planet.SPDECLEQU], self.dataEqu[Planet.SPDISTEQU])
        spec = placspec.PlacidianSpeculum
        self.speculums[0].speculum = (self.data[spec.LON], self.data[spec.LAT], self.dataEqu[spec.RA], self.dataEqu[spec.DECL], pl.speculums[0].speculum[spec.ADLAT], pl.speculums[0].speculum[spec.SA], pl.speculums[0].speculum[spec.MD], pl.speculums[0].speculum[spec.HD], pl.speculums[0].speculum[spec.TH], pl.speculums[0].speculum[spec.HOD], pl.speculums[0].speculum[spec.PMP], pl.speculums[0].speculum[spec.ADPH], pl.speculums[0].speculum[spec.POH], pl.speculums[0].speculum[spec.AODO])
        spec = regiospec.RegiomontanianSpeculum
        self.speculums[1].speculum = (self.data[spec.LON], self.data[spec.LAT], self.dataEqu[spec.RA], self.dataEqu[spec.DECL], pl.speculums[1].speculum[spec.RMD], pl.speculums[1].speculum[spec.RHD], pl.speculums[1].speculum[spec.ZD], pl.speculums[1].speculum[spec.POLE], pl.speculums[1].speculum[spec.Q], pl.speculums[1].speculum[spec.W], pl.speculums[1].speculum[spec.CMP])

    def iterate(self, pl, rao, rdo, robl, rpoh, lon):
        spectype = Planet.PLACIDIAN
        spec = placspec.PlacidianSpeculum
        okGa = okGd = True
        if pl.speculums[spectype].speculum[spec.PMP] < 90.0 or pl.speculums[spectype].speculum[spec.PMP] >= 270.0 and pl.speculums[spectype].speculum[spec.PMP] < 360.0:
            Ga = math.degrees(math.cos(rao) * math.cos(robl) - math.sin(robl) * math.tan(rpoh))
            if Ga != 0.0:
                Fa = math.degrees(math.atan(math.sin(rao) / (math.cos(rao) * math.cos(robl) - math.sin(robl) * math.tan(rpoh))))
                if Fa >= 0.0 and Ga > 0.0:
                    lon = Fa
                elif Fa < 0.0 and Ga > 0.0:
                    lon = Fa + 360.0
                elif Ga < 0.0:
                    lon = Fa + 180.0
            else:
                okGa = False
        else:
            Gd = math.degrees(math.cos(rdo) * math.cos(robl) + math.sin(robl) * math.tan(rpoh))
            if Gd != 0.0:
                Fd = math.degrees(math.atan(math.sin(rdo) / (math.cos(rdo) * math.cos(robl) + math.sin(robl) * math.tan(rpoh))))
                if Fd >= 0.0 and Gd > 0.0:
                    lon = Fd
                elif Fd < 0.0 and Gd > 0.0:
                    lon = Fd + 360.0
                elif Gd < 0.0:
                    lon = Fd + 180.0
            else:
                okGd = False
        return (
         okGa, okGd, lon)

    def calcFullAstronomicalProc(self, da, oblN, raN, declN, placelat, ascmc2):
        ksi = raN + da
        ksi = util.normalize(ksi)
        roblN = math.radians(oblN)
        rksi = math.radians(ksi)
        rdeclN = math.radians(declN)
        longSZ = 0.0
        if ksi == 90.0:
            longSZ = 90.0
        elif ksi == 270.0:
            longSZ = 270.0
        else:
            Fd = 0.0
            if math.cos(rksi) != 0.0:
                Fd = math.degrees(math.atan((math.cos(roblN) * math.sin(rksi) + math.sin(roblN) * math.tan(rdeclN)) / math.cos(rksi)))
            if ksi >= 0.0 and ksi < 90.0:
                longSZ = Fd
            elif ksi > 90.0 and ksi < 270.0:
                longSZ = Fd + 180.0
            elif ksi > 270.0 and ksi < 360.0:
                longSZ = Fd + 360.0
            if longSZ <= 0.0:
                longSZ = Fd + 360.0
        longSZ = util.normalize(longSZ)
        roblN = math.radians(oblN)
        rksi = math.radians(ksi)
        rdeclN = math.radians(declN)
        latSZ = math.degrees(math.asin(math.sin(rdeclN) * math.cos(roblN) - math.cos(rdeclN) * math.sin(rksi) * math.sin(roblN)))
        raSZ, declSZ, distSZ = astrology.swe_cotrans(longSZ, latSZ, 1.0, -oblN)
        self.data = (
         longSZ, latSZ, self.data[Planet.DIST], self.data[Planet.SPLON], self.data[Planet.SPLAT], self.data[Planet.SPDIST])
        self.dataEqu = (raSZ, declSZ, self.dataEqu[Planet.DISTEQU], self.dataEqu[Planet.SPRAEQU], self.dataEqu[Planet.SPDECLEQU], self.dataEqu[Planet.SPDISTEQU])
        self.speculums = []
        self.speculums.append(placspec.PlacidianSpeculum(placelat, ascmc2, self.data[Planet.LON], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU]))
        self.speculums.append(regiospec.RegiomontanianSpeculum(placelat, ascmc2, self.data[Planet.LON], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU]))

    def calcRegioPDsInChartsPos(self, ascmc2, pl, placelat, obl):
        ramc = ascmc2[houses.Houses.MC][houses.Houses.RA]
        raic = ramc + 180.0
        if raic > 360.0:
            raic -= 360.0
        md = pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.MD]
        if md < 0.0:
            md *= -1
        ra = pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.RA]
        if pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] < 90.0:
            ra = raic - md
        elif pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] >= 90.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] < 180.0:
            ra = raic + md
        elif pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] >= 180.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] < 270.0:
            ra = ramc - md
        elif pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] >= 270.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.PMP] < 360.0:
            ra = ramc + md
        ra = util.normalize(ra)
        qreg = math.fabs(pl.speculums[Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.Q])
        wa = wd = 0.0
        if placelat == 0.0 or pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.DECL] == 0.0:
            wa = wd = ra
        if placelat > 0.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.DECL] > 0.0 or placelat < 0.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.DECL] < 0.0:
            wa = ra - qreg
            wd = ra + qreg
        if placelat > 0.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.DECL] < 0.0 or placelat < 0.0 and pl.speculums[Planet.PLACIDIAN].speculum[placspec.PlacidianSpeculum.DECL] > 0.0:
            wa = ra + qreg
            wd = ra - qreg
        wa = util.normalize(wa)
        wd = util.normalize(wd)
        poh = pl.speculums[Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.POLE]
        rwa = math.radians(wa)
        rwd = math.radians(wd)
        robl = math.radians(obl)
        rpoh = math.radians(poh)
        lon = pl.speculums[Planet.REGIOMONTANIAN].speculum[regiospec.RegiomontanianSpeculum.LON]
        okGa, okGd, lon = self.iterateRegio(pl, rwa, rwd, robl, rpoh, lon)
        if not okGa:
            rwa1 = rwa + math.radians(0.5)
            lon1 = self.iterateRegio(pl, rwa1, rwd, robl, rpoh, lon)
            rwa2 = rwa - math.radians(0.5)
            lon2 = self.iterateRegio(pl, rwa2, rwd, robl, rpoh, lon)
            lon = (lon1 + lon2) / 2
            lon = util.normalize(lon)
        elif not okGd:
            rwd1 = rwd + math.radians(0.5)
            lon1 = self.iterateRegio(pl, rwa, rwd1, robl, rpoh, lon)
            rwd2 = rwd - math.radians(0.5)
            lon2 = self.iterateRegio(pl, rwa, rwd2, robl, rpoh, lon)
            lon = (lon1 + lon2) / 2
            lon = util.normalize(lon)
        self.data = (lon, self.data[Planet.LAT], self.data[Planet.DIST], self.data[Planet.SPLON], self.data[Planet.SPLAT], self.data[Planet.SPDIST])
        self.dataEqu = (ra, self.dataEqu[Planet.DECLEQU], self.dataEqu[Planet.DISTEQU], self.dataEqu[Planet.SPRAEQU], self.dataEqu[Planet.SPDECLEQU], self.dataEqu[Planet.SPDISTEQU])
        spec = placspec.PlacidianSpeculum
        self.speculums[0].speculum = (self.data[spec.LON], self.data[spec.LAT], self.dataEqu[spec.RA], self.dataEqu[spec.DECL], pl.speculums[0].speculum[spec.ADLAT], pl.speculums[0].speculum[spec.SA], pl.speculums[0].speculum[spec.MD], pl.speculums[0].speculum[spec.HD], pl.speculums[0].speculum[spec.TH], pl.speculums[0].speculum[spec.HOD], pl.speculums[0].speculum[spec.PMP], pl.speculums[0].speculum[spec.ADPH], pl.speculums[0].speculum[spec.POH], pl.speculums[0].speculum[spec.AODO])
        spec = regiospec.RegiomontanianSpeculum
        self.speculums[1].speculum = (self.data[spec.LON], self.data[spec.LAT], self.dataEqu[spec.RA], self.dataEqu[spec.DECL], pl.speculums[1].speculum[spec.RMD], pl.speculums[1].speculum[spec.RHD], pl.speculums[1].speculum[spec.ZD], pl.speculums[1].speculum[spec.POLE], pl.speculums[1].speculum[spec.Q], pl.speculums[1].speculum[spec.W], pl.speculums[1].speculum[spec.CMP])

    def iterateRegio(self, pl, rwa, rwd, robl, rpoh, lon):
        spectype = Planet.PLACIDIAN
        spec = placspec.PlacidianSpeculum
        spectypeR = Planet.REGIOMONTANIAN
        specR = regiospec.RegiomontanianSpeculum
        okGa = okGd = True
        if pl.speculums[spectype].speculum[spec.PMP] < 90.0 or pl.speculums[spectype].speculum[spec.PMP] >= 270.0 and pl.speculums[spectype].speculum[spec.PMP] < 360.0:
            Ga = math.degrees(math.cos(rwa) * math.cos(robl) - math.sin(robl) * math.tan(rpoh))
            if Ga != 0.0:
                Fa = math.degrees(math.atan(math.sin(rwa) / (math.cos(rwa) * math.cos(robl) - math.sin(robl) * math.tan(rpoh))))
                if Fa >= 0.0 and Ga > 0.0:
                    lon = Fa
                elif Fa < 0.0 and Ga > 0.0:
                    lon = Fa + 360.0
                elif Ga < 0.0:
                    lon = Fa + 180.0
            else:
                okGa = False
        else:
            Gd = math.degrees(math.cos(rwd) * math.cos(robl) + math.sin(robl) * math.tan(rpoh))
            if Gd != 0.0:
                Fd = math.degrees(math.atan(math.sin(rwd) / (math.cos(rwd) * math.cos(robl) + math.sin(robl) * math.tan(rpoh))))
                if Fd >= 0.0 and Gd > 0.0:
                    lon = Fd
                elif Fd < 0.0 and Gd > 0.0:
                    lon = Fd + 360.0
                elif Gd < 0.0:
                    lon = Fd + 180.0
            else:
                okGd = False
        return (
         okGa, okGd, lon)


class Planets:
    """Calculates the positions of the planets"""
    SATURN, JUPITER, MARS, SUN, VENUS, MERCURY, MOON, ANODE, DNODE = range(0, 9)
    PLANETS_NUM = MOON + 1
    BODIES_NUM = DNODE + 1

    def __init__(self, tjd_ut, meannode, flag, placelat, ascmc2, nolat=False, obl=0.0):
        self.planets = []
        self.create(self.planets, tjd_ut, meannode, flag, placelat, ascmc2, nolat, obl)

    def create(self, pls, tjd_ut, meannode, flag, placelat, ascmc2, nolat, obl):
        node = astrology.SE_TRUE_NODE
        if meannode:
            node = astrology.SE_MEAN_NODE
        ids = [Planets.SATURN, Planets.JUPITER, Planets.MARS, Planets.SUN, Planets.VENUS, Planets.MERCURY, Planets.MOON, node]
        for i in ids:
            pls.append(Planet(tjd_ut, i, flag, placelat, ascmc2, None, None, nolat, obl))

        data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        data[Planet.LON] = util.normalize(pls[(-1)].data[Planet.LON] + 180.0)
        data[Planet.LAT] = pls[(-1)].data[Planet.LAT]
        data[Planet.DIST] = pls[(-1)].data[Planet.DIST]
        data[Planet.SPLON] = pls[(-1)].data[Planet.SPLON]
        data[Planet.SPLAT] = pls[(-1)].data[Planet.SPLAT]
        data[Planet.SPDIST] = pls[(-1)].data[Planet.SPDIST]
        dataEqu = [
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        dataEqu[Planet.RAEQU] = util.normalize(pls[(-1)].dataEqu[Planet.RAEQU] + 180.0)
        dataEqu[Planet.DECLEQU] = -1 * pls[(-1)].dataEqu[Planet.DECLEQU]
        dataEqu[Planet.DISTEQU] = pls[(-1)].dataEqu[Planet.DISTEQU]
        dataEqu[Planet.SPRAEQU] = pls[(-1)].dataEqu[Planet.SPRAEQU]
        dataEqu[Planet.SPDECLEQU] = pls[(-1)].dataEqu[Planet.SPDECLEQU]
        dataEqu[Planet.SPDISTEQU] = pls[(-1)].dataEqu[Planet.SPDISTEQU]
        pls.append(Planet(tjd_ut, node, flag, placelat, ascmc2, data, dataEqu, nolat, obl))
        return

    def calcProfPos(self, prof):
        for pl in range(Planets.BODIES_NUM):
            self.planets[pl].calcProfPos(prof)

    def calcMundaneProfPos(self, ascmc2, pls, placelat, obl):
        for pl in range(Planets.BODIES_NUM):
            self.planets[pl].calcMundaneProfPos(ascmc2, pls[pl], placelat, obl)

    def calcFullAstronomicalProc(self, da, oblN, pls, placelat, ascmc2):
        for pl in range(Planets.PLANETS_NUM):
            self.planets[pl].calcFullAstronomicalProc(da, oblN, pls[pl].dataEqu[Planet.RAEQU], pls[pl].dataEqu[Planet.DECLEQU], placelat, ascmc2)

    def calcRegioPDsInChartsPos(self, ascmc2, pls, placelat, obl):
        for pl in range(Planets.BODIES_NUM):
            self.planets[pl].calcRegioPDsInChartsPos(ascmc2, pls[pl], placelat, obl)

    def printPlanets(self):
        print ''
        print 'Planets:'
        for i in range(Planets.BODIES_NUM):
            print '%s: lon=%f lat=%f' % (self.planets[i].name, self.planets[i].data[Planet.LON], self.planets[i].data[Planet.LAT])