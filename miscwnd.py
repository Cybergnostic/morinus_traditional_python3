# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import i18n
import wx
import os
import chart
import houses
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import util
import mtexts

class MiscWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE // 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.LINE_NUM = 3
        self.COLUMN_NUM = 1
        self.CELL_WIDTH = 10 * self.FONT_SIZE
        self.TABLE_HEIGHT = self.LINE_NUM * self.LINE_HEIGHT
        self.TABLE_WIDTH = self.CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = util.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
        self.signs = common.common.signs
        self.deg_symbol = '\xb0'
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Misc']

    def tableRows(self):
        """The label/value pairs of the table, drawn by drawBkg and exported as CSV."""
        sid = self.chart.houses.ascmc[houses.Houses.ARMC] / 15.0
        d, m, s = util.decToDeg(sid)
        sid_text = str(d) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
        d, m, s = util.decToDeg(self.chart.obl[0])
        obl_text = str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
        return [
            [mtexts.txtsmisc['SidTime'], sid_text],
            [mtexts.txtsmisc['OblEcl'], obl_text],
            [mtexts.txtsmisc['JulianDay'], util.floatstr(self.chart.time.jd)],
        ]

    def drawBkg(self):
        if self.bw:
            self.bkgclr = (255, 255, 255)
        else:
            self.bkgclr = self.options.clrbackground
        self.SetBackgroundColour(self.bkgclr)
        tableclr = self.options.clrtable
        if self.bw:
            tableclr = (0, 0, 0)
        txtclr = self.options.clrtexts
        if self.bw:
            txtclr = (0, 0, 0)
        img = Image.new('RGB', i18n.tr((self.WIDTH, self.HEIGHT)), i18n.tr(self.bkgclr))
        draw = ImageDraw.Draw(img)
        BOR = commonwnd.CommonWnd.BORDER
        x = BOR
        y = BOR
        for i in range(self.LINE_NUM + 1):
            draw.line((x, y + self.LINE_HEIGHT * i, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT * i), fill=tableclr)

        for i in range(self.COLUMN_NUM + 1 + 1):
            draw.line((x + self.CELL_WIDTH * i, y, x + self.CELL_WIDTH * i, y + self.TABLE_HEIGHT), fill=tableclr)

        # the same texts as the CSV export (tableRows)
        for i, (label, txt) in enumerate(self.tableRows()):
            w, h = draw.textbbox((0, 0), label, self.fntText)[2:]
            draw.text((BOR + (self.CELL_WIDTH - w) // 2, BOR + self.LINE_HEIGHT * i + (self.LINE_HEIGHT - h) // 2), label, fill=txtclr, font=self.fntText)
            w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
            draw.text((BOR + self.CELL_WIDTH + (self.CELL_WIDTH - w) // 2, BOR + self.LINE_HEIGHT * i + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)

        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)