# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import i18n
import wx
import chart
import planets
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import util
import mtexts
import fortune
import houses

PLANETS_ON = 'Planets on it'
# The course rule: in the antiscion's sign, whole degrees adding up to 29.
NOTE = 'Planets on it: in its sign, the whole degrees adding up to 29 (minutes not counted); distance from the exact point'

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
        self.SPACE = self.FONT_SIZE // 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.SMALL_CELL_WIDTH = 3 * self.FONT_SIZE
        self.CELL_WIDTH = 8 * self.FONT_SIZE
        self.fntMorinus = util.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntSymbol = util.truetype(common.common.symbols, 3 * self.FONT_SIZE // 2)
        self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
        self.signs = common.common.signs
        self.deg_symbol = '\xb0'
        self.hits = self.planetsOnAntiscia()
        measure = ImageDraw.Draw(Image.new('RGB', i18n.tr((1, 1))))
        self.HITS_WIDTH = max([self.hitsWidth(measure, h) for row in self.hits for h in row] + [measure.textbbox((0, 0), PLANETS_ON, self.fntText)[2], 3 * self.FONT_SIZE]) + 2 * self.SPACE
        self.TITLE_HEIGHT = 2 * self.LINE_HEIGHT
        self.TITLE_WIDTH = self.COLUMN_NUM * self.CELL_WIDTH + 2 * self.HITS_WIDTH
        self.SPACE_TITLEY = 0
        self.LINE_NUM = 12
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT
        self.TABLE_WIDTH = self.SMALL_CELL_WIDTH + self.TITLE_WIDTH
        self.WIDTH = commonwnd.CommonWnd.BORDER + max(self.TABLE_WIDTH, measure.textbbox((0, 0), NOTE, self.fntText)[2]) + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + self.LINE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Ant']

    def planetsOnAntiscia(self):
        """For each row (planets, nodes, LoF, Asc, MC): the planets standing on its
        antiscion and on its contraantiscion, as (planet, distance from the exact
        point) nearest first. A planet is on it when it is in the antiscion's
        (or contraantiscion's) sign and the whole degrees of the two add up to
        29, minutes not counted: 10 Aries is in antiscion with 19 Virgo and in
        contraantiscion with 19 Pisces."""
        ants = self.ants
        pls = self.chart.planets.planets
        rows = [(pls[i].data[planets.Planet.LON], ants.plantiscia[i].lon, ants.plcontraant[i].lon, i) for i in range(planets.Planets.BODIES_NUM)]
        rows.append((self.chart.fortune.fortune[fortune.Fortune.LON], ants.lofant.lon, ants.lofcontraant.lon, None))
        for i, h in enumerate((houses.Houses.ASC, houses.Houses.MC)):
            rows.append((self.chart.houses.ascmc[h], ants.ascmcant[i].lon, ants.ascmccontraant[i].lon, None))
        hits = []
        for lon, ant, cant, obj in rows:
            sign, deg = int(lon // 30.0) % 12, int(lon % 30.0)
            antsign = (5 - sign) % 12	# mirrored in the Cancer-Capricorn axis
            row = []
            for target, point in ((antsign, ant), ((antsign + 6) % 12, cant)):
                found = []
                for pl in range(planets.Planets.PLANETS_NUM):
                    plon = pls[pl].data[planets.Planet.LON]
                    dist = abs(util.normalize(point - plon + 180.0) - 180.0)
                    if pl == obj:
                        continue
                    if int(plon // 30.0) % 12 != target or deg + int(plon % 30.0) != 29:
                        continue
                    found.append((pl, dist))
                row.append(sorted(found, key=lambda h: h[1]))
            hits.append(row)
        return hits

    def hitText(self, dist):
        d, m, s = util.decToDeg(dist)
        return str(d) + self.deg_symbol + str(m).zfill(2) + "'"

    def hitsWidth(self, draw, hits):
        wsp = draw.textbbox((0, 0), '  ', self.fntText)[2]
        return sum(draw.textbbox((0, 0), common.common.planets[pl], self.fntMorinus)[2] + draw.textbbox((0, 0), self.hitText(dist), self.fntText)[2] + wsp for pl, dist in hits)

    def drawHits(self, draw, x, y, hits):
        """The planets on an antiscion, each in its colour with its distance."""
        x += (self.HITS_WIDTH - self.hitsWidth(draw, hits)) // 2
        wsp = draw.textbbox((0, 0), '  ', self.fntText)[2]
        for pl, dist in hits:
            clr = (0, 0, 0) if self.bw else self.options.clrplanets[pl]
            w, h = draw.textbbox((0, 0), common.common.planets[pl], self.fntMorinus)[2:]
            draw.text((x, y + (self.LINE_HEIGHT - h) // 2), common.common.planets[pl], fill=clr, font=self.fntMorinus)
            x += w
            txt = self.hitText(dist)
            w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
            draw.text((x, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clr, font=self.fntText)
            x += w + wsp

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
        img = Image.new('RGB', i18n.tr((self.WIDTH, self.HEIGHT)), i18n.tr(self.bkgclr))
        draw = ImageDraw.Draw(img)
        BOR = commonwnd.CommonWnd.BORDER
        draw.rectangle(((BOR + self.SMALL_CELL_WIDTH, BOR), (BOR + self.SMALL_CELL_WIDTH + self.TITLE_WIDTH, BOR + self.TITLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
        txtclr = (
         0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        txt = (
         mtexts.txtsantiscia['Antiscion'], mtexts.txtsantiscia['Contraantiscion'])
        group = 2 * self.CELL_WIDTH + self.HITS_WIDTH
        for i in range(len(txt)):
            w, h = draw.textbbox((0, 0), txt[i], self.fntText)[2:]
            draw.text((BOR + self.SMALL_CELL_WIDTH + group * i + (group - w) // 2, BOR + (self.LINE_HEIGHT - h) // 2), txt[i], fill=txtclr, font=self.fntText)

        txt = (mtexts.txtsantiscia['Longitude'], mtexts.txtsantiscia['Latitude'], PLANETS_ON, mtexts.txtsantiscia['Longitude'], mtexts.txtsantiscia['Latitude'], PLANETS_ON)
        x = BOR + self.SMALL_CELL_WIDTH
        for i in range(len(txt)):
            cw = self.HITS_WIDTH if i % 3 == 2 else self.CELL_WIDTH
            w, h = draw.textbbox((0, 0), txt[i], self.fntText)[2:]
            draw.text((x + (cw - w) // 2, BOR + self.LINE_HEIGHT + (self.LINE_HEIGHT - h) // 2), txt[i], fill=txtclr, font=self.fntText)
            x += cw

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

        w, h = draw.textbbox((0, 0), NOTE, self.fntText)[2:]
        draw.text((x, y + i * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) // 2), NOTE, fill=txtclr, font=self.fntText)
        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)

    def drawline(self, draw, x, y, txt, clr, data, idx, AscMC):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.HITS_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.HITS_WIDTH)
        summa = 0
        for i in range(len(offs)):
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
        w, h = draw.textbbox((0, 0), txt, fnt)[2:]
        offset = (self.SMALL_CELL_WIDTH - w) // 2
        draw.text((x + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clr, font=fnt)
        offs = (
         self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        summa = 0
        for i in range(len(data)):
            if i == 2:
                # after the antiscion: the planets on it
                self.drawHits(draw, x + self.SMALL_CELL_WIDTH + summa, y, self.hits[idx][0])
                summa += self.HITS_WIDTH
            d, m, s = util.decToDeg(data[i])
            if i == 0 or i == 2:
                if self.options.ayanamsha != 0:
                    lona = data[i] - self.chart.ayanamsha
                    lona = util.normalize(lona)
                    d, m, s = util.decToDeg(lona)
                sign = d // chart.Chart.SIGN_DEG
                pos = d % chart.Chart.SIGN_DEG
                wsp, hsp = draw.textbbox((0, 0), ' ', self.fntText)[2:]
                wsg, hsg = draw.textbbox((0, 0), self.signs[sign], self.fntMorinus)[2:]
                txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - (w + wsp + wsg)) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clr, font=self.fntText)
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset + w + wsp, y + (self.LINE_HEIGHT - hsg) // 2), self.signs[sign], fill=clr, font=self.fntMorinus)
            else:
                sign = ''
                if data[i] < 0.0:
                    sign = '-'
                txt = sign + str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - w) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clr, font=self.fntText)
            summa += offs[i]

        # after the contraantiscion: the planets on it
        self.drawHits(draw, x + self.SMALL_CELL_WIDTH + summa, y, self.hits[idx][1])
