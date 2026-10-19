# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math, chart, planets, util

class Points:

    def __init__(self, valid, points):
        self.valid = valid
        self.pts = points


class ZodPars:
    """Computes zodiacal parallels"""

    def __init__(self, pls, obl):
        self.obl = obl
        self.pars = []
        self.calc(pls)

    def calc(self, pls):
        NODES = 2
        for p in range(planets.Planets.PLANETS_NUM):
            pl = pls.planets[p]
            lon = pl.data[planets.Planet.LON]
            lat = pl.data[planets.Planet.LAT]
            decl = pl.dataEqu[planets.Planet.DECLEQU]
            onEcl = False
            if p == planets.Planets.SUN or lat == 0.0:
                onEcl = True
            self.pars.append(self.getEclPoints(lon, decl, onEcl))

    def getEclPoints(self, lon, decl, onEcl):
        """Calculates points of the Ecliptic from declination"""
        PARALLEL = chart.Chart.PARALLEL
        CONTRAPARALLEL = chart.Chart.CONTRAPARALLEL
        origdecl = decl
        if decl < 0.0:
            decl *= -1
        if decl > self.obl:
            return Points(False, ((-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL)))
        if onEcl:
            if decl == self.obl:
                lon += 180.0
                lon = util.normalize(lon)
                return Points(True, ((lon, CONTRAPARALLEL), (-1.0, PARALLEL)))
            else:
                lon1 = lon + 180.0
                lon1 = util.normalize(lon1)
                lon2 = 360.0 - lon1
                lon3 = util.normalize(lon2 + 180.0)
                return Points(True, ((lon1, CONTRAPARALLEL), (lon2, PARALLEL), (lon3, CONTRAPARALLEL)))

        else:
            if decl == self.obl:
                lon1 = math.degrees(math.asin(math.sin(math.radians(origdecl)) / math.sin(math.radians(self.obl))))
                lon1 = util.normalize(lon1)
                lon2 = util.normalize(lon1 + 180.0)
                return Points(True, ((lon1, PARALLEL), (lon2, CONTRAPARALLEL)))
            else:
                lon1 = math.degrees(math.asin(math.sin(math.radians(origdecl)) / math.sin(math.radians(self.obl))))
                lon1 = util.normalize(lon1)
                lon2 = util.normalize(lon1 + 180.0)
                lon3 = 360.0 - lon2
                lon4 = util.normalize(lon3 + 180.0)
                return Points(True, ((lon1, PARALLEL), (lon2, CONTRAPARALLEL), (lon3, PARALLEL), (lon4, CONTRAPARALLEL)))

        return Points(False, ((-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL)))

    def printZodPars(self, pls):
        print('')
        print('Zodiacal Parallels/ContraParallels:')
        for i in range(planets.Planets.PLANETS_NUM):
            if self.pars[i].valid:
                leng = len(self.pars[i].pts)
                for j in range(leng):
                    if self.pars[i].pts[j][0] == -1.0:
                        break
                    txt = 'Parallel'
                    if self.pars[i].pts[j][1] == chart.Chart.CONTRAPARALLEL:
                        txt = 'Contraparallel'
                    print('%s: lon=%f %s' % (pls.planets[i].name, self.pars[i].pts[j][0], txt))