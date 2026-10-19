# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, os, astrology, lots, planets, houses, chart, almutens, common, commonwnd, Image, ImageDraw, ImageFont, util, mtexts

class AlmutenZodsWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE / 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.LINE_NUM = 23
        self.COLUMN_NUM = 7
        self.SMALL_CELL_WIDTH = 5 * self.FONT_SIZE
        self.LONGITUDE_CELL_WIDTH = 7 * self.FONT_SIZE
        self.CELL_WIDTH = 7 * self.FONT_SIZE
        self.DEGREEWINS_CELL_WIDTH = 7 * self.FONT_SIZE
        self.TITLE_HEIGHT = self.LINE_HEIGHT
        self.TITLE_WIDTH = 10 * self.FONT_SIZE
        self.TABLE_WIDTH = self.SMALL_CELL_WIDTH + self.LONGITUDE_CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH + self.DEGREEWINS_CELL_WIDTH
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.LINE_NUM * self.LINE_HEIGHT
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
        self.signs = common.common.signs
        self.deg_symbol = '\xb0'
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Alm']

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
        x = BOR
        y = BOR
        draw.line((x + self.SMALL_CELL_WIDTH, y, x + self.TABLE_WIDTH, y), fill=tableclr)
        y += self.LINE_HEIGHT
        for i in range(self.LINE_NUM + 1):
            draw.line((x, y + i * self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + i * self.LINE_HEIGHT), fill=tableclr)

        draw.line((x, y, x, y + self.TABLE_HEIGHT - self.LINE_HEIGHT), fill=tableclr)
        x += self.SMALL_CELL_WIDTH
        y -= self.LINE_HEIGHT
        draw.line((x, y, x, y + self.TABLE_HEIGHT), fill=tableclr)
        for i in range(self.COLUMN_NUM + 2):
            draw.line((x + self.LONGITUDE_CELL_WIDTH + i * self.CELL_WIDTH, y, x + self.LONGITUDE_CELL_WIDTH + i * self.CELL_WIDTH, y + self.TABLE_HEIGHT), fill=tableclr)

        for i in range(planets.Planets.PLANETS_NUM):
            clr = (0, 0, 0)
            if not self.bw:
                clr = self.options.clrplanets[i]
            txt = common.common.planets[i]
            w, h = draw.textsize(txt, self.fntMorinus)
            draw.text((x + self.LONGITUDE_CELL_WIDTH + i * self.CELL_WIDTH + (self.CELL_WIDTH - w) / 2, y + (self.LINE_HEIGHT - h) / 2), txt, fill=clr, font=self.fntMorinus)
            draw.text((x - self.SMALL_CELL_WIDTH + (self.SMALL_CELL_WIDTH - w) / 2, y + (i + 1) * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=clr, font=self.fntMorinus)
            plon = self.chart.planets.planets[i].data[planets.Planet.LON]
            self.drawLong(draw, x, y + self.TITLE_HEIGHT + i * self.LINE_HEIGHT, plon, clr)
            for j in range(planets.Planets.PLANETS_NUM):
                txt = self.chart.almutens.essentials.essentials2[i][j][0]
                w, h = draw.textsize(txt, self.fntText)
                draw.text((x + self.LONGITUDE_CELL_WIDTH + i * self.CELL_WIDTH + (self.CELL_WIDTH - w) / 2, y + (j + 1) * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)

            txt = self.chart.almutens.essentials.essentials[i][3][0]
            w, h = draw.textsize(txt, self.fntText)
            draw.text((x + self.LONGITUDE_CELL_WIDTH + i * self.CELL_WIDTH + (self.CELL_WIDTH - w) / 2, y + 8 * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
            txt = self.chart.almutens.essentials.essentials[i][4][0]
            w, h = draw.textsize(txt, self.fntText)
            draw.text((x + self.LONGITUDE_CELL_WIDTH + i * self.CELL_WIDTH + (self.CELL_WIDTH - w) / 2, y + 9 * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
            txt = self.chart.almutens.essentials.essentials[i][2][0]
            w, h = draw.textsize(txt, self.fntText)
            draw.text((x + self.LONGITUDE_CELL_WIDTH + i * self.CELL_WIDTH + (self.CELL_WIDTH - w) / 2, y + 10 * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
            txt = self.chart.almutens.essentials.essentialsmc[i][0]
            w, h = draw.textsize(txt, self.fntText)
            draw.text((x + self.LONGITUDE_CELL_WIDTH + i * self.CELL_WIDTH + (self.CELL_WIDTH - w) / 2, y + 11 * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)

        txt = mtexts.txtsalmutenzods['Almuten']
        w, h = draw.textsize(txt, self.fntText)
        draw.text((x + self.LONGITUDE_CELL_WIDTH + 7 * self.CELL_WIDTH + (self.DEGREEWINS_CELL_WIDTH - w) / 2, y + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
        x = BOR + self.SMALL_CELL_WIDTH + 7 * self.CELL_WIDTH
        y = BOR + self.TITLE_HEIGHT
        for i in range(planets.Planets.PLANETS_NUM):
            self.drawDegWinner(draw, x + self.LONGITUDE_CELL_WIDTH, y, i, False, self.chart.almutens.essentials.degwinner2, txtclr)

        x = BOR + self.SMALL_CELL_WIDTH + 7 * self.CELL_WIDTH
        y = BOR + self.TITLE_HEIGHT + 7 * self.LINE_HEIGHT
        self.drawDegWinner(draw, x + self.LONGITUDE_CELL_WIDTH, y, 3, True, self.chart.almutens.essentials.degwinner, txtclr)
        x = BOR + self.SMALL_CELL_WIDTH + 7 * self.CELL_WIDTH
        y = BOR + self.TITLE_HEIGHT + 8 * self.LINE_HEIGHT
        self.drawDegWinner(draw, x + self.LONGITUDE_CELL_WIDTH, y, 4, True, self.chart.almutens.essentials.degwinner, txtclr)
        x = BOR + self.SMALL_CELL_WIDTH + 7 * self.CELL_WIDTH
        y = BOR + self.TITLE_HEIGHT + 9 * self.LINE_HEIGHT
        self.drawDegWinner(draw, x + self.LONGITUDE_CELL_WIDTH, y, 2, True, self.chart.almutens.essentials.degwinner, txtclr)
        x = BOR + self.SMALL_CELL_WIDTH + 7 * self.CELL_WIDTH
        y = BOR + self.TITLE_HEIGHT + 10 * self.LINE_HEIGHT
        self.drawDegWinner2(draw, x + self.LONGITUDE_CELL_WIDTH, y, self.chart.almutens.essentials.degwinnermc, txtclr)
        x = BOR
        y = BOR + self.LINE_HEIGHT
        clr = (0, 0, 0)
        if not self.bw:
            clr = self.options.clrLoF
        txt = common.common.fortune
        w, h = draw.textsize(txt, self.fntMorinus)
        draw.text((x + (self.SMALL_CELL_WIDTH - w) / 2, y + 7 * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=clr, font=self.fntMorinus)
        flon = self.chart.lots.lots[0][lots.Lots.LON]
        self.drawLong(draw, x + self.SMALL_CELL_WIDTH, y + 7 * self.LINE_HEIGHT, flon, clr)
        txt = mtexts.txtsalmutenzods['Syzygy']
        w, h = draw.textsize(txt, self.fntText)
        draw.text((x + (self.SMALL_CELL_WIDTH - w) / 2, y + 8 * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
        slon = self.chart.syzygy.lon
        self.drawLong(draw, x + self.SMALL_CELL_WIDTH, y + 8 * self.LINE_HEIGHT, slon, txtclr)
        txt = mtexts.txtsalmutenzods['Asc']
        w, h = draw.textsize(txt, self.fntText)
        draw.text((x + (self.SMALL_CELL_WIDTH - w) / 2, y + 9 * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
        alon = self.chart.houses.ascmc[houses.Houses.ASC]
        self.drawLong(draw, x + self.SMALL_CELL_WIDTH, y + 9 * self.LINE_HEIGHT, alon, txtclr)
        txt = mtexts.txtsalmutenzods['MC']
        w, h = draw.textsize(txt, self.fntText)
        draw.text((x + (self.SMALL_CELL_WIDTH - w) / 2, y + 10 * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
        mlon = self.chart.houses.ascmc[houses.Houses.MC]
        self.drawLong(draw, x + self.SMALL_CELL_WIDTH, y + 10 * self.LINE_HEIGHT, mlon, txtclr)
        y = BOR + self.LINE_HEIGHT
        hcstxt = [
         mtexts.txtsalmutenzods['HC1'], mtexts.txtsalmutenzods['HC2'], mtexts.txtsalmutenzods['HC3'], mtexts.txtsalmutenzods['HC4'], mtexts.txtsalmutenzods['HC5'], mtexts.txtsalmutenzods['HC6'], mtexts.txtsalmutenzods['HC7'], mtexts.txtsalmutenzods['HC8'], mtexts.txtsalmutenzods['HC9'], mtexts.txtsalmutenzods['HC10'], mtexts.txtsalmutenzods['HC11'], mtexts.txtsalmutenzods['HC12']]
        for i in range(planets.Planets.PLANETS_NUM):
            for j in range(houses.Houses.HOUSE_NUM):
                if i == 0:
                    txt = hcstxt[j]
                    w, h = draw.textsize(txt, self.fntText)
                    draw.text((x + (self.SMALL_CELL_WIDTH - w) / 2, y + 11 * self.LINE_HEIGHT + j * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
                txt = self.chart.almutens.essentials.essentialshcs[i][j][0]
                w, h = draw.textsize(txt, self.fntText)
                draw.text((x + self.SMALL_CELL_WIDTH + self.LONGITUDE_CELL_WIDTH + i * self.CELL_WIDTH + (self.CELL_WIDTH - w) / 2, y + 11 * self.LINE_HEIGHT + j * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
                if i == 0:
                    hlon = self.chart.houses.cusps[(j + 1)]
                    if self.options.ayanamsha != 0 and self.options.hsys != 5:
                        hlon -= self.chart.ayanamsha
                        hlon = util.normalize(hlon)
                    self.drawLong(draw, x + self.SMALL_CELL_WIDTH, y + 11 * self.LINE_HEIGHT + j * self.LINE_HEIGHT, hlon, txtclr, False)

        x = BOR + self.SMALL_CELL_WIDTH + 7 * self.CELL_WIDTH
        y = BOR + self.TITLE_HEIGHT + 11 * self.LINE_HEIGHT
        num = len(self.chart.almutens.essentials.degwinnerhcs)
        for i in range(num):
            self.drawDegWinner(draw, x + self.LONGITUDE_CELL_WIDTH, y, i, False, self.chart.almutens.essentials.degwinnerhcs, txtclr)

        wxImg = wx.EmptyImage(img.size[0], img.size[1])
        wxImg.SetData(img.tostring())
        self.buffer = wx.BitmapFromImage(wxImg)

    def drawDegWinner(self, draw, x, y, i, onlyone, degwinner, txtclr):
        aux = [
         [
          -1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        subnum = len(degwinner[0])
        mwidth = 0
        for j in range(subnum):
            pid = degwinner[i][j][0]
            if pid != -1:
                ptxt = common.common.planets[pid]
                wpl, hpl = draw.textsize(ptxt, self.fntMorinus)
                sco = degwinner[i][0][1]
                txt = '(' + str(sco) + ')'
                w, h = draw.textsize(txt, self.fntText)
                wsp, hsp = draw.textsize(' ', self.fntText)
                aux[j][0] = pid
                aux[j][1] = sco
                aux[j][2] = wpl + wsp + w
                if mwidth != 0:
                    mwidth += wsp
                mwidth += wpl + wsp + w
            else:
                break

        for j in range(subnum):
            if aux[j][0] != -1:
                clr = (0, 0, 0)
                if not self.bw:
                    clr = self.options.clrplanets[aux[j][0]]
                pltxt = common.common.planets[aux[j][0]]
                wpl, hpl = draw.textsize(pltxt, self.fntMorinus)
                txt = '(' + str(aux[j][1]) + ')'
                wsp, hsp = draw.textsize(' ', self.fntText)
                w, h = draw.textsize(txt, self.fntText)
                prev = 0
                for p in range(j):
                    prev += aux[j][2] + wsp

                offs = i
                if onlyone:
                    offs = 0
                draw.text((x + (self.DEGREEWINS_CELL_WIDTH - mwidth) / 2 + prev, y + offs * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), pltxt, fill=clr, font=self.fntMorinus)
                draw.text((x + (self.DEGREEWINS_CELL_WIDTH - mwidth) / 2 + prev + wpl + wsp, y + offs * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)

    def drawDegWinner2(self, draw, x, y, degwinner, txtclr):
        aux = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        subnum = len(degwinner)
        mwidth = 0
        for j in range(subnum):
            pid = degwinner[j][0]
            if pid != -1:
                ptxt = common.common.planets[pid]
                wpl, hpl = draw.textsize(ptxt, self.fntMorinus)
                sco = degwinner[0][1]
                txt = '(' + str(sco) + ')'
                w, h = draw.textsize(txt, self.fntText)
                wsp, hsp = draw.textsize(' ', self.fntText)
                aux[j][0] = pid
                aux[j][1] = sco
                aux[j][2] = wpl + wsp + w
                if mwidth != 0:
                    mwidth += wsp
                mwidth += wpl + wsp + w
            else:
                break

        for j in range(subnum):
            if aux[j][0] != -1:
                clr = (0, 0, 0)
                if not self.bw:
                    clr = self.options.clrplanets[aux[j][0]]
                pltxt = common.common.planets[aux[j][0]]
                wpl, hpl = draw.textsize(pltxt, self.fntMorinus)
                txt = '(' + str(aux[j][1]) + ')'
                wsp, hsp = draw.textsize(' ', self.fntText)
                w, h = draw.textsize(txt, self.fntText)
                prev = 0
                for p in range(j):
                    prev += aux[j][2] + wsp

                draw.text((x + (self.DEGREEWINS_CELL_WIDTH - mwidth) / 2 + prev, y + (self.LINE_HEIGHT - h) / 2), pltxt, fill=clr, font=self.fntMorinus)
                draw.text((x + (self.DEGREEWINS_CELL_WIDTH - mwidth) / 2 + prev + wpl + wsp, y + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)

    def drawLong(self, draw, x, y, lon, clr, nonHCs=True):
        if nonHCs and self.options.ayanamsha != 0:
            lon -= self.chart.ayanamsha
            lon = util.normalize(lon)
        d, m, s = util.decToDeg(lon)
        sign = d / chart.Chart.SIGN_DEG
        pos = d % chart.Chart.SIGN_DEG
        wsp, hsp = draw.textsize(' ', self.fntText)
        wsg, hsg = draw.textsize(self.signs[sign], self.fntMorinus)
        txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
        w, h = draw.textsize(txt, self.fntText)
        offset = (self.LONGITUDE_CELL_WIDTH - (w + wsp + wsg)) / 2
        draw.text((x + offset, y + (self.LINE_HEIGHT - h) / 2), txt, fill=clr, font=self.fntText)
        draw.text((x + offset + w + wsp, y + (self.LINE_HEIGHT - hsg) / 2), self.signs[sign], fill=clr, font=self.fntMorinus)