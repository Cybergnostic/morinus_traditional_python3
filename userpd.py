# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import astrology, placspec, regiospec

class UserPD:
    """Data of User-PrimDir"""
    PLACIDIAN = 0
    REGIOMONTANIAN = 1

    def __init__(self, londeg, lonmin, lonsec, latdeg, latmin, latsec, southern, placelat, ascmc2, obl):
        self.londeg = londeg
        self.lonmin = lonmin
        self.lonsec = lonsec
        self.latdeg = latdeg
        self.latmin = latmin
        self.latsec = latsec
        self.southern = southern
        self.lon = londeg + lonmin / 60.0 + lonsec / 3600.0
        self.lat = latdeg + latmin / 60.0 + latsec / 3600.0
        if self.southern:
            self.lat *= -1
        self.ra, self.decl, dist = astrology.swe_cotrans(self.lon, self.lat, 1.0, -obl)
        self.speculums = []
        self.speculums.append(placspec.PlacidianSpeculum(placelat, ascmc2, self.lon, self.lat, self.ra, self.decl))
        self.speculums.append(regiospec.RegiomontanianSpeculum(placelat, ascmc2, self.lon, self.lat, self.ra, self.decl))