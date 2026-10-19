# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
from datetime import datetime, timedelta
import mtexts

class Firdaria:
    """Firdaria (3 types): 1.Diurnal chart, 2.Nocturnal(Al Biruni) 3.Nocturnal(Bonatti)"""
    TIME_FORMAT = '%Y.%m.%d'

    def __init__(self, by, bm, bd, opts, isdaily):
        self.by = by
        self.bm = bm
        self.bd = bd
        self.startdate = datetime(self.by, self.bm, self.bd)
        self.isdaily = isdaily
        self.options = opts
        self.dailyplanetaryyears = [
         (3, 10), (4, 8), (5, 13), (6, 9), (0, 11), (1, 12), (2, 7), (7, 3), (8, 2)]
        self.nightlyplanetaryyearsalbiruni = [(6, 9), (0, 11), (1, 12), (2, 7), (3, 10), (4, 8), (5, 13), (7, 3), (8, 2)]
        self.nightlyplanetaryyearsbonatti = [(6, 9), (0, 11), (1, 12), (2, 7), (7, 3), (8, 2), (3, 10), (4, 8), (5, 13)]

    def isNode(self, index):
        if self.isdaily:
            return index == 7 or index == 8
        else:
            if self.options.isfirbonatti:
                return index == 4 or index == 5
            return index == 7 or index == 8

    def nextIndex(self, index):
        index = index + 1
        if self.isdaily:
            if self.isNode(index) or index > 8:
                return 0
        elif self.options.isfirbonatti:
            if self.isNode(index):
                return 6
            if index > 8:
                return 0
        elif self.isNode(index) or index > 8:
            return 0
        return index

    def displaySubPeriods(self, planetaryyears, index, starting, ending, pltxts):
        if self.isNode(index):
            return
        subperiodstart = starting
        secs = (ending - starting).total_seconds()
        for i in range(7):
            planet, years = planetaryyears[index]
            subperiodends = subperiodstart + timedelta(seconds=secs / 7)
            print(('       {0:7}: {1}').format(pltxts[planet], subperiodstart.strftime(Firdaria.TIME_FORMAT)))
            subperiodstart = subperiodends
            index = self.nextIndex(index)

    def printFirdaria(self):
        pltxts = (
         mtexts.txtscommon['Saturn'], mtexts.txtscommon['Jupiter'], mtexts.txtscommon['Mars'], mtexts.txtscommon['Sun'], mtexts.txtscommon['Venus'], mtexts.txtscommon['Mercury'], mtexts.txtscommon['Moon'], mtexts.txtscommon['ANode'], mtexts.txtscommon['DNode'])
        if self.isdaily:
            planetaryyears = self.dailyplanetaryyears
        else:
            if self.options.isfirbonatti:
                planetaryyears = self.nightlyplanetaryyearsbonatti
            else:
                planetaryyears = self.nightlyplanetaryyearsalbiruni
        starting = self.startdate
        for index in range(len(planetaryyears) + 3):
            aindex = index % len(planetaryyears)
            planet, years = planetaryyears[aindex]
            ending = datetime(starting.year + years, starting.month, starting.day)
            print(('{0}: {1} - {2} ({3} years)').format(pltxts[planet], starting.strftime(Firdaria.TIME_FORMAT), (ending + timedelta(days=-1)).strftime(Firdaria.TIME_FORMAT), years))
            self.displaySubPeriods(planetaryyears, aindex, starting, ending, pltxts)
            print('')
            starting = ending