# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import planets, transits, mtexts, util

class Revolutions:
    SATURN = 0
    JUPITER = 1
    MARS = 2
    SUN = 3
    VENUS = 4
    MERCURY = 5
    MOON = 6

    def __init__(self):
        self.t = [
         0, 0, 0, 0, 0, 0]

    def compute(self, typ, by, bm, bd, chrt):
        if typ == Revolutions.SUN:
            year = by
            if bm > chrt.time.month or bm == chrt.time.month and bd > chrt.time.day:
                year += 1
            month = chrt.time.month
            day = chrt.time.day
            trans = transits.Transits()
            trans.month(year, month, chrt, planets.Planets.SUN)
            if len(trans.transits) == 0:
                if day < 4:
                    year, month = util.decrMonth(year, month)
                else:
                    year, month = util.incrMonth(year, month)
                trans = transits.Transits()
                trans.month(year, month, chrt, planets.Planets.SUN)
            if len(trans.transits) > 0:
                self.createRevolution(year, month, trans)
                return True
            return False
        if typ == Revolutions.MOON:
            trans = transits.Transits()
            trans.month(by, bm, chrt, planets.Planets.MOON)
            if len(trans.transits) > 0:
                second = False
                if bd > trans.transits[0].day:
                    if len(trans.transits) > 1:
                        if bd > trans.transits[1].day:
                            by, bm = util.incrMonth(by, bm)
                            trans = transits.Transits()
                            trans.month(by, bm, chrt, planets.Planets.MOON)
                        else:
                            second = True
                    else:
                        by, bm = util.incrMonth(by, bm)
                        trans = transits.Transits()
                        trans.month(by, bm, chrt, planets.Planets.MOON)
                if len(trans.transits) > 0:
                    if second:
                        self.createRevolution(by, bm, trans, 1)
                    else:
                        self.createRevolution(by, bm, trans)
                    return True
            return False
        if typ == Revolutions.MERCURY:
            for i in range(14):
                trans = transits.Transits()
                trans.month(by, bm, chrt, planets.Planets.MERCURY)
                if len(trans.transits) > 0:
                    if not (i == 0 and bd > trans.transits[0].day):
                        self.createRevolution(by, bm, trans)
                        return True
                by, bm = util.incrMonth(by, bm)

            return False
        if typ == Revolutions.VENUS:
            for i in range(16):
                trans = transits.Transits()
                trans.month(by, bm, chrt, planets.Planets.VENUS)
                if len(trans.transits) > 0:
                    if not (i == 0 and bd > trans.transits[0].day):
                        self.createRevolution(by, bm, trans)
                        return True
                by, bm = util.incrMonth(by, bm)

            return False
        if typ == Revolutions.MARS:
            for i in range(26):
                trans = transits.Transits()
                trans.month(by, bm, chrt, planets.Planets.MARS)
                if len(trans.transits) > 0:
                    if not (i == 0 and bd > trans.transits[0].day):
                        self.createRevolution(by, bm, trans)
                        return True
                by, bm = util.incrMonth(by, bm)

            return False
        if typ == Revolutions.JUPITER:
            for i in range(144):
                trans = transits.Transits()
                trans.month(by, bm, chrt, planets.Planets.JUPITER)
                if len(trans.transits) > 0:
                    if not (i == 0 and bd > trans.transits[0].day):
                        self.createRevolution(by, bm, trans)
                        return True
                by, bm = util.incrMonth(by, bm)

            return False
        if typ == Revolutions.SATURN:
            for i in range(360):
                trans = transits.Transits()
                trans.month(by, bm, chrt, planets.Planets.SATURN)
                if len(trans.transits) > 0:
                    if not (i == 0 and bd > trans.transits[0].day):
                        self.createRevolution(by, bm, trans)
                        return True
                by, bm = util.incrMonth(by, bm)

            return False
        return False

    def createRevolution(self, year, month, trans, num=0):
        self.t[0] = year
        self.t[1] = month
        self.t[2] = trans.transits[num].day
        h, m, s = util.decToDeg(trans.transits[num].time)
        self.t[3] = h
        self.t[4] = m
        self.t[5] = s