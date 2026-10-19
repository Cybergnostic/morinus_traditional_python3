# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, os, astrology, planets, chart, common, commonwnd, Image, ImageDraw, ImageFont, util, mtexts

class SpeedsWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE / 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.LINE_NUM = planets.Planets.BODIES_NUM - 1
        self.COLUMN_NUM = 2
        self.SMALL_CELL_WIDTH = 3 * self.FONT_SIZE
        self.CELL_WIDTH = 8 * self.FONT_SIZE
        self.TITLE_HEIGHT = self.LINE_HEIGHT
        self.TITLE_WIDTH = self.COLUMN_NUM * self.CELL_WIDTH
        self.SPACE_TITLEY = 0
        self.TABLE_WIDTH = self.SMALL_CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
        self.deg_symbol = '\xb0'
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Spe']

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
        txt = (mtexts.txtsspeeds['InLong'], mtexts.txtsspeeds['InLat'])
        for i in range(len(txt)):
            w, h = draw.textsize(txt[i], self.fntText)
            draw.text((BOR + self.SMALL_CELL_WIDTH + self.CELL_WIDTH * i + (self.CELL_WIDTH - w) / 2, BOR + (self.TITLE_HEIGHT - h) / 2), txt[i], fill=txtclr, font=self.fntText)

        x = BOR
        y = BOR + self.TITLE_HEIGHT + self.SPACE_TITLEY
        draw.line((x, y, x + self.TABLE_WIDTH, y), fill=tableclr)
        for i in range(planets.Planets.BODIES_NUM - 1):
            self.drawline(draw, x, y + i * self.LINE_HEIGHT, tableclr, i)

        wxImg = wx.EmptyImage(img.size[0], img.size[1])
        wxImg.SetData(img.tostring())
        self.buffer = wx.BitmapFromImage(wxImg)

    def drawline(self, draw, x, y, clr, idx):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        BOR = commonwnd.CommonWnd.BORDER
        summa = 0
        for i in range(self.COLUMN_NUM + 1 + 1):
            draw.line((x + summa + offs[i], y, x + summa + offs[i], y + self.LINE_HEIGHT), fill=clr)
            tclr = (0, 0, 0)
            if not self.bw:
                objidx = idx
                if objidx == planets.Planets.BODIES_NUM - 1:
                    objidx -= 1
                tclr = self.options.clrplanets[objidx]
            if i == 1:
                txt = common.common.planets[idx]
                w, h = draw.textsize(txt, self.fntMorinus)
                draw.text((x + summa + (offs[i] - w) / 2, y + (self.LINE_HEIGHT - h) / 2), txt, fill=tclr, font=self.fntMorinus)
            elif i != 0:
                data = self.chart.planets.planets[idx].data[(planets.Planet.SPLON + (i - 2))]
                d, m, s = util.decToDeg(data)
                sign = ''
                if data < 0.0:
                    sign = '-'
                txt = sign + str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                draw.text((x + summa + (offs[i] - w) / 2, y + (self.LINE_HEIGHT - h) / 2), txt, fill=tclr, font=self.fntText)
            summa += offs[i]