# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import planets, fortune, houses, util, math

class Dodecatemoria:
    """Computes dodecatemoria (twelfth parts) of the bodies(planets, LoF, Asc and MC)"""

    def __init__(self, pls, ascmc, lof, ayanopt, ayan):
        self.lons = []
        self.ayanopt = ayanopt
        self.ayan = ayan
        for i in range(planets.Planets.BODIES_NUM):
            lon = pls.planets[i].data[planets.Planet.LON]
            self.lons.append(self.calc(lon))

        lon = ascmc[houses.Houses.ASC]
        self.lons.append(self.calc(lon))
        lon = ascmc[houses.Houses.MC]
        self.lons.append(self.calc(lon))
        lon = lof[fortune.Fortune.LON]
        self.lons.append(self.calc(lon))

    def calc(self, lon):
        if self.ayanopt != 0:
            lon -= self.ayan
            lon = util.normalize(lon)
        return self.KeepInZodiac(30 * self.getSign(lon) + 12 * self.getRelativeLon(lon))

    def KeepBetweenLimit(self, lon, lim):
        """ Keep the longitude between 0..lim """
        return lon - math.floor(lon / lim) * lim

    def KeepInZodiac(self, lon):
        """ Keep the longitude between 0..360 """
        return self.KeepBetweenLimit(lon, 360)

    def getRelativeLon(self, lon):
        """ Returns the longitude relative to the zodiac """
        return self.KeepBetweenLimit(lon, 30)

    def getSign(self, lon):
        """ Returns the sign: 0 - Aries, 1 - Taurus, 2 - Gemini..."""
        return lon // 30