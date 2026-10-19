# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import astrology
import planets
import util

class PlanetsHelio:
    """Data of a Planet"""
    LON, LAT, DIST, SPLON, SPLAT, SPDIST = list(range(0, 6))

    def __init__(self, tjd_ut, flag):
        self.lons = []
        self.names = []
        flag |= astrology.SEFLG_HELCTR
        for i in range(planets.Planets.MOON):
            pId = util.mapChaldeanToModern(i)
            if i == planets.Planets.SUN:
                pId = astrology.SE_EARTH
            rflag, self.data, serr = astrology.swe_calc_ut(tjd_ut, pId, flag)
            self.lons.append(self.data[PlanetsHelio.LON])
            self.names.append(astrology.swe_get_planet_name(pId))