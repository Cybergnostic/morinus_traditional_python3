# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math, houses, util

class RegiomontanianSpeculum:
    """Calculates Regiomontanian Speculum for an object"""
    LON, LAT, RA, DECL, RMD, RHD, ZD, POLE, Q, W, CMP = range(11)

    def __init__(self, placelat, ascmc2, lon, lat, ra, decl):
        ramc = ascmc2[houses.Houses.MC][houses.Houses.RA]
        raic = ramc + 180.0
        if raic > 360.0:
            raic -= 360.0
        self.eastern = True
        if ramc > raic:
            if ra > raic and ra < ramc:
                self.eastern = False
        elif ra > raic and ra < 360.0 or ra < ramc and ra > 0.0:
            self.eastern = False
        med = math.fabs(ramc - ra)
        if med > 180.0:
            med = 360.0 - med
        icd = math.fabs(raic - ra)
        if icd > 180.0:
            icd = 360.0 - icd
        md = med
        tablemd = med
        umd = True
        if icd < med:
            md = icd
            tablemd = icd
            tablemd *= -1
            umd = False
        adlat = 0.0
        val = math.tan(math.radians(placelat)) * math.tan(math.radians(decl))
        if math.fabs(val) <= 1.0:
            adlat = math.degrees(math.asin(val))
        aoasc = ramc + 90.0
        if aoasc >= 360.0:
            aoasc -= 360.0
        dodesc = raic + 90.0
        if dodesc >= 360.0:
            dodesc -= 360.0
        aohd = ra - adlat
        hdasc = aohd - aoasc
        if hdasc < 0.0:
            hdasc *= -1
        if hdasc > 180.0:
            hdasc = 360.0 - hdasc
        dohd = ra + adlat
        hddesc = dohd - dodesc
        if hddesc < 0.0:
            hddesc *= -1
        if hddesc > 180.0:
            hddesc = 360.0 - hddesc
        hd = hdasc
        if hddesc < hdasc:
            hd = hddesc
            hd *= -1
        dsa = 90.0 + adlat
        nsa = 90.0 - adlat
        self.abovehorizon = True
        if med > dsa:
            self.abovehorizon = False
        zd = self.getZD(md, placelat, decl, umd)
        if zd > 90.0:
            zd = 180.0 - zd
        tmpzd = zd
        if not umd:
            zd *= -1
        pole = 0.0
        val = math.sin(math.radians(placelat)) * math.sin(math.radians(tmpzd))
        if math.fabs(val) <= 1.0:
            pole = math.degrees(math.asin(val))
        Q = 0.0
        val = math.tan(math.radians(decl)) * math.tan(math.radians(pole))
        if math.fabs(val) <= 1.0:
            Q = math.degrees(math.asin(val))
        W = 0.0
        if self.eastern:
            W = ra - Q
        else:
            W = ra + Q
        W = util.normalize(W)
        Cmp = 0.0
        if self.eastern:
            if umd:
                Cmp = 270.0 + tmpzd
            else:
                Cmp = 90.0 - tmpzd
        elif umd:
            Cmp = 270.0 - tmpzd
        else:
            Cmp = 90.0 + tmpzd
        self.speculum = (
         lon, lat, ra, decl, tablemd, hd, zd, pole, Q, W, Cmp)

    def getZD(self, md, placelat, decl, umd):
        """Calculates Regiomontan zenith distance """
        zd = 0.0
        if md == 90.0:
            zd = 90.0 - math.degrees(math.atan(math.sin(math.fabs(math.radians(placelat)))) * math.tan(math.radians(decl)))
        elif md < 90.0:
            A = math.degrees(math.atan(math.cos(math.radians(placelat)) * math.tan(math.radians(md))))
            B = math.degrees(math.atan(math.tan(math.fabs(math.radians(placelat))) * math.cos(math.radians(md))))
            C = 0.0
            if decl < 0 and placelat < 0 or decl >= 0 and placelat >= 0:
                if umd:
                    C = B - math.fabs(decl)
                else:
                    C = B + math.fabs(decl)
            elif decl < 0 and placelat > 0 or decl > 0 and placelat < 0:
                if umd:
                    C = B + math.fabs(decl)
                else:
                    C = B - math.fabs(decl)
            F = math.degrees(math.atan(math.sin(math.fabs(math.radians(placelat))) * math.sin(math.radians(md)) * math.tan(math.radians(C))))
            zd = A + F
        return zd