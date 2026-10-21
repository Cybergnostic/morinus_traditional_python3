# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import os
import wx
import astrology
import planets
import chart
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import util
import mtexts

class MunPosWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE // 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.LINE_NUM = planets.Planets.BODIES_NUM - 1
        self.COLUMN_NUM = 1
        self.SPACE_LOTSY = self.LINE_HEIGHT
        self.LINE_NUM_LOTS = 1
        self.COLUMN_NUM_LOTS = 4
        self.SMALL_CELL_WIDTH = 3 * self.FONT_SIZE
        self.CELL_WIDTH = 8 * self.FONT_SIZE
        self.TITLE_HEIGHT = self.LINE_HEIGHT
        self.TITLE_WIDTH = self.COLUMN_NUM * self.CELL_WIDTH
        self.TITLE_WIDTH_LOTS = (self.COLUMN_NUM_LOTS + 1) * self.CELL_WIDTH
        self.SPACE_TITLEY = 0
        self.TABLE_WIDTH = self.SMALL_CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH
        self.TABLE_WIDTH_LOTS = self.TABLE_WIDTH
        self.TABLE_WIDTH_LOTS = self.CELL_WIDTH + self.COLUMN_NUM_LOTS * self.CELL_WIDTH
        self.TABLE_HEIGHT_LOTS = self.SPACE_LOTSY + self.LINE_NUM_LOTS * self.LINE_HEIGHT
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT + self.TABLE_HEIGHT_LOTS
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH_LOTS + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = util.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
        self.signs = common.common.signs
        self.deg_symbol = '\xb0'
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Mun']

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
        draw.rectangle(((BOR + self.SMALL_CELL_WIDTH, BOR), (BOR + self.SMALL_CELL_WIDTH + self.TITLE_WIDTH, BOR + self.TITLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
        txt = mtexts.txtsmunpos['HousePercent']
        w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
        draw.text((BOR + self.SMALL_CELL_WIDTH + (self.CELL_WIDTH - w) // 2, BOR + (self.TITLE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
        x = BOR
        y = BOR + self.TITLE_HEIGHT + self.SPACE_TITLEY
        draw.line((x, y, x + self.TABLE_WIDTH, y), fill=tableclr)
        for i in range(planets.Planets.PLANETS_NUM + 1):
            self.drawline(draw, x, y + i * self.LINE_HEIGHT, tableclr, i)

        x = BOR
        y = BOR + self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT + self.SPACE_LOTSY
        draw.rectangle(((x, y), (x + self.TITLE_WIDTH_LOTS, y + self.LINE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
        self.drawlinelof(draw, x, y, mtexts.txtsmunpos['MLoF'], self.chart.munfortune.mfortune, tableclr, 0)
        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)

    def drawline(self, draw, x, y, clr, idx):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        BOR = commonwnd.CommonWnd.BORDER
        summa = 0
        for i in range(self.COLUMN_NUM + 1 + 1):
            draw.line((x + summa + offs[i], y, x + summa + offs[i], y + self.LINE_HEIGHT), fill=clr)
            tclr = (0, 0, 0)
            if not self.bw:
                tclr = self.options.clrplanets[idx]
            if i == 1:
                txt = common.common.planets[idx]
                w, h = draw.textbbox((0, 0), txt, self.fntMorinus)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=tclr, font=self.fntMorinus)
            elif i != 0:
                # Morinus 6 passed the MC instead of the ARMC and the index instead of the letter of the house system
                ret = self.chart.houses.mundanePosition(self.chart.planets.planets[idx].data[planets.Planet.LON], self.chart.planets.planets[idx].data[planets.Planet.LAT], self.chart.place.lat)
                txt = util.floatstr(ret)
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=tclr, font=self.fntText)
            summa += offs[i]

    def drawlinelof(self, draw, x, y, name, data, clr, idx):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH_LOTS, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        BOR = commonwnd.CommonWnd.BORDER
        summa = 0
        txtclr = (0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        for i in range(self.COLUMN_NUM_LOTS + 1 + 1):
            draw.line((x + summa + offs[i], y, x + summa + offs[i], y + self.LINE_HEIGHT), fill=clr)
            d, m, s = (0, 0, 0)
            if i > 1:
                d, m, s = util.decToDeg(data[(i - 2)])
            if i == 1:
                w, h = draw.textbbox((0, 0), name, self.fntText)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), name, fill=txtclr, font=self.fntText)
            elif i == 2:
                if self.options.ayanamsha != 0:
                    lona = data[(i - 2)] - self.chart.ayanamsha
                    lona = util.normalize(lona)
                    d, m, s = util.decToDeg(lona)
                sign = d // chart.Chart.SIGN_DEG
                pos = d % chart.Chart.SIGN_DEG
                wsp, hsp = draw.textbbox((0, 0), ' ', self.fntText)[2:]
                txtsign = self.signs[sign]
                wsg, hsg = draw.textbbox((0, 0), txtsign, self.fntMorinus)[2:]
                txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - (w + wsp + wsg)) // 2
                draw.text((x + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
                draw.text((x + summa + offset + w + wsp, y + (self.LINE_HEIGHT - h) // 2), txtsign, fill=txtclr, font=self.fntMorinus)
            elif i == 3 or i == 5:
                sign = ''
                if data[(i - 2)] < 0.0:
                    sign = '-'
                txt = sign + str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
            elif i == 4:
                txt = str(d) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                if self.options.intime:
                    d, m, s = util.decToDeg(data[(i - 2)] / 15.0)
                    txt = str(d).rjust(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
            summa += offs[i]