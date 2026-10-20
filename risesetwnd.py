# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import os
import astrology
import planets
import riseset
import rtofsigns
import chart
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import util
import mtexts

class RiseSetWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE // 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.LINE_NUM = planets.Planets.PLANETS_NUM
        self.COLUMN_NUM = 4
        self.SMALL_CELL_WIDTH = 3 * self.FONT_SIZE
        self.CELL_WIDTH = 6 * self.FONT_SIZE
        self.TITLE_HEIGHT = self.LINE_HEIGHT
        self.TITLE_WIDTH = self.COLUMN_NUM * self.CELL_WIDTH
        self.SPACE_TITLEY = 0
        self.TABLE_WIDTH = self.SMALL_CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT
        self.RTOFSIGNS = self.TABLE_HEIGHT + self.LINE_HEIGHT
        self.TABLE_HEIGHT2 = 6 * self.LINE_HEIGHT
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + self.LINE_NUM + self.TABLE_HEIGHT2 + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = util.truetype(common.common.symbols, self.FONT_SIZE)
        self.signs = common.common.signs
        self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Rise']

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
        txt = (mtexts.txtsriseset['Rise'], mtexts.txtsriseset['MC'], mtexts.txtsriseset['Set'], mtexts.txtsriseset['IC'])
        for i in range(len(txt)):
            w, h = draw.textbbox((0, 0), txt[i], self.fntText)[2:]
            draw.text((BOR + self.SMALL_CELL_WIDTH + self.CELL_WIDTH * i + (self.CELL_WIDTH - w) // 2, BOR + (self.TITLE_HEIGHT - h) // 2), txt[i], fill=txtclr, font=self.fntText)

        x = BOR
        y = BOR + self.TITLE_HEIGHT + self.SPACE_TITLEY
        draw.line((x, y, x + self.TABLE_WIDTH, y), fill=tableclr)
        for i in range(planets.Planets.PLANETS_NUM):
            self.drawline(draw, x, y + i * self.LINE_HEIGHT, tableclr, i)

        x = BOR
        y = self.RTOFSIGNS
        for i in range(chart.Chart.SIGN_NUM // 2):
            txt = self.signs[i]
            w, h = draw.textbbox((0, 0), txt, self.fntMorinus)[2:]
            draw.text((x + (self.SMALL_CELL_WIDTH - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntMorinus)
            txt = util.floatstr(self.chart.risetimeofsigns.riseofsigns[i])
            w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
            draw.text((x + 2 * self.SMALL_CELL_WIDTH + (self.SMALL_CELL_WIDTH - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
            txt = self.signs[(chart.Chart.SIGN_NUM - i - 1)]
            w, h = draw.textbbox((0, 0), txt, self.fntMorinus)[2:]
            draw.text((x + 2 * self.SMALL_CELL_WIDTH + self.CELL_WIDTH + (self.SMALL_CELL_WIDTH - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntMorinus)
            y += self.LINE_HEIGHT

        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)

    def drawline(self, draw, x, y, clr, idx):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
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
                # in the chart's own time (the calculation gives UT)
                h, m, s = util.decToDeg((self.chart.riseset.times[idx][(i - 2)] + self.chart.time.localoffset() * 24.0) % 24.0)
                txt = str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=tclr, font=self.fntText)
            summa += offs[i]