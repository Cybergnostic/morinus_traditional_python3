# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, os, chart, houses, common, commonwnd, Image, ImageDraw, ImageFont, util, mtexts

class MiscWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE / 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.LINE_NUM = 3
        self.COLUMN_NUM = 1
        self.CELL_WIDTH = 10 * self.FONT_SIZE
        self.TABLE_HEIGHT = self.LINE_NUM * self.LINE_HEIGHT
        self.TABLE_WIDTH = self.CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
        self.signs = common.common.signs
        self.deg_symbol = '\xb0'
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Misc']

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
        img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.bkgclr)
        draw = ImageDraw.Draw(img)
        BOR = commonwnd.CommonWnd.BORDER
        x = BOR
        y = BOR
        for i in range(self.LINE_NUM + 1):
            draw.line((x, y + self.LINE_HEIGHT * i, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT * i), fill=tableclr)

        for i in range(self.COLUMN_NUM + 1 + 1):
            draw.line((x + self.CELL_WIDTH * i, y, x + self.CELL_WIDTH * i, y + self.TABLE_HEIGHT), fill=tableclr)

        SIDTIME = 0
        OBL = 1
        JD = 2
        txts = (
         mtexts.txtsmisc['SidTime'], mtexts.txtsmisc['OblEcl'], mtexts.txtsmisc['JulianDay'])
        data = (self.chart.houses.ascmc[houses.Houses.ARMC] / 15.0, self.chart.obl[0], self.chart.time.jd)
        dnum = len(txts)
        for i in range(dnum):
            w, h = draw.textsize(txts[i], self.fntText)
            draw.text((BOR + (self.CELL_WIDTH - w) / 2, BOR + self.LINE_HEIGHT * i + (self.LINE_HEIGHT - h) / 2), txts[i], fill=txtclr, font=self.fntText)
            d, m, s = util.decToDeg(data[i])
            if i == SIDTIME:
                txt = str(d) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
                w, h = draw.textsize(txt, self.fntText)
                draw.text((BOR + self.CELL_WIDTH + (self.CELL_WIDTH - w) / 2, BOR + self.LINE_HEIGHT * i + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
            elif i == OBL:
                txt = str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                draw.text((BOR + self.CELL_WIDTH + (self.CELL_WIDTH - w) / 2, BOR + self.LINE_HEIGHT * i + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
            elif i == JD:
                txt = str(data[i])
                w, h = draw.textsize(txt, self.fntText)
                draw.text((BOR + self.CELL_WIDTH + (self.CELL_WIDTH - w) / 2, BOR + self.LINE_HEIGHT * i + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)

        wxImg = wx.EmptyImage(img.size[0], img.size[1])
        wxImg.SetData(img.tostring())
        self.buffer = wx.BitmapFromImage(wxImg)