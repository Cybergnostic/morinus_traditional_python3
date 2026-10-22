# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import i18n
from datetime import datetime, timedelta
import wx
import tablepresentation
import planets
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import mtexts
import firdaria
import util

class FirdariaWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, opts, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, opts, id, size)
        self.parent = parent
        self.fird = chrt.firdaria
        self.options = opts
        self.mainfr = mainfr
        self.bw = self.options.bw
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.COLUMN_NUM = 1
        self.SPACE = self.FONT_SIZE // 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.SMALL_CELL_WIDTH = 3 * self.FONT_SIZE
        self.CELL_WIDTH = 12 * self.FONT_SIZE
        self.BIG_CELL_WIDTH = 20 * self.FONT_SIZE
        self.TITLE_HEIGHT = self.LINE_HEIGHT
        self.TITLE_WIDTH = self.SMALL_CELL_WIDTH + self.BIG_CELL_WIDTH
        self.SPACE_TITLEY = 0
        self.EXTRA_PERIODS = 3
        self.LINE_NUM = (planets.Planets.PLANETS_NUM + self.EXTRA_PERIODS) * (planets.Planets.PLANETS_NUM + 1) + 2
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT
        self.TABLE_WIDTH = self.SMALL_CELL_WIDTH + self.BIG_CELL_WIDTH
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = util.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntSymbol = util.truetype(common.common.symbols, 3 * self.FONT_SIZE // 2)
        self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Fir']

    def drawBkg(self):
        if self.bw:
            self.bkgclr = (255, 255, 255)
        else:
            self.bkgclr = self.options.clrbackground
        self.SetBackgroundColour(self.bkgclr)
        tableclr = self.options.clrtable
        if self.bw:
            tableclr = (0, 0, 0)
        img = Image.new('RGB', i18n.tr((self.WIDTH, self.HEIGHT)), i18n.tr(self.bkgclr))
        draw = ImageDraw.Draw(img)
        BOR = commonwnd.CommonWnd.BORDER
        draw.rectangle(((BOR, BOR), (BOR + self.TITLE_WIDTH, BOR + self.TITLE_HEIGHT)), outline=tableclr, fill=tablepresentation.header_colour(self.bkgclr, tableclr, self.bw))
        txtclr = (0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        txt = mtexts.txtsfirdaria['Firdaria']
        if self.fird.isdaily:
            txt += ' (' + mtexts.txtsfirdaria['Diurnal'] + ')'
        else:
            if self.options.isfirbonatti:
                txt += ' (' + mtexts.txtsfirdaria['Nocturnal'] + ': ' + mtexts.txtsfirdaria['Bonatus'] + ')'
            else:
                txt += ' (' + mtexts.txtsfirdaria['Nocturnal'] + ': ' + mtexts.txtsfirdaria['AlBiruni'] + ')'
        w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
        draw.text((BOR + (self.BIG_CELL_WIDTH - w) // 2, BOR + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
        plstxts = (
         common.common.planets[0], common.common.planets[1], common.common.planets[2], common.common.planets[3], common.common.planets[4], common.common.planets[5], common.common.planets[6], common.common.planets[7], common.common.planets[8])
        if self.fird.isdaily:
            planetaryyears = self.fird.dailyplanetaryyears
        elif self.options.isfirbonatti:
            planetaryyears = self.fird.nightlyplanetaryyearsbonatti
        else:
            planetaryyears = self.fird.nightlyplanetaryyearsalbiruni
        ln = 0
        starting = self.fird.startdate
        for index in range(len(planetaryyears) + self.EXTRA_PERIODS):
            aindex = index % len(planetaryyears)
            planet, years = planetaryyears[aindex]
            ending = firdaria.addyears(starting, years)
            txt = plstxts[planet]
            w, h = draw.textbbox((0, 0), txt, self.fntMorinus)[2:]
            clr = (0, 0, 0)
            if not self.bw:
                objidx = planet
                if planet > planets.Planets.ANODE:
                    objidx -= 1
                clr = self.options.clrplanets[objidx]
            draw.rectangle(((BOR, BOR + (ln + 1) * self.LINE_HEIGHT), (BOR + self.SMALL_CELL_WIDTH + self.BIG_CELL_WIDTH, BOR + (ln + 2) * self.LINE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
            draw.line((BOR + self.SMALL_CELL_WIDTH, BOR + (ln + 1) * self.LINE_HEIGHT, BOR + self.SMALL_CELL_WIDTH, BOR + (ln + 2) * self.LINE_HEIGHT), fill=tableclr)
            draw.text((BOR + (self.SMALL_CELL_WIDTH - w) // 2, BOR + (self.LINE_HEIGHT - h) // 2 + (ln + 1) * self.LINE_HEIGHT), txt, fill=clr, font=self.fntMorinus)
            ending2 = ending + timedelta(days=-1)
            txt = str(starting.year) + '.' + str(starting.month).zfill(2) + '.' + str(starting.day).zfill(2) + ' - ' + str(ending2.year) + '.' + str(ending2.month).zfill(2) + '.' + str(ending2.day).zfill(2) + ' (' + str(years) + ' ' + mtexts.txtsfirdaria['Years'] + ')'
            w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
            draw.text((BOR + self.SMALL_CELL_WIDTH + (self.BIG_CELL_WIDTH - w) // 2, BOR + (self.LINE_HEIGHT - h) // 2 + (ln + 1) * self.LINE_HEIGHT), txt, fill=txtclr, font=self.fntText)
            ln += 1
            ln = self.displaySubPeriods(draw, planetaryyears, aindex, starting, ending, plstxts, ln, BOR, txtclr, tableclr)
            starting = ending

        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)

    def displaySubPeriods(self, draw, planetaryyears, index, starting, ending, plstxts, ln, BOR, txtclr, tableclr):
        if self.fird.isNode(index):
            return ln
        subperiodstart = starting
        secs = (ending - starting).total_seconds()
        for i in range(planets.Planets.PLANETS_NUM):
            planet, years = planetaryyears[index]
            subperiodends = subperiodstart + timedelta(seconds=secs / 7)
            txt = plstxts[planet]
            w, h = draw.textbbox((0, 0), txt, self.fntMorinus)[2:]
            clr = (0, 0, 0)
            if not self.bw:
                objidx = planet
                if planet > planets.Planets.ANODE:
                    objidx -= 1
                clr = self.options.clrplanets[objidx]
            draw.rectangle(((BOR + self.SMALL_CELL_WIDTH, BOR + (ln + i + 1) * self.LINE_HEIGHT), (BOR + 2 * self.SMALL_CELL_WIDTH + self.CELL_WIDTH, BOR + (ln + i + 2) * self.LINE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
            draw.line((BOR + 2 * self.SMALL_CELL_WIDTH, BOR + (ln + i + 1) * self.LINE_HEIGHT, BOR + 2 * self.SMALL_CELL_WIDTH, BOR + (ln + i + 2) * self.LINE_HEIGHT), fill=tableclr)
            draw.text((BOR + self.SMALL_CELL_WIDTH + (self.SMALL_CELL_WIDTH - w) // 2, BOR + (self.LINE_HEIGHT - h) // 2 + (ln + i + 1) * self.LINE_HEIGHT), txt, fill=clr, font=self.fntMorinus)
            txt = str(subperiodstart.year) + '.' + str(subperiodstart.month).zfill(2) + '.' + str(subperiodstart.day).zfill(2)
            w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
            draw.text((BOR + 2 * self.SMALL_CELL_WIDTH + (self.CELL_WIDTH - w) // 2, BOR + (self.LINE_HEIGHT - h) // 2 + (ln + i + 1) * self.LINE_HEIGHT), txt, fill=txtclr, font=self.fntText)
            subperiodstart = subperiodends
            index = self.fird.nextIndex(index)

        return ln + i + 1