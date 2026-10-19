# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import planets
import chart
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import util
import mtexts

class AlmutenTopicalsWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, idx, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, chrt.options, id, size)
        self.idx = idx
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE // 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.LINE_NUM = len(self.chart.almutens.topicals.collections[idx])
        self.DLINE_HEIGHT = 2 * self.LINE_HEIGHT
        self.COLUMN_NUM = 7
        self.LONGITUDE_CELL_WIDTH = 7 * self.FONT_SIZE
        self.DEGREEWINS_CELL_WIDTH = 7 * self.FONT_SIZE
        self.CELL_WIDTH = 7 * self.FONT_SIZE
        self.TITLE_HEIGHT = self.LINE_HEIGHT
        self.TABLE_WIDTH = self.LONGITUDE_CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH + self.DEGREEWINS_CELL_WIDTH
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + (self.LINE_NUM * self.LINE_HEIGHT + 2 * self.DLINE_HEIGHT)
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = util.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
        self.fntLargeText = util.truetype(common.common.abc, 5 * self.FONT_SIZE // 4)
        self.fntBigText = util.truetype(common.common.abc, 3 * self.FONT_SIZE // 2)
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
        draw.rectangle(((x, y), (x + self.TABLE_WIDTH, y + self.TABLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
        x = BOR
        y = BOR + self.TITLE_HEIGHT
        for i in range(self.LINE_NUM + 1):
            draw.line((x, y + i * self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + i * self.LINE_HEIGHT), fill=tableclr)

        draw.line((x, y + i * self.LINE_HEIGHT + self.DLINE_HEIGHT, x + self.TABLE_WIDTH, y + i * self.LINE_HEIGHT + self.DLINE_HEIGHT), fill=tableclr)
        x = BOR + self.LONGITUDE_CELL_WIDTH
        y = BOR + self.TITLE_HEIGHT
        draw.line((x, y, x, y + self.TABLE_HEIGHT - self.TITLE_HEIGHT), fill=tableclr)
        for i in range(self.COLUMN_NUM + 1):
            draw.line((x + self.LONGITUDE_CELL_WIDTH + i * self.CELL_WIDTH, y, x + self.LONGITUDE_CELL_WIDTH + i * self.CELL_WIDTH, y + self.TABLE_HEIGHT - self.TITLE_HEIGHT), fill=tableclr)

        x = BOR + self.LONGITUDE_CELL_WIDTH
        y = BOR
        for i in range(planets.Planets.PLANETS_NUM):
            clr = (0, 0, 0)
            if not self.bw:
                clr = self.options.clrplanets[i]
            txt = common.common.planets[i]
            w, h = draw.textbbox((0, 0), txt, self.fntMorinus)[2:]
            draw.text((x + i * self.CELL_WIDTH + (self.CELL_WIDTH - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clr, font=self.fntMorinus)

        txt = mtexts.txtsalmutentopicals['DegreeWins']
        w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
        draw.text((x + 7 * self.CELL_WIDTH + (self.DEGREEWINS_CELL_WIDTH - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
        x = BOR
        y = BOR + self.TITLE_HEIGHT
        for i in range(self.LINE_NUM):
            lon = self.chart.almutens.topicals.collections[self.idx][i]
            self.drawLong(draw, x, y + i * self.LINE_HEIGHT, lon, txtclr)
            for j in range(planets.Planets.PLANETS_NUM):
                txt = self.chart.almutens.topicals.data[self.idx][j][i][0]
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                draw.text((x + self.LONGITUDE_CELL_WIDTH + j * self.CELL_WIDTH + (self.CELL_WIDTH - w) // 2, y + i * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)

        x = BOR
        y = BOR + self.TITLE_HEIGHT + self.LINE_NUM * self.LINE_HEIGHT
        txt = mtexts.txtsalmutentopicals['TotalShares1']
        w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
        draw.text((x + (self.LONGITUDE_CELL_WIDTH - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
        txt = mtexts.txtsalmutentopicals['TotalShares2']
        w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
        draw.text((x + (self.LONGITUDE_CELL_WIDTH - w) // 2, y + self.LINE_HEIGHT + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
        y += self.DLINE_HEIGHT
        txt = mtexts.txtsalmutentopicals['TotalScores1']
        w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
        draw.text((x + (self.LONGITUDE_CELL_WIDTH - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
        txt = mtexts.txtsalmutentopicals['TotalScores2']
        w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
        draw.text((x + (self.LONGITUDE_CELL_WIDTH - w) // 2, y + self.LINE_HEIGHT + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
        x = BOR + self.LONGITUDE_CELL_WIDTH
        y = BOR + self.TITLE_HEIGHT + self.LINE_NUM * self.LINE_HEIGHT
        for i in range(planets.Planets.PLANETS_NUM):
            fnt = self.fntLargeText
            if self.chart.almutens.topicals.maxshare[self.idx][0] != -1 and self.chart.almutens.topicals.maxshare[self.idx][0] == i and not self.chart.almutens.topicals.maxshare[self.idx][2]:
                fnt = self.fntBigText
            txt = str(self.chart.almutens.topicals.shares[self.idx][i])
            w, h = draw.textbbox((0, 0), txt, fnt)[2:]
            draw.text((x + i * self.CELL_WIDTH + (self.CELL_WIDTH - w) // 2, y + (self.DLINE_HEIGHT - h) // 2), txt, fill=txtclr, font=fnt)

        y += self.DLINE_HEIGHT
        for i in range(planets.Planets.PLANETS_NUM):
            fnt = self.fntLargeText
            if self.chart.almutens.topicals.maxscore[self.idx][0] != -1 and self.chart.almutens.topicals.maxscore[self.idx][0] == i and not self.chart.almutens.topicals.maxscore[self.idx][2]:
                fnt = self.fntBigText
            txt = str(self.chart.almutens.topicals.scores[self.idx][i])
            w, h = draw.textbbox((0, 0), txt, fnt)[2:]
            draw.text((x + i * self.CELL_WIDTH + (self.CELL_WIDTH - w) // 2, y + (self.DLINE_HEIGHT - h) // 2), txt, fill=txtclr, font=fnt)

        x = BOR + self.LONGITUDE_CELL_WIDTH + 7 * self.CELL_WIDTH
        y = BOR + self.TITLE_HEIGHT
        num = len(self.chart.almutens.topicals.degwinner[self.idx])
        for i in range(num):
            aux = [
             [
              -1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
            subnum = len(self.chart.almutens.topicals.degwinner[self.idx][0])
            mwidth = 0
            for j in range(subnum):
                pid = self.chart.almutens.topicals.degwinner[self.idx][i][j][0]
                if pid != -1:
                    ptxt = common.common.planets[pid]
                    wpl, hpl = draw.textbbox((0, 0), ptxt, self.fntMorinus)[2:]
                    sco = self.chart.almutens.topicals.degwinner[self.idx][i][0][1]
                    txt = '(' + str(sco) + ')'
                    w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                    wsp, hsp = draw.textbbox((0, 0), ' ', self.fntText)[2:]
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
                    wpl, hpl = draw.textbbox((0, 0), pltxt, self.fntMorinus)[2:]
                    txt = '(' + str(aux[j][1]) + ')'
                    wsp, hsp = draw.textbbox((0, 0), ' ', self.fntText)[2:]
                    w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                    prev = 0
                    for p in range(j):
                        prev += aux[j][2] + wsp

                    draw.text((x + (self.DEGREEWINS_CELL_WIDTH - mwidth) // 2 + prev, y + i * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) // 2), pltxt, fill=clr, font=self.fntMorinus)
                    draw.text((x + (self.DEGREEWINS_CELL_WIDTH - mwidth) // 2 + prev + wpl + wsp, y + i * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)

        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)

    def drawLong(self, draw, x, y, lon, clr):
        if self.options.ayanamsha != 0:
            lon -= self.chart.ayanamsha
            lon = util.normalize(lon)
        d, m, s = util.decToDeg(lon)
        sign = d // chart.Chart.SIGN_DEG
        pos = d % chart.Chart.SIGN_DEG
        wsp, hsp = draw.textbbox((0, 0), ' ', self.fntText)[2:]
        wsg, hsg = draw.textbbox((0, 0), self.signs[sign], self.fntMorinus)[2:]
        txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
        w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
        offset = (self.LONGITUDE_CELL_WIDTH - (w + wsp + wsg)) // 2
        draw.text((x + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clr, font=self.fntText)
        draw.text((x + offset + w + wsp, y + (self.LINE_HEIGHT - hsg) // 2), self.signs[sign], fill=clr, font=self.fntMorinus)