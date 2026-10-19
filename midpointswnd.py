# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, chart, planets, common, commonwnd, Image, ImageDraw, ImageFont, util, mtexts

class MidPointsWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE / 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.YOFFSET = self.LINE_HEIGHT
        self.TABLE_HEIGHT = 16 * self.LINE_HEIGHT + 4 * self.YOFFSET
        self.SMALL_CELL_WIDTH = 5 * self.FONT_SIZE
        self.CELL_WIDTH = 8 * self.FONT_SIZE
        self.XOFFSET = self.SMALL_CELL_WIDTH
        self.TABLE_WIDTH = 3 * (self.SMALL_CELL_WIDTH + self.CELL_WIDTH) + 3 * self.XOFFSET
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
        self.signs = common.common.signs
        self.deg_symbol = u'\xb0'
        LN = 9
        BOR = commonwnd.CommonWnd.BORDER
        self.ar = [[BOR, BOR], [BOR + self.SMALL_CELL_WIDTH + self.CELL_WIDTH + self.XOFFSET, BOR], [BOR + 2 * (self.SMALL_CELL_WIDTH + self.CELL_WIDTH + self.XOFFSET), BOR], [BOR, BOR + LN * self.LINE_HEIGHT + self.YOFFSET], [BOR + self.SMALL_CELL_WIDTH + self.CELL_WIDTH + self.XOFFSET, BOR + LN * self.LINE_HEIGHT + self.YOFFSET], [BOR + 2 * (self.SMALL_CELL_WIDTH + self.CELL_WIDTH + self.XOFFSET), BOR + LN * self.LINE_HEIGHT + self.YOFFSET], [BOR, BOR + (LN + 6) * self.LINE_HEIGHT + 2 * self.YOFFSET]]
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Mid']

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
        txt = mtexts.txtsmidpoints['Longitude']
        w, h = draw.textsize(txt, self.fntText)
        num = len(self.ar)
        for i in range(num):
            x = self.ar[i][0] + self.SMALL_CELL_WIDTH
            y = self.ar[i][1]
            draw.line((x, y, x + self.CELL_WIDTH, y), fill=tableclr)
            draw.line((x, y, x, y + self.LINE_HEIGHT), fill=tableclr)
            draw.line((x + self.CELL_WIDTH, y, x + self.CELL_WIDTH, y + self.LINE_HEIGHT), fill=tableclr)
            draw.line((x - self.SMALL_CELL_WIDTH, y + self.LINE_HEIGHT, x + self.CELL_WIDTH, y + self.LINE_HEIGHT), fill=tableclr)
            draw.text((x + (self.CELL_WIDTH - w) / 2, self.ar[i][1] + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)

        artmp = [8, 7, 6, 5, 4, 3, 2]
        length = len(artmp)
        arln = [
         0]
        for i in range(length):
            arln.append(arln[i] + artmp[i])

        for i in range(num):
            ln = 1
            for j in range(arln[i], arln[(i + 1)]):
                wsp, hsp = draw.textsize(' - ', self.fntText)
                p1 = common.common.planets[self.chart.midpoints.mids[j].p1]
                p2 = common.common.planets[self.chart.midpoints.mids[j].p2]
                wpl1, hpl1 = draw.textsize(p1, self.fntMorinus)
                wpl2, hpl2 = draw.textsize(p2, self.fntMorinus)
                clr1 = (0, 0, 0)
                clr2 = (0, 0, 0)
                if not self.bw:
                    objidx1 = self.chart.midpoints.mids[j].p1
                    objidx2 = self.chart.midpoints.mids[j].p2
                    if objidx1 >= planets.Planets.BODIES_NUM - 1:
                        objidx1 -= 1
                    if objidx2 >= planets.Planets.BODIES_NUM - 1:
                        objidx2 -= 1
                    clr1 = self.options.clrplanets[objidx1]
                    clr2 = self.options.clrplanets[objidx2]
                draw.text((self.ar[i][0] + (self.SMALL_CELL_WIDTH - (wpl1 + wsp + wpl2)) / 2, self.ar[i][1] + self.LINE_HEIGHT * ln + (self.LINE_HEIGHT - hsp) / 2), p1, fill=clr1, font=self.fntMorinus)
                draw.text((self.ar[i][0] + (self.SMALL_CELL_WIDTH - (wpl1 + wsp + wpl2)) / 2 + wpl1, self.ar[i][1] + self.LINE_HEIGHT * ln + (self.LINE_HEIGHT - hsp) / 2), ' - ', fill=txtclr, font=self.fntText)
                draw.text((self.ar[i][0] + (self.SMALL_CELL_WIDTH - (wpl1 + wsp + wpl2)) / 2 + wpl1 + wsp, self.ar[i][1] + self.LINE_HEIGHT * ln + (self.LINE_HEIGHT - hsp) / 2), p2, fill=clr2, font=self.fntMorinus)
                lona = self.chart.midpoints.mids[j].m
                if self.options.ayanamsha != 0:
                    lona -= self.chart.ayanamsha
                    lona = util.normalize(lona)
                lon = lona
                d, m, s = util.decToDeg(lon)
                sign = int(lon / chart.Chart.SIGN_DEG)
                pos = int(lon % chart.Chart.SIGN_DEG)
                wsp, hsp = draw.textsize(' ', self.fntText)
                wsg, hsg = draw.textsize(self.signs[sign], self.fntMorinus)
                txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offs = (self.CELL_WIDTH - (w + wsp + wsg)) / 2
                draw.text((self.ar[i][0] + self.SMALL_CELL_WIDTH + offs, self.ar[i][1] + self.LINE_HEIGHT * ln + (self.LINE_HEIGHT - hsp) / 2), txt, fill=txtclr, font=self.fntText)
                draw.text((self.ar[i][0] + self.SMALL_CELL_WIDTH + offs + w, self.ar[i][1] + self.LINE_HEIGHT * ln + (self.LINE_HEIGHT - hsp) / 2), ' ', fill=txtclr, font=self.fntText)
                draw.text((self.ar[i][0] + self.SMALL_CELL_WIDTH + offs + w + wsp, self.ar[i][1] + self.LINE_HEIGHT * ln + (self.LINE_HEIGHT - hsp) / 2), self.signs[sign], fill=txtclr, font=self.fntMorinus)
                x = self.ar[i][0]
                y = self.ar[i][1] + self.LINE_HEIGHT * ln
                draw.line((x, y + self.LINE_HEIGHT, x + self.SMALL_CELL_WIDTH + self.CELL_WIDTH, y + self.LINE_HEIGHT), fill=tableclr)
                draw.line((x, y + self.LINE_HEIGHT, x, y), fill=tableclr)
                draw.line((x + self.SMALL_CELL_WIDTH, y + self.LINE_HEIGHT, x + self.SMALL_CELL_WIDTH, y), fill=tableclr)
                draw.line((x + self.SMALL_CELL_WIDTH + self.CELL_WIDTH, y + self.LINE_HEIGHT, x + self.SMALL_CELL_WIDTH + self.CELL_WIDTH, y), fill=tableclr)
                ln += 1

        wxImg = wx.EmptyImage(img.size[0], img.size[1])
        wxImg.SetData(img.tostring())
        self.buffer = wx.BitmapFromImage(wxImg)