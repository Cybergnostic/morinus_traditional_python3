# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math, astrology, houses, planets, chart, mtexts, util

class Lots:
    """Computes lots"""
    NAME = 0
    FORMULA = 1
    REFORDEG = 2
    DIURNAL = 3
    LON = 4
    DEGWINNER = 5
    REFASC = 0
    REFHC2 = REFASC + 1
    REFHC3 = REFHC2 + 1
    REFIC = REFHC3 + 1
    REFHC5 = REFIC + 1
    REFHC6 = REFHC5 + 1
    REFDESC = REFHC6 + 1
    REFHC8 = REFDESC + 1
    REFHC9 = REFHC8 + 1
    REFMC = REFHC9 + 1
    REFHC11 = REFMC + 1
    REFHC12 = REFHC11 + 1
    ASC = 0
    HC2 = ASC + 1
    HC3 = HC2 + 1
    IC = HC3 + 1
    HC5 = IC + 1
    HC6 = HC5 + 1
    DESC = HC6 + 1
    HC8 = DESC + 1
    HC9 = HC8 + 1
    MC = HC9 + 1
    HC11 = MC + 1
    HC12 = HC11 + 1
    PLOFFS = HC12 + 1
    SATURN = PLOFFS
    JUPITER = SATURN + 1
    MARS = JUPITER + 1
    SUN = MARS + 1
    VENUS = SUN + 1
    MERCURY = VENUS + 1
    MOON = MERCURY + 1
    HCLORDOFFS = MOON + 1
    ASCLORD = HCLORDOFFS
    HC2LORD = ASCLORD + 1
    HC3LORD = HC2LORD + 1
    ICLORD = HC3LORD + 1
    HC5LORD = ICLORD + 1
    HC6LORD = HC5LORD + 1
    DESCLORD = HC6LORD + 1
    HC8LORD = DESCLORD + 1
    HC9LORD = HC8LORD + 1
    MCLORD = HC9LORD + 1
    HC11LORD = MCLORD + 1
    HC12LORD = HC11LORD + 1
    PLLORDOFFS = HC12LORD + 1
    SATURNLORD = PLLORDOFFS
    JUPITERLORD = SATURNLORD + 1
    MARSLORD = JUPITERLORD + 1
    SUNLORD = MARSLORD + 1
    VENUSLORD = SUNLORD + 1
    MERCURYLORD = VENUSLORD + 1
    MOONLORD = MERCURYLORD + 1
    SPECIAL = MOONLORD + 1
    SYZ = SPECIAL
    SYZLORD = SYZ + 1
    LTI = SYZLORD + 1
    LTILORD = LTI + 1
    LHO = LTILORD + 1
    LHOLORD = LHO + 1
    DEG = LHOLORD + 1
    DEGLORD = DEG + 1
    REF = DEGLORD + 1
    REFLORD = REF + 1

    def __init__(self, ar, ascmc, pls, hs, cusps, syz, plhour, opts, abovehorizon, ayan):
        if ar == None:
            self.lots = None
        else:
            self.doms = [
             2, 4, 5, 6, 3, 5, 4, 2, 1, 0, 0, 1]
            self.exals = [3, 6, -1, 1, -1, 5, 0, -1, -1, 2, -1, 4]
            self.tripls = [0, 3, 1, 2, 0, 3, 1, 2, 0, 3, 1, 2]
            asc = hs.ascmc[houses.Houses.ASC]
            desc = util.normalize(hs.ascmc[houses.Houses.ASC] + 180.0)
            mc = hs.ascmc[houses.Houses.MC]
            ic = util.normalize(hs.ascmc[houses.Houses.MC] + 180.0)
            cps = (
             asc, cusps[2], cusps[3], ic, cusps[5], cusps[6], desc, cusps[8], cusps[9], mc, cusps[11], cusps[12])
            if opts.lotsusehouses:
                signasc = int(asc / chart.Chart.SIGN_DEG) * chart.Chart.SIGN_DEG
                cps = (signasc, signasc + chart.Chart.SIGN_DEG, signasc + 2 * chart.Chart.SIGN_DEG, signasc + 3 * chart.Chart.SIGN_DEG, signasc + 4 * chart.Chart.SIGN_DEG, signasc + 5 * chart.Chart.SIGN_DEG, signasc + 6 * chart.Chart.SIGN_DEG, signasc + 7 * chart.Chart.SIGN_DEG, signasc + 8 * chart.Chart.SIGN_DEG, signasc + 9 * chart.Chart.SIGN_DEG, signasc + 10 * chart.Chart.SIGN_DEG, signasc + 11 * chart.Chart.SIGN_DEG)
                if opts.ayanamsha != 0:
                    cuspsayan = []
                    signasc = int(util.normalize(asc - ayan) / chart.Chart.SIGN_DEG) * chart.Chart.SIGN_DEG
                    cuspsayan.append(signasc)
                    for i in range(1, houses.Houses.HOUSE_NUM):
                        hc = util.normalize(cuspsayan[(i - 1)] + chart.Chart.SIGN_DEG)
                        cuspsayan.append(hc)

                    cps = tuple(cuspsayan)
            self.lots = []
            num = len(ar)
            if syz == None:
                num = 1
            for i in range(num):
                part = [
                 ar[i][Lots.NAME], (ar[i][Lots.FORMULA][0], ar[i][Lots.FORMULA][1], ar[i][Lots.FORMULA][2]), (ar[i][Lots.REFORDEG][0], ar[i][Lots.REFORDEG][1], ar[i][Lots.REFORDEG][2]), ar[i][Lots.DIURNAL], 0.0, [[-1, 0], [-1, 0], [-1, 0]]]
                lons = [
                 0.0, 0.0, 0.0]
                ok = True
                for l in range(3):
                    ID = part[Lots.FORMULA][l]
                    if ID < Lots.PLOFFS:
                        ID = self.adjustAscendant(ID, opts)
                        lons[l] = cps[ID]
                    elif ID < Lots.HCLORDOFFS:
                        lons[l] = pls.planets[(ID - Lots.PLOFFS)].data[planets.Planet.LON]
                        if opts.ayanamsha != 0:
                            lons[l] = util.normalize(lons[l] - ayan)
                    elif ID < Lots.PLLORDOFFS:
                        ID -= Lots.HCLORDOFFS
                        ID = self.adjustAscendant(ID, opts)
                        lonTmp = cps[ID]
                        lord = self.getLord(pls, opts, lonTmp)
                        if lord != -1:
                            lons[l] = pls.planets[lord].data[planets.Planet.LON]
                            if opts.ayanamsha != 0:
                                lons[l] = util.normalize(lons[l] - ayan)
                        else:
                            ok = False
                            continue
                    elif ID < Lots.SPECIAL:
                        lonTmp = pls.planets[(ID - Lots.PLLORDOFFS)].data[planets.Planet.LON]
                        if opts.ayanamsha != 0:
                            lonTmp = util.normalize(lonTmp - ayan)
                        lord = self.getLord(pls, opts, lonTmp)
                        if lord != -1:
                            lons[l] = pls.planets[lord].data[planets.Planet.LON]
                            if opts.ayanamsha != 0:
                                lons[l] = util.normalize(lons[l] - ayan)
                        else:
                            ok = False
                            continue
                    elif ID < Lots.LTI:
                        lons[l] = syz.lon
                        if ID == Lots.SYZLORD:
                            if opts.ayanamsha != 0:
                                lons[l] = util.normalize(syz.lon - ayan)
                            lord = self.getLord(pls, opts, lons[l])
                            if lord != -1:
                                lons[l] = pls.planets[lord].data[planets.Planet.LON]
                                if opts.ayanamsha != 0:
                                    lons[l] = util.normalize(lons[l] - ayan)
                            else:
                                ok = False
                                continue
                    elif ID < Lots.LHO:
                        lons[l] = pls.planets[planets.Planets.SUN].data[planets.Planet.LON]
                        if not abovehorizon:
                            lons[l] = pls.planets[planets.Planets.MOON].data[planets.Planet.LON]
                        if ID == Lots.LTILORD:
                            if opts.ayanamsha != 0:
                                lons[l] = util.normalize(lons[l] - ayan)
                            lord = self.getLord(pls, opts, lons[l])
                            if lord != -1:
                                lons[l] = pls.planets[lord].data[planets.Planet.LON]
                                if opts.ayanamsha != 0:
                                    lons[l] = util.normalize(lons[l] - ayan)
                            else:
                                ok = False
                                continue
                    elif ID < Lots.DEG:
                        lons[l] = pls.planets[plhour].data[planets.Planet.LON]
                        if ID == Lots.LHOLORD:
                            if opts.ayanamsha != 0:
                                lons[l] = util.normalize(lons[l] - ayan)
                            lord = self.getLord(pls, opts, lons[l])
                            if lord != -1:
                                lons[l] = pls.planets[lord].data[planets.Planet.LON]
                                if opts.ayanamsha != 0:
                                    lons[l] = util.normalize(lons[l] - ayan)
                            else:
                                ok = False
                                continue
                    elif ID < Lots.REF:
                        lons[l] = part[Lots.REFORDEG][l]
                        if ID == Lots.DEGLORD:
                            if opts.ayanamsha != 0:
                                lons[l] = util.normalize(lons[l] - ayan)
                            lord = self.getLord(pls, opts, lons[l])
                            if lord != -1:
                                lons[l] = pls.planets[lord].data[planets.Planet.LON]
                                if opts.ayanamsha != 0:
                                    lons[l] = util.normalize(lons[l] - ayan)
                            else:
                                ok = False
                                continue
                    elif ID >= Lots.REF:
                        rpart = self.lots[(part[Lots.REFORDEG][l] - 1)]
                        lons[l] = rpart[Lots.LON]
                        if ID == Lots.REFLORD:
                            if opts.ayanamsha != 0:
                                lons[l] = util.normalize(lons[l] - ayan)
                            lord = self.getLord(pls, opts, lons[l])
                            if lord != -1:
                                lons[l] = pls.planets[lord].data[planets.Planet.LON]
                                if opts.ayanamsha != 0:
                                    lons[l] = util.normalize(lons[l] - ayan)
                            else:
                                ok = False
                                continue

                if not ok:
                    continue
                if part[Lots.DIURNAL] and not abovehorizon:
                    tmp = lons[1]
                    lons[1] = lons[2]
                    lons[2] = tmp
                if opts.lotsusehouses:
                    lons[0] = float(int(lons[0] / chart.Chart.SIGN_DEG) * chart.Chart.SIGN_DEG)
                    lons[1] = float(int(lons[1] / chart.Chart.SIGN_DEG) * chart.Chart.SIGN_DEG)
                    lons[2] = float(int(lons[2] / chart.Chart.SIGN_DEG) * chart.Chart.SIGN_DEG)
                diff = lons[1] - lons[2]
                if diff < 0.0:
                    diff += 360.0
                lon = lons[0] + diff
                if lon >= 360.0:
                    lon -= 360.0
                if opts.ayanamsha != 0 and not opts.lotsusehouses:
                    lon = util.normalize(lon - ayan)
                part[Lots.LON] = lon
                degwinner = [
                 [
                  -1, 0], [-1, 0], [-1, 0]]
                for p in range(planets.Planets.PLANETS_NUM):
                    score = 0
                    scoretxt = ''
                    s, st, sh = self.getData(opts, p, lon, abovehorizon)
                    score += s
                    scoretxt += st
                    if score > degwinner[0][1]:
                        degwinner[0][0] = p
                        degwinner[0][1] = score
                        degwinner[1][0] = -1
                        degwinner[2][0] = -1
                    elif score == degwinner[0][1]:
                        if degwinner[1][0] == -1:
                            degwinner[1][0] = p
                        else:
                            degwinner[2][0] = p

                part[Lots.DEGWINNER] = degwinner
                self.lots.append(part)

        return

    def adjustAscendant(self, Id, opts):
        if opts.lotsref != 0:
            Id += opts.lotsref
            if Id > houses.Houses.HOUSE_NUM - 1:
                Id -= houses.Houses.HOUSE_NUM - 1
        return Id

    def getLord(self, pls, opts, lon):
        sign = int(lon / chart.Chart.SIGN_DEG)
        lord = -1
        for pid in range(planets.Planets.PLANETS_NUM):
            if opts.dignities[pid][0][sign]:
                lord = pid

        return lord

    def getData(self, opts, i, lon, daytime):
        """i is the index of the planet, and lon is the longitude to check"""
        score = 0
        scoretxt = ''
        share = 0
        sign = int(lon / chart.Chart.SIGN_DEG)
        if i == self.doms[sign]:
            sc = opts.dignityscores[0]
            score += sc
            add = '+'
            if scoretxt == '':
                add = ''
            scoretxt += add + str(sc)
            share += 1
        if self.exals[sign] != -1 and i == self.exals[sign]:
            sc = opts.dignityscores[1]
            score += sc
            add = '+'
            if scoretxt == '':
                add = ''
            scoretxt += add + str(sc)
            share += 1
        if opts.oneruler:
            tr = self.tripls[sign]
            tripl = 0
            if daytime:
                tripl = opts.trips[opts.seltrip][tr][0]
            else:
                tripl = opts.trips[opts.seltrip][tr][1]
            if tripl == i:
                sc = opts.dignityscores[2]
                score += sc
                add = '+'
                if scoretxt == '':
                    add = ''
                scoretxt += add + str(sc)
                share += 1
        else:
            tr = self.tripls[sign]
            for k in range(3):
                tripl = opts.trips[opts.seltrip][tr][k]
                if tripl != -1 and tripl == i:
                    sc = opts.dignityscores[2]
                    score += sc
                    add = '+'
                    if scoretxt == '':
                        add = ''
                    scoretxt += add + str(sc)
                    share += 1
                    break

        pos = lon % chart.Chart.SIGN_DEG
        subnum = len(opts.terms[0][0])
        summa = 0.0
        for t in range(subnum):
            summa += opts.terms[opts.selterm][sign][t][1]
            if summa > pos:
                break

        term = opts.terms[opts.selterm][sign][t][0]
        if term == i:
            sc = opts.dignityscores[3]
            score += sc
            add = '+'
            if scoretxt == '':
                add = ''
            scoretxt += add + str(sc)
            share += 1
        dec = int(pos / 10)
        decan = opts.decans[opts.seldecan][sign][dec]
        if decan == i:
            sc = opts.dignityscores[4]
            score += sc
            add = '+'
            if scoretxt == '':
                add = ''
            scoretxt += add + str(sc)
            share += 1
        return (score, scoretxt, share)