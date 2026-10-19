# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import os
import planets
import houses
import chart
import fortune
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import util
import mtexts

class ProfectionsMonWnd(commonwnd.CommonWnd):
    AGE, DATE, ASC, MC, SUN, MOON, FORTUNE, SATURN, JUPITER, MARS, VENUS, MERCURY = list(range(0, 12))

    def __init__(self, parent, age, pchrts, dates, options, mainfr, mainsigs, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, pchrts[0][0], options, id, size)
        self.age = age
        self.pcharts = pchrts
        self.dates = dates
        self.mainfr = mainfr
        self.mainsigs = mainsigs
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE // 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.LINE_NUM = len(dates)
        if self.mainsigs:
            self.COLUMN_NUM = 7
        else:
            self.COLUMN_NUM = 12
        self.CELL_WIDTH = 3 * self.FONT_SIZE
        self.BIG_CELL_WIDTH = 7 * self.FONT_SIZE
        self.TITLE_HEIGHT = self.LINE_HEIGHT
        self.TITLE_WIDTH = self.CELL_WIDTH + (self.COLUMN_NUM - 1) * self.BIG_CELL_WIDTH
        self.SPACE_TITLEY = 0
        self.TABLE_WIDTH = (self.COLUMN_NUM - 1) * self.BIG_CELL_WIDTH + self.CELL_WIDTH
        val = 0
        if len(self.dates) == 12:
            val = self.LINE_HEIGHT
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT + val
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = util.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
        self.signs = common.common.signs
        self.deg_symbol = '\xb0'
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsprofmonwnd['Pro']

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
        draw.rectangle(((BOR, BOR), (BOR + self.TITLE_WIDTH, BOR + self.TITLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
        txt = (mtexts.txtsprofwnd['Age'], mtexts.txtsprofwnd['Date'], mtexts.txtsprofwnd['Asc'], mtexts.txtsprofwnd['MC'], common.common.planets[planets.Planets.SUN], common.common.planets[planets.Planets.MOON], common.common.fortune, common.common.planets[planets.Planets.SATURN], common.common.planets[planets.Planets.JUPITER], common.common.planets[planets.Planets.MARS], common.common.planets[planets.Planets.VENUS], common.common.planets[planets.Planets.MERCURY])
        arclrs = (txtclr, txtclr, txtclr, txtclr, self.options.clrplanets[planets.Planets.SUN], self.options.clrplanets[planets.Planets.MOON], self.options.clrLoF, self.options.clrplanets[planets.Planets.SATURN], self.options.clrplanets[planets.Planets.JUPITER], self.options.clrplanets[planets.Planets.MARS], self.options.clrplanets[planets.Planets.VENUS], self.options.clrplanets[planets.Planets.MERCURY])
        cols = (
         self.CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH)
        offs = 0
        for i in range(self.COLUMN_NUM):
            fnt = self.fntText
            if i > ProfectionsMonWnd.MC:
                fnt = self.fntMorinus
            tclr = (0, 0, 0)
            if not self.bw:
                tclr = arclrs[i]
            w, h = draw.textbbox((0, 0), txt[i], fnt)[2:]
            clr = txtclr
            if i > ProfectionsMonWnd.MC:
                clr = tclr
            draw.text((BOR + offs + (cols[i] - w) // 2, BOR + (self.TITLE_HEIGHT - h) // 2), txt[i], fill=clr, font=fnt)
            offs += cols[i]

        x = BOR
        y = BOR + self.TITLE_HEIGHT + self.SPACE_TITLEY
        txtclr = (0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        txt = str(self.age)
        w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
        draw.text((x + (self.CELL_WIDTH - w) // 2, y + (self.TABLE_HEIGHT - h) // 2 - self.LINE_HEIGHT // 2), txt, fill=txtclr, font=self.fntText)
        agestart = agecont = self.age % 12
        for i in range(self.LINE_NUM):
            if i < len(self.pcharts):
                self.drawline(draw, x, y + i * self.LINE_HEIGHT, tableclr, self.pcharts[agecont], self.dates, i)
            else:
                self.drawline(draw, x, y + i * self.LINE_HEIGHT, tableclr, self.pcharts[agestart], self.dates, i)
            agecont += 1
            if agecont > 11:
                agecont = 0

        y = BOR + self.TABLE_HEIGHT
        if len(self.dates) == 12:
            draw.line((x, y, x + self.TABLE_WIDTH, y), fill=tableclr)
            offs = (self.CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH)
            draw.line((x, y - self.LINE_HEIGHT, x, y), fill=tableclr)
            summa = 0
            for i in range(self.COLUMN_NUM):
                draw.line((x + summa + offs[i], y - self.LINE_HEIGHT, x + summa + offs[i], y), fill=tableclr)
                summa += offs[i]

        else:
            draw.line((x, y, x + self.TABLE_WIDTH, y), fill=tableclr)
        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)

    def drawline(self, draw, x, y, clr, pcharts, dates, idx):
        val = self.CELL_WIDTH
        draw.line((x + val, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         self.CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH)
        BOR = commonwnd.CommonWnd.BORDER
        draw.line((x, y, x, y + self.LINE_HEIGHT), fill=clr)
        summa = 0
        for i in range(self.COLUMN_NUM):
            draw.line((x + summa + offs[i], y, x + summa + offs[i], y + self.LINE_HEIGHT), fill=clr)
            tclr = (0, 0, 0)
            if not self.bw:
                txtclr = self.options.clrtexts
            if i == ProfectionsMonWnd.DATE:
                txt = str(dates[idx][0]) + '.' + str(dates[idx][1]).zfill(2) + '.' + str(dates[idx][2]).zfill(2) + '.'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=tclr, font=self.fntText)
            elif i != ProfectionsMonWnd.AGE:
                if i == ProfectionsMonWnd.ASC:
                    lon = pcharts[0].houses.ascmc[houses.Houses.ASC]
                if i == ProfectionsMonWnd.MC:
                    lon = pcharts[0].houses.ascmc[houses.Houses.MC]
                if i == ProfectionsMonWnd.SUN:
                    lon = pcharts[0].planets.planets[planets.Planets.SUN].data[planets.Planet.LON]
                if i == ProfectionsMonWnd.MOON:
                    lon = pcharts[0].planets.planets[planets.Planets.MOON].data[planets.Planet.LON]
                if i == ProfectionsMonWnd.FORTUNE:
                    lon = pcharts[0].fortune.fortune[fortune.Fortune.LON]
                if i >= ProfectionsMonWnd.SATURN:
                    lon = pcharts[0].planets.planets[(i - 5)].data[planets.Planet.LON]
                if self.options.ayanamsha != 0:
                    lon -= self.chart.ayanamsha
                    lon = util.normalize(lon)
                d, m, s = util.decToDeg(lon)
                sign = d // chart.Chart.SIGN_DEG
                pos = d % chart.Chart.SIGN_DEG
                wsp, hsp = draw.textbbox((0, 0), ' ', self.fntText)[2:]
                wsg, hsg = draw.textbbox((0, 0), self.signs[sign], self.fntMorinus)[2:]
                txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - (w + wsp + wsg)) // 2
                draw.text((x + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=tclr, font=self.fntText)
                draw.text((x + summa + offset + w + wsp, y + (self.LINE_HEIGHT - hsg) // 2), self.signs[sign], fill=tclr, font=self.fntMorinus)
            summa += offs[i]