# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, chart, planets, common, commonwnd, Image, ImageDraw, ImageFont, util, mtexts

class AntisciaWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.parent = parent
        self.ants = chrt.antiscia
        self.options = options
        self.mainfr = mainfr
        self.bw = self.options.bw
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.COLUMN_NUM = 4
        self.SPACE = self.FONT_SIZE / 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.SMALL_CELL_WIDTH = 3 * self.FONT_SIZE
        self.CELL_WIDTH = 8 * self.FONT_SIZE
        self.TITLE_HEIGHT = 2 * self.LINE_HEIGHT
        self.TITLE_WIDTH = self.COLUMN_NUM * self.CELL_WIDTH
        self.SPACE_TITLEY = 0
        self.LINE_NUM = 12
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT
        self.TABLE_WIDTH = self.SMALL_CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntSymbol = ImageFont.truetype(common.common.symbols, 3 * self.FONT_SIZE / 2)
        self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
        self.signs = common.common.signs
        self.deg_symbol = u'\xb0'
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Ant']

    def drawBkg(self):
        if self.bw:
            self.bkgclr = (
             255, 255, 255)
        else:
            self.bkgclr = self.options.clrbackground
        self.SetBackgroundColour(self.bkgclr)
        tableclr = self.options.clrtable
        if self.bw:
            tableclr = (
             0, 0, 0)
        img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.bkgclr)
        draw = ImageDraw.Draw(img)
        BOR = commonwnd.CommonWnd.BORDER
        draw.rectangle(((BOR + self.SMALL_CELL_WIDTH, BOR), (BOR + self.SMALL_CELL_WIDTH + self.TITLE_WIDTH, BOR + self.TITLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
        txtclr = (
         0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        txt = (
         mtexts.txtsantiscia['Antiscion'], mtexts.txtsantiscia['Contraantiscion'])
        for i in range(len(txt)):
            w, h = draw.textsize(txt[i], self.fntText)
            offs = 0
            if i == 1:
                offs = self.CELL_WIDTH
            draw.text((BOR + self.SMALL_CELL_WIDTH + self.CELL_WIDTH / 2 + offs + self.CELL_WIDTH * i + (self.CELL_WIDTH - w) / 2, BOR + (self.LINE_HEIGHT - h) / 2), txt[i], fill=txtclr, font=self.fntText)

        txt = (mtexts.txtsantiscia['Longitude'], mtexts.txtsantiscia['Latitude'], mtexts.txtsantiscia['Longitude'], mtexts.txtsantiscia['Latitude'])
        for i in range(len(txt)):
            w, h = draw.textsize(txt[i], self.fntText)
            draw.text((BOR + self.SMALL_CELL_WIDTH + self.CELL_WIDTH * i + (self.CELL_WIDTH - w) / 2, BOR + self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt[i], fill=txtclr, font=self.fntText)

        x = BOR
        y = BOR + self.TITLE_HEIGHT + self.SPACE_TITLEY
        draw.line((x, y, x + self.TABLE_WIDTH, y), fill=tableclr)
        txts = (
         common.common.planets[0], common.common.planets[1], common.common.planets[2], common.common.planets[3], common.common.planets[4], common.common.planets[5], common.common.planets[6], common.common.planets[7], common.common.planets[8], common.common.fortune, '0', '1')
        data = ((self.ants.plantiscia[0].lon, self.ants.plantiscia[0].lat, self.ants.plcontraant[0].lon, self.ants.plcontraant[0].lat), (self.ants.plantiscia[1].lon, self.ants.plantiscia[1].lat, self.ants.plcontraant[1].lon, self.ants.plcontraant[1].lat), (self.ants.plantiscia[2].lon, self.ants.plantiscia[2].lat, self.ants.plcontraant[2].lon, self.ants.plcontraant[2].lat), (self.ants.plantiscia[3].lon, 0.0, self.ants.plcontraant[3].lon, 0.0), (self.ants.plantiscia[4].lon, self.ants.plantiscia[4].lat, self.ants.plcontraant[4].lon, self.ants.plcontraant[4].lat), (self.ants.plantiscia[5].lon, self.ants.plantiscia[5].lat, self.ants.plcontraant[5].lon, self.ants.plcontraant[5].lat), (self.ants.plantiscia[6].lon, self.ants.plantiscia[6].lat, self.ants.plcontraant[6].lon, self.ants.plcontraant[6].lat), (self.ants.plantiscia[7].lon, self.ants.plantiscia[7].lat, self.ants.plcontraant[7].lon, self.ants.plcontraant[7].lat), (self.ants.plantiscia[8].lon, self.ants.plantiscia[8].lat, self.ants.plcontraant[8].lon, self.ants.plcontraant[8].lat), (self.ants.lofant.lon, self.ants.lofant.lat, self.ants.lofcontraant.lon, self.ants.lofcontraant.lat), (self.ants.ascmcant[0].lon, self.ants.ascmcant[0].lat, self.ants.ascmccontraant[0].lon, self.ants.ascmccontraant[0].lat), (self.ants.ascmcant[1].lon, self.ants.ascmcant[1].lat, self.ants.ascmccontraant[1].lon, self.ants.ascmccontraant[1].lat))
        i = 0
        for j in range(len(txts)):
            ascmc = False
            if j > 9:
                ascmc = True
            self.drawline(draw, x, y + i * self.LINE_HEIGHT, txts[j], tableclr, data[j], j, ascmc)
            i += 1

        wxImg = wx.EmptyImage(img.size[0], img.size[1])
        wxImg.SetData(img.tostring())
        self.buffer = wx.BitmapFromImage(wxImg)

    def drawline(self, draw, x, y, txt, clr, data, idx, AscMC):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        summa = 0
        for i in range(self.COLUMN_NUM + 1 + 1):
            draw.line((x + summa + offs[i], y, x + summa + offs[i], y + self.LINE_HEIGHT), fill=clr)
            summa += offs[i]

        clr = (0, 0, 0)
        if not self.bw:
            if not AscMC:
                if idx < planets.Planets.BODIES_NUM:
                    objidx = idx
                    if idx > planets.Planets.ANODE:
                        objidx -= 1
                    clr = self.options.clrplanets[objidx]
                else:
                    clr = self.options.clrLoF
            else:
                clr = self.options.clrtexts
        fnt = self.fntMorinus
        if AscMC:
            fnt = self.fntSymbol
        w, h = draw.textsize(txt, fnt)
        offset = (self.SMALL_CELL_WIDTH - w) / 2
        draw.text((x + offset, y + (self.LINE_HEIGHT - h) / 2), txt, fill=clr, font=fnt)
        offs = (
         self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        summa = 0
        for i in range(len(data)):
            d, m, s = util.decToDeg(data[i])
            if i == 0 or i == 2:
                if self.options.ayanamsha != 0:
                    lona = data[i] - self.chart.ayanamsha
                    lona = util.normalize(lona)
                    d, m, s = util.decToDeg(lona)
                sign = d / chart.Chart.SIGN_DEG
                pos = d % chart.Chart.SIGN_DEG
                wsp, hsp = draw.textsize(' ', self.fntText)
                wsg, hsg = draw.textsize(self.signs[sign], self.fntMorinus)
                txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offset = (offs[i] - (w + wsp + wsg)) / 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) / 2), txt, fill=clr, font=self.fntText)
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset + w + wsp, y + (self.LINE_HEIGHT - hsg) / 2), self.signs[sign], fill=clr, font=self.fntMorinus)
            else:
                sign = ''
                if data[i] < 0.0:
                    sign = '-'
                txt = sign + str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offset = (offs[i] - w) / 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) / 2), txt, fill=clr, font=self.fntText)
            summa += offs[i]