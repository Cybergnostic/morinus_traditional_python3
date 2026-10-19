# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import chart
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import fixedstars
import util
import mtexts

class FixedStarsWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE // 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.LINE_NUM = len(self.chart.fixedstars.data)
        self.SMALL_CELL_WIDTH = 3 * self.FONT_SIZE
        self.BIG_CELL_WIDTH = 10 * self.FONT_SIZE
        self.CELL_WIDTH = 8 * self.FONT_SIZE
        self.COLUMN_NUM = 6
        self.TITLE_HEIGHT = self.LINE_HEIGHT
        self.TITLE_WIDTH = self.BIG_CELL_WIDTH + (self.COLUMN_NUM - 1) * self.CELL_WIDTH
        self.SPACE_TITLEY = 0
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT
        self.TABLE_WIDTH = self.SMALL_CELL_WIDTH + self.BIG_CELL_WIDTH + (self.COLUMN_NUM - 1) * self.CELL_WIDTH
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = util.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
        self.signs = common.common.signs
        self.deg_symbol = '\xb0'
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Fix']

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
        txt = (mtexts.txtsfixedstars['Name'], mtexts.txtsfixedstars['Nomencl'], mtexts.txtsfixedstars['Longitude'], mtexts.txtsfixedstars['Latitude'], mtexts.txtsfixedstars['Rectascension'], mtexts.txtsfixedstars['Declination'])
        summa = 0
        offs = (self.BIG_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        for i in range(len(txt)):
            w, h = draw.textbbox((0, 0), txt[i], self.fntText)[2:]
            draw.text((BOR + self.SMALL_CELL_WIDTH + summa + (offs[i] - w) // 2, BOR + (self.TITLE_HEIGHT - h) // 2), txt[i], fill=txtclr, font=self.fntText)
            summa += offs[i]

        x = BOR
        y = BOR + self.TITLE_HEIGHT + self.SPACE_TITLEY
        draw.line((x, y, x + self.TABLE_WIDTH, y), fill=tableclr)
        for i in range(len(self.chart.fixedstars.data)):
            self.drawline(draw, x, y + i * self.LINE_HEIGHT, tableclr, i)

        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)

    def drawline(self, draw, x, y, clr, idx):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.SMALL_CELL_WIDTH, self.BIG_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        OFFS = 2
        BOR = commonwnd.CommonWnd.BORDER
        summa = 0
        txtclr = (0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        for i in range(self.COLUMN_NUM + OFFS):
            draw.line((x + summa + offs[i], y, x + summa + offs[i], y + self.LINE_HEIGHT), fill=clr)
            d, m, s = (0, 0, 0)
            if i >= fixedstars.FixedStars.LON + OFFS:
                d, m, s = util.decToDeg(self.chart.fixedstars.data[idx][(i - OFFS)])
            if i == 1:
                txt = str(idx + 1) + '.'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
            elif i == fixedstars.FixedStars.NAME + OFFS or i == fixedstars.FixedStars.NOMNAME + OFFS:
                txt = self.chart.fixedstars.data[idx][(i - OFFS)]
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
            elif i == fixedstars.FixedStars.LON + OFFS:
                if self.options.ayanamsha != 0:
                    lona = self.chart.fixedstars.data[idx][(i - OFFS)] - self.chart.ayanamsha
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
            elif i == fixedstars.FixedStars.LAT + OFFS or i == fixedstars.FixedStars.DECL + OFFS:
                sign = ''
                if self.chart.fixedstars.data[idx][(i - 2)] < 0.0:
                    sign = '-'
                txt = sign + str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
            elif i == fixedstars.FixedStars.RA + OFFS:
                txt = str(d) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                if self.options.intime:
                    d, m, s = util.decToDeg(self.chart.fixedstars.data[idx][(i - 2)] / 15.0)
                    txt = str(d).rjust(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
            summa += offs[i]