# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import astrology, planets, fortune, houses, util

class Antiscion:
    """Antiscion of a planet, LoF or AscMC"""
    ANTISCION = 0
    CONTRAANT = 1
    LOF = planets.Planets.BODIES_NUM
    ASC = LOF + 1
    MC = ASC + 1

    def __init__(self, typ, Id, lon, lat, ra, decl):
        self.typ = typ
        self.Id = Id
        self.lon = lon
        self.lat = lat
        self.ra = ra
        self.decl = decl


class Antiscia:
    """Computes antiscia of the bodies(planets, LoF, Asc and MC)"""
    CANCER0 = 90.0
    CAPRICORN0 = 270.0

    def __init__(self, pls, ascmc, lof, obl):
        self.obl = obl
        self.plantiscia = []
        self.plcontraant = []
        self.lofant = None
        self.lofcontraant = None
        self.ascmcant = []
        self.ascmccontraant = []
        plcants = []
        for i in range(planets.Planets.BODIES_NUM):
            ant, cant = self.calc(pls.planets[i].data[planets.Planet.LON])
            lat = pls.planets[i].data[planets.Planet.LAT]
            plcants.append((cant, lat))
            raant, declant, dist = astrology.swe_cotrans(ant, lat, 1.0, -obl)
            self.plantiscia.append(Antiscion(Antiscion.ANTISCION, i, ant, lat, raant, declant))

        for i in range(planets.Planets.BODIES_NUM):
            raant, declant, dist = astrology.swe_cotrans(plcants[i][0], plcants[i][1], 1.0, -obl)
            self.plcontraant.append(Antiscion(Antiscion.CONTRAANT, i, plcants[i][0], plcants[i][1], raant, declant))

        ant, cant = self.calc(lof[fortune.Fortune.LON])
        raant, declant, dist = astrology.swe_cotrans(ant, 0.0, 1.0, -self.obl)
        self.lofant = Antiscion(Antiscion.ANTISCION, Antiscion.LOF, ant, 0.0, raant, declant)
        raant, declant, dist = astrology.swe_cotrans(cant, 0.0, 1.0, -self.obl)
        self.lofcontraant = Antiscion(Antiscion.CONTRAANT, Antiscion.LOF, cant, 0.0, raant, declant)
        antasc, cantasc = self.calc(ascmc[houses.Houses.ASC])
        raantasc, declantasc, dist = astrology.swe_cotrans(antasc, 0.0, 1.0, -self.obl)
        self.ascmcant.append(Antiscion(Antiscion.ANTISCION, Antiscion.ASC, antasc, 0.0, raantasc, declantasc))
        antmc, cantmc = self.calc(ascmc[houses.Houses.MC])
        raantmc, declantmc, dist = astrology.swe_cotrans(antmc, 0.0, 1.0, -self.obl)
        self.ascmcant.append(Antiscion(Antiscion.ANTISCION, Antiscion.MC, antmc, 0.0, raantmc, declantmc))
        raantasc, declantasc, dist = astrology.swe_cotrans(cantasc, 0.0, 1.0, -self.obl)
        self.ascmccontraant.append(Antiscion(Antiscion.CONTRAANT, Antiscion.ASC, cantasc, 0.0, raantasc, declantasc))
        raantmc, declantmc, dist = astrology.swe_cotrans(cantmc, 0.0, 1.0, -self.obl)
        self.ascmccontraant.append(Antiscion(Antiscion.CONTRAANT, Antiscion.MC, cantmc, 0.0, raantmc, declantmc))
        return

    def calc(self, lon):
        ant = 0.0
        if lon == Antiscia.CANCER0 or lon == Antiscia.CAPRICORN0:
            ant = lon
        elif lon > Antiscia.CANCER0 and lon < Antiscia.CAPRICORN0:
            ant = util.normalize(Antiscia.CAPRICORN0 + (Antiscia.CAPRICORN0 - lon))
        elif lon < Antiscia.CANCER0:
            ant = util.normalize(Antiscia.CANCER0 + (Antiscia.CANCER0 - lon))
        elif lon > Antiscia.CAPRICORN0:
            ant = util.normalize(Antiscia.CAPRICORN0 - (lon - Antiscia.CAPRICORN0))
        cant = util.normalize(ant + 180.0)
        return (
         ant, cant)

    def printants(self, pls):
        anttxt = ('Antiscia', 'Contraantiscia')
        print ''
        print 'Antiscia:'
        for i in range(planets.Planets.BODIES_NUM):
            print '%s %s %f %f %f %f' % (anttxt[self.plantiscia[i].typ], pls.planets[self.plantiscia[i].Id].name, self.plantiscia[i].lon, self.plantiscia[i].lat, self.plantiscia[i].ra, self.plantiscia[i].decl)
            print '%s %s %f %f %f %f' % (anttxt[self.plcontraant[i].typ], pls.planets[self.plcontraant[i].Id].name, self.plcontraant[i].lon, self.plcontraant[i].lat, self.plcontraant[i].ra, self.plcontraant[i].decl)

        print '%s %s %f %f %f %f' % (anttxt[self.lofant.typ], 'LoF', self.lofant.lon, self.lofant.lat, self.lofant.ra, self.lofant.decl)
        print '%s %s %f %f %f %f' % (anttxt[self.lofcontraant.typ], 'LoF', self.lofcontraant.lon, self.lofcontraant.lat, self.lofcontraant.ra, self.lofcontraant.decl)
        print '%s %s %f %f %f %f' % (anttxt[self.ascmcant[0].typ], 'Asc', self.ascmcant[0].lon, self.ascmcant[0].lat, self.ascmcant[0].ra, self.ascmcant[0].decl)
        print '%s %s %f %f %f %f' % (anttxt[self.ascmcant[1].typ], 'MC', self.ascmcant[1].lon, self.ascmcant[1].lat, self.ascmcant[1].ra, self.ascmcant[1].decl)
        print '%s %s %f %f %f %f' % (anttxt[self.ascmccontraant[0].typ], 'Asc', self.ascmccontraant[0].lon, self.ascmccontraant[0].lat, self.ascmccontraant[0].ra, self.ascmccontraant[0].decl)
        print '%s %s %f %f %f %f' % (anttxt[self.ascmccontraant[1].typ], 'MC', self.ascmccontraant[1].lon, self.ascmccontraant[1].lat, self.ascmccontraant[1].ra, self.ascmccontraant[1].decl)