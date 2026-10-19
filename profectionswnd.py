# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, profectionsmonthly, planets, houses, chart, fortune, proftablemondlg, profstablemonframe, common, commonwnd, Image, ImageDraw, ImageFont, util, mtexts

class ProfectionsWnd(commonwnd.CommonWnd):
    AGE, DATE, ASC, MC, SUN, MOON, FORTUNE, SATURN, JUPITER, MARS, VENUS, MERCURY = range(0, 12)

    def __init__(self, parent, age, pchrts, options, mainfr, mainsigs, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, pchrts[0][0], options, id, size)
        self.age = age
        self.pcharts = pchrts
        self.mainfr = mainfr
        self.mainsigs = mainsigs
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE / 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.LINE_NUM = 12
        if self.mainsigs:
            self.COLUMN_NUM = 7
        else:
            self.COLUMN_NUM = 12
        self.CELL_WIDTH = 3 * self.FONT_SIZE
        self.BIG_CELL_WIDTH = 7 * self.FONT_SIZE
        self.LEFTCLICKY = commonwnd.CommonWnd.BORDER
        self.LEFTCLICKX = commonwnd.CommonWnd.BORDER
        self.LEFTCLICK_HEIGHT = self.LINE_HEIGHT
        self.TITLE_HEIGHT = self.LINE_HEIGHT
        self.TITLE_WIDTH = self.CELL_WIDTH + (self.COLUMN_NUM - 1) * self.BIG_CELL_WIDTH
        self.SPACE_TITLEY = 0
        self.TABLE_WIDTH = (self.COLUMN_NUM - 1) * self.BIG_CELL_WIDTH + self.CELL_WIDTH
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + 2 * self.LINE_HEIGHT + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
        self.signs = common.common.signs
        self.deg_symbol = u'\xb0'
        self.Bind(wx.EVT_LEFT_UP, self.onMonthly)
        self.drawBkg()

    def onMonthly(self, event):
        xu, yu = self.GetScrollPixelsPerUnit()
        xs, ys = self.GetViewStart()
        scrolledoffs = yu * ys
        x, y = event.GetPosition()
        if y + scrolledoffs > commonwnd.CommonWnd.BORDER + 2 * self.LINE_HEIGHT + self.TITLE_HEIGHT and y + scrolledoffs < commonwnd.CommonWnd.BORDER + 2 * self.LINE_HEIGHT + self.TABLE_HEIGHT and x > commonwnd.CommonWnd.BORDER and x < commonwnd.CommonWnd.BORDER + self.CELL_WIDTH:
            rownum = (y + scrolledoffs - (commonwnd.CommonWnd.BORDER + 2 * self.LINE_HEIGHT + self.TITLE_HEIGHT)) / self.LINE_HEIGHT
            dlg = proftablemondlg.ProfTableMonDlg(self)
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                steps12 = dlg.steps12rb.GetValue()
                profsmonthly = profectionsmonthly.ProfectionsMonthly(self.pcharts, steps12, rownum)
                profsmonfr = profstablemonframe.ProfsTableMonFrame(self.mainfr, self.mainfr.title, self.pcharts, profsmonthly.dates, self.options, self.mainsigs, self.age + rownum)
                profsmonfr.Show(True)
            dlg.Destroy()

    def getExt(self):
        return mtexts.txtsprofwnd['Pro']

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
        txt = mtexts.txtsprofwnd['LeftClick']
        fnt = self.fntText
        w, h = draw.textsize(txt, fnt)
        draw.text((BOR, BOR + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=fnt)
        draw.rectangle(((BOR, BOR + 2 * self.LINE_HEIGHT), (BOR + self.TITLE_WIDTH, BOR + 2 * self.LINE_HEIGHT + self.TITLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
        txt = (mtexts.txtsprofwnd['Age'], mtexts.txtsprofwnd['Date'], mtexts.txtsprofwnd['Asc'], mtexts.txtsprofwnd['MC'], common.common.planets[planets.Planets.SUN], common.common.planets[planets.Planets.MOON], common.common.fortune, common.common.planets[planets.Planets.SATURN], common.common.planets[planets.Planets.JUPITER], common.common.planets[planets.Planets.MARS], common.common.planets[planets.Planets.VENUS], common.common.planets[planets.Planets.MERCURY])
        arclrs = (txtclr, txtclr, txtclr, txtclr, self.options.clrplanets[planets.Planets.SUN], self.options.clrplanets[planets.Planets.MOON], self.options.clrLoF, self.options.clrplanets[planets.Planets.SATURN], self.options.clrplanets[planets.Planets.JUPITER], self.options.clrplanets[planets.Planets.MARS], self.options.clrplanets[planets.Planets.VENUS], self.options.clrplanets[planets.Planets.MERCURY])
        cols = (
         self.CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH)
        offs = 0
        for i in range(self.COLUMN_NUM):
            fnt = self.fntText
            if i > ProfectionsWnd.MC:
                fnt = self.fntMorinus
            tclr = (0, 0, 0)
            if not self.bw:
                tclr = arclrs[i]
            w, h = draw.textsize(txt[i], fnt)
            clr = txtclr
            if i > ProfectionsWnd.MC:
                clr = tclr
            draw.text((BOR + offs + (cols[i] - w) / 2, BOR + 2 * self.LINE_HEIGHT + (self.TITLE_HEIGHT - h) / 2), txt[i], fill=clr, font=fnt)
            offs += cols[i]

        x = BOR
        y = BOR + 2 * self.LINE_HEIGHT + self.TITLE_HEIGHT + self.SPACE_TITLEY
        for i in range(self.LINE_NUM):
            self.drawline(draw, x, y + i * self.LINE_HEIGHT, tableclr, self.pcharts[i], self.age, i)

        wxImg = wx.EmptyImage(img.size[0], img.size[1])
        wxImg.SetData(img.tostring())
        self.buffer = wx.BitmapFromImage(wxImg)

    def drawline(self, draw, x, y, clr, pcharts, age, idx):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         self.CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH)
        draw.line((x, y, x, y + self.LINE_HEIGHT), fill=clr)
        summa = 0
        for i in range(self.COLUMN_NUM):
            draw.line((x + summa + offs[i], y, x + summa + offs[i], y + self.LINE_HEIGHT), fill=clr)
            tclr = (0, 0, 0)
            if not self.bw:
                txtclr = self.options.clrtexts
            if i == ProfectionsWnd.AGE:
                txt = str(age + idx)
                w, h = draw.textsize(txt, self.fntText)
                draw.text((x + summa + (offs[i] - w) / 2, y + (self.LINE_HEIGHT - h) / 2), txt, fill=tclr, font=self.fntText)
            elif i == ProfectionsWnd.DATE:
                txt = str(pcharts[1]) + '.' + str(pcharts[2]).zfill(2) + '.' + str(pcharts[3]).zfill(2) + '.'
                w, h = draw.textsize(txt, self.fntText)
                draw.text((x + summa + (offs[i] - w) / 2, y + (self.LINE_HEIGHT - h) / 2), txt, fill=tclr, font=self.fntText)
            else:
                if i == ProfectionsWnd.ASC:
                    lon = pcharts[0].houses.ascmc[houses.Houses.ASC]
                if i == ProfectionsWnd.MC:
                    lon = pcharts[0].houses.ascmc[houses.Houses.MC]
                if i == ProfectionsWnd.SUN:
                    lon = pcharts[0].planets.planets[planets.Planets.SUN].data[planets.Planet.LON]
                if i == ProfectionsWnd.MOON:
                    lon = pcharts[0].planets.planets[planets.Planets.MOON].data[planets.Planet.LON]
                if i == ProfectionsWnd.FORTUNE:
                    lon = pcharts[0].fortune.fortune[fortune.Fortune.LON]
                if i >= ProfectionsWnd.SATURN:
                    lon = pcharts[0].planets.planets[(i - 5)].data[planets.Planet.LON]
                if self.options.ayanamsha != 0:
                    lon -= self.chart.ayanamsha
                    lon = util.normalize(lon)
                d, m, s = util.decToDeg(lon)
                sign = d / chart.Chart.SIGN_DEG
                pos = d % chart.Chart.SIGN_DEG
                wsp, hsp = draw.textsize(' ', self.fntText)
                wsg, hsg = draw.textsize(self.signs[sign], self.fntMorinus)
                txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offset = (offs[i] - (w + wsp + wsg)) / 2
                draw.text((x + summa + offset, y + (self.LINE_HEIGHT - h) / 2), txt, fill=tclr, font=self.fntText)
                draw.text((x + summa + offset + w + wsp, y + (self.LINE_HEIGHT - hsg) / 2), self.signs[sign], fill=tclr, font=self.fntMorinus)
            summa += offs[i]