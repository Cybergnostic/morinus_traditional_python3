# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import astrology, chart, util

class Houses:
    """Calculates the cusps of the Houses"""
    HOUSE_NUM = 12
    hsystems = ('P', 'K', 'R', 'C', 'E', 'W', 'X', 'M', 'H', 'T', 'B', 'O')
    ASC, MC, ARMC, VERTEX, EQUASC, COASC, COASC2, POLARASC = list(range(0, 8))
    LON, LAT, RA, DECL = list(range(0, 4))

    def __init__(self, tjd_ut, flag, placelat, placelon, hsys, obl, ayanopt, ayan):
        if hsys >= 0 and hsys < len(Houses.hsystems):
            self.hsys = hsys
        else:
            self.hsys = 0
        self.obl = obl
        res, self.cusps, self.ascmc = astrology.swe_houses_ex(tjd_ut, flag, placelat, placelon, ord(Houses.hsystems[self.hsys]))
        if ayanopt != 0 and self.hsys == 5:
            del self.cusps
            cusps = [0.0]
            sign = int(util.normalize(self.ascmc[Houses.ASC] - ayan)) // 30
            cusps.append(sign * 30.0)
            for i in range(2, Houses.HOUSE_NUM + 1):
                hc = util.normalize(cusps[(i - 1)] + 30.0)
                cusps.append(hc)

            self.cusps = tuple(cusps)
        ascra, ascdecl, dist = astrology.swe_cotrans(self.ascmc[Houses.ASC], 0.0, 1.0, -obl)
        mcra, mcdecl, dist = astrology.swe_cotrans(self.ascmc[Houses.MC], 0.0, 1.0, -obl)
        self.ascmc2 = ((self.ascmc[Houses.ASC], 0.0, ascra, ascdecl), (self.ascmc[Houses.MC], 0.0, mcra, mcdecl))
        self.cuspstmp = [
         [
          0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
        for i in range(Houses.HOUSE_NUM):
            self.cuspstmp[i][0], self.cuspstmp[i][1], dist = astrology.swe_cotrans(self.cusps[(i + 1)], 0.0, dist, -obl)

        self.cusps2 = ((self.cuspstmp[0][0], self.cuspstmp[0][1]), (self.cuspstmp[1][0], self.cuspstmp[1][1]), (self.cuspstmp[2][0], self.cuspstmp[2][1]), (self.cuspstmp[3][0], self.cuspstmp[3][1]), (self.cuspstmp[4][0], self.cuspstmp[4][1]), (self.cuspstmp[5][0], self.cuspstmp[5][1]), (self.cuspstmp[6][0], self.cuspstmp[6][1]), (self.cuspstmp[7][0], self.cuspstmp[7][1]), (self.cuspstmp[8][0], self.cuspstmp[8][1]), (self.cuspstmp[9][0], self.cuspstmp[9][1]), (self.cuspstmp[10][0], self.cuspstmp[10][1]), (self.cuspstmp[11][0], self.cuspstmp[11][1]))

    def getHousePos(self, lon, opts, useorbs=False):
        for i in range(1, Houses.HOUSE_NUM):
            orb1 = 0.0
            orb2 = 0.0
            if useorbs:
                orb1 = opts.orbscuspH
                orb2 = opts.orbscuspH
                if i == 1 or i == 4 or i == 7 or i == 10:
                    orb1 = opts.orbscuspAscMC
                if i + 1 == 4 or i + 1 == 7 or i + 1 == 10:
                    orb2 = opts.orbscuspAscMC
            cusp1 = util.normalize(self.cusps[i] - orb1)
            cusp2 = util.normalize(self.cusps[(i + 1)] - orb2)
            pos = lon
            if cusp1 > 240.0 and cusp2 < 120.0:
                if pos > 240.0:
                    cusp2 += 360.0
                else:
                    cusp2 += 360.0
                    pos += 360.0
            if cusp1 <= pos and cusp2 > pos:
                return i - 1

        orb1 = 0.0
        orb2 = 0.0
        if useorbs:
            orb1 = opts.orbscuspH
            orb2 = opts.orbscuspAscMC
        cusp1 = util.normalize(self.cusps[12] - orb1)
        cusp2 = util.normalize(self.cusps[1] - orb2)
        pos = lon
        if cusp1 > 240.0 and cusp2 < 120.0:
            if pos > 240.0:
                cusp2 += 360.0
            else:
                cusp2 += 360.0
                pos += 360.0
        if cusp1 <= pos and cusp2 > pos:
            return 11
        return 0

    def calcProfPos(self, prof):
        hcs = [
         self.cusps[0]]
        for i in range(1, Houses.HOUSE_NUM + 1):
            hcs.append(util.normalize(self.cusps[i] + prof.offs))

        self.cusps = tuple(hcs)
        self.ascmc = (
         util.normalize(self.ascmc[Houses.ASC] + prof.offs), util.normalize(self.ascmc[Houses.MC] + prof.offs), self.ascmc[Houses.ARMC], self.ascmc[Houses.VERTEX], self.ascmc[Houses.EQUASC], self.ascmc[Houses.COASC], self.ascmc[Houses.COASC2], self.ascmc[Houses.POLARASC])
        ascra, ascdecl, dist = astrology.swe_cotrans(self.ascmc[Houses.ASC], 0.0, 1.0, -self.obl)
        mcra, mcdecl, dist = astrology.swe_cotrans(self.ascmc[Houses.MC], 0.0, 1.0, -self.obl)
        self.ascmc2 = (
         (
          self.ascmc[Houses.ASC], 0.0, ascra, ascdecl), (self.ascmc[Houses.MC], 0.0, mcra, mcdecl))

    def printAscMC(self):
        print('')
        print('Asc: lon=%f' % self.ascmc[Houses.ASC])
        print('MC: lon=%f' % self.ascmc[Houses.MC])

    def printHouses(self):
        housesystems = ('Placidus', 'Koch', 'Regiomontanus', 'Campanus', 'Equal', 'Whole Sign',
                        'Axial', 'Morinus', 'Horizontal', 'Page-Polich', 'Alcabitus',
                        'Porphyrius')
        print('')
        print('Selected housesystem: %s' % housesystems[self.hsys])
        for i in range(1, Houses.HOUSE_NUM + 1):
            print('%d. %f' % (i, self.cusps[i]))