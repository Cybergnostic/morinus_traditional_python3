# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math
import util

class RiseTimeOfSigns:
    """Calculates rising times of signs"""

    def __init__(self, placelat, obl):
        aos = []
        self.riseofsigns = []
        lon = 0.0
        for i in range(7):
            ra, decl = util.transform(lon, 0.0, obl)
            adlat = 0.0
            val = math.tan(math.radians(placelat)) * math.tan(math.radians(decl))
            if math.fabs(val) <= 1.0:
                adlat = math.degrees(math.asin(val))
            aos.append(ra - adlat)
            lon += 30.0

        for i in range(6):
            self.riseofsigns.append(aos[(i + 1)] - aos[i])

    def printrts(self):
        for i in range(6):
            print(self.riseofsigns[i])