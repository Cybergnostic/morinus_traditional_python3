# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math
import wx
import planets
import houses
import chart
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import mtexts
import util

class AspectsWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(2 * 18 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE // 4
        self.XOFFSET = self.SPACE
        self.YOFFSET = self.SPACE // 2
        self.SQUARE_SIZE = self.SPACE + self.FONT_SIZE + self.SPACE
        self.LINE_NUM = 10
        self.HOUSESOFFS = 11
        self.COLUMN_NUM = 17
        self.TABLE_HEIGHT = self.LINE_NUM * (self.SQUARE_SIZE + self.SPACE)
        self.TABLE_WIDTH = self.COLUMN_NUM * (self.SQUARE_SIZE + self.SPACE)
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = util.truetype(common.common.symbols, 4 * self.FONT_SIZE // 5)
        self.fntSymbol = util.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntAspects = util.truetype(common.common.symbols, self.FONT_SIZE // 2)
        self.fntText = util.truetype(common.common.abc, 2 * self.FONT_SIZE // 3)
        self.fntText2 = util.truetype(common.common.abc, self.FONT_SIZE // 3)
        self.fntText3 = util.truetype(common.common.abc, self.FONT_SIZE // 2)
        self.hidx = (1, 2, 3, 10, 11, 12)
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Asps']

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
        x = BOR
        for i in range(planets.Planets.BODIES_NUM):
            y = BOR + (i + 1) * (self.SQUARE_SIZE + self.SPACE)
            self.drawSquare(draw, x, y, tableclr)
            clr = (0, 0, 0)
            if not self.bw:
                clridx = i
                if i > planets.Planets.PLANETS_NUM:
                    clridx -= 1
                clr = self.options.clrplanets[clridx]
            w, h = draw.textbbox((0, 0), common.common.planets[i], self.fntMorinus)[2:]
            draw.text((x + (self.SQUARE_SIZE - w) // 2, y + (self.SQUARE_SIZE - h) // 2), common.common.planets[i], fill=clr, font=self.fntMorinus)

        txt = ('0', '1')
        y = BOR
        for i in range(len(txt)):
            x = BOR + (self.SQUARE_SIZE + self.SPACE) * (i + 1)
            self.drawSquare(draw, x, y, tableclr)
            w, h = draw.textbbox((0, 0), txt[i], self.fntSymbol)[2:]
            draw.text((x + (self.SQUARE_SIZE - w) // 2, y + (self.SQUARE_SIZE - h) // 2), txt[i], fill=txtclr, font=self.fntSymbol)

        arAscMC = (self.chart.houses.ascmc[houses.Houses.ASC], self.chart.houses.ascmc[houses.Houses.MC])
        for i in range(len(self.chart.aspmatrixAscMC)):
            for j in range(len(self.chart.aspmatrixAscMC[i])):
                x = BOR + (i + 1) * (self.SPACE + self.SQUARE_SIZE)
                y = BOR + (j + 1) * (self.SQUARE_SIZE + self.SPACE)
                self.drawSquare(draw, x, y, tableclr)
                lon1 = arAscMC[i]
                lon2 = self.chart.planets.planets[j].data[planets.Planet.LON]
                if self.chart.aspmatrixAscMC[i][j].typ != chart.Chart.NONE:
                    if self.chart.aspmatrixAscMC[i][j].exact:
                        draw.rectangle(((x + self.XOFFSET // 2, y + self.XOFFSET // 2), (x + self.SQUARE_SIZE - self.XOFFSET // 2, y + self.SQUARE_SIZE - self.XOFFSET // 2 - 1)), fill=self.bkgclr, outline=tableclr)
                    if self.chart.aspmatrixAscMC[i][j].appl:
                        draw.polygon(((x, y), (x + self.SPACE, y), (x, y + self.SPACE)), fill=tableclr, outline=tableclr)
                    txt = common.common.aspects[self.chart.aspmatrixAscMC[i][j].typ]
                    clr = self.options.clraspect[self.chart.aspmatrixAscMC[i][j].typ]
                    if self.bw:
                        clr = (0, 0, 0)
                    draw.text((BOR + (i + 1) * (self.SPACE + self.SQUARE_SIZE) + self.XOFFSET, BOR + (self.SQUARE_SIZE + self.SPACE) * (j + 1) + self.YOFFSET, self.SQUARE_SIZE), txt, fill=clr, font=self.fntAspects)
                showasp = self.chart.aspmatrixAscMC[i][j].parallel != chart.Chart.NONE
                if showasp:
                    pclr = (0, 0, 0)
                    if not self.bw:
                        pclr = self.options.clrtexts
                    txt = 'X'
                    if self.chart.aspmatrixAscMC[i][j].parallel == chart.Chart.CONTRAPARALLEL:
                        txt = 'Y'
                    w, h = draw.textbbox((0, 0), txt, self.fntAspects)[2:]
                    draw.text((BOR + (i + 1) * (self.SPACE + self.SQUARE_SIZE) + self.SQUARE_SIZE - w - self.SPACE, BOR + (self.SQUARE_SIZE + self.SPACE) * (j + 1) + self.YOFFSET, self.SQUARE_SIZE), txt, fill=pclr, font=self.fntAspects)
                txt = util.floatstr(self.chart.aspmatrixAscMC[i][j].dif)
                if showasp:
                    txt = str(self.chart.aspmatrixAscMC[i][j].aspdif)
                t = txt.partition('.')
                txt = t[0] + t[1] + t[2][0]
                fnt = self.fntText2
                clr = (0, 0, 0)
                if showasp:
                    fnt = self.fntText3
                    if not self.bw:
                        clr = self.options.clraspect[self.chart.aspmatrixAscMC[i][j].typ]
                elif not self.bw:
                    clr = txtclr
                w, h = draw.textbbox((0, 0), txt, fnt)[2:]
                draw.text((BOR + (i + 1) * (self.SPACE + self.SQUARE_SIZE) + (self.SQUARE_SIZE - w) // 2, BOR + (self.SQUARE_SIZE + self.SPACE) * (j + 1) + self.SQUARE_SIZE - h - self.YOFFSET, self.SQUARE_SIZE), txt, fill=clr, font=fnt)

        x = BOR + 3 * self.SQUARE_SIZE + 3 * self.SPACE
        for i in range(planets.Planets.PLANETS_NUM):
            self.drawSquare(draw, x + (self.SQUARE_SIZE + self.SPACE) * i, BOR + (self.SQUARE_SIZE + self.SPACE) * (i + 1), tableclr)
            clr = (0, 0, 0)
            if not self.bw:
                clr = self.options.clrplanets[i]
            w, h = draw.textbbox((0, 0), common.common.planets[i], self.fntMorinus)[2:]
            draw.text((x + (self.SQUARE_SIZE + self.SPACE) * i + (self.SQUARE_SIZE - w) // 2, BOR + (self.SQUARE_SIZE + self.SPACE) * (i + 1) + (self.SQUARE_SIZE - h) // 2), common.common.planets[i], fill=clr, font=self.fntMorinus)

        x = BOR + (self.SQUARE_SIZE + self.SPACE) * 3
        y = BOR + (self.SQUARE_SIZE + self.SPACE)
        ii = 0
        for i in range(planets.Planets.BODIES_NUM - 1):
            jj = 0
            for j in range(planets.Planets.BODIES_NUM):
                if jj > ii:
                    k = x + (self.SQUARE_SIZE + self.SPACE) * ii
                    l = y + (self.SQUARE_SIZE + self.SPACE) * jj
                    if j == planets.Planets.BODIES_NUM - 1 and i == planets.Planets.PLANETS_NUM:
                        continue
                    self.drawSquare(draw, k, l, tableclr)
                    lon1 = self.chart.planets.planets[i].data[planets.Planet.LON]
                    lon2 = self.chart.planets.planets[j].data[planets.Planet.LON]
                    showasp = self.chart.aspmatrix[j][i].typ != chart.Chart.NONE
                    if showasp:
                        if self.chart.aspmatrix[j][i].exact:
                            draw.rectangle(((k + self.XOFFSET // 2, l + self.XOFFSET // 2), (k + self.SQUARE_SIZE - self.XOFFSET // 2, l + self.SQUARE_SIZE - self.XOFFSET // 2 - 1)), fill=self.bkgclr, outline=tableclr)
                        if self.chart.aspmatrix[j][i].appl:
                            draw.polygon(((k, l), (k + self.SPACE, l), (k, l + self.SPACE)), fill=tableclr, outline=tableclr)
                        txt = common.common.aspects[self.chart.aspmatrix[j][i].typ]
                        clr = self.options.clraspect[self.chart.aspmatrix[j][i].typ]
                        if self.bw:
                            clr = (0, 0, 0)
                        draw.text((x + (self.SQUARE_SIZE + self.SPACE) * ii + self.XOFFSET, y + (self.SQUARE_SIZE + self.SPACE) * jj + self.YOFFSET), txt, fill=clr, font=self.fntAspects)
                    if self.chart.aspmatrix[j][i].parallel != chart.Chart.NONE:
                        pclr = (0, 0, 0)
                        if not self.bw:
                            pclr = self.options.clrtexts
                        txt = 'X'
                        if self.chart.aspmatrix[j][i].parallel == chart.Chart.CONTRAPARALLEL:
                            txt = 'Y'
                        w, h = draw.textbbox((0, 0), txt, self.fntAspects)[2:]
                        draw.text((x + (self.SQUARE_SIZE + self.SPACE) * ii + self.SQUARE_SIZE - w - self.SPACE, y + (self.SQUARE_SIZE + self.SPACE) * jj + self.YOFFSET), txt, fill=pclr, font=self.fntAspects)
                    txt = util.floatstr(self.chart.aspmatrix[j][i].dif)
                    if showasp:
                        txt = util.floatstr(self.chart.aspmatrix[j][i].aspdif)
                    t = txt.partition('.')
                    txt = t[0] + t[1] + t[2][0]
                    fnt = self.fntText2
                    clr = (0, 0, 0)
                    if showasp:
                        fnt = self.fntText3
                        if not self.bw:
                            clr = self.options.clraspect[self.chart.aspmatrix[j][i].typ]
                    elif not self.bw:
                        clr = txtclr
                    w, h = draw.textbbox((0, 0), txt, fnt)[2:]
                    draw.text((x + (self.SQUARE_SIZE + self.SPACE) * ii + (self.SQUARE_SIZE - w) // 2, y + (self.SQUARE_SIZE + self.SPACE) * jj + self.SQUARE_SIZE - h - self.YOFFSET), txt, fill=clr, font=fnt)
                jj += 1

            ii += 1

        hidx = (1, 2, 3, 10, 11, 12)
        x = BOR + self.HOUSESOFFS * self.SQUARE_SIZE + self.HOUSESOFFS * self.SPACE
        for i in range(len(hidx)):
            self.drawSquare(draw, x + (self.SQUARE_SIZE + self.SPACE) * i, BOR, tableclr)
            w, h = draw.textbbox((0, 0), common.common.housenames2[(hidx[i] - 1)], self.fntText)[2:]
            draw.text((x + (self.SQUARE_SIZE + self.SPACE) * i + (self.SQUARE_SIZE - w) // 2, BOR + (self.SQUARE_SIZE - h) // 2), common.common.housenames2[(hidx[i] - 1)], fill=(0,
                                                                                                                                                                                0,
                                                                                                                                                                                0), font=self.fntText)

        x = BOR + self.HOUSESOFFS * (self.SQUARE_SIZE + self.SPACE)
        y = BOR + (self.SQUARE_SIZE + self.SPACE)
        for i in range(len(self.chart.aspmatrixH)):
            kk = 0
            for j in range(len(self.chart.aspmatrixH[i])):
                k = x + (self.SQUARE_SIZE + self.SPACE) * i
                l = y + (self.SQUARE_SIZE + self.SPACE) * kk
                self.drawSquare(draw, k, l, tableclr)
                lon1 = self.chart.houses.cusps[self.hidx[i]]
                lon2 = self.chart.planets.planets[j].data[planets.Planet.LON]
                showasp = self.chart.aspmatrixH[i][j].typ != chart.Chart.NONE
                if showasp:
                    if self.chart.aspmatrixH[i][j].exact:
                        draw.rectangle(((k + self.XOFFSET // 2, l + self.XOFFSET // 2), (k + self.SQUARE_SIZE - self.XOFFSET // 2, l + self.SQUARE_SIZE - self.XOFFSET // 2 - 1)), fill=self.bkgclr, outline=tableclr)
                    if self.chart.aspmatrixH[i][j].appl:
                        draw.polygon(((k, l), (k + self.SPACE, l), (k, l + self.SPACE)), fill=tableclr, outline=tableclr)
                    txt = common.common.aspects[self.chart.aspmatrixH[i][j].typ]
                    clr = self.options.clraspect[self.chart.aspmatrixH[i][j].typ]
                    if self.bw:
                        clr = (0, 0, 0)
                    draw.text((x + i * (self.SPACE + self.SQUARE_SIZE) + self.XOFFSET, BOR + (self.SQUARE_SIZE + self.SPACE) * (kk + 1) + self.YOFFSET, self.SQUARE_SIZE), txt, fill=clr, font=self.fntAspects)
                if self.chart.aspmatrixH[i][j].parallel != chart.Chart.NONE:
                    pclr = (0, 0, 0)
                    if not self.bw:
                        pclr = self.options.clrtexts
                    txt = 'X'
                    if self.chart.aspmatrixH[i][j].parallel == chart.Chart.CONTRAPARALLEL:
                        txt = 'Y'
                    w, h = draw.textbbox((0, 0), txt, self.fntAspects)[2:]
                    draw.text((x + (self.SQUARE_SIZE + self.SPACE) * i + self.SQUARE_SIZE - w - self.SPACE, y + (self.SQUARE_SIZE + self.SPACE) * kk + self.YOFFSET), txt, fill=pclr, font=self.fntAspects)
                txt = util.floatstr(self.chart.aspmatrixH[i][j].dif)
                if showasp:
                    txt = util.floatstr(self.chart.aspmatrixH[i][j].aspdif)
                t = txt.partition('.')
                txt = t[0] + t[1] + t[2][0]
                fnt = self.fntText2
                clr = (0, 0, 0)
                if showasp:
                    fnt = self.fntText3
                    if not self.bw:
                        clr = self.options.clraspect[self.chart.aspmatrixH[i][j].typ]
                elif not self.bw:
                    clr = txtclr
                w, h = draw.textbbox((0, 0), txt, fnt)[2:]
                draw.text((x + (self.SQUARE_SIZE + self.SPACE) * i + (self.SQUARE_SIZE - w) // 2, y + (self.SQUARE_SIZE + self.SPACE) * kk + self.SQUARE_SIZE - h - self.YOFFSET), txt, fill=clr, font=fnt)
                kk += 1

        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)

    def drawSquare(self, draw, x, y, tableclr):
        draw.line((x, y, x + self.SQUARE_SIZE, y), fill=tableclr)
        draw.line((x, y, x, y + self.SQUARE_SIZE), fill=tableclr)
        draw.line((x, y + self.SQUARE_SIZE, x + self.SQUARE_SIZE, y + self.SQUARE_SIZE), fill=tableclr)
        draw.line((x + self.SQUARE_SIZE, y + self.SQUARE_SIZE, x + self.SQUARE_SIZE, y), fill=tableclr)