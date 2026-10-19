# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math, wx, planets, fixedstars, fortune, houses, chart, common, commonwnd, Image, ImageDraw, ImageFont, mtexts, util

class FixedStarsAspectsWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(36 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE / 6
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.LINE_NUM = len(self.chart.fixedstars.data)
        self.CELL_WIDTH = 6 * self.FONT_SIZE
        self.SQUARE_SIZE = self.SPACE + self.FONT_SIZE + self.SPACE
        self.COLUMN_NUM = 20
        self.PLANETSOFFS = 4
        self.LOFOFFS = 13
        self.HOUSESOFFS = 14
        self.TITLE_HEIGHT = self.SQUARE_SIZE
        self.TITLE_WIDTH = self.COLUMN_NUM * self.SQUARE_SIZE
        self.SPACE_TITLEY = 0
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * (self.LINE_HEIGHT + self.SPACE)
        self.TABLE_WIDTH = self.CELL_WIDTH + self.COLUMN_NUM * (self.SQUARE_SIZE + self.SPACE)
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = ImageFont.truetype(common.common.symbols, 4 * self.FONT_SIZE / 5)
        self.fntSymbol = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntAspects = ImageFont.truetype(common.common.symbols, 3 * self.FONT_SIZE / 4)
        self.fntText = ImageFont.truetype(common.common.abc, 3 * self.FONT_SIZE / 5)
        self.hidx = (1, 2, 3, 10, 11, 12)
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['FSAsps']

    def drawBkg(self):
        if self.bw:
            self.bkgclr = (255, 255, 255)
        else:
            self.bkgclr = self.options.clrbackground
        self.SetBackgroundColour(self.bkgclr)
        tableclr = self.options.clrtable
        if self.bw:
            tableclr = (0, 0, 0)
        img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.bkgclr)
        draw = ImageDraw.Draw(img)
        BOR = commonwnd.CommonWnd.BORDER
        txtclr = (0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        yy = BOR + self.TITLE_HEIGHT + self.SPACE
        num = len(self.chart.fixedstars.data)
        for i in range(num):
            xx = BOR + self.CELL_WIDTH + self.SPACE
            for j in range(self.COLUMN_NUM):
                self.drawSquare(draw, xx, yy, tableclr)
                xx += self.SQUARE_SIZE + self.SPACE

            yy += self.SQUARE_SIZE + self.SPACE

        x = BOR
        y = BOR + self.TITLE_HEIGHT + self.SPACE
        num = len(self.chart.fixedstars.data)
        for i in range(num):
            self.drawRect(draw, x, y + i * (self.LINE_HEIGHT + self.SPACE), tableclr)
            name = self.chart.fixedstars.data[i][fixedstars.FixedStars.NAME]
            if name == '':
                name = self.chart.fixedstars.data[i][fixedstars.FixedStars.NOMNAME]
            w, h = draw.textsize(name, self.fntText)
            draw.text((x + (self.CELL_WIDTH - w) / 2, y + i * (self.LINE_HEIGHT + self.SPACE) + (self.LINE_HEIGHT - h) / 2), name, fill=txtclr, font=self.fntText)

        x = BOR + self.CELL_WIDTH + self.SPACE
        y = BOR
        txts = ('0', '3', '1', '2')
        for i in range(len(txts)):
            self.drawSquare(draw, x, y, tableclr)
            w, h = draw.textsize(txts[i], self.fntSymbol)
            draw.text((x + (self.SQUARE_SIZE - w) / 2, y + (self.SQUARE_SIZE - h) / 2), txts[i], fill=txtclr, font=self.fntSymbol)
            x += self.SQUARE_SIZE + self.SPACE

        ASC = self.chart.houses.ascmc[houses.Houses.ASC]
        DESC = util.normalize(self.chart.houses.ascmc[houses.Houses.ASC] + 180.0)
        MC = self.chart.houses.ascmc[houses.Houses.MC]
        IC = util.normalize(self.chart.houses.ascmc[houses.Houses.MC] + 180.0)
        ascmc = [ASC, DESC, MC, IC]
        num = len(self.chart.fsaspmatrixAngles)
        for i in range(num):
            num2 = len(self.chart.fsaspmatrixAngles[i][1])
            for j in range(num2):
                txt = common.common.aspects[chart.Chart.CONIUNCTIO]
                w, h = draw.textsize(txt, self.fntAspects)
                clr = self.options.clraspect[chart.Chart.CONIUNCTIO]
                if self.bw:
                    clr = (0, 0, 0)
                xx = BOR + self.CELL_WIDTH + self.SPACE + self.chart.fsaspmatrixAngles[i][1][j] * (self.SQUARE_SIZE + self.SPACE)
                yy = BOR + self.TITLE_HEIGHT + self.SPACE + self.chart.fsaspmatrixAngles[i][0] * (self.SQUARE_SIZE + self.SPACE)
                draw.text((xx + (self.SQUARE_SIZE - w) / 2, yy + (self.SQUARE_SIZE - h) / 2), txt, fill=clr, font=self.fntAspects)

        j = 0
        for i in range(planets.Planets.BODIES_NUM):
            self.drawSquare(draw, x, y, tableclr)
            clr = (0, 0, 0)
            if not self.bw:
                objidx = i
                if i == planets.Planets.BODIES_NUM - 1:
                    objidx -= 1
                clr = self.options.clrplanets[objidx]
            w, h = draw.textsize(common.common.planets[i], self.fntMorinus)
            draw.text((x + (self.SQUARE_SIZE - w) / 2, y + (self.SQUARE_SIZE - h) / 2), common.common.planets[i], fill=clr, font=self.fntMorinus)
            x += self.SQUARE_SIZE + self.SPACE
            j += 1

        num = len(self.chart.fsaspmatrix)
        for i in range(num):
            num2 = len(self.chart.fsaspmatrix[i][1])
            for j in range(num2):
                k = self.chart.fsaspmatrix[i][1][j]
                txt = common.common.aspects[chart.Chart.CONIUNCTIO]
                w, h = draw.textsize(txt, self.fntAspects)
                clr = self.options.clraspect[chart.Chart.CONIUNCTIO]
                if self.bw:
                    clr = (0, 0, 0)
                xx = BOR + self.CELL_WIDTH + self.SPACE + self.PLANETSOFFS * (self.SQUARE_SIZE + self.SPACE) + k * (self.SQUARE_SIZE + self.SPACE)
                yy = BOR + self.TITLE_HEIGHT + self.SPACE + self.chart.fsaspmatrix[i][0] * (self.SQUARE_SIZE + self.SPACE)
                draw.text((xx + (self.SQUARE_SIZE - w) / 2, yy + (self.SQUARE_SIZE - h) / 2), txt, fill=clr, font=self.fntAspects)

        self.drawSquare(draw, x, y, tableclr)
        w, h = draw.textsize(common.common.fortune, self.fntText)
        clr = (0, 0, 0)
        if not self.bw:
            clr = self.options.clrLoF
        draw.text((x + (self.SQUARE_SIZE - w) / 2, y + (self.SQUARE_SIZE - h) / 2), common.common.fortune, clr, font=self.fntMorinus)
        num = len(self.chart.fsaspmatrixLoF)
        for i in range(num):
            txt = common.common.aspects[chart.Chart.CONIUNCTIO]
            w, h = draw.textsize(txt, self.fntAspects)
            clr = self.options.clraspect[chart.Chart.CONIUNCTIO]
            if self.bw:
                clr = (0, 0, 0)
            xx = BOR + self.CELL_WIDTH + self.SPACE + self.LOFOFFS * (self.SQUARE_SIZE + self.SPACE)
            yy = BOR + self.TITLE_HEIGHT + self.SPACE + self.chart.fsaspmatrixLoF[i] * (self.SQUARE_SIZE + self.SPACE)
            draw.text((xx + (self.SQUARE_SIZE - w) / 2, yy + (self.SQUARE_SIZE - h) / 2), txt, fill=clr, font=self.fntAspects)

        x += self.SQUARE_SIZE + self.SPACE
        for i in range(len(self.hidx)):
            self.drawSquare(draw, x + (self.SQUARE_SIZE + self.SPACE) * i, y, tableclr)
            w, h = draw.textsize(common.common.housenames2[(self.hidx[i] - 1)], self.fntText)
            draw.text((x + (self.SQUARE_SIZE + self.SPACE) * i + (self.SQUARE_SIZE - w) / 2, y + (self.SQUARE_SIZE - h) / 2), common.common.housenames2[(self.hidx[i] - 1)], fill=(0,
                                                                                                                                                                                   0,
                                                                                                                                                                                   0), font=self.fntText)

        aroffs = (0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5)
        isopp = (False, False, False, True, True, True, True, True, True, False, False, False)
        num = len(self.chart.fsaspmatrixHCs)
        for i in range(num):
            num2 = len(self.chart.fsaspmatrixHCs[i][1])
            for j in range(num2):
                k = self.chart.fsaspmatrixHCs[i][1][j]
                asp = chart.Chart.CONIUNCTIO
                if isopp[k]:
                    asp = chart.Chart.OPPOSITIO
                txt = common.common.aspects[asp]
                w, h = draw.textsize(txt, self.fntAspects)
                clr = self.options.clraspect[asp]
                if self.bw:
                    clr = (0, 0, 0)
                xx = BOR + self.CELL_WIDTH + self.SPACE + self.HOUSESOFFS * (self.SQUARE_SIZE + self.SPACE) + aroffs[k] * (self.SQUARE_SIZE + self.SPACE)
                yy = BOR + self.TITLE_HEIGHT + self.SPACE + self.chart.fsaspmatrixHCs[i][0] * (self.SQUARE_SIZE + self.SPACE)
                draw.text((xx + (self.SQUARE_SIZE - w) / 2, yy + (self.SQUARE_SIZE - h) / 2), txt, fill=clr, font=self.fntAspects)

        wxImg = wx.EmptyImage(img.size[0], img.size[1])
        wxImg.SetData(img.tostring())
        self.buffer = wx.BitmapFromImage(wxImg)

    def drawSquare(self, draw, x, y, tableclr):
        draw.line((x, y, x + self.SQUARE_SIZE, y), fill=tableclr)
        draw.line((x, y, x, y + self.SQUARE_SIZE), fill=tableclr)
        draw.line((x, y + self.SQUARE_SIZE, x + self.SQUARE_SIZE, y + self.SQUARE_SIZE), fill=tableclr)
        draw.line((x + self.SQUARE_SIZE, y + self.SQUARE_SIZE, x + self.SQUARE_SIZE, y), fill=tableclr)

    def drawRect(self, draw, x, y, tableclr):
        draw.line((x, y, x + self.CELL_WIDTH, y), fill=tableclr)
        draw.line((x, y, x, y + self.SQUARE_SIZE), fill=tableclr)
        draw.line((x, y + self.SQUARE_SIZE, x + self.CELL_WIDTH, y + self.SQUARE_SIZE), fill=tableclr)
        draw.line((x + self.CELL_WIDTH, y + self.SQUARE_SIZE, x + self.CELL_WIDTH, y), fill=tableclr)