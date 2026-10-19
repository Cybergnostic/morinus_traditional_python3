# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math
import astrology
import chart
import dodecatemoria
import houses
import planets
import fortune
import fixedstars
import lots
import lotswnd
import options
import common
import util
import mtexts

class GraphChart:
    DEG1 = math.pi / 180
    DEG5 = math.pi / 36
    DEG10 = math.pi / 18
    DEG30 = math.pi / 6
    SMALL_SIZE = 400
    MEDIUM_SIZE = 600

    def __init__(self, chrt, size, opts, bw, plId=None, chart2=None):
        self.chart = chrt
        self.w, self.h = size
        self.options = opts
        self.plId = plId
        self.chart2 = chart2
        self.bw = bw
        self.buffer = wx.Bitmap(self.w, self.h)
        self.bdc = wx.BufferedDC(None, self.buffer)
        self.chartsize = min(self.w, self.h)
        self.maxradius = self.chartsize // 2
        self.center = wx.Point(size[0] // 2, size[1] // 2)
        self.arrowlen = 0.04
        self.retrdiff = 0.01
        self.deg01510len = 0.01
        if chart2 == None:
            if self.chart.full and self.options.showobject != 0:
                if self.options.showobject == chart.Chart.SHOWFIXEDSTARS or self.options.showobject == chart.Chart.SHOWLOTS:
                    self.symbolSize = self.maxradius // 18
                    self.signSize = self.maxradius // 18
                    self.planetsectorlen = 0.12
                    self.signsectorlen = 0.15
                    self.signoffs = self.signsectorlen / 2.0 * self.maxradius
                    self.planetoffs = self.planetsectorlen / 2.5 * self.maxradius
                    self.planetlinelen = 0.015
                    self.rHousesectorlen = 0.06
                    self.rAntis = self.maxradius * 0.92
                    self.rAntisLines = self.maxradius * 0.8
                    self.rDodec = self.maxradius * 0.92
                    self.rDodecLines = self.maxradius * 0.8
                    self.rFixedStars = self.maxradius * 0.8
                    self.r30 = self.maxradius * 0.75
                    self.rOuterLine = self.r30 + 0.03 * self.maxradius
                    self.rOuter0 = self.r30
                    self.rOuter1 = self.rOuter0 - self.deg01510len * self.maxradius
                    self.rOuter5 = self.rOuter1 - self.deg01510len * self.maxradius
                    self.rOuter10 = self.rOuter5 - self.deg01510len * self.maxradius
                    self.rOuterMin = self.maxradius * 0.68
                    self.rSign = self.r30 - self.signoffs
                    self.r0 = self.r30 - self.signsectorlen * self.maxradius
                    self.rInner = self.r0
                    self.r1 = self.r0 + self.deg01510len * self.maxradius
                    self.r5 = self.r1 + self.deg01510len * self.maxradius
                    self.r10 = self.r5 + self.deg01510len * self.maxradius
                    self.rASCMC = self.rSign
                    self.rArrow = self.rASCMC + self.arrowlen * self.maxradius
                    self.rTerms = self.r0
                    self.termssectorlen = 0.0
                    if self.options.showterms:
                        self.termssectorlen = 0.06
                    self.termsoffs = self.termssectorlen / 2.0 * self.maxradius
                    self.rTermsPlanet = self.r0 - self.termsoffs
                    self.rDecans = self.rTerms - self.termssectorlen * self.maxradius
                    self.decanssectorlen = 0.0
                    if self.options.showdecans:
                        self.decanssectorlen = 0.06
                    self.decansoffs = self.decanssectorlen / 2.0 * self.maxradius
                    self.rInner = self.rDecans - self.decanssectorlen * self.maxradius
                    self.rDecansPlanet = self.rInner + self.decansoffs
                    self.rLLine = self.rInner - self.planetlinelen * self.maxradius
                    self.rPlanet = self.rInner - self.planetoffs
                    self.rPosDeg = self.rInner - self.planetsectorlen * self.maxradius
                    self.rPosMin = self.rPosDeg - 0.04 * self.maxradius
                    self.rRetr = self.rPosMin - 0.04 * self.maxradius
                    posascmc = 0.34
                    poshouses = 0.34
                    self.rPosAscMC = self.maxradius * posascmc
                    self.rPosAscMCMin = self.rPosAscMC - self.maxradius * 0.05
                    self.rPosHouses = self.maxradius * poshouses
                    self.rPosHousesMin = self.rPosHouses - self.maxradius * 0.05
                    baseoffset = 0.0
                    if self.options.showterms and self.options.showdecans:
                        baseoffset = self.maxradius * 0.08
                    self.rBase = self.maxradius * 0.3 - baseoffset
                    self.rHouse = self.rBase + self.rHousesectorlen * self.maxradius
                    self.rHouseName = self.rBase + self.rHousesectorlen * self.maxradius / 2.0
                else:
                    self.symbolSize = self.maxradius // 16
                    self.signSize = self.maxradius // 20
                    self.planetsectorlen = 0.15
                    self.signsectorlen = self.planetsectorlen
                    self.signoffs = self.signsectorlen / 2.0 * self.maxradius
                    self.planetoffs = self.planetsectorlen / 2.0 * self.maxradius
                    self.planetlinelen = 0.03
                    self.rHousesectorlen = 0.06
                    self.rAntis = self.maxradius * 0.92
                    self.rAntisLines = self.maxradius * 0.88
                    self.rDodec = self.maxradius * 0.92
                    self.rDodecLines = self.maxradius * 0.88
                    self.rFixedStars = self.maxradius * 0.9
                    self.r30 = self.maxradius * 0.85
                    self.rOuterLine = self.r30 + self.planetlinelen * self.maxradius
                    self.rOuter0 = self.r30
                    self.rOuter1 = self.rOuter0 - self.deg01510len * self.maxradius
                    self.rOuter5 = self.rOuter1 - self.deg01510len * self.maxradius
                    self.rOuter10 = self.rOuter5 - self.deg01510len * self.maxradius
                    self.rOuterMin = self.maxradius * 0.78
                    self.rSign = self.r30 - self.signoffs
                    self.r0 = self.r30 - self.signsectorlen * self.maxradius
                    self.rInner = self.r0
                    self.r1 = self.r0 + self.deg01510len * self.maxradius
                    self.r5 = self.r1 + self.deg01510len * self.maxradius
                    self.r10 = self.r5 + self.deg01510len * self.maxradius
                    self.rASCMC = self.rSign
                    self.rArrow = self.rASCMC + self.arrowlen * self.maxradius
                    self.rTerms = self.r0
                    self.termssectorlen = 0.0
                    if self.options.showterms:
                        self.termssectorlen = 0.08
                    self.termsoffs = self.termssectorlen / 2.0 * self.maxradius
                    self.rTermsPlanet = self.r0 - self.termsoffs
                    self.rDecans = self.rTerms - self.termssectorlen * self.maxradius
                    self.decanssectorlen = 0.0
                    if self.options.showdecans:
                        self.decanssectorlen = 0.08
                    self.decansoffs = self.decanssectorlen / 2.0 * self.maxradius
                    self.rInner = self.rDecans - self.decanssectorlen * self.maxradius
                    self.rDecansPlanet = self.rInner + self.decansoffs
                    self.rLLine = self.rInner - self.planetlinelen * self.maxradius
                    self.rPlanet = self.rInner - self.planetoffs
                    self.rPosDeg = self.rInner - self.planetsectorlen * self.maxradius
                    self.rPosMin = self.rPosDeg - 0.04 * self.maxradius
                    self.rRetr = self.rPosMin - 0.05 * self.maxradius
                    posascmc = 0.34
                    poshouses = 0.34
                    self.rPosAscMC = self.maxradius * posascmc
                    self.rPosAscMCMin = self.rPosAscMC - self.maxradius * 0.05
                    self.rPosHouses = self.maxradius * poshouses
                    self.rPosHousesMin = self.rPosHouses - self.maxradius * 0.05
                    baseoffset = 0.0
                    if self.options.showterms and self.options.showdecans:
                        baseoffset = self.maxradius * 0.08
                    self.rBase = self.maxradius * 0.3 - baseoffset
                    self.rHouse = self.rBase + self.rHousesectorlen * self.maxradius
                    self.rHouseName = self.rBase + self.rHousesectorlen * self.maxradius / 2.0
            else:
                self.symbolSize = self.maxradius // 12
                self.signSize = self.maxradius // 12
                self.signsectorlen = 0.16
                self.planetsectorlen = 0.18
                self.planetoffs = self.planetsectorlen / 2.0 * self.maxradius
                self.planetlinelen = 0.03
                self.rHousesectorlen = 0.08
                self.r30 = self.maxradius * 0.96
                self.signoffs = (self.signsectorlen / 2.0 - 0.01) * self.maxradius
                self.rSign = self.r30 - self.signoffs
                self.rASCMC = self.maxradius * 0.88
                self.rArrow = self.rASCMC + self.arrowlen * self.maxradius
                self.r0 = self.r30 - self.signsectorlen * self.maxradius
                self.r1 = self.r0 + self.deg01510len * self.maxradius
                self.r5 = self.r1 + self.deg01510len * self.maxradius
                self.r10 = self.r5 + self.deg01510len * self.maxradius
                self.rTerms = self.r0
                self.termssectorlen = 0.0
                if self.options.showterms:
                    self.termssectorlen = 0.08
                self.termsoffs = self.termssectorlen / 2.0 * self.maxradius
                self.rTermsPlanet = self.r0 - self.termsoffs
                self.rDecans = self.rTerms - self.termssectorlen * self.maxradius
                self.decanssectorlen = 0.0
                if self.options.showdecans:
                    self.decanssectorlen = 0.08
                self.decansoffs = self.decanssectorlen / 2.0 * self.maxradius
                self.rInner = self.rDecans - self.decanssectorlen * self.maxradius
                self.rDecansPlanet = self.rInner + self.decansoffs
                self.rLLine = self.rInner - self.planetlinelen * self.maxradius
                self.rPlanet = self.rInner - self.planetoffs
                self.rPosDeg = self.rInner - self.planetsectorlen * self.maxradius
                self.rPosMin = self.rPosDeg - 0.05 * self.maxradius
                self.rRetr = self.rPosMin - 0.05 * self.maxradius
                posascmc = 0.42
                poshouses = 0.42
                self.rPosAscMC = self.maxradius * posascmc
                self.rPosAscMCMin = self.rPosAscMC - self.maxradius * 0.05
                self.rPosHouses = self.maxradius * poshouses
                self.rPosHousesMin = self.rPosHouses - self.maxradius * 0.05
                baseoffset = 0.0
                if self.options.showterms and self.options.showdecans:
                    baseoffset = self.maxradius * 0.08
                self.rBase = self.maxradius * 0.3 - baseoffset
                self.rHouse = self.rBase + self.rHousesectorlen * self.maxradius
                self.rHouseName = self.rBase + self.rHousesectorlen * self.maxradius / 2.0
        else:
            # duads of the second chart (return/transit) go in an outer ring; the wheel is drawn smaller to make room
            self.duads2 = self.options.showobject == chart.Chart.SHOWDODECATEMORIA
            if self.duads2:
                fullradius = self.maxradius
                self.maxradius = int(self.maxradius * 0.86)
                self.rDodec = fullradius * 0.94
                self.rDodecLines = fullradius * 0.89
            self.symbolSize = self.maxradius // 16
            self.signSize = self.maxradius // 20
            self.outerplanetsectorlen = 0.12
            self.planetsectorlen = 0.15
            self.signsectorlen = self.planetsectorlen
            self.signoffs = self.signsectorlen / 2.0 * self.maxradius
            self.planetoffs = self.planetsectorlen / 2.0 * self.maxradius
            self.planetlinelen = 0.03
            self.rHousesectorlen = 0.06
            self.rOuterMax = self.maxradius * 0.97
            if self.options.houses:
                self.rOuterHouseName = self.rOuterMax - self.rHousesectorlen * self.maxradius / 2.0
                self.rOuterHouse = self.rOuterMax - self.rHousesectorlen * self.maxradius
                self.r30 = self.rOuterHouse - self.outerplanetsectorlen * self.maxradius
            else:
                self.r30 = self.rOuterMax - self.outerplanetsectorlen * self.maxradius
                self.rOuterASCMC = self.maxradius * 0.92
            self.rOuterPlanet = self.r30 + self.planetoffs
            self.rOuterASCMC = self.maxradius * 0.92
            self.rOuterArrow = self.rOuterASCMC + self.arrowlen * self.maxradius
            self.rOuterLine = self.r30 + self.planetlinelen * self.maxradius
            self.rOuterRetr = self.rOuterLine + self.maxradius * self.retrdiff
            self.rOuter0 = self.r30
            self.rOuter1 = self.rOuter0 - self.deg01510len * self.maxradius
            self.rOuter5 = self.rOuter1 - self.deg01510len * self.maxradius
            self.rOuter10 = self.rOuter5 - self.deg01510len * self.maxradius
            self.rOuterMin = self.maxradius * 0.78
            self.rSign = self.r30 - self.signoffs
            self.r0 = self.r30 - self.signsectorlen * self.maxradius
            self.r1 = self.r0 + self.deg01510len * self.maxradius
            self.r5 = self.r1 + self.deg01510len * self.maxradius
            self.r10 = self.r5 + self.deg01510len * self.maxradius
            self.rASCMC = self.rSign
            self.rArrow = self.rASCMC + self.arrowlen * self.maxradius
            self.rTerms = self.r0
            self.termssectorlen = 0.0
            if self.options.showterms:
                self.termssectorlen = 0.08
            self.termsoffs = self.termssectorlen / 2.0 * self.maxradius
            self.rTermsPlanet = self.r0 - self.termsoffs
            self.rDecans = self.rTerms - self.termssectorlen * self.maxradius
            self.decanssectorlen = 0.0
            if self.options.showdecans:
                self.decanssectorlen = 0.08
            self.decansoffs = self.decanssectorlen / 2.0 * self.maxradius
            self.rInner = self.rDecans - self.decanssectorlen * self.maxradius
            self.rDecansPlanet = self.rInner + self.decansoffs
            self.rLLine = self.rInner - self.planetlinelen * self.maxradius
            self.rPlanet = self.rInner - self.planetoffs
            self.rPosDeg = self.rInner - self.planetsectorlen * self.maxradius
            self.rPosMin = self.rPosDeg - 0.05 * self.maxradius
            self.rRetr = self.rPosMin - 0.05 * self.maxradius
            posascmc = 0.34
            poshouses = 0.34
            self.rPosAscMC = self.maxradius * posascmc
            self.rPosAscMCMin = self.rPosAscMC - self.maxradius * 0.05
            self.rPosHouses = self.maxradius * poshouses
            self.rPosHousesMin = self.rPosHouses - self.maxradius * 0.05
            baseoffset = 0.0
            if self.options.showterms and self.options.showdecans:
                baseoffset = self.maxradius * 0.16
            elif self.options.showterms or self.options.showdecans:
                baseoffset = self.maxradius * 0.08
            self.rBase = self.maxradius * 0.3 - baseoffset
            self.rHouse = self.rBase + self.rHousesectorlen * self.maxradius
            self.rHouseName = self.rBase + self.rHousesectorlen * self.maxradius / 2.0
        self.smallsymbolSize = 2 * self.symbolSize // 3
        self.dataTxtSize = self.maxradius // 24
        self.dataTxtSize2 = self.maxradius // 32
        self.dataTxtSize3 = self.maxradius // 48
        self.fntMorinus = util.truetype(common.common.symbols, self.symbolSize)
        self.fntSmallMorinus = util.truetype(common.common.symbols, self.smallsymbolSize)
        self.fntMorinusSigns = util.truetype(common.common.symbols, self.signSize)
        self.fntText = util.truetype(common.common.abc, self.symbolSize // 2)
        self.fntAntisText = util.truetype(common.common.abc, self.symbolSize)
        self.fntDodecText = util.truetype(common.common.abc, self.symbolSize)
        self.fntSmallText = util.truetype(common.common.abc, self.symbolSize // 2)
        self.fntRetr = util.truetype(common.common.symbols, self.symbolSize // 2)
        self.fntRetrOuter = util.truetype(common.common.symbols, self.symbolSize // 4)
        self.fntSmallTextOuter = util.truetype(common.common.abc, self.symbolSize // 4)
        self.fntSmallText2 = util.truetype(common.common.abc, self.symbolSize // 3)
        self.fntMorinusData = util.truetype(common.common.symbols, self.dataTxtSize)
        self.fntMorinusData2 = util.truetype(common.common.symbols, self.dataTxtSize2)
        self.fntMorinusData3 = util.truetype(common.common.symbols, self.dataTxtSize3)
        self.fntDataText = util.truetype(common.common.abc, self.dataTxtSize)
        self.fntDataText2 = util.truetype(common.common.abc, self.dataTxtSize2)
        self.fntDataText3 = util.truetype(common.common.abc, self.dataTxtSize3)
        self.deg_symbol = '\xb0'
        self.hsystem = (
         mtexts.txtscommon['HSPlacidus'], mtexts.txtscommon['HSKoch'], mtexts.txtscommon['HSRegiomontanus'], mtexts.txtscommon['HSCampanus'], mtexts.txtscommon['HSEqual'], mtexts.txtscommon['HSWholeSign'], mtexts.txtscommon['HSAxial'], mtexts.txtscommon['HSMorinus'], mtexts.txtscommon['HSHorizontal'], mtexts.txtscommon['HSPagePolich'], mtexts.txtscommon['HSAlcabitus'], mtexts.txtscommon['HSPorphyrius'])
        self.ayans = {
            0: mtexts.txtsayanamsha['None'],
            1: mtexts.txtsayanamsha['FaganBradley'],
            2: mtexts.txtsayanamsha['Lahiri'],
            3: mtexts.txtsayanamsha['Deluce'],
            4: mtexts.txtsayanamsha['Raman'],
            5: mtexts.txtsayanamsha['Ushashashi'],
            6: mtexts.txtsayanamsha['Krishnamurti'],
            7: mtexts.txtsayanamsha['DjwhalKhul'],
            8: mtexts.txtsayanamsha['Yukteshwar'],
            9: mtexts.txtsayanamsha['JNBhasin'],
            10: mtexts.txtsayanamsha['BabylonianKuglerI2'],
            11: mtexts.txtsayanamsha['BabylonianKuglerII2'],
            12: mtexts.txtsayanamsha['BabylonianKuglerIII2'],
            13: mtexts.txtsayanamsha['BabylonianHuber2'],
            14: mtexts.txtsayanamsha['BabylonianMercier2'],
            15: mtexts.txtsayanamsha['Aldebaran15Tau2'],
            16: mtexts.txtsayanamsha['Hipparchos'],
            17: mtexts.txtsayanamsha['Sassanian'],
            18: mtexts.txtsayanamsha['GalacticCenter0Sag2'],
            19: mtexts.txtsayanamsha['J2000'],
            20: mtexts.txtsayanamsha['J1900'],
            21: mtexts.txtsayanamsha['B1950']}
        return

    def drawChart(self):
        self.drawCircles()
        if self.options.showterms:
            self.drawTermsLines()
        if self.options.showdecans:
            self.drawDecansLines()
        if self.options.houses:
            self.drawHouses(self.chart.houses, self.rBase, self.rInner)
            if self.chart2 != None:
                self.drawHouses(self.chart2.houses, self.r30, self.rOuterMax)
        wxImag = self.buffer.ConvertToImage()
        self.img = Image.new('RGB', (wxImag.GetWidth(), wxImag.GetHeight()))
        self.img.frombytes(wxImag.GetData())
        self.draw = ImageDraw.Draw(self.img)
        if self.options.houses:
            self.drawHouseNames(self.chart, self.rHouseName)
            if self.chart2 != None:
                self.drawHouseNames(self.chart2, self.rOuterHouseName)
        self.drawSigns()
        wxImg = wx.Image(self.img.size[0], self.img.size[1])
        wxImg.SetData(self.img.tobytes())
        self.buffer = wx.Bitmap(wxImg)
        self.bdc = wx.BufferedDC(None, self.buffer)
        self.drawAscMC(self.chart.houses.ascmc, self.rBase, self.rASCMC, self.rArrow)
        if self.chart2 != None:
            self.drawAscMC(self.chart2.houses.ascmc, self.rOuterMin, self.rOuterASCMC, self.rOuterArrow)
        lons = []
        objs = []
        fnts = []
        for i in range(planets.Planets.BODIES_NUM):
            lons.append(self.chart.planets.planets[i].data[planets.Planet.LON])
            objs.append(common.common.planets[i])
            fnts.append(self.fntMorinus)

        addendum = 0.0
        if self.options.lotsusehouses:
            addendum = 15.0
        if self.options.lotsvisible[0]:
            lonLoF = self.chart.fortune.fortune[fortune.Fortune.LON]
            if self.options.ayanamsha != 0:
                lonLoF += self.chart.ayanamsha
                lonLoF = util.normalize(lonLoF)
            lonLoF = util.normalize(lonLoF + addendum)
            lons.append(lonLoF)
            objs.append(common.common.fortune)
            fnts.append(self.fntMorinus)
        idorder = self.getIdOrder(lons)
        self.pshift = self.arrangeObjs(objs, lons, fnts, idorder, self.rPlanet)
        self.drawObjLines(self.pshift, lons, self.rInner, self.rLLine)
        if self.chart2 != None:
            lons2 = []
            objs2 = []
            fnts2 = []
            for i in range(planets.Planets.BODIES_NUM):
                lons2.append(self.chart2.planets.planets[i].data[planets.Planet.LON])
                objs2.append(common.common.planets[i])
                fnts2.append(self.fntMorinus)

            if self.options.lotsvisible[0]:
                lonLoF = self.chart2.fortune.fortune[fortune.Fortune.LON]
                if self.options.ayanamsha != 0:
                    lonLoF += self.chart2.ayanamsha
                    lonLoF = util.normalize(lonLoF)
                lonLoF = util.normalize(lonLoF + addendum)
                lons2.append(lonLoF)
                objs2.append(common.common.fortune)
                fnts2.append(self.fntMorinus)
            idorder2 = self.getIdOrder(lons2)
            self.pshift2 = self.arrangeObjs(objs2, lons2, fnts2, idorder2, self.rOuterPlanet)
            self.drawObjLines(self.pshift2, lons2, self.r30, self.rOuterLine)
        if self.chart2 == None and self.chart.full and self.options.showobject != chart.Chart.SHOWNONE:
            if self.options.showobject == chart.Chart.SHOWFIXEDSTARS:
                self.showfss = self.mergefsaspmatrices()
                lonsfs = []
                objsfs = []
                fntsfs = []
                added = False
                if self.options.showfixedstarsoutoforb:
                    for i in range(len(self.chart.fixedstars.data)):
                        lonsfs.append(self.chart.fixedstars.data[i][fixedstars.FixedStars.LON])
                        txt = self.chart.fixedstars.data[i][fixedstars.FixedStars.NAME]
                        txt.strip()
                        if txt == '':
                            txt = self.chart.fixedstars.data[i][fixedstars.FixedStars.NOMNAME]
                        objsfs.append(txt)
                        fntsfs.append(self.fntText)
                        if not added:
                            added = True

                else:
                    for i in range(len(self.showfss)):
                        lonsfs.append(self.chart.fixedstars.data[self.showfss[i]][fixedstars.FixedStars.LON])
                        txt = self.chart.fixedstars.data[self.showfss[i]][fixedstars.FixedStars.NAME]
                        txt.strip()
                        if txt == '':
                            txt = self.chart.fixedstars.data[self.showfss[i]][fixedstars.FixedStars.NOMNAME]
                        objsfs.append(txt)
                        fntsfs.append(self.fntText)
                        if not added:
                            added = True

                if added:
                    self.fsnames = objsfs[:]
                    self.fslons = lonsfs[:]
                    if len(objsfs) > 1:
                        idorderfs = self.getIdOrder(lonsfs)
                        self.fsshift = self.arrangeObjs(objsfs, lonsfs, fntsfs, idorderfs, self.rFixedStars)
                    else:
                        self.fsshift = [
                         0.0]
                    self.drawObjLines(self.fsshift, lonsfs, self.r30, self.rOuterLine)
                    self.bdc.SetFont(wx.Font(self.symbolSize // 2, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                    self.drawTexts2(self.bdc, self.fsnames, self.fslons, self.fsshift, self.fntText, self.rFixedStars)
                else:
                    self.fsnames = None
                    self.fslons = None
            elif self.options.showobject == chart.Chart.SHOWANTIS:
                lonsant = []
                objsant = []
                fntsant = []
                for i in range(planets.Planets.BODIES_NUM):
                    lonsant.append(self.chart.antiscia.plantiscia[i].lon)
                    objsant.append(common.common.planets[i])
                    fntsant.append(self.fntMorinus)

                artxt = (mtexts.txtscommon['AntAsc'], mtexts.txtscommon['AntMC'])
                for i in range(2):
                    lonsant.append(self.chart.antiscia.ascmcant[i].lon)
                    objsant.append(artxt[i])
                    fntsant.append(self.fntAntisText)

                if self.options.lotsvisible[0]:
                    lonsant.append(self.chart.antiscia.lofant.lon)
                    objsant.append(common.common.fortune)
                    fntsant.append(self.fntMorinus)
                idorderant = self.getIdOrder(lonsant)
                self.antshift = self.arrangeObjs(objsant, lonsant, fntsant, idorderant, self.rAntis)
                self.drawObjLines(self.antshift, lonsant, self.r30, self.rAntisLines)
            elif self.options.showobject == chart.Chart.SHOWLOTS:
                if self.chart.lots.lots != None and len(self.chart.lots.lots) > 1:
                    lonslot = []
                    objslot = []
                    fntslot = []
                    added = False
                    for i in range(1, len(self.chart.lots.lots)):
                        if self.options.lotsvisible[i]:
                            lonLot = self.chart.lots.lots[i][lots.Lots.LON]
                            if self.options.ayanamsha != 0:
                                lonLot += self.chart.ayanamsha
                                lonLot = util.normalize(lonLot)
                            lonLot = util.normalize(lonLot + addendum)
                            lonslot.append(lonLot)
                            txt = self.chart.lots.lots[i][lots.Lots.NAME]
                            txt.strip()
                            objslot.append(txt)
                            fntslot.append(self.fntText)
                            if not added:
                                added = True

                    if added:
                        self.lotnames = objslot[:]
                        self.lotlons = lonslot[:]
                        if len(objslot) > 1:
                            idorderlot = self.getIdOrder(lonslot)
                            self.lotshift = self.arrangeObjs(objslot, lonslot, fntslot, idorderlot, self.rFixedStars)
                        else:
                            self.lotshift = [
                             0.0]
                        self.drawObjLines(self.lotshift, lonslot, self.r30, self.rOuterLine)
                        self.bdc.SetFont(wx.Font(self.symbolSize // 2, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                        self.drawTexts2(self.bdc, self.lotnames, self.lotlons, self.lotshift, self.fntText, self.rFixedStars)
                    else:
                        self.lotnames = None
                        self.lotlons = None
            elif self.options.showobject == chart.Chart.SHOWDODECATEMORIA:
                lonsdodec, objsdodec, fntsdodec = self.dodecObjs(self.chart)
                idorderant = self.getIdOrder(lonsdodec)
                self.dodecshift = self.arrangeObjs(objsdodec, lonsdodec, fntsdodec, idorderant, self.rDodec)
                self.drawObjLines(self.dodecshift, lonsdodec, self.r30, self.rDodecLines)
        if self.chart2 != None and self.duads2:
            lonsdodec2, objsdodec2, fntsdodec2 = self.dodecObjs(self.chart2)
            self.dodecshift2 = self.arrangeObjs(objsdodec2, lonsdodec2, fntsdodec2, self.getIdOrder(lonsdodec2), self.rDodec)
            self.drawObjLines(self.dodecshift2, lonsdodec2, self.rOuterMax, self.rDodecLines)
        wxImag = self.buffer.ConvertToImage()
        self.img = Image.new('RGB', (wxImag.GetWidth(), wxImag.GetHeight()))
        self.img.frombytes(wxImag.GetData())
        self.draw = ImageDraw.Draw(self.img)
        if self.options.showdata:
            self.drawData(self.draw, self.chart)
        self.drawPlanets(self.chart, self.pshift, self.rPlanet, self.rRetr)
        if self.chart2 != None:
            self.drawPlanets(self.chart2, self.pshift2, self.rOuterPlanet, self.rOuterRetr, True)
        if self.options.lotsvisible[0]:
            self.drawLoF(self.chart, self.pshift, self.rPlanet, addendum)
            if self.chart2 != None:
                self.drawLoF(self.chart2, self.pshift2, self.rOuterPlanet, addendum, True)
        if self.options.showterms:
            self.drawTerms()
        if self.options.showdecans:
            self.drawDecans()
        if self.chart2 == None and self.chart.full and self.options.showobject != chart.Chart.SHOWNONE:
            if self.options.showobject == chart.Chart.SHOWFIXEDSTARS:
                pass
            elif self.options.showobject == chart.Chart.SHOWANTIS:
                self.drawAntis(self.chart, self.chart.antiscia.plantiscia, self.chart.antiscia.lofant, self.chart.antiscia.ascmcant, self.antshift, self.rAntis)
            elif self.options.showobject == chart.Chart.SHOWLOTS:
                pass
            elif self.options.showobject == chart.Chart.SHOWDODECATEMORIA:
                self.drawDodecatemoria(self.chart, lonsdodec, self.dodecshift, self.rDodec)
        if self.chart2 != None and self.duads2:
            self.drawDodecatemoria(self.chart2, lonsdodec2, self.dodecshift2, self.rDodec)
        if self.plId != None:
            self.drawOrbs(self.draw, self.chart)
        wxImg = wx.Image(self.img.size[0], self.img.size[1])
        wxImg.SetData(self.img.tobytes())
        self.buffer = wx.Bitmap(wxImg)
        return self.buffer

    def drawOrbs(self, draw, chrt):
        wait = wx.BusyCursor()
        cx, cy = self.center.Get()
        radiuses = []
        for i in range(planets.Planets.PLANETS_NUM):
            lon = chrt.planets.planets[i].data[planets.Planet.LON]
            x = cx + math.cos(math.pi + math.radians(chrt.houses.ascmc[houses.Houses.ASC] - lon)) * self.r0
            y = cy + math.sin(math.pi + math.radians(chrt.houses.ascmc[houses.Houses.ASC] - lon)) * self.r0
            orb = self.options.orbs[i]
            xo = cx + math.cos(math.pi + math.radians(chrt.houses.ascmc[houses.Houses.ASC] - (lon + orb / 2))) * self.r0
            yo = cy + math.sin(math.pi + math.radians(chrt.houses.ascmc[houses.Houses.ASC] - (lon + orb / 2))) * self.r0
            radius = math.sqrt(math.pow(math.fabs(x - xo), 2) + math.pow(math.fabs(y - yo), 2))
            clr = (0, 0, 0)
            if not self.bw:
                clr = self.options.clrplanets[i]
            self.rasterCircle(x, y, radius, draw, clr)
            radiuses.append(radius)

        j = self.plId
        lenasps = len(chart.Chart.Aspects)
        lon = chrt.planets.planets[j].data[planets.Planet.LON]
        for i in range(1, lenasps):
            lonasp = util.normalize(lon + chart.Chart.Aspects[i])
            x1 = cx + math.cos(math.pi + math.radians(chrt.houses.ascmc[houses.Houses.ASC] - chrt.planets.planets[j].data[planets.Planet.LON])) * self.r0
            y1 = cy + math.sin(math.pi + math.radians(chrt.houses.ascmc[houses.Houses.ASC] - chrt.planets.planets[j].data[planets.Planet.LON])) * self.r0
            x2 = cx + math.cos(math.pi + math.radians(chrt.houses.ascmc[houses.Houses.ASC] - lonasp)) * self.r0
            y2 = cy + math.sin(math.pi + math.radians(chrt.houses.ascmc[houses.Houses.ASC] - lonasp)) * self.r0
            clrasp = (0, 0, 0)
            if not self.bw:
                clrasp = self.options.clraspect[i]
            draw.line((x1, y1, x2, y2), fill=clrasp)
            clr = (0, 0, 0)
            if not self.bw:
                clr = self.options.clrplanets[j]
            self.rasterCircle(x2, y2, radiuses[j], draw, clr)
            if i != lenasps - 1:
                lonasp = util.normalize(lon - chart.Chart.Aspects[i])
                x1 = cx + math.cos(math.pi + math.radians(chrt.houses.ascmc[houses.Houses.ASC] - chrt.planets.planets[j].data[planets.Planet.LON])) * self.r0
                y1 = cy + math.sin(math.pi + math.radians(chrt.houses.ascmc[houses.Houses.ASC] - chrt.planets.planets[j].data[planets.Planet.LON])) * self.r0
                x2 = cx + math.cos(math.pi + math.radians(chrt.houses.ascmc[houses.Houses.ASC] - lonasp)) * self.r0
                y2 = cy + math.sin(math.pi + math.radians(chrt.houses.ascmc[houses.Houses.ASC] - lonasp)) * self.r0
                clrasp = (0, 0, 0)
                if not self.bw:
                    clrasp = self.options.clraspect[i]
                draw.line((x1, y1, x2, y2), fill=clrasp)
                clr = (0, 0, 0)
                if not self.bw:
                    clr = self.options.clrplanets[j]
                self.rasterCircle(x2, y2, radiuses[j], draw, clr)

    def rasterCircle(self, x0, y0, radius, draw, clr):
        f = 1 - radius
        ddF_x = 1
        ddF_y = -2 * radius
        x = 0
        y = radius
        draw.point((x0, y0 + radius), fill=clr)
        draw.point((x0, y0 - radius), fill=clr)
        draw.point((x0 + radius, y0), fill=clr)
        draw.point((x0 - radius, y0), fill=clr)
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            draw.point((x0 + x, y0 + y), fill=clr)
            draw.point((x0 - x, y0 + y), fill=clr)
            draw.point((x0 + x, y0 - y), fill=clr)
            draw.point((x0 - x, y0 - y), fill=clr)
            draw.point((x0 + y, y0 + x), fill=clr)
            draw.point((x0 - y, y0 + x), fill=clr)
            draw.point((x0 + y, y0 - x), fill=clr)
            draw.point((x0 - y, y0 - x), fill=clr)

    def drawCircles(self):
        bkgclr = self.options.clrbackground
        if self.bw:
            bkgclr = (255, 255, 255)
        self.bdc.SetBackground(wx.Brush(bkgclr))
        self.bdc.Clear()
        self.bdc.SetBrush(wx.Brush(bkgclr))
        cx, cy = self.center.Get()
        clr = self.options.clrframe
        if self.bw:
            clr = (0, 0, 0)
        if self.chart2 != None and self.options.houses:
            pen = wx.Pen(clr, 1)
            self.bdc.SetPen(pen)
            self.bdc.DrawCircle(int(cx), int(cy), int(self.rOuterMax))
            self.bdc.DrawCircle(int(cx), int(cy), int(self.rOuterHouse))
        if self.chart2 != None or self.chart.full and self.options.showobject != chart.Chart.SHOWNONE:
            w = 3
            if self.chartsize <= GraphChart.SMALL_SIZE:
                w = 1
            elif self.chartsize <= GraphChart.MEDIUM_SIZE:
                w = 2
            pen = wx.Pen(clr, w)
            self.bdc.SetPen(pen)
            self.bdc.DrawCircle(int(cx), int(cy), int(self.r30))
            pen = wx.Pen(clr, 1)
            self.bdc.SetPen(pen)
            self.bdc.DrawCircle(int(cx), int(cy), int(self.rOuter10))
        else:
            pen = wx.Pen(clr, 1)
            self.bdc.SetPen(pen)
            self.bdc.DrawCircle(int(cx), int(cy), int(self.r30))
        pen = wx.Pen(clr, 1)
        self.bdc.SetPen(pen)
        self.bdc.DrawCircle(int(cx), int(cy), int(self.r10))
        clr = self.options.clrframe
        if self.bw:
            clr = (0, 0, 0)
        if self.options.showterms or self.options.showdecans:
            pen = wx.Pen(clr, 1)
            self.bdc.SetPen(pen)
            self.bdc.DrawCircle(int(cx), int(cy), int(self.r0))
            if self.options.showterms:
                clr = self.options.clrframe
                if self.bw:
                    clr = (0, 0, 0)
                pen = wx.Pen(clr, 1)
                self.bdc.SetPen(pen)
                self.bdc.DrawCircle(int(cx), int(cy), int(self.rDecans))
        w = 3
        if self.chartsize <= GraphChart.SMALL_SIZE:
            w = 1
        elif self.chartsize <= GraphChart.MEDIUM_SIZE:
            w = 2
        pen = wx.Pen(clr, w)
        self.bdc.SetPen(pen)
        self.bdc.DrawCircle(int(cx), int(cy), int(self.rInner))
        if self.options.houses:
            clr = self.options.clrhouses
            if self.bw:
                clr = (0, 0, 0)
            pen = wx.Pen(clr, 1)
            self.bdc.SetPen(pen)
            self.bdc.DrawCircle(int(cx), int(cy), int(self.rHouse))
        clr = self.options.clrAscMC
        if self.bw:
            clr = (0, 0, 0)
        w = self.options.maxascmcsize
        if self.chartsize <= GraphChart.SMALL_SIZE and (w == 5 or w == 4 or w == 3):
            w = 2
        elif self.chartsize <= GraphChart.MEDIUM_SIZE and (w == 5 or w == 4):
            w = 3
        pen = wx.Pen(clr, w)
        self.bdc.SetPen(pen)
        self.bdc.DrawCircle(int(cx), int(cy), int(self.rBase))
        asclon = self.chart.houses.ascmc[houses.Houses.ASC]
        if self.options.ayanamsha != 0:
            asclon -= self.chart.ayanamsha
            asclon = util.normalize(asclon)
        clr = self.options.clrframe
        if self.bw:
            clr = (0, 0, 0)
        w = 3
        if self.chartsize <= GraphChart.SMALL_SIZE:
            w = 1
        elif self.chartsize <= GraphChart.MEDIUM_SIZE:
            w = 2
        pen = wx.Pen(clr, w)
        self.bdc.SetPen(pen)
        self.drawLines(GraphChart.DEG30, asclon, self.rInner, self.r30)
        clr = self.options.clrframe
        if self.bw:
            clr = (0, 0, 0)
        w = 2
        if self.chartsize <= GraphChart.MEDIUM_SIZE:
            w = 1
        pen = wx.Pen(clr, w)
        self.bdc.SetPen(pen)
        self.drawLines(GraphChart.DEG10, asclon, self.r0, self.r10)
        self.drawLines(GraphChart.DEG5, asclon, self.r0, self.r5)
        clr = self.options.clrframe
        if self.bw:
            clr = (0, 0, 0)
        pen = wx.Pen(clr, 1)
        self.bdc.SetPen(pen)
        self.drawLines(GraphChart.DEG1, asclon, self.r0, self.r1)
        if self.chart2 != None or self.chart.full and self.options.showobject != chart.Chart.SHOWNONE:
            clr = self.options.clrframe
            if self.bw:
                clr = (0, 0, 0)
            w = 2
            if self.chartsize <= GraphChart.MEDIUM_SIZE:
                w = 1
            pen = wx.Pen(clr, w)
            self.bdc.SetPen(pen)
            self.drawLines(GraphChart.DEG10, asclon, self.rOuter0, self.rOuter10)
            self.drawLines(GraphChart.DEG5, asclon, self.rOuter0, self.rOuter5)
            clr = self.options.clrframe
            if self.bw:
                clr = (0, 0, 0)
            pen = wx.Pen(clr, 1)
            self.bdc.SetPen(pen)
            self.drawLines(GraphChart.DEG1, asclon, self.rOuter0, self.rOuter1)
        return

    def drawSigns(self):
        cx, cy = self.center.Get()
        clr = self.options.clrsigns
        if self.bw:
            clr = (0, 0, 0)
        asclon = self.chart.houses.ascmc[houses.Houses.ASC]
        if self.options.ayanamsha != 0:
            asclon -= self.chart.ayanamsha
            asclon = util.normalize(asclon)
        i = math.pi + math.radians(asclon) - GraphChart.DEG30 / 2
        signs = common.common.signs
        j = 0
        while j < chart.Chart.SIGN_NUM:
            x = cx + math.cos(i) * self.rSign
            y = cy + math.sin(i) * self.rSign
            self.draw.text((x - self.signSize // 2, y - self.signSize // 2), signs[j], font=self.fntMorinusSigns, fill=clr)
            i -= GraphChart.DEG30
            j += 1

    def drawHouses(self, chouses, r1, r2):
        cx, cy = self.center.Get()
        clr = self.options.clrhouses
        if self.bw:
            clr = (0, 0, 0)
        pen = wx.Pen(clr, 1)
        self.bdc.SetPen(pen)
        asc = self.chart.houses.ascmc[houses.Houses.ASC]
        if self.options.ayanamsha != 0 and self.options.hsys == 5:
            asc = util.normalize(self.chart.houses.ascmc[houses.Houses.ASC] - self.chart.ayanamsha)
        for i in range(1, houses.Houses.HOUSE_NUM + 1):
            dif = math.radians(util.normalize(asc - chouses.cusps[i]))
            x1 = cx + math.cos(math.pi + dif) * r1
            y1 = cy + math.sin(math.pi + dif) * r1
            x2 = cx + math.cos(math.pi + dif) * r2
            y2 = cy + math.sin(math.pi + dif) * r2
            self.bdc.DrawLine(int(x1), int(y1), int(x2), int(y2))

    def drawAscMC(self, ascmc, r1, r2, rArrow):
        cx, cy = self.center.Get()
        clr = self.options.clrAscMC
        if self.bw:
            clr = (0, 0, 0)
        w = self.options.maxascmcsize
        if self.chartsize <= GraphChart.SMALL_SIZE and (w == 5 or w == 4 or w == 3):
            w = 2
        else:
            if self.chartsize <= GraphChart.MEDIUM_SIZE and (w == 5 or w == 4):
                w = 3
        pen = wx.Pen(clr, w)
        self.bdc.SetPen(pen)
        for i in range(4):
            ang = math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC])
            if i == 0:
                ang -= math.radians(ascmc[houses.Houses.ASC])
            if i == 1:
                ang -= math.radians(ascmc[houses.Houses.ASC]) + math.pi
            if i == 2:
                ang -= math.radians(ascmc[houses.Houses.MC])
            if i == 3:
                ang -= math.radians(ascmc[houses.Houses.MC]) + math.pi
            x1 = cx + math.cos(ang) * r1
            y1 = cy + math.sin(ang) * r1
            x2 = cx + math.cos(ang) * r2
            y2 = cy + math.sin(ang) * r2
            self.bdc.DrawLine(int(x1), int(y1), int(x2), int(y2))
            if i == 0 or i == 2:
                self.drawArrow(ang, r2, clr, rArrow)

    def drawArrow(self, ang, r2, clr, rArrow):
        cx, cy = self.center.Get()
        offs = math.pi / 360.0
        xl = cx + math.cos(ang + offs) * r2
        yl = cy + math.sin(ang + offs) * r2
        xr = cx + math.cos(ang - offs) * r2
        yr = cy + math.sin(ang - offs) * r2
        xm = cx + math.cos(ang) * rArrow
        ym = cy + math.sin(ang) * rArrow
        li = (
         (
          xl, yl, xr, yr), (xr, yr, xm, ym), (xm, ym, xl, yl))
        self.bdc.DrawLineList([[int(v) for v in ln] for ln in li])

    def drawHouseNames(self, chrt, rHouseNames):
        cx, cy = self.center.Get()
        clr = self.options.clrhousenumbers
        if self.bw:
            clr = (0, 0, 0)
        pen = wx.Pen(clr, 1)
        self.bdc.SetPen(pen)
        asc = self.chart.houses.ascmc[houses.Houses.ASC]
        if self.options.ayanamsha != 0 and self.options.hsys == 5:
            asc = util.normalize(self.chart.houses.ascmc[houses.Houses.ASC] - self.chart.ayanamsha)
        for i in range(1, houses.Houses.HOUSE_NUM + 1):
            width = 0.0
            if i != houses.Houses.HOUSE_NUM:
                width = chrt.houses.cusps[(i + 1)] - chrt.houses.cusps[i]
            else:
                width = chrt.houses.cusps[1] - chrt.houses.cusps[houses.Houses.HOUSE_NUM]
            width = util.normalize(width)
            halfwidth = math.radians(width / 2.0)
            dif = math.radians(util.normalize(asc - chrt.houses.cusps[i]))
            x = cx + math.cos(math.pi + dif - halfwidth) * rHouseNames
            y = cy + math.sin(math.pi + dif - halfwidth) * rHouseNames
            if i == 1 or i == 2:
                xoffs = 0
                yoffs = self.symbolSize // 4
                if i == 2:
                    xoffs = self.symbolSize // 8
            else:
                xoffs = self.symbolSize // 4
                yoffs = self.symbolSize // 4
            self.draw.text((x - xoffs, y - yoffs), common.common.housenames[(i - 1)], fill=clr, font=self.fntText)

    def drawData(self, draw, chrt):
        bctxt = ''
        if chrt.time.bc:
            bctxt = '-'
        datetxt = bctxt + str(chrt.time.origyear) + '.' + mtexts.months[(chrt.time.origmonth - 1)] + '.' + str(chrt.time.origday).zfill(2)
        if chrt.time.cal == chart.Time.JULIAN:
            datetxt += ' ' + mtexts.txtscommon['J']
        zonetxts = (mtexts.txtscommon['ZN'], mtexts.txtscommon['UT'], mtexts.txtscommon['LC'], mtexts.txtscommon['LC'])
        timetxt = str(chrt.time.hour).zfill(2) + ':' + str(chrt.time.minute).zfill(2) + ':' + str(chrt.time.second).zfill(2) + ' ' + zonetxts[chrt.time.zt]
        placetxt = chrt.place.placename
        dirlontxt = mtexts.txtscommon['E']
        if not chrt.place.east:
            dirlontxt = mtexts.txtscommon['W']
        dirlattxt = mtexts.txtscommon['N']
        if not chrt.place.north:
            dirlattxt = mtexts.txtscommon['S']
        coordtxt = str(chrt.place.deglon).zfill(2) + self.deg_symbol + str(chrt.place.minlon).zfill(2) + "'" + dirlontxt + '  ' + str(chrt.place.deglat).zfill(2) + self.deg_symbol + str(chrt.place.minlat).zfill(2) + "'" + dirlattxt
        nametxt = chrt.name
        typetxt = mtexts.typeList[chrt.htype]
        hstxt = self.hsystem[self.options.hsys]
        ayantxt = mtexts.txtsayanamsha['Tropical']
        if self.options.ayanamsha != 0:
            ayantxt = self.ayans[self.options.ayanamsha]
        txtclr = (0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        fntsize = self.dataTxtSize
        fnttxt = self.fntDataText
        fntsym = self.fntMorinusData
        offsx = self.chartsize // 11
        offsy = self.chartsize // 9
        if self.chart2 == None and self.options.showterms and self.options.showdecans or self.chart2 != None and (self.options.showterms or self.options.showdecans):
            if self.chart2 == None:
                fnttxt = self.fntDataText2
                fntsym = self.fntMorinusData2
                fntsize = self.dataTxtSize2
                offsx = self.chartsize // 15
                offsy = self.chartsize // 13
            else:
                fnttxt = self.fntDataText3
                fntsym = self.fntMorinusData3
                fntsize = self.dataTxtSize3
                offsx = self.chartsize // 22
                offsy = self.chartsize // 20
        SPACE = fntsize // 8
        LINE_HEIGHT = SPACE + fntsize + SPACE
        cx, cy = self.center.Get()
        x = cx - offsx
        y = cy - offsy
        draw.text((x, y), datetxt, fill=txtclr, font=fnttxt)
        draw.text((x, y + LINE_HEIGHT), timetxt, fill=txtclr, font=fnttxt)
        draw.text((x, y + 2 * LINE_HEIGHT), placetxt, fill=txtclr, font=fnttxt)
        draw.text((x, y + 3 * LINE_HEIGHT), coordtxt, fill=txtclr, font=fnttxt)
        draw.text((x, y + 4 * LINE_HEIGHT), nametxt, fill=txtclr, font=fnttxt)
        draw.text((x, y + 5 * LINE_HEIGHT), typetxt, fill=txtclr, font=fnttxt)
        draw.text((x, y + 6 * LINE_HEIGHT), ayantxt, fill=txtclr, font=fnttxt)
        draw.text((x, y + 7 * LINE_HEIGHT), hstxt, fill=txtclr, font=fnttxt)
        ar = (6, 2, 5, 1, 4, 0, 3)
        draw.text((x, y + 8 * LINE_HEIGHT), common.common.planets[ar[chrt.time.ph.weekday]], fill=txtclr, font=fntsym)
        wsym, hsym = draw.textbbox((0, 0), common.common.planets[ar[chrt.time.ph.weekday]], fntsym)[2:]
        wsp, hsp = draw.textbbox((0, 0), ' ', fnttxt)[2:]
        draw.text((x + wsym + wsp, y + 8 * LINE_HEIGHT), mtexts.txtscommon['Day'], fill=txtclr, font=fnttxt)
        wday, hday = draw.textbbox((0, 0), mtexts.txtscommon['Day'], fnttxt)[2:]
        wsym2, hsym2 = draw.textbbox((0, 0), common.common.planets[chrt.time.ph.planetaryhour], fntsym)[2:]
        draw.text((x + wsym + wsp + wday + 2 * wsp, y + 8 * LINE_HEIGHT), common.common.planets[chrt.time.ph.planetaryhour], fill=txtclr, font=fntsym)
        draw.text((x + wsym + wsp + wday + 2 * wsp + wsym2 + wsp, y + 8 * LINE_HEIGHT), mtexts.txtscommon['Hour'], fill=txtclr, font=fnttxt)
        return

    def drawRotatedText(self, text, fnt, angle, fill=None):
        size = fnt.getbbox(text)[2:]
        im = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), text, font=fnt, fill=fill)
        return im.rotate(angle, expand=True)

    def drawPlanets(self, chrt, pshift, rPlanet, rRetr, outer=False):
        cx, cy = self.center.Get()
        for i in range(planets.Planets.BODIES_NUM):
            lon = chrt.planets.planets[i].data[planets.Planet.LON]
            x = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - pshift[i])) * rPlanet
            y = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - pshift[i])) * rPlanet
            clr = (0, 0, 0)
            if not self.bw:
                if i < planets.Planets.BODIES_NUM - 1:
                    clr = self.options.clrplanets[i]
                else:
                    clr = self.options.clrplanets[(i - 1)]
            self.draw.text((x - self.symbolSize // 2, y - self.symbolSize // 2), common.common.planets[i], fill=clr, font=self.fntMorinus)
            if not outer:
                alon = lon
                if self.options.ayanamsha != 0:
                    alon -= self.chart.ayanamsha
                    alon = util.normalize(alon)
                d, m, s = util.decToDeg(alon)
                d = d % chart.Chart.SIGN_DEG
                degtxt = str(d).zfill(2) + self.deg_symbol
                wdeg, hdeg = self.draw.textbbox((0, 0), degtxt, self.fntText)[2:]
                x = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - pshift[i])) * self.rPosDeg
                y = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - pshift[i])) * self.rPosDeg
                xdeg = x - wdeg // 2
                ydeg = y - hdeg // 2
                self.draw.text((xdeg, ydeg), degtxt, fill=clr, font=self.fntText)
                mintxt = str(m).zfill(2) + "'"
                wdeg, hdeg = self.draw.textbbox((0, 0), mintxt, self.fntSmallText2)[2:]
                x = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - pshift[i])) * self.rPosMin
                y = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - pshift[i])) * self.rPosMin
                xdeg = x - wdeg // 2
                ydeg = y - hdeg // 2
                self.draw.text((xdeg, ydeg), mintxt.zfill(2), fill=clr, font=self.fntSmallText2)
                if chrt.planets.planets[i].data[planets.Planet.SPLON] <= 0.0:
                    if chrt.planets.planets[i].data[planets.Planet.SPLON] == 0.0:
                        t = 'S'
                        rfnt = self.fntSmallText
                    elif chrt.planets.planets[i].data[planets.Planet.SPLON] < 0.0:
                        t = common.common.retr
                        rfnt = self.fntRetr
                    wdeg, hdeg = self.draw.textbbox((0, 0), t, rfnt)[2:]
                    x = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - chrt.planets.planets[i].data[planets.Planet.LON] - pshift[i])) * rRetr
                    y = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - chrt.planets.planets[i].data[planets.Planet.LON] - pshift[i])) * rRetr
                    xdeg = x - wdeg // 2
                    ydeg = y - hdeg // 2
                    self.draw.text((xdeg, ydeg), t, fill=clr, font=rfnt)
            elif i < planets.Planets.BODIES_NUM:
                if chrt.planets.planets[i].data[planets.Planet.SPLON] <= 0.0:
                    t = 'S'
                    rfnt = self.fntSmallTextOuter
                    if chrt.planets.planets[i].data[planets.Planet.SPLON] < 0.0:
                        t = common.common.retr
                        rfnt = self.fntRetrOuter
                    x = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - chrt.planets.planets[i].data[planets.Planet.LON] - pshift[i])) * rRetr
                    y = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - chrt.planets.planets[i].data[planets.Planet.LON] - pshift[i])) * rRetr
                    self.draw.text((x - self.symbolSize // 8, y - self.symbolSize // 8), t, fill=clr, font=rfnt)

    def onClick(self, pos):
        cx, cy = self.center.Get()
        for i in range(planets.Planets.PLANETS_NUM):
            lon = self.chart.planets.planets[i].data[planets.Planet.LON]
            x = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - self.pshift[i])) * self.rPlanet
            y = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - self.pshift[i])) * self.rPlanet
            if pos[0] > x - self.symbolSize // 2 and pos[0] < x + self.symbolSize // 2 and pos[1] > y - self.symbolSize // 2 and pos[1] < y + self.symbolSize // 2:
                return i

        return

    def drawLoF(self, chrt, pshift, rPlanet, addendum, outer=False):
        cx, cy = self.center.Get()
        lon = chrt.fortune.fortune[fortune.Fortune.LON]
        offs = 0.0
        if self.options.ayanamsha != 0:
            offs += self.chart.ayanamsha
            offs = util.normalize(offs)
        lon = util.normalize(lon + addendum)
        x = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - offs - pshift[planets.Planets.BODIES_NUM])) * rPlanet
        y = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - offs - pshift[planets.Planets.BODIES_NUM])) * rPlanet
        clr = (0, 0, 0)
        if not self.bw:
            clr = self.options.clrLoF
        self.draw.text((x - self.symbolSize // 2, y - self.symbolSize // 2), common.common.fortune, fill=clr, font=self.fntMorinus)
        if not outer:
            d, m, s = util.decToDeg(lon)
            d = d % chart.Chart.SIGN_DEG
            degtxt = str(d).zfill(2) + self.deg_symbol
            wdeg, hdeg = self.draw.textbbox((0, 0), degtxt, self.fntText)[2:]
            x = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - offs - pshift[planets.Planets.BODIES_NUM])) * self.rPosDeg
            y = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - offs - pshift[planets.Planets.BODIES_NUM])) * self.rPosDeg
            xdeg = x - wdeg // 2
            ydeg = y - hdeg // 2
            self.draw.text((xdeg, ydeg), degtxt, fill=clr, font=self.fntText)
            mintxt = str(m).zfill(2) + "'"
            wdeg, hdeg = self.draw.textbbox((0, 0), mintxt, self.fntSmallText2)[2:]
            x = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - offs - pshift[planets.Planets.BODIES_NUM])) * self.rPosMin
            y = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - offs - pshift[planets.Planets.BODIES_NUM])) * self.rPosMin
            xdeg = x - wdeg // 2
            ydeg = y - hdeg // 2
            self.draw.text((xdeg, ydeg), mintxt.zfill(2), fill=clr, font=self.fntSmallText2)

    def drawLines(self, deg, shift, r1, r2):
        cx, cy = self.center.Get()
        i = math.pi + math.radians(shift)
        while i > -math.pi + math.radians(shift):
            x1 = cx + math.cos(i) * r1
            y1 = cy + math.sin(i) * r1
            x2 = cx + math.cos(i) * r2
            y2 = cy + math.sin(i) * r2
            self.bdc.DrawLine(int(x1), int(y1), int(x2), int(y2))
            i -= deg

    def drawTermsLines(self):
        cx, cy = self.center.Get()
        asclon = self.chart.houses.ascmc[houses.Houses.ASC]
        if self.options.ayanamsha != 0:
            asclon -= self.chart.ayanamsha
            asclon = util.normalize(asclon)
        shift = math.radians(asclon)
        signdeg = float(chart.Chart.SIGN_DEG)
        num = len(self.options.terms[self.options.selterm])
        subnum = len(self.options.terms[self.options.selterm][0])
        sign = 0.0
        for i in range(num):
            deg = sign
            for j in range(subnum):
                deg += float(self.options.terms[self.options.selterm][i][j][1])
                x1 = cx + math.cos(math.pi + shift - math.radians(deg)) * self.rTerms
                y1 = cy + math.sin(math.pi + shift - math.radians(deg)) * self.rTerms
                x2 = cx + math.cos(math.pi + shift - math.radians(deg)) * self.rDecans
                y2 = cy + math.sin(math.pi + shift - math.radians(deg)) * self.rDecans
                self.bdc.DrawLine(int(x1), int(y1), int(x2), int(y2))

            sign += signdeg

    def drawTerms(self):
        cx, cy = self.center.Get()
        clr = (0, 0, 0)
        if not self.bw:
            clr = self.options.clrsigns
        asclon = self.chart.houses.ascmc[houses.Houses.ASC]
        if self.options.ayanamsha != 0:
            asclon -= self.chart.ayanamsha
            asclon = util.normalize(asclon)
        shift = math.radians(asclon)
        signdeg = float(chart.Chart.SIGN_DEG)
        num = len(self.options.terms[self.options.selterm])
        subnum = len(self.options.terms[self.options.selterm][0])
        sign = 0.0
        for i in range(num):
            deg = sign
            for j in range(subnum):
                pldeg = deg + float(self.options.terms[self.options.selterm][i][j][1]) / 2.0
                deg += float(self.options.terms[self.options.selterm][i][j][1])
                x = cx + math.cos(math.pi + shift - math.radians(pldeg)) * self.rTermsPlanet
                y = cy + math.sin(math.pi + shift - math.radians(pldeg)) * self.rTermsPlanet
                self.draw.text((x - self.smallsymbolSize // 2, y - self.smallsymbolSize // 2), common.common.planets[self.options.terms[self.options.selterm][i][j][0]], fill=clr, font=self.fntSmallMorinus)

            sign += signdeg

    def drawDecansLines(self):
        cx, cy = self.center.Get()
        asclon = self.chart.houses.ascmc[houses.Houses.ASC]
        if self.options.ayanamsha != 0:
            asclon -= self.chart.ayanamsha
            asclon = util.normalize(asclon)
        shift = asclon
        deg = GraphChart.DEG10
        i = math.pi + math.radians(shift)
        while i > -math.pi + math.radians(shift):
            x1 = cx + math.cos(i) * self.rInner
            y1 = cy + math.sin(i) * self.rInner
            x2 = cx + math.cos(i) * self.rDecans
            y2 = cy + math.sin(i) * self.rDecans
            self.bdc.DrawLine(int(x1), int(y1), int(x2), int(y2))
            i -= deg

    def drawDecans(self):
        cx, cy = self.center.Get()
        clr = (0, 0, 0)
        if not self.bw:
            clr = self.options.clrsigns
        asclon = self.chart.houses.ascmc[houses.Houses.ASC]
        if self.options.ayanamsha != 0:
            asclon -= self.chart.ayanamsha
            asclon = util.normalize(asclon)
        shift = math.radians(asclon)
        num = len(self.options.decans[self.options.seldecan])
        subnum = len(self.options.decans[self.options.seldecan][0])
        deg = 5.0
        for i in range(num):
            for j in range(subnum):
                x = cx + math.cos(math.pi + shift - math.radians(deg)) * self.rDecansPlanet
                y = cy + math.sin(math.pi + shift - math.radians(deg)) * self.rDecansPlanet
                self.draw.text((x - self.smallsymbolSize // 2, y - self.smallsymbolSize // 2), common.common.planets[self.options.decans[self.options.seldecan][i][j]], fill=clr, font=self.fntSmallMorinus)
                deg += 10.0

    def dodecObjs(self, chrt):
        """Duad longitudes, symbols and fonts of a chart (computed here for charts made without them)"""
        if chrt.dodecatemoria is None:
            chrt.dodecatemoria = dodecatemoria.Dodecatemoria(chrt.planets, chrt.houses.ascmc, chrt.fortune.fortune, chrt.options.ayanamsha, chrt.ayanamsha)
        lonsdodec = []
        objsdodec = []
        fntsdodec = []
        artxt = (mtexts.txtscommon['AntAsc'], mtexts.txtscommon['AntMC'])
        for i in range(planets.Planets.BODIES_NUM + 2):
            lon = chrt.dodecatemoria.lons[i]
            if self.options.ayanamsha != 0:
                lon += chrt.ayanamsha
                lon = util.normalize(lon)
            lonsdodec.append(lon)
            if i < planets.Planets.BODIES_NUM:
                objsdodec.append(common.common.planets[i])
                fntsdodec.append(self.fntMorinus)
            else:
                objsdodec.append(artxt[(i - planets.Planets.BODIES_NUM)])
                fntsdodec.append(self.fntDodecText)

        if self.options.lotsvisible[0]:
            lon = chrt.dodecatemoria.lons[(planets.Planets.BODIES_NUM + 2)]
            if self.options.ayanamsha != 0:
                lon += chrt.ayanamsha
                lon = util.normalize(lon)
            lonsdodec.append(lon)
            objsdodec.append(common.common.fortune)
            fntsdodec.append(self.fntMorinus)
        return lonsdodec, objsdodec, fntsdodec

    def drawObjLines(self, objshift, lons, r1, r2):
        clr = (0, 0, 0)
        if not self.bw:
            clr = self.options.clrframe
        w = 2
        if self.chartsize <= GraphChart.MEDIUM_SIZE:
            w = 1
        pen = wx.Pen(clr, w)
        self.bdc.SetPen(pen)
        num = len(lons)
        for i in range(num):
            self.drawPlanetLine(objshift, lons[i], i, r1, r2)

    def drawPlanetLine(self, objshift, lon, iD, r1, r2):
        cx, cy = self.center.Get()
        x1 = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon)) * r1
        y1 = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon)) * r1
        x2 = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - objshift[iD])) * r2
        y2 = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - objshift[iD])) * r2
        self.bdc.DrawLine(int(x1), int(y1), int(x2), int(y2))

    def drawTexts(self, img, names, lons, shift, fnt, radius):
        cx, cy = self.center.Get()
        clr = self.options.clrtexts
        if self.bw:
            clr = (0, 0, 0)
        num = len(names)
        for i in range(num):
            rangle = math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lons[i] - shift[i])
            x = cx + math.cos(rangle) * radius
            y = cy + math.sin(rangle) * radius
            lon = lons[i]
            d, m, s = util.decToDeg(lon)
            d = d % chart.Chart.SIGN_DEG
            txt = names[i]
            txt += ' ' + str(d) + self.deg_symbol + str(m).zfill(2) + "'"
            w, h = fnt.getbbox(txt)[2:]
            x -= h // 2
            y -= h // 2
            angle = int(math.degrees(rangle))
            if angle < 0:
                angle += 360
            angle = 360 - angle
            if angle > 90 and angle < 270:
                if angle > 180:
                    angle -= 180
                else:
                    angle += 180
            imgRot = self.drawRotatedText(txt, fnt, angle, clr)
            img.paste(imgRot, (int(x), int(y)), imgRot)

    def drawTexts2(self, bdc, names, lons, shift, fnt, radius):
        cx, cy = self.center.Get()
        clr = self.options.clrtexts
        if self.bw:
            clr = (0, 0, 0)
        bdc.SetTextForeground(clr)
        wa, ha = fnt.getbbox('a')[2:]
        BASERAD = 0.9
        STEP = 0.02
        num = len(names)
        for i in range(num):
            rangle = math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lons[i] - shift[i])
            angle = int(util.normalize(math.degrees(rangle)))
            rad = radius
            if angle > 90 and angle < 270:
                wt, ht = fnt.getbbox(names[i])[2:]
                chnum = wt // wa + 1
                val = BASERAD + chnum * STEP
                rad = self.maxradius * val
            x = cx + math.cos(rangle) * rad
            y = cy + math.sin(rangle) * rad
            lon = lons[i]
            if self.options.ayanamsha != 0:
                lon -= self.chart.ayanamsha
                lon = util.normalize(lon)
            d, m, s = util.decToDeg(lon)
            d = d % chart.Chart.SIGN_DEG
            txt = names[i]
            txt += ' ' + str(d) + self.deg_symbol + str(m).zfill(2) + "'"
            w, h = fnt.getbbox(txt)[2:]
            x -= h // 2
            y -= h // 2
            if angle < 0:
                angle += 360
            angle = 360 - angle
            if angle > 90 and angle < 270:
                if angle > 180:
                    angle -= 180
                else:
                    angle += 180
            bdc.DrawRotatedText(txt, int(x), int(y), angle)

    def drawAntis(self, chrt, plnts, lof, ascmc, pshift, r):
        cx, cy = self.center.Get()
        clrtxt = self.options.clrtexts
        num = planets.Planets.BODIES_NUM + 3
        if not self.options.lotsvisible[0]:
            num -= 1
        for i in range(num):
            lon = 0.0
            txt = ''
            fnt = self.fntMorinus
            clr = (0, 0, 0)
            if i < planets.Planets.BODIES_NUM:
                lon = plnts[i].lon
                txt = common.common.planets[i]
                if not self.bw:
                    objidx = i
                    if i == planets.Planets.BODIES_NUM - 1:
                        objidx -= 1
                    clr = self.options.clrplanets[objidx]
            elif i == planets.Planets.BODIES_NUM:
                lon = ascmc[0].lon
                txt = mtexts.txtscommon['AntAsc']
                fnt = self.fntAntisText
                if not self.bw:
                    clr = clrtxt
            elif i == planets.Planets.BODIES_NUM + 1:
                lon = ascmc[1].lon
                txt = mtexts.txtscommon['AntMC']
                fnt = self.fntAntisText
                if not self.bw:
                    clr = clrtxt
            elif i == planets.Planets.BODIES_NUM + 2:
                lon = lof.lon
                txt = common.common.fortune
                if not self.bw:
                    clr = self.options.clrLoF
            x = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - pshift[i])) * r
            y = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - pshift[i])) * r
            self.draw.text((x - self.symbolSize // 2, y - self.symbolSize // 2), txt, fill=clr, font=fnt)

    def drawDodecatemoria(self, chrt, plnts, pshift, r):
        cx, cy = self.center.Get()
        clrtxt = self.options.clrtexts
        num = planets.Planets.BODIES_NUM + 3
        if not self.options.lotsvisible[0]:
            num -= 1
        for i in range(num):
            lon = 0.0
            txt = ''
            fnt = self.fntMorinus
            clr = (0, 0, 0)
            lon = plnts[i]
            if i < planets.Planets.BODIES_NUM:
                txt = common.common.planets[i]
                if not self.bw:
                    objidx = i
                    if i == planets.Planets.BODIES_NUM - 1:
                        objidx -= 1
                    clr = self.options.clrplanets[objidx]
            elif i == planets.Planets.BODIES_NUM:
                txt = mtexts.txtscommon['AntAsc']
                fnt = self.fntDodecText
                if not self.bw:
                    clr = clrtxt
            elif i == planets.Planets.BODIES_NUM + 1:
                txt = mtexts.txtscommon['AntMC']
                fnt = self.fntDodecText
                if not self.bw:
                    clr = clrtxt
            elif i == planets.Planets.BODIES_NUM + 2:
                txt = common.common.fortune
                if not self.bw:
                    clr = self.options.clrLoF
            x = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - pshift[i])) * r
            y = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lon - pshift[i])) * r
            self.draw.text((x - self.symbolSize // 2, y - self.symbolSize // 2), txt, fill=clr, font=fnt)

    def getIdOrder(self, lons):
        idorder = []
        order = lons[:]
        length = len(lons)
        for i in range(length):
            idorder.append(i)

        for j in range(length):
            for i in range(length - 1):
                if order[i] > order[(i + 1)]:
                    tmp = order[i]
                    order[i] = order[(i + 1)]
                    order[i + 1] = tmp
                    tmp = idorder[i]
                    idorder[i] = idorder[(i + 1)]
                    idorder[i + 1] = tmp

        return idorder

    def arrangeObjs(self, objs, lons, fnts, idorder, rObj):
        """Arranges Objects so they won't overlap each other"""
        objnum = len(objs)
        objshift = []
        for i in range(objnum):
            objshift.append(0.0)

        for i in range(objnum + 1):
            self.doArrange(objshift, objs, lons, fnts, idorder, rObj)

        shifted = self.doShift(objnum - 1, 0, objs[idorder[(objnum - 1)]], objs[idorder[0]], objshift, lons, fnts, idorder, rObj, True)
        if shifted:
            for i in range(objnum):
                self.doArrange(objshift, objs, lons, fnts, idorder, rObj, True)

        elif lons[idorder[(objnum - 1)]] > 300.0 and lons[idorder[0]] < 60.0:
            lon1 = lons[idorder[(objnum - 1)]] + objshift[idorder[(objnum - 1)]]
            lon2 = lons[idorder[0]] + 360.0 + objshift[idorder[0]]
            if lon1 > lon2:
                dist = lon1 - lon2
                objshift[idorder[0]] += dist
                self.doShift(objnum - 1, 0, objs[idorder[(objnum - 1)]], objs[idorder[0]], objshift, lons, fnts, idorder, rObj, True)
                for i in range(objnum - 1):
                    lon1 = lons[idorder[i]] + objshift[idorder[i]]
                    lon2 = lons[idorder[(i + 1)]] + objshift[idorder[(i + 1)]]
                    if lon1 < 180.0 and lon2 < 180.0:
                        if lon1 > lon2:
                            dist = lon1 - lon2
                            objshift[idorder[(i + 1)]] += dist
                            self.doShift(i, i + 1, objs[idorder[i]], objs[idorder[(i + 1)]], objshift, lons, fnts, idorder, rObj, True)
                        else:
                            break
                    else:
                        break

                for i in range(objnum):
                    self.doArrange(objshift, objs, lons, fnts, idorder, rObj, True)

        return objshift[:]

    def doArrange(self, objshift, objs, lons, fnts, idorder, rObj, forward=False):
        objnum = len(objshift)
        shifted = False
        for i in range(objnum - 1):
            shifted = self.doShift(i, i + 1, objs[idorder[i]], objs[idorder[(i + 1)]], objshift, lons, fnts, idorder, rObj, forward)

        if shifted:
            self.doArrange(objshift, objs, lons, fnts, idorder, rObj, forward)

    def doShift(self, id1, id2, o1, o2, objshift, lons, fnts, idorder, rObj, forward=False):
        cx, cy = self.center.Get()
        shifted = False
        x1 = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lons[idorder[id1]] - objshift[idorder[id1]])) * rObj
        y1 = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lons[idorder[id1]] - objshift[idorder[id1]])) * rObj
        x2 = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lons[idorder[id2]] - objshift[idorder[id2]])) * rObj
        y2 = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lons[idorder[id2]] - objshift[idorder[id2]])) * rObj
        if len(o1) > 3:
            o1 = o1[0:3]
        if len(o2) > 3:
            o2 = o2[0:3]
        w1, h1 = fnts[idorder[id1]].getbbox(o1)[2:]
        w2, h2 = fnts[idorder[id2]].getbbox(o2)[2:]
        while self.overlap(x1, y1, w1, h1, x2, y2, w2, h2):
            if not forward:
                objshift[idorder[id1]] -= 0.1
            objshift[idorder[id2]] += 0.1
            x1 = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lons[idorder[id1]] - objshift[idorder[id1]])) * rObj
            y1 = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lons[idorder[id1]] - objshift[idorder[id1]])) * rObj
            x2 = cx + math.cos(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lons[idorder[id2]] - objshift[idorder[id2]])) * rObj
            y2 = cy + math.sin(math.pi + math.radians(self.chart.houses.ascmc[houses.Houses.ASC] - lons[idorder[id2]] - objshift[idorder[id2]])) * rObj
            if not shifted:
                shifted = True

        return shifted

    def overlap(self, x1, y1, w1, h1, x2, y2, w2, h2):
        xoverlap = x1 <= x2 and x2 <= x1 + w1 or x2 <= x1 and x1 <= x2 + w2
        yoverlap = y1 <= y2 and y2 <= y1 + h1 or y2 <= y1 and y1 <= y2 + h2
        if xoverlap and yoverlap:
            return True
        return False

    def mergefsaspmatrices(self):
        showfss = []
        num = len(self.chart.fsaspmatrix)
        for i in range(num):
            ins = False
            num2 = len(self.chart.fsaspmatrix[i][1])
            for j in range(num2):
                b = self.chart.fsaspmatrix[i][1][j]
                if b <= planets.Planets.MOON or b == planets.Planets.ANODE and self.options.showfixedstarsnodes or b == planets.Planets.DNODE and self.options.showfixedstarsnodes:
                    ins = True
                    break

            if ins:
                showfss.append(self.chart.fsaspmatrix[i][0])

        ASC = self.chart.houses.ascmc[houses.Houses.ASC]
        DESC = util.normalize(self.chart.houses.ascmc[houses.Houses.ASC] + 180.0)
        MC = self.chart.houses.ascmc[houses.Houses.MC]
        IC = util.normalize(self.chart.houses.ascmc[houses.Houses.MC] + 180.0)
        ascmc = [ASC, DESC, MC, IC]
        num = len(self.chart.fsaspmatrixAngles)
        for i in range(num):
            showfss.append(self.chart.fsaspmatrixAngles[i][0])

        if self.options.showfixedstarshcs:
            num = len(self.chart.fsaspmatrixHCs)
            for i in range(num):
                showfss.append(self.chart.fsaspmatrixHCs[i][0])

        if self.options.showfixedstarslof:
            num = len(self.chart.fsaspmatrixLoF)
            for i in range(num):
                showfss.append(self.chart.fsaspmatrixLoF[i])

            s = set(showfss)
            showfss = list(s)
            showfss.sort()
        return showfss[:]